# 2026-11-23 (/lm, PC1, Fable): RE3, every by-hand gun run by robot hands (the real headset lying on the desk)

The third game of Tefa's ask of the morning (Village: visceral-re8-vr `modding-notes/2026-11-23b` / `23c`; RE2: its note of
today, which also says how the robot is driven here: the same tools, `RV_GAME_DIR` = this game). Build 27 as installed,
unchanged. Save: the all-weapons save (slot 2, Jill, the Sewer Manager's Office typewriter).

## Getting in

`drive_real_re.sh re3`, then A. ⚠️ **Three presses reach play on this save; the fourth opened the typewriter's save list**
("Overwrite saved data" under the lit slot) because the save stands at the typewriter. Nothing was overwritten (the files
kept their morning time). VR Bench's B did not leave the list; the keyboard's Escape did (`tools/sim/key.py 01`).

## The table `[verified-live 2026-11-23, robot, n=1 each]`

| gun | by hand | magazine / rounds |
| --- | --- | --- |
| G19 (WP0000) | slide pass | B drops it; a spare from the pouch seats at the gun's root ⚠️; the rack after was not run (my tool's read failed once) |
| Lightning Hawk (WP3000) | slide pass, and after the reload | B drops it; a spare from the pouch seats ⚠️ |
| CQBR (WP2000) | bolt `_01` pass | long magazine (LT with the hand on it): not run |
| M3 (WP1000) | pump pass (LG at the fore-end, LT, 10 cm back, LT let go) | 1 shell from the pouch, "1 at the port (0.109 m)", LT: "shells in (loaded 4)" |
| MGL (WP4100) | drum: LG + LT at `_02`: "opening" | rounds given by script (item 37, `addItemCount`); the pouch gave 2; at an empty chamber (`_08`) LT: "took item 37 in chamber 1 (0.062 m from the hand); the drum: >35 37 - - - -" |

- ⚠️ G19 and Lightning Hawk: "0 carried" at the drop, and the pouch still gave a magazine that seated (as RE2's M19 and
  MQ 11 today): the same question, not looked into.
- **The MGL's drum was found closed again twice without a "closing" line**: after "opening", the hand went to the pouch and
  back, and the next LG + LT at the drum said "opening" again (n=2; once after a pouch grab that gave nothing, once after a
  round went in). Either it shuts by itself when the hand leaves or a round goes in, or the line is missing: not looked into.
- Not run: the hand on a seated magazine with B into the hand and back in with LT (RE2's note says why it was not found
  there), firing to empty, the spent cases tipping out, the kind of round stepped with LT (it logged "the pouch gives item 37
  now (was 37)": only one kind was carried), G18 / MUP (not in the save).

## Hands and fingers

As RE2 (the same code): no finger poses, no stage numbers, Hand Poser not installed and reading the old slots 57 / 58 here.
See RE2's board row "HAND POSES THROUGH RELOAD AND RACK NEED BUILDING HERE FIRST": one design covers both games.
