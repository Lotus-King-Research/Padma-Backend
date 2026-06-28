#!/usr/bin/env python3
"""Output-parity harness: compare the new (lean) backend against the live
production API across every matching mode, so we can prove behaviour is
preserved before any DNS cutover.

Usage:
    python tests/parity_test.py NEW_BASE [PROD_BASE]
    # e.g. python tests/parity_test.py http://localhost:5000 https://api.padma.io

For each query it calls both backends and compares the JSON. exact/similar are
expected to match exactly. partial/fuzzy/description are bounded by SCAN_LIMIT on
the new side, so they are checked as "new is a prefix of prod" (prod truncated to
the cap), which is what the paginated UI shows. The known pre-existing fuzzy 500
on prod is reported, not counted as a regression.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

NEW = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
PROD = sys.argv[2] if len(sys.argv) > 2 else "https://api.padma.io"
CAP = 200  # must match PADMA_SCAN_LIMIT
# api.padma.io sits behind Cloudflare, which 403s rapid header-less bursts.
# Send a browser UA and throttle requests to production.
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 parity-test"
PROD_DELAY = 1.0

# (matching mode, query, dictionaries-or-None)
WORDS = ["སེམས་", "ཆོས་", "བྱང་ཆུབ་", "རྣམ་ཤེས་", "སྟོང་པ་ཉིད་", "པདྨ་འབྱུང་གནས་",
         "ཀུན་བརྟགས་", "བདེ་བ་", "ཤེས་རབ་", "དགེ་བ་"]
CASES = []
for w in WORDS:
    CASES.append(("exact", w, None))
    CASES.append(("exact", w, None, "true"))       # tokenize=true
    CASES.append(("partial", w, None))
    CASES.append(("fuzzy", w, None))
    CASES.append(("similar", w, None))
CASES.append(("description", "lotus", "84000"))
CASES.append(("description", "buddha", "84000"))
CASES.append(("description", "wisdom", "84000"))


def call(base, mode, query, dicts, tokenize=None):
    params = {"query": query, "matching": mode}
    if dicts:
        params["dictionaries"] = dicts
    if tokenize:
        params["tokenize"] = tokenize
    url = base + "/dictionary_lookup?" + urllib.parse.urlencode(params)
    if base == PROD:
        time.sleep(PROD_DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or "null")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return "ERR:" + type(e).__name__, None


def _txt(t):
    return tuple(t) if isinstance(t, list) else t


def result_set(mode, body):
    """Normalise any response to an order-insensitive set of result tuples.
    exact uses (source, text) pairs; list modes use (search_query, text).
    Order is nondeterministic across processes (set-intersection / hashing),
    so set comparison is the correct parity invariant."""
    if body is None:
        return frozenset()
    if isinstance(body, dict):                       # exact shape
        out = set()
        for grp_t, grp_s in zip(body.get("text", []), body.get("source", [])):
            for t, s in zip(grp_t, grp_s):
                out.add((s, _txt(t)))
        return frozenset(out)
    if isinstance(body, list):                       # partial/fuzzy/similar/description
        return frozenset((item.get("search_query"), _txt(item.get("text")))
                         for item in body)
    return frozenset()


def main():
    exact_ok = exact_bad = bounded_ok = bounded_bad = skipped = 0
    failures = []
    for case in CASES:
        mode, query, dicts = case[0], case[1], case[2]
        tok = case[3] if len(case) > 3 else None
        sc_n, body_n = call(NEW, mode, query, dicts, tok)
        sc_p, body_p = call(PROD, mode, query, dicts, tok)
        label = "%s/%s%s" % (mode, query, "+tok" if tok else "")

        if str(sc_p).startswith("5") or sc_p == "ERR:HTTPError":
            print("SKIP  %-22s prod=%s (pre-existing)" % (label, sc_p)); skipped += 1; continue
        if sc_n == 404 and sc_p == 404:
            print("OK=   %-22s both 404" % label); exact_ok += 1; continue
        if sc_n != sc_p:
            print("FAIL  %-22s status new=%s prod=%s" % (label, sc_n, sc_p))
            failures.append(label); exact_bad += 1; continue

        rs_n, rs_p = result_set(mode, body_n), result_set(mode, body_p)
        if mode in ("exact", "similar"):
            if rs_n == rs_p:
                print("OK    %-22s exact set-match (%d)" % (label, len(rs_n))); exact_ok += 1
            else:
                print("FAIL  %-22s set differs  new=%d prod=%d  only_new=%d only_prod=%d"
                      % (label, len(rs_n), len(rs_p), len(rs_n - rs_p), len(rs_p - rs_n)))
                failures.append(label); exact_bad += 1
        else:  # bounded: new is a capped subset of prod (== when prod <= cap)
            if rs_n <= rs_p and (len(rs_p) > CAP or rs_n == rs_p):
                print("OK    %-22s bounded subset (new=%d prod=%d)" % (label, len(rs_n), len(rs_p)))
                bounded_ok += 1
            else:
                print("DIFF  %-22s new=%d prod=%d only_new=%d (inspect)"
                      % (label, len(rs_n), len(rs_p), len(rs_n - rs_p)))
                bounded_bad += 1; failures.append(label)

    print("\n=== PARITY SUMMARY ===")
    print("exact modes  : %d ok, %d fail" % (exact_ok, exact_bad))
    print("bounded modes: %d ok, %d differ" % (bounded_ok, bounded_bad))
    print("skipped (prod 5xx): %d" % skipped)
    if failures:
        print("ATTENTION: %d case(s) to inspect: %s" % (len(failures), ", ".join(failures)))
        return 1
    print("ALL CLEAR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
