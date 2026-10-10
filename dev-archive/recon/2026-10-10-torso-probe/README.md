# Torso push when Jill stops: measured, then fixed (2026-10-10, Tefa in the headset)

The view is tied to Jill's head (head fwd 0.000 always), so the push is the body moving under the head.
Numbers are metres ahead of the view, flattened, from probe-log.txt `[verified-live 2026-10-10, n=1 each]`:

| standing pose (slot 0xa0/0xa6) | walking: COG / spine_2 | standing: COG / spine_2 | Tefa |
| --- | --- | --- | --- |
| 0160 Gazing_Idle (stock) / 0161 Relax | -0.07 / -0.06 | +0.01..+0.03 / -0.01 | "still pushing the torso forward" |
| es_2000 TypeA Gazing_Idle | -0.03..-0.06 / -0.03 | -0.19..-0.33 / -0.13..-0.21 | "seems fine" |

With es_2000 the body stays behind the view when she stops, so nothing pushes forward. It sways a few cm in its 4.8 s
loop (the speed column reads 0.02-0.05 m/s) and the feet stand ~0.2 m behind the head; Tefa saw nothing wrong.
Installed: swap_idle_re3.py --idle es_2000_TypeA_Gazing_Idle_F_Loop over the port 1+2 lists + cmn (Jill only).
