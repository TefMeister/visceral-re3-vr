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

## Later the same day: the drum has chambers (b012, simulator only, unworn)

Tefa: *"rounds fire follow the drums chambers if at all possible"* (and: only two kinds of ammo in RE games; checked: RE3's
MGL has four by the game's own names, RE2's GM 79 two).

- **The game has no chambers.** Its drum joint `_02` does not turn when the gun fires (the same local rotation after one and
  after three shots) and nothing in the gun says which chamber holds what. `[measured 2026-11-10]`
- So the chambers are ours (`guns/rounds.cpp`, `RoundGun` in `gun_data.h`: the drum joint, the turn direction, the six chamber
  joints `_06` .. `_11`, `_06` at the barrel at rest): a round goes into the EMPTY CHAMBER NEAREST THE HAND, a shot fires the
  chamber at the barrel (or the next loaded one round the drum) and the drum turns one on, and the game's kind is kept on
  the chamber that fires next. The drum joint is turned by us each frame, 60 degrees per chamber, so the gun shows it.
- Robot test `[verified-live 2026-11-10, simulator, n=1]`: `mgl_test.py fire4 left@leftlow right@rightside fire4` on an empty
  drum: Explosive into chambers 4 and 5 (the hand 1 mm and 47 mm away), then Acid into chambers 1 and 2; the shell kinds
  made on firing: 2, 2, 1, 1 (acid first: drum order, not loading order). After two shots the chamber joint `_08` sat at
  the barrel's place (0, 0.098) in the gun's space: the turn direction is right.
- Still as before: the drum is closed while the hand loads it (the round passes through the drum's wall, nothing is drawn
  in the hand), and with the barrel's chamber empty the drum only turns to the next loaded one when the shot is fired.
- A lead for the round in the hand, not followed: the gun's `ShellCartridgeController` holds nothing between reloads
  (UserData nil, State 5); the gun's children are an acid effect object and its `BulletGrenadeGenerator`. The loose round
  the game's own reload shows must be looked for WHILE that reload plays.

## The same day, third part: the drum swings open, rounds are drawn (b013, b014; simulator only, unworn)

Tefa: "carry on" (the round in the hand, and design D5's open / close).

- **Where the rounds are.** Lifting one joint at a time 1.5 m away and reading the gun mesh's world bounding box: the box
  grows for each chamber joint (`_06`, `_07`, `_09` tried; also `_03`, `_05`, other gun parts) and does NOT for `_100` /
  `_101`. So every chamber joint carries a round of the gun's own, and `_100` / `_101` carry nothing. `[measured 2026-11-10]`
  (A screenshot could not settle it; the bounding box did in one question each.)
- **Drawn from that** (`guns/rounds.cpp`): a chamber's round is shown when the chamber is loaded or holds a spent case and
  shrunk to nothing when it is empty; the rounds in the hand are empty chambers' rounds moved to the hand (two, 4.5 cm
  apart). All kinds look the same (one mesh). Seen: two rounds in Jill's left hand in a simulator picture
  `[verified-live 2026-11-10, simulator, n=1]`; how they sit in the fingers is for the poser tools.
- **`guns/cylinder.{h,cpp}` (shared; D5's first cut):** the left wrist within 15 cm of the drum, LG held, LT pressed, the hand
  empty: the drum swings out on joint `_01`, 100 degrees to the gun's LEFT (b013 swung it up and to the right; b014 turned
  it), 400 degrees a second; the same press closes it. While it is not fully closed the gun does not fire. Rounds go in only
  while it is open. A fired chamber keeps a spent case (`x` in the log) and cannot be loaded until the open gun is tipped
  muzzle-up 30 degrees, when all spent cases leave at once.
- Robot test `[verified-live 2026-11-10, simulator, n=1]`, `mgl_test.py fire3 open tip left@_10 right@_07 close fire5`:
  `opening`, `3 spent case(s) tipped out`, Explosive into chambers 0 and 2 and Acid into chamber 1 (the chambers nearest the
  hand, with the drum swung out: `_10` at (-0.078, 0.119, 0.150) in the gun's space), `closing`, then the shell kinds made:
  1, 1, 1 (chambers 3, 4, 5), 1 (chamber 0), 2 (chamber 1: the acid round in its turn). On b013: a trigger pull with the
  drum open made no shot.
- For the robot: the gun points level with the right hand at pitch 78 (pitch 0 points it at the floor), muzzle-up at pitch
  125; a trigger press of 0.4 s is sometimes missed, 0.8 s is not; the left arm reaches the drum only with the gun held
  close (right hand at (0.08, 1.40, -0.16)).
- **Not done:** the closing flick (D5: a downward flick also closes), a sound of its own (the shotgun's are used), a spent
  case that looks spent (it is drawn as a whole round), cases seen falling. Whether the swing matches the game's own reload
  turn was not compared `[hypothesis]`: left was chosen because the left hand loads.
