# Visceral RE3: the archived source (2026-11-07, the clean rebuild)

Moved here unchanged when the clean rebuild started (`modding-notes/2026-11-07-clean-rebuild-design.md`); git tag
`pre-rebuild-2026-11-07` marks the last commit before the move. Kept for reading and diffing, never built again.

| folder | what it is |
| --- | --- |
| `native-gen1/` | the native plugin of 2026-10-10 to 2026-11-02 (RE2's b145 port with `offline.` names, then the 10-31 Village rules and the 11-02 shells): RE3's body files were copied out of it into the new tree |
| `lua-gen1/` | the Lua that ran beside it (body_anchor, body_direct, lefthand_hold, mute_music) and older probes |
| `visceral_title_level.lua` | the 2026-11-01 title-menu levelling try (did nothing) |

The released mod in `mod/` is left as it is until the rebuilt mod replaces it.
