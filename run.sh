#!/usr/bin/env bash
# Build (cached after first run) and run the CARLA client.
#   ./run.sh                     # default spawn_test.py
#   ./run.sh python watch_drive.py
#   ./run.sh bash                # shell inside the container
set -euo pipefail
export DOCKER_CONTEXT=colima
cd "$(dirname "$0")"
IMAGE="carla-client:0.9.15"
docker build --platform=linux/amd64 -t "$IMAGE" .
exec docker run --rm -it \
    --platform=linux/amd64 \
    --add-host=host.docker.internal:host-gateway \
    -v "$PWD:/app" \
    "$IMAGE" "$@"
