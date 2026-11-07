# Visceral RE3: the clean rebuild (design, 2026-11-07, Fable, home PC)

Tefa, 2026-11-07: *"can you do all the same work on re 3 as well, as you just did on re2, save the build that's there and then
start from scratch, build the mod up again ... test as far as you did with re2"*; the why: builds done and recorded, so people
working on RE2 and RE3 can see where this stands before they spend their time.

This is a DELTA on RE2's design (`visceral-re2-vr/modding-notes/2026-11-07-clean-rebuild-design.md`): everything there holds
here unless this document says otherwise. Read that one first.

## 1. Where RE3 stands today `[measured 2026-11-07]`

- The mod is RE2's code of 2026-10-10 (b145) with the game's type names swapped (`app.ropeway.` -> `offline.`), plus three later
  pieces (the gen-1 Village reload rules of 10-31, the two-shell shotgun of 11-02, hand smoothing). Its reload and rack files
  differ from RE2's gen-1 by 250-310 lines beyond the names: the two drifted apart.
- The loader is RE3's own build of 76298bd (`dinput8.dll` bafff0dd): RE2's b145-era patch (dock socket VERSION 1: active +
  pose only, no `owned` / `steer` words) plus the 11-02 gun-only smoothing. RE2's current patch is gated
  `#if defined(RE2) || defined(RE3)` and touches the same four source files, so ONE patch set can build both games' loaders.
- The game folder holds saved build b003 (series v0.1.0): the loader, the plugin, the bridge, body_anchor / body_direct /
  lefthand_hold / steady_light / mute_music / hand_smooth (Lua), hand_poser.lua, the DLSS pair (off), 37 generated hold-pose
  files under natives/, custom_sfx, the REFramework MCP plugin, an old clips folder. No jitterlog (a rule miss).
- Jill's finger takes exist for 14 guns (2026-11-02, `finger-takes/2026-11-02/re3-jill`, the same 148-column shape as RE2's).
- No shadow head, no flashlight module, no title rain (RE2-only things); RE3's own flashlight is the game's.

## 2. The decisions (Fable, 2026-11-07)

