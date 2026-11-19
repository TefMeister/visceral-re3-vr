# RE3: ideas and board check, 2026-11-19

By the /lm session's reader (read only), 2026-11-19, Fable session; saved by the /lm session unchanged, with its own section
at the end. Everything is `[inferred-static]` unless it quotes the board (`[reported]`) or Tefa. Line numbers are of
`claude-memory/status/visceral-re3-vr.md` AS READ at about 11:00 on 2026-11-19: 167 lines, the `LIVE:` claim on line 15, the
OPEN heading on line 16, the OPEN block lines 16 to 135, "DECIDED / DONE" from line 137. Search by the quoted words once rows
move.

Code read: `dev-archive/native/src/` and `lua/` (8,668 lines), `tools/install-list.txt`, `game-folder/re2_fw_config.txt`, the
newest REFramework patch by grep, today's uncommitted change by `git diff`.

NOT checked: the game itself, any log, the builds store, the REFramework patches beyond greps, `ideas/chosen/` (only the 16
numbered ideas), the poser repos, RE3's `KNOWN.md`. The reader edited, launched and committed nothing.

**Worn or not, in one line:** the board records Tefa in the headset on 2026-10-10 (body), 2026-11-01 (the G19, step 3) and
the play run of 2026-11-09 (his list of 17). Every build from b009 to b026 is simulator-checked only `[reported]`.

## 1. The ideas (numbers as in `ideas.py list visceral-re3-vr`)

