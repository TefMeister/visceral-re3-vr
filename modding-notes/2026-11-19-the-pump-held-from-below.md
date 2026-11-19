# 2026-11-19: the M3's left hand goes UNDER the pump handle (Developer PC, Fable, Tefa away; RE3 b027)

Tefa, 2026-11-19: RE2 and RE3 "both also need the shotgun hand rotated 180 degrees, as at the moment left hand on the
shotgun docks above the pump handle, not under it". RE2 got it this morning (b217, its note of the same name); this is RE3's.

## What is built
- **The shared hold, taken from RE2** with `tools/sync_shared.py` (RE2 commit 7ae859d): `src/guns/rack.cpp` `pump_shotgun()` /
  `pump_dock()`, `settings_guns.h` `PUMP_DOCK_YPR {173, 18, 0}`, `PUMP_DOCK_OFF {0.078, -0.026, 0.035}`, the tuning file
  `reframework/data/visceral_pump_dock.txt` ("yaw pitch roll x y z"; not installed). The M3 (WP1000) is in RE3's `SHELL_GUNS`
  and `is_pump()`, so it takes the new hold; the MGL is a shell gun but not a pump, so it does not `[inferred-static, then seen]`.
- **RE3's own 7 cm forward shift.** New in the shared code: `pump_dock_shift(int wp)` (declared in `guns/gun_data.h`, answered
  by each game's `src/game/guns_table.cpp`), added to the built-in place; the tuning file's numbers are taken as they are.
  RE2 answers zero (no change there, compiled, not reinstalled: its b217 behaves the same); RE3 answers `{0, 0, 0.070}` for
  the M3.
- Why: the M3's fore-end joint `_01` sits 42.5 cm ahead of the gun's root `[measured, live, n=1]` and, by the side view, at the
  REAR end of the handle: with the W-870's numbers the hand gripped the handle's back edge `[verified-live 2026-11-19,
  simulator, n=2 pictures]`. 7 cm forward the hand is on the handle, a little behind its middle `[simulator, n=1 picture]`.

## Simulator `[verified-live 2026-11-19, simulator, n=2 launches]`
- Jill's usual save, 2 s back from the typewriter desk, the M3 from slot 4 (`tools/sim/q_give_m3.lua`), RE2's `pump_hold.py`.
- Launch 1 (the W-870's numbers): docked (the loader: "0.018 m from the socket"); `q_pump_hold.lua`: wrist 0.078 left,
  0.026 UNDER, 0.035 forward, palm facing up 0.96. The same numbers as RE2. The side picture: the arm comes up from below,
  the hand under the handle, fingers curled up the far side.
- Launch 2 (the final build, the shift built in, no tuning file): docked, palm up 0.96, wrist 0.015 under, 0.078 forward
  (the place asked for is 0.105 forward: the robot's left arm was at full stretch and stopped 2.7 cm short `[hypothesis]`;
  the same shortfall showed with the tuning file on launch 1).
- One pump by hand (`tools/sim/pump_stroke.py`: LG, then LG + LT, 9 cm back and home): `rack: WP1000 pump done (for show),
  3 loaded`.
- Ghost Hand BeG0nE (launch 1): both hands trail the controller by 1 frame; the left "wanders up to 6.3 cm from its usual
  place", which is the dock itself.

## Learned on the way
- At the typewriter desk the gun held forward meets the desk: the walls feature (b026) turns the gun away ("the gun turned at
  the wrist, away from a wall") and the muzzle read 24 degrees up. Measure hands in open floor.
- Changing the hold's place while the hand is docked moves the socket away from the still controller: the hand lets go and
  the gun swings (the left hand steers a pump gun). Move the controller by the same amount as the hold.
- The head pose (-0.5, 1.32, -0.38, yaw -90) broke the dock; RE2's (-0.45, 1.38, -0.45, yaw -75, pitch -10) did not, twice.
- The game closed on the first window close both times today (window in front, 2 s wait).

## Not established
- How it looks and feels in the headset (Tefa): `[ID RE3-001]`. Whether 7 cm is the right amount is a matter of feel: the
  tuning file is there for it ("173 18 0 0.078 -0.026 0.105" is what is built in).
- The forearm's twist in the new hold; Carlos's hands; whether the full stretch of the robot's arm is the whole of the
  2.7 cm.
- Kept logs: `dev-archive/native/build/re3_fw_log_2026-11-19_run1.txt`, `..._run2_b027.txt` (local, not in git).

## Tools left behind (`dev-archive/native/tools/sim/`)
`q_give_m3.lua` (the M3 into Jill's hand: the slot that holds it, or a gift), `walk.py` (hold the left stick for a time: 2 s
back from the desk), `pump_stroke.py` (one pump by hand). RE2's `pump_hold.py`, `q_pump_hold.lua`, `sim_window.py` were used
as they are.
