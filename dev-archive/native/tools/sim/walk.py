"""walk.py <seconds> [x y] -- RE3 / RE2 on the OpenXR Simulator: hold the LEFT stick (default 0 -1 = straight back) for a
time, then let go. The usual RE3 save starts Jill at the typewriter desk: 2 s back puts her in open floor, where a long gun
held forward meets no furniture (the walls feature turns a gun away from a desk and spoils a hand measurement). The game
must be in front. 2026-11-19."""
import os, sys, time
sys.path.insert(0, os.path.expanduser("~/github-backups/_lanes-next-wt/plugins/lanes/tools/vrbench"))
import vb_input as I, vb_settings as S
secs = float(sys.argv[1])
xy = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) >= 4 else (0.0, -1.0)
t0 = time.time()
while time.time() - t0 < secs:
    I.write(I.Input().mode(poses="pass", buttons="set").hand(S.HAND_LEFT, stick=xy))
    time.sleep(0.05)
I.write(I.Input().mode(poses="pass", buttons="set"))
print("left stick %s held %.1f s" % (xy, secs))
