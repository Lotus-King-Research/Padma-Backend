# Render migration (single 512 MB Starter)

Goal: run the whole app on one Render **Starter** instance (512 MB / 0.5 CPU,
~$7/mo) instead of the current AWS setup (~$100/mo), with no loss of features
and a verifiable, reversible cutover.

## Why the old setup needs ~1 GB

`app/__init__.py` used to load, at startup, **all 21 dictionaries as in-RAM
pandas DataFrames** (~600 MB–1 GB), the **botok** tokenizer trie (~230 MB) and
the **gensim** word-vectors. Measured peak RSS under load was ~900 MB (transient
~1 GB), which is why the production container is pinned at `-m 1000m`.

## What changed (all measured to matter)

| Lever | Effect |
|---|---|
| Dictionaries → on-disk **SQLite** (`app/sqlite_dictionary.py`), built at image-build time (`scripts/build_dicts.py`) | dict RAM ~0 |
| `partial`/`fuzzy`/`description`/`similar` scan **only `dictionaries[0]`** (the only one those modes ever used) | ~21× less CPU + cache, **output-identical** |
| `LIMIT` (`PADMA_SCAN_LIMIT`, default 200) on scanning queries; ordered by length so the cap is the first page | bounds memory; matches the paginated UI |
| `similar` → **precomputed** neighbours (`scripts/build_similar.py` → `similar.sqlite`, packed one row/word), **gensim removed** | −63 MB import, no vector matrix |
| pandas no longer imported at runtime | −44 MB |
| botok kept resident (~230 MB) | tokenize unchanged |

Result under a hard **512 MB / 0.5 CPU** cap (emulating Starter): idle 281 MiB,
all five modes + tokenize functional, **no OOM up to 75 concurrent**, 90 s soak
at 8 concurrent stable at 510 MiB / 45 req/s / p99 0.5 s. Latency p99 < 0.3 s at
realistic load; graceful degradation (no crash) under heavy load.

## Build & run

```sh
docker build -t padma-render -f Dockerfile.render .          # builds dicts.sqlite + similar.sqlite in-image
docker run -m 512m --cpus 0.5 -e PORT=5000 -p 5000:5000 padma-render
```

The data files are produced deterministically in the `databuilder` stage from
`app/data/tibetan.vec` and the published dictionary data, so the runtime image
stays lean (no pandas/gensim loaded). `Dockerfile` (the AWS one) and its CI are
left untouched for the parallel-run phase.

## Verify (output parity vs live production)

```sh
python tests/parity_test.py http://localhost:5000 https://api.padma.io
```

`exact` and `similar` are expected to match exactly (order-insensitive — the
old `set`-intersection ordering is nondeterministic on prod too). `partial` is a
capped subset. `fuzzy`/`description` differences are explained by the `LIMIT`
cap, prod's pre-existing `fuzzy` 500 bug, and **dictionary data drift** (prod
runs a stale image; this build uses current dictionary data).

## Frontend (separate, free)

The frontend is a Vue SPA and is deployed as a **free Render Static Site** —
the backend stays API-only. Because the SPA targets the API by hostname
(`VUE_APP_API_URL`), keeping `api.padma.io` pointed at the new backend means the
frontend needs no change at all. Static-site config for the Padma-Frontend repo:

```yaml
# render.yaml in Padma-Frontend
services:
  - type: web
    name: padma-frontend
    runtime: static
    buildCommand: yarn install && yarn build
    staticPublishPath: ./dist
    envVars:
      - key: VUE_APP_API_URL
        value: https://api.padma.io      # the Render backend's custom domain
    routes:
      - type: rewrite                     # SPA history-mode fallback
        source: /*
        destination: /index.html
```

Total cost: backend Starter ~$7/mo + static site $0 = **~$7/mo**.

## Cutover (no-risk)

1. Deploy the backend as a new Render Starter alongside the untouched AWS prod.
2. Run `tests/parity_test.py`; confirm `exact`/`similar`/`partial` clean.
3. Add `api.padma.io` as the backend's custom domain; point DNS at Render.
   Keep AWS warm for one-step rollback (flip DNS back).
4. Deploy the frontend static site (optional; only if moving it off its current
   host).
