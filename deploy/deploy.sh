#!/bin/sh
# Update the server to the latest master and (re)deploy the backend stack.
# Run on the server:  sh /opt/padma/backend/deploy/deploy.sh [--refresh-data]
#   --refresh-data  re-download the dictionaries from Padma-Dictionary-Data
#                   (otherwise the cached data from the previous build is kept)
set -eu
cd "$(dirname "$0")/.."
REFRESH=0
[ "${1:-}" = "--refresh-data" ] && REFRESH=$(date +%s)

git fetch -q origin
git checkout -q master
git pull -q --ff-only origin master
docker compose -f deploy/docker-compose.yml build --build-arg DICT_DATA_REFRESH="$REFRESH"
docker compose -f deploy/docker-compose.yml up -d
docker image prune -f >/dev/null
docker compose -f deploy/docker-compose.yml ps