D1. **The gun code is SHARED, byte for byte, between RE2 and RE3.** RE2's new `src/guns/` (layer 3, 2026-11-07) is the one
    copy; `src/core/`, `src/hands/`, `src/tools/` the same. RE2's repo OWNS them (one writer per file); a sync script
    (`tools/sync_shared.py` in RE2's repo) copies them into RE3's `dev-archive/native/` and REFUSES when RE3's copy was
    edited (hash list). Not a git submodule (friction in every Lanes session). This is where "a fix lands in both" becomes
    real, two months earlier than the Village plan.
D2. **Everything game-specific leaves the shared files into `src/game/`.** Found by grepping the shared files for
    `app.ropeway`, `pl1`, WP numbers and joint names: the type namespace (`game::NS` = "app.ropeway." / "offline.", used by a
    `game::type("survivor.Equipment")` helper), the character test (`game::claire()` becomes `game::character_key()` +
    `game::second_character()` : Claire in RE2, Carlos in RE3 `[check: pl1xxx in both? Opus reads it from the player name]`),
    the per-gun tables (`gun_data.h` keeps the structs and the lookups; the TABLES move to `src/game/guns_re2.cpp` /
    `guns_re3.cpp`), `MAG_LONG_WP` (RE2: the LE 5 2200; RE3: the CQBR 2000 and 2100), the pump list (RE3: the M3 1000 only),
    the Spark Shot (RE2 only). RE3's table: G19 0, G18 100 / 200, Samurai Edge 300, MUP 600 (magazines, Andyalpa's RE2
    numbers by WP id, as gen-1 RE3 used them; CORRECTED 2026-11-07 (Opus): re3check.cpp ran only on the M3 (joints _01 / _04
    present); the G19's slide and rack were worn 2026-11-01 with these numbers; no magazine number was ever checked in RE3: the
    simulator drive's magreport shows whether each magazine joint sits where the table says), Lightning Hawk 3000, CQBR 2000 / 2100 (long magazine),
    M3 1000 (pump + shells), MGL 4100 (layer 4).
D3. **The loader: RE3's current one first, then the shared patch set as its own layer.** Layer 1 installs the bafff0dd loader
    RE3 wore (known good). Layer 1b (after the body and guns are worn): REFramework 76298bd + RE2's cumulative 2026-11-02 patch
    built for the RE3 target, saved and worn on its own, so both games run ONE patch set and RE3 gets the version-2 socket
    (the magazine as the only left-hand spot, the pump's grip ours, no steering on the slide), the menu-close hold and the
    inventory-close fix. Until 1b the shared gun code runs on the v1 loader: the `owned` and `steer` words are simply not read
    (the struct's first nine fields are the same), so the hand can still dock on the grip with a magazine in it (the bug RE2
    had before b183). Known, accepted, says so on the board.
D4. **The body = what RE3 really ran** (the inventory, not the released mod folder): the gen-1 C++ body files (ladder,
    menu_body, menu_tint, pickup, exposure, run, fire, suppress, holster, shortcut, subweapon, options, spread, sfx) moved
    over unchanged as RE3's own `src/body/` (they carry `offline.` names; they stay per game), plus the five Lua that ran.
    `re3check.cpp`, `menu_probe`, `spreadprobe`, the gen-1 reload / rack / block / pump / shellclip: out (replaced by the shared
    guns, or probes). jitterlog + Ghost Hand go in (the rule).
D5. **The MGL is layer 4**, Tefa's rule of 2026-11-01: opens ONLY with LG + LT (on the drum / front), spent cases fall out when
    the gun is tilted 30 deg up (the revolver rule), rounds in from the pouch, closes with LG + LT or a DOWNWARD flick. The
    game turns its cylinder joint `_01` 100 deg about its length; there is no barrel hinge. It is RE3's own file in `src/game/`
    or a shared `guns/cylinder.cpp` if the revolvers of RE2 (layer 4 there) turn out to be the same mechanism `[decide when
    both are built; a first guess: shared]`.
D6. **Tools shared too**: `deploy.py`, `build.sh`, `test_deploy.py`, the clip tools and the simulator boot are made game-aware
    by a small per-repo `game.conf` (the game folder, the backup folder, the Steam app id 952060, the log name, the A presses
    to gameplay: FOUR in RE3) instead of RE2's constants. RE3's install list is its own file.
D7. **Hands (layer 6)**: Jill's takes, the same pipeline; `motion_table.py --game re3` first (RE3 may chain motions
    differently). Carlos falls back to Jill. No new takes.
D8. **Backup place**: `D:/claude video game stuff/re3-before-clean-rebuild-2026-11-07/` (a plain folder; `D:/RE3 REFramework
    builds` is a plain folder too, checked, but the new place keeps both games alike).

## 3. The keep list for RE3 (Tefa's "do all the same" = approved; say a number to change it)

KEEP as files: ladder hold (1), menus over the world (2), pick-up world (3: pickup.cpp only; RE3 had no Lua half), steady
light (5), run / fire / grip rules (6), holsters + knife + grenade (7), options (8), hand smoothing guns only (12), spread (25),
the 37 hold-pose files (0b), the bindings json, the music script (then native).
SHARED from RE2's clean code: magazines (13, with the CQBR as the long gun), shells (14: the M3), racking (15), the empty click
(18), the swap guard and the left hand (22-23 as RE2 has them), timings (24, later), the ammo counter (24b, later).
LAYER 4: the MGL (D5). LAYER 6: the hands on Jill's takes (26-28, 30).
DROP: tuning sliders, RELOADED poses, probes (re3check, menu_probe, spreadprobe), the DLSS pair, the hand-smoothing menu
script, the old clips folder (regenerated), reframework_revision.txt (a stray note file).
NOT IN RE3: the flashlight module (9), the shadow head (4), the title rain (10), the GM 79 (16), the revolvers (17).

## 4. The layers

| layer | what | the check |
| --- | --- | --- |
| 0 | inventory + hashes, tuned numbers (RE3 had none set: check), b003 confirmed, everything out to the backup, saves copied, the gen-1 tree archived, Steam verify, a flat start to the title | the title |
| 1 | RE3's own patched loader bafff0dd + openxr_loader + bindings + config + package scripts + music script | picture, hands, height, no music |
| 2 | the body (D4) + the shared core + bridge + jitterlog + Ghost Hand; the shared guns compiled in with RE3's table | simulator: hooks in, holsters |
| 3 | the guns driven on the simulator as RE2's were: a G19 magazine out / in / chamber round / rack due; the M3 shells + pump; the CQBR's LG + LT pull-out | the log, every path |
| 1b | the shared loader patch built for RE3 (D3) | the same pass again, plus: the hand never docks on the grip with a magazine in it |
| 4 | the MGL (D5) | by hand, the simulator first |
| 5-7 | as RE2's | |

## 5. Model plan

Fable's part is this document: D1-D8. Everything else is Opus: making RE2's shared files game-agnostic (a mechanical grep
with a clear list), the sync script, RE3's game layer and table, the layer 0-3 steps as RE2's, the simulator drive. Likely
Fable rows, said the moment they resist: the loader rebuild for the RE3 target if it does not boot (1b); the MGL's open /
close mechanics if the cylinder turn fights the hand (layer 4).
