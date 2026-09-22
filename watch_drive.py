import os, sys, time, math, random
import carla

HOST = os.environ.get("CARLA_HOST", "host.docker.internal")
PORT = int(os.environ.get("CARLA_PORT", "2000"))
DRIVE_SECONDS = int(os.environ.get("DRIVE_SECONDS", "60"))
RECORD_NAME = "watch_drive.log"

def chase(tf):
    yaw = math.radians(tf.rotation.yaw)
    loc = carla.Location(tf.location.x - 6*math.cos(yaw),
                         tf.location.y - 6*math.sin(yaw), tf.location.z + 3)
    return carla.Transform(loc, carla.Rotation(pitch=-15, yaw=tf.rotation.yaw))

def main() -> int:
    c = carla.Client(HOST, PORT); c.set_timeout(20.0)
    w = c.get_world(); spec = w.get_spectator()
    bp = (w.get_blueprint_library().filter("vehicle.tesla.model3")
          or w.get_blueprint_library().filter("vehicle.*"))[0]
    veh = None
    spawns = w.get_map().get_spawn_points()
    for tf in random.sample(spawns, k=min(99, len(spawns))):
        veh = w.try_spawn_actor(bp, tf)
        if veh: break
    if veh is None:
        raise RuntimeError("No free vehicle spawn point")
    print("Spawned", veh.type_id)
    c.start_recorder(RECORD_NAME, True); veh.set_autopilot(True)
    print(f"Following for {DRIVE_SECONDS}s — watch the CARLA.app window!")
    try:
        end = time.monotonic() + DRIVE_SECONDS
        while time.monotonic() < end:
            vehicle = w.wait_for_tick(2.0).find(veh.id)
            if vehicle:
                spec.set_transform(chase(vehicle.get_transform()))
    finally:
        c.stop_recorder(); veh.destroy(); print("Recording saved.")
    return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except RuntimeError as e:
        print("ERROR:", e, file=sys.stderr); sys.exit(1)
