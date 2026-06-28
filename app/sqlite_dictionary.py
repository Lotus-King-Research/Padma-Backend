"""SQLite-backed, drop-in replacement for Tibetan-Lookup's DictionaryLookup.

The original loads all 21 dictionaries into memory as pandas DataFrames
(~600 MB-1 GB RSS). This holds them on disk in an indexed SQLite file instead,
so resident memory stays flat regardless of corpus size. Output shapes match
what app/utils/matching_*.py expect, so the rest of the app is unchanged.

Lookups map 1:1 to the original semantics:
  exact        -> WHERE Tibetan = ?            (indexed point lookup)
  partial      -> WHERE Tibetan LIKE '%q%'     (bounded by SCAN_LIMIT)
  description  -> WHERE Description LIKE '%q%'  (bounded by SCAN_LIMIT)

Thread-local connections so concurrent requests (Starlette runs sync routes in
a threadpool) execute real parallel reads -- sqlite3 releases the GIL during
query execution.
"""
import os
import re
import sqlite3
import threading

# Cap rows a single scanning query may materialise. The frontend paginates
# (vue-infinite-loading), so a server-side cap matches how results are consumed
# and bounds peak memory under load.
SCAN_LIMIT = int(os.environ.get("PADMA_SCAN_LIMIT", "200"))

DB_PATH = os.environ.get("PADMA_SQLITE", "app/data/dicts.sqlite")

_VALID_TABLE = re.compile(r"^[A-Za-z0-9_]+$")


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
            self._local.con = con
        return con

    @staticmethod
    def _table(source):
        if not _VALID_TABLE.match(source):
            raise ValueError("invalid dictionary name: %r" % source)
        return '"%s"' % source

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
                # ORDER BY length so the capped rows are the shortest matches --
                # this mirrors the original `sorted(out, key=len)` and the
                # frontend's first page, keeping output stable under SCAN_LIMIT.
                rows = con.execute(
                    "SELECT Tibetan, Description FROM %s "
                    "WHERE Tibetan LIKE ? ORDER BY length(Tibetan) LIMIT ?" % tbl,
                    ("%" + string + "%", SCAN_LIMIT)).fetchall()
                d = {t: str(desc) for t, desc in rows}
                d = {k: d[k] for k in sorted(d, key=lambda x: len(x))}
                if fuzzy_match:
                    from dictionary_lookup.utils.fuzzy_matching import fuzzy_matching
                    fm = fuzzy_matching(string, d, n=20)
                    d = {k: d[k] for k in d if k in fm}
                out[source] = d

            elif description_match:
                rows = con.execute(
                    "SELECT Tibetan, Description FROM %s "
                    "WHERE Description LIKE ? LIMIT ?" % tbl,
                    ("%" + string + "%", SCAN_LIMIT)).fetchall()
                out[source] = {t: str(desc) for t, desc in rows}

            else:  # exact
                rows = con.execute(
                    "SELECT Description FROM %s WHERE Tibetan = ?" % tbl,
                    (string,)).fetchall()
                out[source] = {string: [r[0] for r in rows]}

        return out
