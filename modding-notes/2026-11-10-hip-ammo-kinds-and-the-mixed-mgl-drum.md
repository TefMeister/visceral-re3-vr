# 2026-11-10: a second ammo pouch on the right hip, and the MGL's mixed drum (b011, simulator only, unworn)

Tefa picked this from the numbered ideas list: *"left hip for normal ammo, left hand on right hip for alternate, re3 grenade
launcher to be able to insert different ammo into the same grenade launcher drum and gave game recognize what ammo is in the
barrel"*. Home PC, session alone, OpenXR Simulator + VR Bench hands, the live question line (`zz_visceral_eval.lua`).

## What the game does (asked of the running game)

- A gun's loaded kind of round is ONE number on its inventory slot: `offline.inventory.Slot.get_BulletID / set_BulletID`
  (an `Item.ID`), beside the count `get_Number`. `Equipment.get_BulletType()` follows it at once.
  `[verified-live 2026-11-10, n=6 switches]`
- RE3's item numbers: 31 Handgun Ammo, 32 Shotgun Shells, 33 Assault Rifle Ammo, 34 MAG Ammo, **36 Mine Rounds, 37 Explosive
  Rounds, 38 Acid Rounds, 39 Flame Rounds** (35 is not an ammo item). The MGL is WeaponType 42 (WP4100). `[measured]`
- **Changing the slot's kind keeps the count and costs nothing**: 6 Explosive loaded, kind set to Mine, then Acid, then back:
  6 loaded each time, the carried stacks untouched. `[verified-live 2026-11-10, n=3]`
- **The next shot is of the kind set**: three shots from one drum with the kind changed between them made grenade shell
  kinds 1 (explosive), 2 (acid) and 4 (mine) in `ShellGeneratorBase.generateShell`, the count going 6, 5, 4, 3.
  `[verified-live 2026-11-10, n=1 each]`
- **One round of any kind goes into a part-full drum**: set the kind, then `Equipment.executeReload(WeaponType, 1)`: the count
  goes up by one and that kind's carried stack down by one. (`Inventory.reloadMainSlot` takes one number in RE3, and from a
  script it refused; our `ammo.cpp` already falls back to `executeReload`.) `[verified-live 2026-11-10, n=3]`
- The game's own answers about a second kind: `InventoryManager.isAbleToMainWeaponChangeBullet()`,
  `getMainWeaponChangeBulletNumber(Item.ID)` (the carried count of a kind that is NOT the loaded one; 0 for the loaded
  kind, whose count is `getMainWeaponReloadableBullet()`).
- The MGL's model: the drum is joints `_01` > `_02`, the six chambers `_06` .. `_11` under `_02`, `_100` / `_101` beside the
  drum (the round the game's own reload moves). All 256 mesh part switches read "on": the round in the hand is not a mesh
  part of the gun as the shotgun's shell is. `[measured]`
- Giving the gun by script needs free slots (Jill's 16 were full): `Inventory.removeSlot(Int32)`, then
  `InventoryManager.addAndEquipMainWeapon(42, 6, 37)` (the third number is the round's item).

## What was built

- **`guns/rounds.{h,cpp}` (shared with RE2)**: our own list of what is in the drum, in the order it went in; the game's kind
  is kept on the round that fires next (first in, first out). A shot shortens the list from the front; rounds the game put
  in itself (a loaded save) take the kind the game says. The list lasts the session, per gun.
- **The hips**: the left hip gives the gun's normal round (the first of its list that is carried), the right hip the next
  kind carried, both to the LEFT hand with LG. The right-hip spot is only there (buzz included) while the gun in hand has a
  second kind carried (`guns::alt_pouch`). RE3's `body/holster.cpp` has the new spot; `guns/shells.cpp` takes
  `pouch_grab(right_hip)`.
- **The MGL loads by hand as the pump shotgun does**: two rounds per grab, the hand docks at the drum (the port is the
  middle of the drum, 0.12 m), LT puts them in one after the other. Table: `game/guns_table.cpp`, `{4100, {37, 38, 39, 36}}`.

## The robot's test `[verified-live 2026-11-10, simulator, n=1]`

`dev-archive/tools/sim-mgl/mgl_test.py fire5 fire1 left right fire4`: the drum emptied, two Explosive from the left hip, two
Acid from the right hip (the log: `the drum: 37 37 38 38`), four shots: the shell kinds made were 1, 1, 2, 2. Before that:
a part-full drum took two Explosive then one Acid (`37 37 37 37 37 38`). The M3 shotgun: nothing at the right hip, two shells
at the left hip as before (the insert itself was not run again).

## Not done, said plainly

- **Nothing was worn.** The reach of the left hand to the right hip (the cameras' weak spot) is the thing to judge.
- **No round is drawn in the hand** for the MGL (the dock buzz and the insert sound are the shotgun's). The MGL's open /
  close mechanics (design D5: LG + LT opens, cases fall at 30 degrees, a flick closes) are not built; this is the loading
  half only.
- More than two kinds carried: the right hip gives only the first other kind. Flame and Mine reach a hip only when the
  kinds before them run out. A way to choose is Tefa's call.
- RE2 has the shared code (it compiles) but no gun in its table: the GM 79's flame / acid item numbers are not read yet.
- The order rounds fire in is first in, first out. A real drum would fire in chamber order; say if it should differ.
