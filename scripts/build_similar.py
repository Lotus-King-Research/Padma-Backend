#!/usr/bin/env python3
"""Precompute the `similar` matching neighbours from the word-vectors, so the
running app needs neither gensim nor the vector matrix.

For every word we store the same neighbours the app used to compute live:
`similar_by_word(word, topn=50)` filtered to score >= 0.35, in rank order,
packed as a single tab-joined string per word (one row -> tiny, indexed lookup).
Deterministic from app/data/tibetan.vec; run at image-build time.
"""
import os
import sqlite3
import sys

VEC = os.environ.get("PADMA_VEC", "app/data/tibetan.vec")
OUT = os.environ.get("PADMA_SIMILAR", "app/data/similar.sqlite")
THRESHOLD = 0.35   # must match app/similar_lookup expectations
TOPN = 50


def main():
    from gensim.models import KeyedVectors

    print("Loading vectors from %s ..." % VEC, flush=True)
    v = KeyedVectors.load(VEC, mmap="r")
    vocab = v.index_to_key
    print("vocab=%d dim=%d" % (len(vocab), v.vector_size), flush=True)

    if os.path.exists(OUT):
        os.remove(OUT)
    con = sqlite3.connect(OUT)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("CREATE TABLE sim (word TEXT PRIMARY KEY, neighbors TEXT)")

    batch = []
    for i, w in enumerate(vocab):
        neighbors = [nb for nb, sc in v.similar_by_word(w, topn=TOPN)
                     if sc >= THRESHOLD]
        if neighbors:
            batch.append((w, "\t".join(neighbors)))
        if len(batch) >= 20000:
            con.executemany("INSERT OR IGNORE INTO sim VALUES (?,?)", batch)
            batch = []
        if i % 10000 == 0:
            print("  %d/%d" % (i, len(vocab)), flush=True)
    if batch:
        con.executemany("INSERT OR IGNORE INTO sim VALUES (?,?)", batch)

    con.commit()
    n = con.execute("SELECT COUNT(*) FROM sim").fetchone()[0]
    con.close()
    size_mb = os.path.getsize(OUT) / 1048576
    print("Wrote %s: %d words, %.1f MiB" % (OUT, n, size_mb), flush=True)


if __name__ == "__main__":
    sys.exit(main())
