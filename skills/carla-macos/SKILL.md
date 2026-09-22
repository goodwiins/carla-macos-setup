---
name: carla-macos
description: Install, run, or troubleshoot this repository's CARLA 0.9.15 setup on Apple Silicon using Sikarugir, D3DMetal, Colima, and Rosetta. Use for this macOS setup, not other CARLA versions or platforms.
---

# CARLA on Apple Silicon

Use the [setup repository](https://github.com/goodwiins/carla-macos-setup) as the source of truth. Find its checkout (normally `~/CARLA/client`) and read `README.md` before installation or troubleshooting. Keep the Windows CARLA build, Wine wrapper, and recordings out of Git.

## Install

When asked to install, follow the README's server and client sections. Check the machine's architecture, macOS version, free disk space, and existing tools first; skip steps already complete. Pin the Windows server and Python client to **0.9.15**. Use the official CARLA release URL in the README. Sikarugir wrapper creation and D3DMetal selection use its GUI; guide the user through those steps when needed.

Installation is complete only after the CARLA town renders and `~/CARLA/client/run.sh` prints matching client/server versions and `Round-trip OK`.

## Run

```sh
open ~/Applications/Sikarugir/CARLA.app
colima status || colima start
lsof -nP -iTCP:2000 -sTCP:LISTEN
~/CARLA/client/run.sh
```

Wait for the town to render before the client check; a listener on port 2000 alone does not prove the world is ready. `run.sh` selects the Colima Docker context, even if Docker Desktop is active. For a visible autopilot demo, run `~/CARLA/client/run.sh python watch_drive.py`. Its camera follows simulation ticks; the recorder creates a binary CARLA log, not a video.

## Troubleshoot

- If no process listens on port 2000, inspect or relaunch the Sikarugir wrapper.
- If the client times out, check that the CARLA window is still open, the town has rendered, and both versions are 0.9.15. A version handshake without `Round-trip OK` is incomplete.
- If the container cannot find the image, check that Colima is running; do not switch the user's global Docker context to repair this script.
- If the server exits or the world RPC keeps timing out after it has rendered, report the observed state and error. Avoid repeated blind restarts.
