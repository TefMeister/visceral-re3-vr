# 2026-11-23 (late evening, /lm by hand-on, PC1, Opus): RE3's stages seen by robot, "any gun" poses; build 30

Same rig as RE2's note of the same evening (`visceral-re2-vr/modding-notes/2026-11-23c-any-gun-poses-and-the-w870-stages.md`):
the desk headset, VR Bench's hands, Jill's save (Continue), nobody wearing it. Build 30 = build 29 + Hand Poser's new script
(a docked spot a gun has no pose for takes "any gun @ <spot>"); `sync_shared.py` had nothing to copy.

## Seen by robot `[verified-live 2026-11-23, robot, n=1 each]`

- **The MGL's drum, stage 6**: LG at `_02` gives stage 6; LG + LT: "opening". The moment the drum swings out (about 9 cm to the
  left, build 28) the hand is no longer at the drum joint and the stage drops to 0: the hand's drum pose is lost while the drum
  is open. Not changed: a question for Tefa (should the hand ride along with the drum as it swings, or let go?).
- **The G19, stages 3, 4 and 13**: the slide (`re_go.py _01`, LG), the seated magazine (`re_seek.py _04 "left hand 4" 6 lg`:
  0 -6 0 cm from `_04`), B: "sliding out", "in the left hand".
- **Poses for every gun**: RE2's "any gun @ slide / magazine / magazine in hand" (the Matilda's coarse poses) sent through the
  window at each stage and kept as RE3's "any gun" poses (`pose.py <joints>`, then `pose.py save_as=any`).

## Found, not fixed: the magazine in the hand is not drawn

With "magazine in hand" (stage 13, the log: "in the left hand"), the magazine joint `_04` sits in the fingers by numbers
(`q_re_maghand.lua`: 9.9 / -2.4 / 5.6 cm in the wrist's frame), but three pictures from three sides show the hand with NO
magazine (`2026-11-23b-sheets/g19-magazine-in-hand-not-drawn.jpg`). In RE2 the Matilda's carried magazine IS drawn. n=1, the
G19 only; on the fault list. The log also said "out with 33 loaded" for the G19.

## Not done

- No picture judged the copied poses on the slide or the magazine (only the hand in the air, three sides: a curled hand).
- The other RE3 guns (11, 21, 31, 42, 47) were not run tonight.
