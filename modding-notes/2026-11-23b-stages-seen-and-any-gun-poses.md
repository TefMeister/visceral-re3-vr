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

## Build 31: the drum moved by the hand (Tefa, the same night)

Tefa: *"have to open with motion, LG+LT held until it clicks, can either push closed from the handle or place hand on the drum
and push close, always LG+LT for these actions. and hand should always ride along in any games on any weapoins, until said
otherwise"*. Shared `guns/cylinder.cpp` (RE2's repo owns it): LG + LT on the drum TAKE it (either button may come last); while
both stay held the drum follows the left CONTROLLER sideways (the drawn wrist is pinned to the drum, so it cannot be the measure:
my first cut used it and nothing moved), `CYLINDER_TRAVEL_M` 9.4 cm of hand for the whole swing (the drum joint's own travel),
clicks OPEN at 97 % (sound, buzz), and pushed back clicks SHUT; let go part way it stays (the gun will not fire until shut);
latches at both ends so a hand's wobble does not leave it a hair open. The one-press toggle and the swing by itself are gone.
Run `[verified-live 2026-11-23, robot, n=1 after the latch fix]`: "drum taken (LG + LT)", "clicked OPEN (pulled out by the
hand)", "clicked SHUT (pushed back by the hand)", "let go at 0% open (shut)"; the left hand's stage stayed 6 (on the drum) the
whole way. NOT done: closing "from the handle" (which part is the handle, and which way it pushes: asked); the drawn hand is
not docked to the drum (it follows the controller; within the swing it stays 10-13 cm from the drum joint, as when it took it).

## Build 32: round its hinge, and from the front grip (Tefa: "push down and to the right to close, left and up to open, yes the grip")

- The MGL's hinge (`_01`) sits 9.6 cm ABOVE the drum (`_02`), so a 100 degree swing carries the drum 9.4 cm left AND about
  11 cm up: build 31 measured the hand along the gun's left only. Now `cylinder.cpp` learns the hinge once per gun with the
  drum shut (the log: "hinge at 0.0 14.6 16.1 cm, the drum shut at 0.0 5.1 26.1 cm (the gun's frame)"), and the drum's angle
  follows the left CONTROLLER's angle round the hinge's axis (room space). Up and left opens, down and right closes.
- LG + LT also take the drum at the place it sits shut: the front grip hangs just ahead of the drum, so with the drum open the
  hand on the grip (15 cm from the open drum) takes it and pushes it shut.
- Run `[verified-live 2026-11-23, robot, n=1 each]` (`tools/sim/drumtest.py` in the Village repo): from the drum, the hand
  round the hinge: "clicked OPEN (pulled up and out by the hand)", the drawn wrist stayed 10.5 to 11 cm from the drum the whole
  way (the hand rides along with it); from the grip, the hand down and right: the drum back to shut. The robot's arc is not
  exact (its room is turned and the drawn wrist does not follow the controller one to one), so one close stopped at 11 %
  short of the click: a hand on the drum carries it round its true arc; the wearer's to feel.
