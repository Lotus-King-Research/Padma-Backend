#!/usr/bin/env python3
"""Build the on-disk dictionary store: download all dictionaries (via the
Tibetan-Lookup package) and write them to an indexed SQLite file.

Run at image-build time (needs pandas + network). The resulting
app/data/dicts.sqlite is what the running app queries -- the app itself never
imports pandas. Table order follows dictionaries.csv so that the default
`dictionaries[0]` selection matches the previous pandas implementation.
"""
import os
import sqlite3
import sys

OUT = os.environ.get("PADMA_SQLITE", "app/data/dicts.sqlite")


def main():
    import pandas  # noqa: F401  (ensures a clear error if missing at build time)
    from dictionary_lookup import DictionaryLookup

    print("Downloading all dictionaries (this loads them via pandas)...", flush=True)
    d = DictionaryLookup()

    if os.path.exists(OUT):
        os.remove(OUT)
    con = sqlite3.connect(OUT)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")

    total_rows = 0
    for name, df in d.dictionaries.items():        # dictionaries.csv order
        df = df[["Tibetan", "Description"]].dropna()
        con.execute('DROP TABLE IF EXISTS "%s"' % name)
        con.execute('CREATE TABLE "%s" (Tibetan TEXT, Description TEXT)' % name)
        con.executemany('INSERT INTO "%s" VALUES (?,?)' % name,
                        list(df.itertuples(index=False, name=None)))
        con.execute('CREATE INDEX "idx_%s" ON "%s"(Tibetan)' % (name, name))
        total_rows += len(df)
        print("  %-24s %7d rows" % (name, len(df)), flush=True)

    con.commit()
    con.close()
    size_mb = os.path.getsize(OUT) / 1048576
    print("Wrote %s: %d tables, %d rows, %.1f MiB" % (
        OUT, len(d.dictionaries), total_rows, size_mb), flush=True)


if __name__ == "__main__":
    sys.exit(main())
