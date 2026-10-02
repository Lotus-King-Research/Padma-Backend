"""SQLite-backed, drop-in replacement for Tibetan-Lookup's DictionaryLookup.

The original loads all 21 dictionaries into memory as pandas DataFrames
(~600 MB-1 GB RSS). This holds them on disk in an indexed SQLite file instead,
so resident memory stays flat regardless of corpus size. Output shapes match
what app/utils/matching_*.py expect, so the rest of the app is unchanged.

Lookups mirror the original pandas `DictionaryLookup._query` exactly:
  exact        -> Tibetan == q                      (indexed point lookup)
  partial      -> Tibetan.str.contains(q)           then sorted by length
  fuzzy        -> Tibetan.str.contains(first syllable of q), then fuzzy_matching
  description  -> Description.str.contains(q)
`str.contains` is a case-sensitive regex search; see `_contains`. Rows are read
in the original file order, and duplicate headwords keep the last occurrence,
as the original dict-building loop did.

Thread-local connections so concurrent requests (Starlette runs sync routes in
a threadpool) execute real parallel reads -- sqlite3 releases the GIL during
query execution.
"""
import functools
import os
import re
import sqlite3
import threading

# Optional safety cap on rows a single scanning query may return. Default -1 is
# SQLite's "no limit", which keeps results identical to the original.
SCAN_LIMIT = int(os.environ.get("PADMA_SCAN_LIMIT", "-1"))

DB_PATH = os.environ.get("PADMA_SQLITE", "app/data/dicts.sqlite")

_VALID_TABLE = re.compile(r"^[A-Za-z0-9_]+$")
_REGEX_META = frozenset(".^$*+?{}[]\\|()")


@functools.lru_cache(maxsize=256)
def _compiled(pattern):
    return re.compile(pattern)


def _regexp(pattern, value):
    return value is not None and _compiled(pattern).search(value) is not None


def _contains(column, needle):
    """SQL predicate equivalent to pandas `Series.str.contains(needle)`, i.e. a
    case-sensitive `re.search`. Plain needles (the normal case) use the fast
    instr(); needles with regex metacharacters go through Python's re so the
    semantics -- including errors on invalid patterns -- are identical."""
    if _REGEX_META.intersection(needle):
        return "padma_regexp(?, %s)" % column
    return "instr(%s, ?) > 0" % column


class DictionaryLookup:

    def __init__(self, db_path=None, labels=None):
        self._db_path = db_path or DB_PATH
        self._local = threading.local()
        if labels is None:
            labels = [r[0] for r in self._conn().execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY rowid")]
        # `.dictionaries` keys are read as the default source list elsewhere
        self.dictionaries = {label: True for label in labels}

    def _conn(self):
        con = getattr(self._local, "con", None)
        if con is None:
            con = sqlite3.connect(self._db_path, check_same_thread=False)
            con.execute("PRAGMA query_only=ON")
            con.execute("PRAGMA cache_size=-2000")  # ~2 MB page cache per conn
            con.create_function("padma_regexp", 2, _regexp, deterministic=True)
            self._local.con = con
        return con

    @staticmethod
    def _table(source):
        if not _VALID_TABLE.match(source):
            raise ValueError("invalid dictionary name: %r" % source)
        return '"%s"' % source

    def _scan(self, con, tbl, column, needle):
        rows = con.execute(
            "SELECT Tibetan, Description FROM %s WHERE %s ORDER BY rowid LIMIT ?"
            % (tbl, _contains(column, needle)), (needle, SCAN_LIMIT)).fetchall()
        out = {}
        for tibetan, description in rows:      # last occurrence wins
            out[tibetan] = str(description)
        return out

    def lookup(self, string, sources=None,
               partial_match=False, fuzzy_match=False, description_match=False):

        from dictionary_lookup.utils.check_if_wylie import check_if_wylie

        string = string.strip()
        if not description_match:
            string = check_if_wylie(string)

        if not sources:
            sources = list(self.dictionaries.keys())

        con = self._conn()
        out = {}

        for source in sources:
            tbl = self._table(source)

            if partial_match or fuzzy_match:
                # partial searches the whole query, fuzzy only its first syllable
                needle = string if partial_match else string.split("་")[0]
                d = self._scan(con, tbl, "Tibetan", needle)
                if partial_match:
                    d = {k: d[k] for k in sorted(d, key=lambda x: len(x))}
                if fuzzy_match:
                    from dictionary_lookup.utils.fuzzy_matching import fuzzy_matching
                    fm = fuzzy_matching(string, d, n=20)
                    d = {k: d[k] for k in d if k in fm}
                out[source] = d

            elif description_match:
                out[source] = self._scan(con, tbl, "Description", string)

            else:  # exact
                rows = con.execute(
                    "SELECT Description FROM %s WHERE Tibetan = ? ORDER BY rowid" % tbl,
                    (string,)).fetchall()
                out[source] = {string: [r[0] for r in rows]}

        return out