1. **A different ammo type on each hip: PARTLY, overtaken by Tefa.** Built as b011 / b012 (right hip = second kind), then
   scrapped by Tefa 2026-11-10: one pouch, LT steps the kind (`src/guns/shells.cpp` line 105, `rounds.cpp` `g_sel`;
   `src/game/guns_table.cpp` `ROUND_GUNS` has the MGL's four kinds). Board line 29, b016. Simulator and robot hands only,
   unworn. The idea as worded is dead by his own later word: ask.
2. **Right grip holds the weapon, and a stick dodge: PARTLY.** The dodge is the side step, left stick + right stick click
   (`src/hands/sidestep.cpp`, b022; the game's roll off, b023; line 20). Simulator only. "Let go of the grip and the gun goes
   back" is not built (`src/body/holster.cpp`: RG takes out and puts away at a spot).
3. **A settings menu dressed as something from the game: PARTLY.** The UBCS binder hangs in the world on X + A
   (`lua/visceral_options_book.lua`, b009, line 31). No options on it, no pages. Simulator only.
4. **Pistol in two hands, smoothing down 75%: NOT STARTED.** The smoothing asks only "is a real gun in hand" (patch
   `2026-11-02-re3-b145-plus-hand-smoothing-guns-only.patch`, `lua/visceral_hand_smooth.lua`).
5. **Two LT presses, one shell each: NOT STARTED.** One press starts the feed and the rest follow by themselves
   (`shells.cpp` lines 130 to 143, `g_feeding`, `SHELLS_STEP_S`). Also Tefa's item 2, line 34.
6. **A map held in the hand: NOT STARTED.** Menu tap = the game's map screen exists (b021, line 21, unworn).
7. **The game's animations take over the hands: NOT STARTED.** Finger takes recorded (line 57); no player in `src/`.
8. **Two hands, no spread: DONE in code** (`src/body/spread.cpp`, `settings_body.h` lines 122 to 131, RE2's tiers). No RE3
   headset word on the board; line 110 only says "spread per weapon" seen working on 2026-10-10.
9. **Controller drift when one hides the other: NOT STARTED** (only the recorder line in `lua/jitterlog.lua`).
10. **A launcher to switch features: NOT STARTED.**
11. **Left- and right-handed profiles: NOT STARTED.**
12. **Casings stay on the floor: NOT STARTED** (no eject file in `src/guns/`).
13. **VR comfort options: NOT STARTED** (the book's "Comfort" page is a plan, line 50).
14. **The MGL loads two shells from the pouch: DONE in code.** LG at the left hip gives two rounds, LT puts each into the
    nearest empty chamber (`rounds.cpp`, `cylinder.cpp`, `shells.cpp`; b014 / b016, line 29). Robot test only, unworn. Left
    over: how the rounds sit in the fingers.
15. **Mixed rounds in the MGL's drum: DONE in code** (`rounds.cpp`: one kind per chamber, the game's kind set back before
    each shot; b012, line 29). Robot test only, unworn. Limit: a mixed drum shows one colour.
16. **Cutscenes on a big flat screen: PARTLY.** The code is in RE3's REFramework (patch `2026-11-18-hands-walls.patch`,
    `VisceralCutsceneScreen`), default off, and `re2_fw_config.txt` has no line switching it on; line 20 says "switched off
    in RE3". Never run in RE3. No board row.

## 2. The board

The OPEN block is 120 lines; about 25 are live work.

### (a) Ticked, superseded or empty rows still inside OPEN

| Lines | Why |
| --- | --- |
| 22, 55, 68, 72 | ticked ✅ |
| 75 | "(all three built 2026-10-19, see the row above)" |
| 19 | `[PD]` "WAITING: Tefa's go": built as b025 (line 18) |
| 50 | "NEXT WEEK ... first milestone": built as b009 (line 31) |
| 53 | "DESIGN WRITTEN, NOTHING BUILT": built as b004 to b007 (line 52) |
| 61, 62, 63 | the MGL decided / "NOT built" / "no hinge, asked": all answered and built (line 29) |
| 57, 64 | `[PD]` rows that only say DONE (finger takes; the gun sweep) |
| 80 to 89 | "FLAT CHECK DONE" under a `[VR USER]` tag |
| 54, 65, 67 | old headings, no work |
| 39 (item 7) | line 22 says it is replaced by the shared layout |

No struck-through rows.

### (b) Rows a newer row or the code contradicts

- **21** (b021): "Jill dodges that way (the old dodge button still works too)". Line 20: the side step replaced that dodge
  and the roll is off. Only its menu-button half is still true.
- **23**: "Dodge on RS down asked for every game" and "which back side not said yet": line 22 has dodge = left stick + right
  stick click and "Map at the LEFT back holster". The code has **medicine** at back left, doing nothing yet (`holster.cpp`
  lines 12, 132). Ask Tefa which holds (the same question as RE2).
- **26**: its first half says itself it is done; left: our Blender torch and the chest push (also item 6, line 38).
- **27**: "COMPILED here, NOT installed ... install with the next RE3 build": eight builds have been installed since.
- **29**: one row carrying b016 and, as history, b014, b012, b011 with the scrapped right hip. **66** says "Not ported: the
  MGL".
- **56, 58, 66, 69, 74, 77 to 79, 90 to 97, 112 to 124**: first-generation builds, replaced by the clean rebuild (b007,
  line 52). 69 says "RE3 has no saved-builds folder yet"; 74 says the one-grip spot is "not ported" (line 68 says done); 97
  and 135 say a snapshot is "owed" (b001 to b026 exist).
- **76** `[FLAT]` "UNRUN": the re3check has run (line 52 "re3check 11-02"; `guns_table.cpp` header).
- **71** `[FLAT]` "NOT RUN": `src/game/plugin.cpp` line 44 says RE3 never installed that hook, only the per-frame write; and
  `lua/visceral_steady_light.lua` is on the install list although its own header says not to install it beside RE3's native
  fix. Two things write the brightness `[hypothesis: they may fight]`. Needs one look at a kept log.
- **83**: "the after-reload ammo counter will not show in RE3": fixed in b016 (line 29, "it does now").
- **105 to 111** "SETTINGS FIX, UNWORN": line 98 says "Worn with the settings fix".
- **59**: (b) is fixed inside the row; live work is only (a) the main menu tilt and (c) "G19 shoots with the slide pulled
  back".
- **Missing rows:** today's b027 (the pump hold) has no row yet; the Samurai Edge is still not a by-hand gun
  (`guns_table.cpp`, no 300 in `MAG_GUNS`) and only line 64 mentions it; the cutscene screen (idea 16) has no row.

### (c) Proposed feature IDs (headset rows stay until Tefa's word)

| ID | Feature | Lines |
| --- | --- | --- |
| RE3-001 | the pump shotgun's left hand under the handle (b027) | no row yet; item 4 (line 36) is its neighbour, not the same |
| RE3-002 | hands and gun stop at walls (b026) | 17 |
| RE3-003 | doors pushed by hand, body and gun (b025, b026) | 18, 17 (last check), 19 |
| RE3-004 | side step; A only interact, Y the inventory (b022 to b024) | 20, 21 (part 1), 39 |
| RE3-005 | cutscenes on a flat screen | none: in the loader, off, never run |
| RE3-006 | menu button: tap = map, hold = pause (b020, b021) | 21 (part 2) |
| RE3-007 | six spots and the torch; chest lamp gone (b018, b019) | 24, 26, 23 |
| RE3-008 | rounds seen in the magazines (b017) | 28, 27 |
| RE3-009 | the options book (b009) | 31, 50 |
| RE3-010 | guns by hand: magazine, slide, shells, pump (b007, b008) | 52, 51, 53, 56, 59 (c), 66, 69, 74, 75, 77 to 79, 90 to 97; items 2, 9, 10 (lines 34, 41, 42) |
| RE3-011 | the ideas list and the board re-cut (no headset) | this note |
| RE3-012 | the MGL by hand, one pouch, mixed drum (b011 to b016) | 29, 30, 61, 62, 63 |
| RE3-013 | hand smoothing, guns only, and its sliders (b008) | 51, 58 |
| RE3-014 | Jill's body: relaxed idle, torso / chest push | 98 to 104, 125 to 135, 26, 38 |
| RE3-015 | brightness kept steady; Single Frame Multipass | 70, 71 |
| RE3-016 | pick-up and inventory screens show the world and the item | 40, 47, 78 |
| RE3-017 | the main menu tilted and raised | 59 (a) |

Line 51 sits in two groups (b008 = b007 + sliders): split it or pick RE3-010. No ID proposed for one-off list items 1, 3, 5,
11 to 14, 16, 17 (lines 33, 35, 37, 43 to 46, 48, 49), for the unlock row (73, `[FLAT]`; no unlock code in the clean tree,
only in `archive/native-gen1`) or for the b139 bulk port (112 to 124).

### (d) Gate tags

- Lines 33 to 49 sit under one `[VR USER]` tag (32), but most first need a look or a build with no headset: items 1, 3, 8,
  12, 15, 16 are `[PD]` / `[FLAT]`.
- 59 is `[PD]` with a headset report in it and flat work left: `[FLAT]`.
- 61 `[VR CLAUDE]`: done.
- No tag: 54, 65, 67, 75.

### (e) Facts above the block that look untrue now

- **Line 16 (heading):** "touch-to-open proposed, waiting for Tefa" (built, b025); "b020 ... dodge on the right stick click"
  (replaced by the side step); nothing about today's b027.
- **Lines 12 to 13:** "Install (home PC ...): praydog v1.5.9.1 + the six 76298bd DLSS files ...": the loader is now our own
  patched REFramework (install list: `dinput8-b84a16fe-re3-patch-2026-11-18-hands-walls`); "home PC" is the Developer PC
  since 2026-11-11. "DLSS OFF" still holds (`TemporalUpscaler_Enabled=false`).
- **Lines 8 to 10 and 155 to 167:** the job as "porting ... in the same order" and the port order: overtaken by the clean
  rebuild sharing RE2's code (line 53). History, not wrong.
- **Below the block, 138 to 142:** "release with Arcade Controls style racking", replaced by Tefa 2026-10-19 (line 75: hand
  racking).
- **143 to 145:** D-pad = right stick click + left stick; the side step uses the same two controls and the profile file is
  still on the install list. Clash is `[hypothesis]`; one look in the log.

## 3. Code shape (`code-shape-scan.py`)

0 files over 1,500 lines, 0 near the Lua locals limit, 1 over 800:

| File | Lines | Whose |
| --- | --- | --- |
| `dev-archive/native/include/reframework/API.hpp` | 1,090 | REFramework's own header, not ours |

Our own source is well inside the limits: the largest is `src/body/ladder.cpp` at 427 lines, then `body/menu_body.cpp` and
`lua/visceral_walls.lua` at 330. **Nothing to split.**

Loose numbers (40 or more): `src/game/guns_table.cpp` (142, a data table by design), `lua/visceral_walls.lua` (53) and
`lua/visceral_bridge.lua` (45, mostly bridge slot numbers that already have names). Suggested verdict: `keep` for all three.

## What the /lm session did with it (2026-11-19)

- **The board:** re-cut the same day. Rows of 2(a) moved out of the OPEN block to "Done, moved out of the OPEN block on
  2026-11-19" (no line lost, compared before and after); the heading re-dated; a new top row for b027; IDs RE3-001 to RE3-017
  written on the rows and into `claude-memory/feature-ids.md` as proposed above. The contradictions of 2(b) are listed in
  one new `[PD]` row rather than rewritten row by row (old rows are history; headset rows come off only on Tefa's word).
- **Code shape:** verdict `keep` for the three loose-number files, as suggested; no split.
- **Ideas:** nothing picked or dropped (Tefa answers with numbers). The questions for Tefa are on the board row `[ID RE3-011]`.
- **Not done, queued as board rows:** the brightness double-write look (71), the D-pad / side step clash look (143 to 145),
  the cutscene screen switched on for a first RE3 run (idea 16, RE3-005), the Samurai Edge by hand.
