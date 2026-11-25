# 2026-11-25 (/lm reader, static only): the MGL's rounds in RE3's files, for the spent-shell + coloured-band row

For the board row "SPENT SHELLS AS OUR OWN MODEL, A WORN COLOURED BAND ON EVERY ROUND, AS IN VILLAGE". Nothing was run in
the game; files only. Village's version: visceral-re8-vr `modding-notes/2026-11-25b-gm79-spent-shell-our-own-model-and-round-bands.md`.
Dossier sections it speaks to: the weapon table (WP4100 `wp4100_grenadelauncher`) and the MGL drum. RE2's twin file:
visceral-re2-vr `engine-research/inbox/2026-11-25-lm-gl-shell-recon.md`. (This repo had no `engine-research/inbox/` yet;
this file made it.)

Extracted with visceral-re2-vr `dev-archive/tools/re-engine/pak_pull.py` + Ekey's `RE3_RT_STM_Release.list` (in
`D:\RE2 REFramework builds\tools\REE.PAK.Tool\Projects\`) into
`D:\RE3 REFramework builds\extracted (game data - never commit)\gl-shell-2026-11-25\` (game data, never commit). Read with
RE Mesh Editor 0.66's parser outside Blender. No Blender was run.

## 1. The launcher and its rounds `[measured 2026-11-25]`

- `escape/character/weapon/wp4100/mesh/wp4100_grenadelauncher.mesh.2109108288`, two materials:
  `wp4100_Grenadelauncher_Mat` (part 0, the gun) and `wp4100_GrenadeBullet_Mat` (parts 1-6, the rounds), both
  Weapon_Default.mmtr. One LOD.
- **Parts 1 .. 6 are the six rounds in the drum, one per chamber joint: part 1 on `_06`, 2 `_07`, 3 `_08`, 4 `_09`, 5 `_10`,
  6 `_11`** (688 verts each, 100 % on its joint). Every bind rotation is identity; each chamber joint sits at the middle of
  its round's CASE (z 0.1501; e.g. `_06` at (0, 0.0982, 0.1501), RE axes, metres, gun space, muzzle +z).
- Each round = 4.22 cm across (the rim), 9.64 cm long. **Case and warhead are separate islands of the same part**
  (same material, so the game cannot hide one without the other):
  case (6 islands, 347 verts): z 0.1295 .. 0.1720 (4.25 cm); rim r 0.0211 (z 0.1295 .. 0.131) with a primer r 0.0064
  recessed in the base; **a groove r 0.0177 from z 0.131 to 0.1335, a bevel up to the body at 0.1365**; body r 0.0196;
  **hollow**: inner wall r 0.0188 from the mouth (z 0.172) down to a floor at z 0.1605 (1.15 cm deep), normals inward.
  warhead (3 islands, 341 verts): z 0.1615 .. 0.2255, seated inside the case mouth; r 0.0196 driving band at 0.1745-0.1755,
  body r 0.0180, a raised ring r 0.0189 at 0.194-0.1995, ogive to the tip.
  This is the same layout as Village's GM 79 case (groove, rim, primer, hollow mouth), so Village's band/soot method fits.
- **`wp4101/mesh/wp4101_grenadebullet.mesh` is the same round as its own file, already split: part 0 = the case (347
  verts, identical profile), part 1 = the warhead (341)**, on one joint `__00` (identity, at the origin = the case middle).
  So the empty case exists ready-made, as Village's part 9 did, and it is ALREADY in the chamber joints' local frame (the
  chamber round's case minus z 0.1501 = wp4101's case exactly): no bind conversion needed.
- `_100` / `_101` (both at (0.057, -0.0235, 0.331), under `_01`) carry no vertices: the round the game's own reload moves
  is a separate object `[inferred-static: presumably wp4101]`.
- `wp4107_minethrowerbullet.mesh`: a different object (6.9 x 18.8 cm, a spike joint `_01` and eight petals `_02`..`_09`, a
  blue emissive light material): the fired mine, not what sits in the drum `[inferred-static]`. In the drum every kind
  is parts 1-6 with `wp4100_GrenadeBullet_Mat`.

## 2. Pickups and per-kind looks `[measured]`

- Per-kind round textures (material files only, they dress the wp4101 mesh): `wp4103_flamebullet.mdf2.21`
  (`wp4103_FlameBullet_ALBMSC`), `wp4105_acidbullet.mdf2.21` (`wp4105_AcidBullet_ALBMSC`); the explosive look is the base
  `wp4100_GrenadeBullet_ALBMSC`. No separate mine-round texture for the drum.
- Pickup boxes: `escape/setmodel/.../sm70_105_minethrowerbullet01a` (its own box, BaseColor (0, 0.62, 1) blue);
  `objectroot/setmodel/.../sm70_106 / 107 / 108_grenadelauncher_*bullet01a` = byte-identical to RE2's box mesh, RE3
  materials: 106 white (1,1,1), 107 yellow (1, 0.93, 0), 108 red (0.91, 0.12, 0.12).

## 3. Bullet item ids

- **36 Mine, 37 Explosive, 38 Acid, 39 Flame** `[verified-live 2026-11-10, modding-notes/2026-11-10-hip-ammo-kinds-and-the-mixed-mgl-drum.md;
  in src/game/guns_table.cpp]`. The MGL is WeaponType 42.
- They line up with the pickups if `Item.ID` = sm70_1xx in order from 31 (100 handgun ... 104 = 35 "not an ammo item",
  105 mine, 106 explosive, 107 acid, 108 flame) `[inferred-static]`.
- `shell_bands.json` row: `"re3": {"ammo": {"explosive": [37], "acid": [38], "flame": [39], "mine": [36]}}`.

## 4. What our RE3 code knows now `[inferred-static, read 2026-11-25]`

- `src/game/guns_table.cpp`: `ROUND_GUNS {4100, {37, 38, 39, 36}, drum "_02", chambers "_06".."_11", crane "_01" 100 deg,
  round_mat 1, round_var 0, tints}`; SHELL_GUNS 4100 with no round part (-1).
- `src/guns/rounds.cpp` (SHARED, owned by visceral-re2-vr): **already tracks every chamber: `Drum.ch[c]` = the item id,
  0 empty, SPENT (-1) a fired case kept until `dump_spent()` (a drum that swings out)**; `draw()` scales each chamber joint
  1 when loaded OR spent, 0 when empty, and `paint()` tints the ONE round material for all chambers (the known limit: a mixed
  drum cannot show each chamber's own colour). `show_hand()` lends chamber joints to the hand.
- So the S_GL_ROUND equivalent is per chamber: in `draw()`, a SPENT chamber should get scale 0 (the game's whole round with
  its warhead is what shows now) and our spent shell drawn at that joint; a live chamber gets our band in ITS kind's colour
  (which also lifts the one-colour limit). Bridge (`src/core/bridge.h`, SHARED, edit in RE2): array 653 long, 651 / 652
  kept; a block at 653+ of six chamber values (item id / 0 / -1) plus a stamp serves RE3, and RE2's one chamber uses the
  first value. Grow N in `lua/visceral_bridge.lua` with it.
- Spawning our own mesh by script in RE3 is proven by the shared `lua/visceral_options_book.lua` (the UBCS folder in RE3):
  GameObject.create with the camera's folder + Mesh + setMesh / set_Material through resource holders.

## 5. Village's two build scripts, pointed at RE3

`build_gm79_spent_shell.py` (constants are Blender axes: Blender x = RE x, Blender y = -RE z, Blender z = RE y):
- SRC `wp4101_grenadebullet.mesh.2109108288`, CASE_PART `Group_0_Sub_0`, JOINT `__00` (identity at the origin, so the
  "into the joint's bind frame" step changes nothing and the result fits `_06`..`_11` as it is).
- CX, CZ = 0.0, -0.0002 · Y_MOUTH = -0.0220 · Y_FLOOR = -0.0110 · Y_BODY_BACK = 0.0135 · Y_RIM_FRONT = 0.0185 ·
  BAND_R_IN ~ 0.0175 (groove floor r 0.0177) · the rim-UV window's hard-coded `-0.0813` becomes the rim back, Y 0.0205 ·
  the floor test's `rr < 0.0186` becomes ~0.0192 (inner wall r 0.0188). The band spans the 2 mm flat groove plus the 3 mm
  bevel (Village's groove was 4 mm flat) `[hypothesis: look at the render with Tefa]`.
- Export `filename_ext=".2109108288"` (RE2 RT / RE3 RT mesh, as visceral-re2-vr `tools/blender/build_bracelets.py`), new
  names (e.g. `mgl_spent_shell`, `mgl_round_band`), materials named to match.
`mdf_build_gm79_shells.py`:
- output `.mdf2.21`; `--template wp4101_grenadebullet.mdf2.21` (`wp4100_GrenadeBullet_Mat`, Weapon_Default, BaseColor /
  Metallic / Roughness present); for a spent FLAME / ACID case the template's BaseMetalMap may want the kind's own
  ALBMSC `[hypothesis: whether the case part of those textures differs is not looked at]`.
- `--container`: RE3 has NO original three-material Weapon_Default file among the guns read (G19 6 mixed, G18 2, Samurai
  Edge 2, MUP 1, M3 `wp1000_shotgun` 4, CQBR `wp2000_assaultrifle` 4, Magnum `wp3000_magnum` 4, all `[measured]`). Use a
  four-material one and leave the fourth unused (the RE2 bracelets file keeps the template's unused materials the same way,
  for the writer's count bug): the script's `len(...) != 3` check becomes `>= 3`, fill the first three.
- `--game re3` and the `re3.ammo` row above. Mine: purple band (Tefa), on the same case.
