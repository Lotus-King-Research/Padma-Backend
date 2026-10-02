# Deployment

The backend runs as a Docker Compose service on a single server, behind the
server's shared nginx edge proxy (configured on the server in `/opt/edge`, not
in this repo), which terminates TLS for every site on the machine and reaches
this container as `padma-backend` on the external `edge` Docker network.
Cloudflare (proxied, SSL mode Full/strict) sits in front of `api.padma.io`.
The frontend's static build is served by the same nginx at `padma.io`.

```
Cloudflare ──443──▶ edge nginx (TLS, :80→:443 redirect) ──▶ padma-backend (uvicorn :5000)
```

## Deploy / update

On the server, from a checkout at `/opt/padma/backend`:

```sh
sh deploy/deploy.sh                 # pull master, rebuild, restart
sh deploy/deploy.sh --refresh-data  # also re-download the dictionaries
```

TLS (a Cloudflare Origin CA certificate for `*.padma.io`) lives with the edge
proxy in `/opt/edge/certs` on the server.

The image (`Dockerfile.render`) builds all data in a separate stage — the 21
dictionaries into `dicts.sqlite` (`scripts/build_dicts.py`) and the `similar`
neighbours into `similar.sqlite` (`scripts/build_similar.py`) — so the runtime
needs no network and never loads pandas or gensim at startup. Dependencies are
pinned to the versions verified by the parity test; upgrade them deliberately
and re-run it.

## Why it needs ~1/4 of the old memory

The original loaded all 21 dictionaries as pandas DataFrames (~480 MB), gensim
(~110 MB) and the botok trie (~210 MB) at startup: ~880 MB resident. Now the
dictionaries and `similar` neighbours are queried from on-disk SQLite, so the
container idles at ~280 MB (mostly the botok trie).

Limits in `deploy/docker-compose.yml`: 1 GB memory (no swap), 1 CPU. Normal
traffic stays under 512 MB; 1 GB covers the worst case — 40+ concurrent
multi-megabyte queries (e.g. `description` for "the") — with no OOM. The app is
one uvicorn worker and GIL-bound, so more CPUs would not help.

## Behaviour vs. the original

`app/sqlite_dictionary.py` mirrors the original pandas `DictionaryLookup._query`:
case-sensitive regex-equivalent matching, first-syllable candidates for
`fuzzy`, file order with last-duplicate-wins, no result cap. Against the
original implementation running side by side (same data, same library
versions), `tests/parity_test.py` finds **63 of 68 cases byte-identical**. The
other 5 are queries where the original returns HTTP 500:

- `fuzzy`: the original runs fuzzy matching on all 21 dictionaries and crashes
  if any of them has no candidates, although only `dictionaries[0]` is
  returned. The new code queries just that dictionary and returns exactly what
  the original algorithm computes for it.
- `similar` for a word missing from the vector model: the original crashes
  (500); the new code returns "not found" (404).

Every request type is also faster (exact 20x, partial 40x, similar 600x, broad
description/partial queries 2-3x).

```sh
python tests/parity_test.py http://127.0.0.1:5000 https://api.padma.io
```

`exact` is compared as a set because its source order comes from a Python
`set()` in `app/utils/matching_exact.py` and is random per process in the
original too.
