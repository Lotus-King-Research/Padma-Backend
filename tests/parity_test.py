#!/usr/bin/env python3
"""Output-parity harness: compare the new (SQLite) backend against a reference
backend (the original pandas implementation, or live production) across every
matching mode, to prove behaviour is unchanged.

Usage:
    python tests/parity_test.py NEW_BASE REF_BASE
    # e.g. python tests/parity_test.py http://127.0.0.1:5000 http://127.0.0.1:5001
    #      python tests/parity_test.py http://127.0.0.1:5000 https://api.padma.io

Standard: every response must be byte-identical (same status, same JSON, same
order) -- except `exact`, whose source ordering comes from a Python set() in
app/utils/matching_exact.py and is random per process in the original too, so
it is compared as an order-insensitive set.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

NEW = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000"
REF = sys.argv[2] if len(sys.argv) > 2 else "https://api.padma.io"
# api.padma.io sits behind Cloudflare, which 403s rapid header-less bursts:
# send a browser UA and throttle requests to https endpoints.
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 parity-test"
HTTPS_DELAY = 1.0

WORDS = ["སེམས་", "ཆོས་", "བྱང་ཆུབ་", "རྣམ་ཤེས་", "སྟོང་པ་ཉིད་", "པདྨ་འབྱུང་གནས་",
         "ཀུན་བརྟགས་", "བདེ་བ་", "ཤེས་རབ་", "དགེ་བ་"]

# (label, params)
CASES = []
for w in WORDS:
    CASES.append(("exact/" + w, {"query": w, "matching": "exact"}))
    CASES.append(("exact+tok/" + w, {"query": w, "matching": "exact", "tokenize": "true"}))
    CASES.append(("partial/" + w, {"query": w, "matching": "partial"}))
    CASES.append(("fuzzy/" + w, {"query": w, "matching": "fuzzy"}))
    CASES.append(("similar/" + w, {"query": w, "matching": "similar"}))
for q in ["lotus", "buddha", "Buddha", "wisdom", "mind", "the"]:
    CASES.append(("description/" + q, {"query": q, "matching": "description", "dictionaries": "84000"}))
CASES += [
    ("description/regex", {"query": "bodhisattva|arhat", "matching": "description", "dictionaries": "84000"}),
    ("description/bad-regex", {"query": "(", "matching": "description", "dictionaries": "84000"}),
    ("exact/wylie", {"query": "sems", "matching": "exact"}),
    ("partial/wylie", {"query": "chos", "matching": "partial"}),
    ("exact/2-dicts", {"query": "སེམས་", "matching": "exact", "dictionaries": "84000,tony_duff"}),
    ("partial/tony_duff", {"query": "སེམས་", "matching": "partial", "dictionaries": "tony_duff"}),
    ("fuzzy/tony_duff", {"query": "ཤེས་རབ་", "matching": "fuzzy", "dictionaries": "tony_duff"}),
    ("similar/monlam", {"query": "སེམས་", "matching": "similar", "dictionaries": "lobsang_monlam"}),
    ("exact/no-match", {"query": "ཀཀཀཀ་", "matching": "exact"}),
    # multi-word tokenization (botok segmentation)
    ("tokenize/sentence-1", {"query": "བཀྲ་ཤིས་བདེ་ལེགས་ཕུན་སུམ་ཚོགས།", "matching": "exact", "tokenize": "true"}),
    ("tokenize/sentence-2", {"query": "སངས་རྒྱས་ཀྱི་བསྟན་པ་རིན་པོ་ཆེ་", "matching": "exact", "tokenize": "true"}),
    ("tokenize/sentence-3", {"query": "བྱང་ཆུབ་སེམས་དཔའ་སེམས་དཔའ་ཆེན་པོ་", "matching": "exact", "tokenize": "true"}),
]


def call(base, params):
    url = base + "/dictionary_lookup?" + urllib.parse.urlencode(params)
    if base.startswith("https://"):
        time.sleep(HTTPS_DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read() or "null")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return "ERR:" + type(e).__name__, None


def exact_set(body):
    out = set()
    for grp_t, grp_s in zip(body.get("text", []), body.get("source", [])):
        for t, s in zip(grp_t, grp_s):
            out.add((s, json.dumps(t, sort_keys=True)))
    return out


def main():
    ok = bad = 0
    failures = []
    for label, params in CASES:
        sc_n, body_n = call(NEW, params)
        sc_r, body_r = call(REF, params)
        if sc_n != sc_r:
            verdict = "FAIL  status new=%s ref=%s" % (sc_n, sc_r)
        elif body_n == body_r:
            verdict = "OK    identical" + (" (both %s)" % sc_n if sc_n != 200 else "")
        elif params["matching"] == "exact" and isinstance(body_n, dict) and isinstance(body_r, dict) and \
                exact_set(body_n) == exact_set(body_r) and body_n.get("tokens") == body_r.get("tokens"):
            verdict = "OK    identical as a set (order is random in the original too)"
        else:
            n_n = len(body_n) if isinstance(body_n, list) else "-"
            n_r = len(body_r) if isinstance(body_r, list) else "-"
            verdict = "FAIL  content differs (new=%s ref=%s items)" % (n_n, n_r)
        if verdict.startswith("OK"):
            ok += 1
        else:
            bad += 1
            failures.append(label)
        print("%-34s %s" % (label, verdict), flush=True)

    print("\n=== PARITY SUMMARY: %d identical, %d different (of %d) ===" % (ok, bad, len(CASES)))
    if failures:
        print("different: " + ", ".join(failures))
        return 1
    print("ALL IDENTICAL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
