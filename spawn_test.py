import os, sys, time, random
import carla

HOST = os.environ.get("CARLA_HOST", "host.docker.internal")
PORT = int(os.environ.get("CARLA_PORT", "2000"))

def main() -> int:
    print(f"Connecting to {HOST}:{PORT} ...")
    client = carla.Client(HOST, PORT); client.set_timeout(20.0)
    print("  client:", client.get_client_version(), "| server:", client.get_server_version())
    world = client.get_world()
    bp = world.get_blueprint_library()
    spawns = world.get_map().get_spawn_points()
    print(f"Map: {world.get_map().name} | {len(spawns)} spawn points")
    veh = None
    for tf in random.sample(spawns, k=min(10, len(spawns))):
        veh = world.try_spawn_actor(random.choice(bp.filter("vehicle.*")), tf)
        if veh: break
    if not veh: print("spawn failed", file=sys.stderr); return 1
    print("Spawned", veh.type_id, "id", veh.id); veh.set_autopilot(True)
    for i in range(5):
        time.sleep(1.0); l = veh.get_location()
        print(f"  t+{i+1}s ({l.x:.1f},{l.y:.1f},{l.z:.1f})")
    veh.destroy(); print("Round-trip OK"); return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except RuntimeError as e:
        print("ERROR:", e, "\nIs CARLA.app running on port 2000?", file=sys.stderr); sys.exit(1)
