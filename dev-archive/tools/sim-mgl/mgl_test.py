"""mgl_test.py: the robot hands load RE3's MGL from the two hips and fire it (session alone, simulator)."""
import os, subprocess, sys, time
sys.path.insert(0, os.path.expanduser("~/github-backups/_lanes-next-wt/plugins/lanes/tools/vrbench"))
import vb_input as I, vb_settings as S, vb_sim

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = r"C:\Steam\steamapps\common\RE3\re2_framework_log.txt"
RIGHT = I.pose_from_ypr((0.15, 1.40, -0.30), 0, 0)        # the gun held forward
LEFT_REST = (-0.30, 1.30, -0.25)
HIP = {"left": (-0.20, 1.08, -0.02), "right": (0.20, 1.08, -0.02)}


def send(lpos, lkw=None, rkw=None):
    lp = I.pose_from_ypr(lpos, 0, 0)
    inp = I.Input().mode(poses="set", buttons="set")
    inp.hand(S.HAND_LEFT, grip=lp, aim=lp, **(lkw or {}))
    inp.hand(S.HAND_RIGHT, grip=RIGHT, aim=RIGHT, **(rkw or {}))
    I.write(inp)


def ask(*args):
    env = dict(os.environ, RV_GAME_DIR=r"C:\Steam\steamapps\common\RE3")
    rv = os.path.expanduser("~/github-backups/visceral-re8-vr/dev-archive/native/tools/sim/rv.py")
    return subprocess.run([sys.executable, rv, *args], capture_output=True, text=True, env=env).stdout.strip()


def log_tail(mark):
    with open(LOG, "rb") as f:
        f.seek(mark)
        text = f.read().decode("utf-8", "replace")
    return [ln.split("[info] ", 1)[-1][:170] for ln in text.splitlines() if "rounds:" in ln or "shells:" in ln or "ammo:" in ln]


def fire(n=1):
    for _ in range(n):
        send(LEFT_REST, rkw={"trigger": 1.0}); time.sleep(0.4); send(LEFT_REST); time.sleep(2.2)


def load_from(hip):
    """LG at that hip, carry to the port (closing in on it by asking the game), LT, let go"""
    send(HIP[hip]); time.sleep(0.8)
    send(HIP[hip], lkw={"squeeze": 1.0}); time.sleep(0.8)
    pos = list(LEFT_REST)
    send(pos, lkw={"squeeze": 1.0}); time.sleep(0.8)
    d = 9.0
    for _ in range(8):
        a = ask("-f", os.path.join(HERE, "port.lua")).split()
        if len(a) != 4:
            print("   port ask failed:", a); break
        ex, ey, ez, d = map(float, a)
        if d < 0.05:
            break
        pos = [pos[0] + ex, pos[1] + ey, pos[2] + ez]
        send(pos, lkw={"squeeze": 1.0}); time.sleep(0.7)
    print(f"   {hip} hip: shell {d:.3f} m from the port")
    time.sleep(0.8)
    send(pos, lkw={"squeeze": 1.0, "trigger": 1.0}); time.sleep(0.4)
    send(pos, lkw={"squeeze": 1.0}); time.sleep(2.0)
    send(LEFT_REST); time.sleep(1.0)


def main():
    vb_sim.head(0, 1.7, 0, 0, 0)
    mark = os.path.getsize(LOG)
    send(LEFT_REST); time.sleep(1)
    for step in sys.argv[1:]:
        if step.startswith("fire"):
            fire(int(step[4:] or 1))
        elif step in ("left", "right"):
            load_from(step)
        print(f"-- after {step}")
        for ln in log_tail(mark):
            print("   " + ln)
        mark = os.path.getsize(LOG)


if __name__ == "__main__":
    main()
