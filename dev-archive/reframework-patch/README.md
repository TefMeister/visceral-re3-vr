# REFramework patches for Visceral RE3

- `2026-11-15-re2-re3-shared-layout-menu-and-dodge.patch` — against `76298bd`, cumulative (everything in `D:/ref-76b`,
  which builds BOTH games: `build2/bin/RE2` and `build2/bin/RE3`; apply this one alone). THE SHARED VISCERAL LAYOUT
  (Tefa 2026-11-14; 2026-11-15: "the shared layout everywhere, where the functions apply"), in `VR.cpp
  openvr_input_to_re2_re3`: the menu (system) button TAPPED = the map screen (`MINIMAP` for 6 frames after the let-go),
  HELD 0.3 s = `PAUSE` (REFramework's own pause request still pauses at once); RE3 only: dodge = the right stick CLICK
  as well as its own dodge action (the left stick gives the direction, the game's own). RE2 has no dodge, jump or
  crouch; RE3 no jump or crouch: those stick gestures stay unused. `[compile-verified 2026-11-15]`, installed (RE2
  dinput8 b0cff3eb = build b209, RE3 4677adbd = build b020), not run. Previous files in
  `D:/Visceral build versions/_backup-2026-11-15-shared-layout-refw/`. Build: `D:/ref-76b/build2`, targets RE2 and RE3.

- 2026-11-15 (later), the same patch file rewritten: the menu button tapped no longer pauses (REFramework raises `handle_pause` on the same press; it is no longer ORed into PAUSE). Installed RE2 b210 (dinput8 340ef5f7), RE3 b021 (1501c371). Found by the Village /lm session's reader `[inferred-static 2026-11-15, OpenXR.cpp:325]`, compiled, not run.

- `2026-11-16b-re2-re3-sidestep-click.patch` — against `76298bd`, cumulative (CONTAINS the 2026-11-16 cutscene screen patch;
  apply this one alone; one tree, `D:\ref-76b`, builds both games: `build-76b.bat` RE2, `build-76b-re3.bat` RE3). RE3 only:
  the right stick click goes to the game's dodge only when `visceral_native.dll` does not export `visceral_own_sidestep()`
  returning 1; with our plugin it is the side step (`src/hands/sidestep.cpp`). The game's own dodge action still dodges.
  Log: `[Visceral] RE3 right stick click: the side step ...`.

- `2026-11-16c-re3-no-game-roll.patch` — cumulative (CONTAINS 2026-11-16b; apply this one alone). RE3: with the side step in
  (`visceral_own_sidestep()` = 1) the game's own dodge (bit 51, `RE3_Dodge`, right A when nothing is near) is never asked
  for (Tefa 2026-11-16: "please remove the original dodge roll if possible"). A in open floor then opens the inventory, its
  other job, as in RE2.

- `2026-11-16d-a-only-interact.patch` — cumulative (CONTAINS 2026-11-16c; apply this one alone). RE2 and RE3 (Tefa 2026-11-16:
  "A should only be interact, and inventory should only be Y"): right A no longer sends ITEM, and sends PRESS_START only
  while FirstPerson is not driving (the title and menus still start / confirm on A); left B (Y) keeps INVENTORY. Seen on
  the simulator in both games: A in the open does nothing, Y opens the inventory, X closes it. (In RE3 A next to the
  typewriter opens the wall map, `openInventoryMapMode`: that is the map's own interaction.)
