"""pump_stroke.py [lx ly lz] [metres] -- RE3 / RE2 on the OpenXR Simulator: one pump by hand. The gun level and forward in the
right hand (RG held, as RE2's pump_hold.py), the left controller on the fore-end with LG for 2 s (the dock), then LG + LT,
pulled back along the barrel (room +z) by <metres> (default 0.09) and pushed home, then held 1 s. The plugin's log should
say "rack: WP1000 pump done". One writer at a time: stop pump_hold.py first. 2026-11-19."""
import math, os, sys, time
sys.path.insert(0, os.path.expanduser("~/github-backups/_lanes-next-wt/plugins/lanes/tools/vrbench"))
import vb_input as I, vb_settings as S

RIGHT = [0.15, 1.30, 0.05, 29.6, 77.8]
left = [float(v) for v in sys.argv[1:4]] if len(sys.argv) >= 4 else [0.13, 1.29, -0.43]
pull = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.09


def put(back, lt, secs):
    t0 = time.time()
    while time.time() - t0 < secs:
        w = 0.002 * math.sin((time.time() - t0) * 40.0)
        inp = I.Input().mode(poses="set", buttons="set")
        rp = I.pose_from_ypr([RIGHT[0] + w, RIGHT[1], RIGHT[2]], RIGHT[3], RIGHT[4])
        inp.hand(S.HAND_RIGHT, grip=rp, aim=rp, squeeze=1.0)
        lp = I.pose_from_ypr([left[0] + w, left[1], left[2] + back], 0, 0)
        inp.hand(S.HAND_LEFT, grip=lp, aim=lp, squeeze=1.0, trigger=lt)
        I.write(inp)
        time.sleep(0.01)


put(0.0, 0.0, 2.0)
put(0.0, 1.0, 0.5)
for i in range(1, 11): put(pull * i / 10, 1.0, 0.05)
put(pull, 1.0, 0.4)
for i in range(9, -1, -1): put(pull * i / 10, 1.0, 0.05)
put(0.0, 1.0, 0.5)
put(0.0, 0.0, 1.0)
print("one pump: %.2f m back and home" % pull)
