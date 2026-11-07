# RE3's clean rebuild, layers 0-3 and 1b, built and driven on the simulator (2026-11-07, Opus, home PC)

Tefa: *"do all the same work on re 3 as well, as you just did on re2 ... test as far as you did with re2"*. Design:
`2026-11-07-clean-rebuild-design.md` (Fable). Builds in `visceral-re3-vr/clean rebuild/` (lanes builds.py).

## What was done

| step | what | build |
| --- | --- | --- |
| 0 | inventory of 186 files (hash + verdict each, `dev-archive/rebuild/`); the folder held exactly b003; all of it MOVED to `D:/claude video game stuff/re3-before-clean-rebuild-2026-11-07/` (hashes matched, 0 left), saves copied; gen-1 source to `dev-archive/archive/` (tag `pre-rebuild-2026-11-07`); Steam verify clean in 41 s; the plain title reached flat and taught to State-o-matiC | - |
| 1 | RE3's own patched loader (bafff0dd), the bindings, praydog's package scripts, the config, the music script | b004 |
| 2-3 | the new tree: the SHARED files from RE2's repo (`tools/sync_shared.py`: core, guns, hands, tools, game.h, the bridge Lua, jitterlog, the tools); RE3's own `src/body/` (its gen-1 body files, moved unchanged), `src/game/` (offline. names, RE3's gun table), the Lua that ran in b003, jitterlog (missing in b003) | b005 |
| 1b | REFramework 76298bd + RE2's cumulative 2026-11-02 patch built for the RE3 target (the `D:/ref-76b` tree holds exactly that patch, 541 lines): dinput8 d60128e7, socket v2 | b006, clean folder b007 |

RE2's repo got the per-game layer the sharing needs (its b196 / b197): `src/game/` answers the type namespace, the project name,
the second character and the gun tables; `plugin.cpp` and `weapons.cpp` are per game; the body's numbers are per game
(including the shells' timing and port reach, which RE3 had tuned to 0.4 s / 0.12 m on 2026-11-02).

## Why layer 1b came forward

On RE3's own loader (socket v1, no `owned` word) the left hand docked on the gun's grip while it carried a magazine: on the
simulator the magazine-to-magwell distance stayed at exactly 0.130 m whatever the hand did `[measured 2026-11-07, simulator]`,
the fault RE2 had before b183. With the shared patch the same drive put the magazine in at once.

## Driven on the OpenXR Simulator with VR Bench `[verified-live 2026-11-07, simulator, n=1 each]`

With RE3's tools build (the hand readers) and the test-only gun script, both taken out after:

- G19: right B dropped the magazine; the chambered round fired once, then the hammer click; a pouch magazine steered to the
  magwell went in with the hand docked on it, topped up 12 -> 15; "a rack due (the chamber was fired empty)"; RT clicked; the
  slide racked by hand; it fired.
- M3: a shot with a shell behind it made a pump due; RT clicked; pumped by hand (LT let go at the bottom: back up by itself); it
  fired; two shells from the pouch docked at the port (0.083 m) and went in with LT.
- CQBR (a long-magazine gun now): B did nothing; LG on the magazine + LT pulled it into the hand; LT at the magwell put the same
  magazine back with only its own round. The magazine numbers (Andyalpa's MQ 11 set) put the magwell where the hand could reach
  it (magreport went to 0.001 m).
- Shells on the OLD loader also went in, but the gun swung with the left hand while it carried them (the v1 dock again).

Not driven: the G18s, the MUP, the Lightning Hawk (same code paths as the G19, their own table rows), a magazine kept out
across a swap, the MGL (layer 4).

## Open

- Wear it (Tefa): RE2 b197 and RE3 b007 in one go.
- The game's reload-order switch (`ActionOrder.Precede`, setInhibitPrecede) was reported NOT FOUND by re3check on 2026-11-02:
  the other blocks held in every drive today (no game reload played), but the RELOAD action inhibit may be doing nothing in RE3.
- Which RE3 character `game::second_character` picks (the "pl1" test kept from gen-1) is unread.
- RE3's own `src/body/pickup.cpp` warns C4127 (an old constant condition), harmless.
