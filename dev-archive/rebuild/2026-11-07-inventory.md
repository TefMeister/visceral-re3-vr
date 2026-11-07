# The RE3 game folder before the clean rebuild (2026-11-07, Task 1)

`2026-11-07-inventory.tsv`: every file in the RE3 folder Steam does not own, with its size, sha256 and verdict
`[measured 2026-11-07]`. 186 files: KEEP 146 (incl. 37 generated hold-pose files under natives/ and the custom sounds),
TOOL 30 (the REFramework MCP plugin, Hand Poser), DROP 4 (the DLSS pair, a stray revision note, the hand-smoothing menu),
LOG 3, REWRITE 2 (the plugin and the bridge), GAME DATA 1 (an old clip). The folder held exactly saved build b003; all 186
moved to `D:/claude video game stuff/re3-before-clean-rebuild-2026-11-07/game/` (a plain folder), every hash matched, 0
left; the saves copied (4 files). `builds.py restore visceral-re3-vr 3` puts the old install back.

RE3 never had tuned hand numbers (no tuning files in its folder). jitterlog was missing in b003 (now in layer 2).
