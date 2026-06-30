"""Precomputed nearest-neighbour lookup, replacing the gensim word-vectors.

The original `similar` matching loaded a 31 MB word2vec model via gensim
(KeyedVectors) and called `similar_by_word` at request time -- which pulls the
full vector matrix into RAM and drags in gensim + numpy + scipy (~170 MB).

Instead we precompute, offline, the same `similar_by_word(token, topn=50)`
neighbours (filtered to score >= 0.35, the threshold the app used) and store
them packed one row per word in SQLite. Runtime cost: a single indexed lookup,
zero gensim. See scripts/build_similar.py for the (deterministic) build step.
"""
import os
import re
import sqlite3
import threading

DB_PATH = os.environ.get("PADMA_SIMILAR", "app/data/similar.sqlite")

_local = threading.local()
_TRAIL = re.compile(r"\་+$")


def _conn():
    con = getattr(_local, "con", None)
    if con is None:
        con = sqlite3.connect(DB_PATH, check_same_thread=False)
        con.execute("PRAGMA query_only=ON")
        _local.con = con
    return con


def similar_words(token):
    """Return the post-processed neighbour list, matching the original
    matching_similar() pipeline: score>=0.35, strip trailing tsheg, dedupe,
    re-append a single tsheg."""
    row = _conn().execute(
        "SELECT neighbors FROM sim WHERE word = ?", (token,)).fetchone()
    if not row or not row[0]:
        return []
    words = row[0].split("\t")          # stored score>=0.35, in rank order
    words = [_TRAIL.sub("", w) for w in words]
    words = list(dict.fromkeys(words))
    words = [w + "་" for w in words]
    return words
