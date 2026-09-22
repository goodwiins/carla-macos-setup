import os, sys, time
import carla

HOST = os.environ.get("CARLA_HOST", "host.docker.internal")
PORT = int(os.environ.get("CARLA_PORT", "2000"))
RECORD_NAME = os.environ.get("RECORD_NAME", "watch_drive.log")

def main() -> int:
    c = carla.Client(HOST, PORT); c.set_timeout(20.0)
    print(c.show_recorder_file_info(RECORD_NAME, False))
    print(f"Replaying {RECORD_NAME} — watch the CARLA.app window!")
    c.replay_file(RECORD_NAME, 0.0, 0.0, 0, False)
    time.sleep(2.0); return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except RuntimeError as e:
        print("ERROR:", e, file=sys.stderr); sys.exit(1)
