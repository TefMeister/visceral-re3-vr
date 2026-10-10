# RE2-only assumptions left in the RE3 port of the native plugin

Date: 2026-10-10. Author: static reader helper for the /lm session (read-only; nothing launched, nothing installed).
Source read: `dev-archive/native/src` (the port of `visceral-re2-vr/dev-archive/native/src`), the public RE3 file list
(`RE3_RT_STM_Release.list`), and the startup lines of the plugin in `C:\Steam\steamapps\common\RE3\re2_framework_log.txt`
(written by the live session at 21:23; no weapon was held in that log).

**Nothing in this note was measured live by me.** Every claim is `[inferred-static]` (read from code, file names or the
existing startup log) or `[hypothesis]`.

## 1. What the RE3 weapon numbers are (from file names in the RE3 file list)

`natives/stm/escape/weapon/wpNNNN/mesh/...` names each gun [inferred-static]:

| WP | RE3 mesh name | What it most likely is | weapons.cpp calls it |
| --- | --- | --- | --- |
| 0000 | `wp0000_g19` (+ magazine, sight, suppressor parts) | G19, Jill's handgun | G19 (ok) |
| 0100 | `wp0100_g18` (+ magazine) | G18 burst | ok |
| 0200 | `wp0200_g18` | G18 | ok |
| 0300 | `wp0300_samuraiedge` | Samurai Edge | ok |
| 0600 | `wp0600_mup` | MUP | ok |
| 1000 | `wp1000_shotgun` (+ shell, stock, barrel parts) | M3 shotgun | ok |
| 2000 | `wp2000_assaultrifle` (+ dualmagazine, foregrip, sight) | CQBR assault rifle | ok |
| 2100 | `wp2100_assaultrifle` | a second assault rifle (variant / unlockable) [hypothesis] | ok |
| 3000 | `wp3000_magnum` (+ longbarrel, standardbarrel) | Lightning Hawk [hypothesis] | ok |
| 3100 | `wp3100_lightning` (+ meter) | RAI-DEN [hypothesis] | "Magnum (other)" |
| 4100 | `wp4100_grenadelauncher` | MGL grenade launcher | ok |
| 4200 | no weapon mesh; only `bomb/wp4200`, `radiate/wp4200` | not a held gun; probably a launcher round / effect [hypothesis] | "Special weapon 4200" |
| 4400 | `wp4400_rocketlauncher` | Rocket launcher | "Special weapon 4400" |
| 4500 / 4510 | `combatknife` | Combat knife / second knife | ok |
| 4520 | `wp4520_knife` (+ `knife_hot_msk3`) | Hot Dogger [hypothesis] | "Knife 4520" |
| 4600 | `wp4600_rocketlauncher` | second (infinite?) rocket launcher [hypothesis] | "Rocket Launcher" |
| 4700 | `wp4700_railgun` | the railgun (boss fight) | "Special weapon 4700" |
| 6200 / 6300 | `grenade` / `flash` | Hand / flash grenade | ok |
| 9000 / 9100 / 9200 / 9500 | r-launcher, flamethrower, rubble, g19 | Nemesis's and NPC weapons, not Jill's/Carlos's [hypothesis] | not listed (fine) |

The game's own weapon sound banks are `escape/sound/.../container_weapon/wp0000, wp1000, wp2000, wp3000, wp3100, wp4100,
wp4400, wp4500, wp4520, wp4700, wp6200, wp6300` [inferred-static].

Same number does not mean same gun: RE2 wp0000 Matilda vs RE3 G19, RE2 wp2000 MQ 11 SMG vs RE3 CQBR rifle, RE2 wp0100/0200
vs RE3 G18s. Every per-weapon number copied from RE2 below is for a different gun.

## 2. Findings, file by file

Fails safe = only logs / does nothing. Misbehaves = can change what the game does in a bad way.

### reload_data.h (all of it is RE2/Andyalpa data)
- **:203-214 `MAG_WEAPONS`** — RE2 IDs 0, 100, 200, 400, 600, 700, 2000, 2200, 3000, 7000, with RE2 joint names (`_04`, `_01`
  for 400), RE2 magwell exit points, dock distances, sound folders and Leon/Claire hand holds [inferred-static].
  In RE3 this matches 0, 100, 200, 600, 2000, 3000 — but they are **other guns** (G19, G18s, MUP, CQBR rifle, RE3 magnum).
  400/700/2200/7000 do not exist in RE3 (harmless). 300 Samurai Edge, 2100 rifle, 3100 RAI-DEN are not listed and keep
  the game's reload (inconsistent but harmless) [inferred-static].
  - Joint `_04` as "the magazine" on RE3 meshes: unknown; RE3 meshes were not read [hypothesis].
  - **Misbehaves if `_04` is missing:** `reload::managed_now()` (reload.cpp:371) only needs the table entry, the gun and the
    headset, not the joint. So the game's own reload is blocked (reload_block hooks + orderer inhibit) while
    `begin_drop()` (reload.cpp:354) refuses with "joint not found, no drop". Result: **that gun cannot be reloaded at all**
    while the headset is on [inferred-static].
  - If `_04` exists but is another part (trigger, hammer, sight), that part slides out, falls and is hidden, then is
    restored on insert [hypothesis].
  - Exit points / dock (e.g. wp2000 `{-0.002,-0.108,0.006}` for the MQ 11) put the "magwell" at RE2-gun positions; the
    insert spot may be in the air or inside the rifle [hypothesis]. Partly softened by `RELOAD_DOCK_MIN_M` 6 cm.
  - Sound folders: wp2000 -> `smg_mq11`, wp3000 -> `magnum`, handguns -> `handgun`. The RE3 install already has
    `reframework/data/custom_sfx/{handgun, magnum, smg_mq11, shotgun_w870, ...}` (RE2 recordings), so they will play, as
    RE2 sounds on RE3 guns [inferred-static].
- **:220-237 `SLIDE_WEAPONS`** — slide joint `_01` and RE2 slide travel (rest/parked/back Z) for the same RE2 IDs; wp2000
  uses the MQ 11 bolt numbers on the CQBR rifle. Pumps 1000/1100/1200/1500 and 4300 Spark Shot: only 1000 exists in RE3
  [inferred-static]. Travel is applied as an offset from the joint's real rest (rack.cpp:80-82), so a wrong joint moves a
  wrong part by a few cm along its local Z [inferred-static].
- **:243 `is_pump`** — 1000 is a pump. Whether the RE3 M3 is pumped by hand in its animation is not checked [hypothesis].
- **:250-255 `SHELL_WEAPONS`** — wp1000 shell = mesh part **31** on joint `_04`, loading port from the RE2 W-870. RE3's
  wp1000 has a shell texture (`wp1000_shell_*`), so a shell part probably exists, but its index and joint are unknown
  [hypothesis]. **Misbehaves:** `setPartsEnable(31, true/false)` (reload.cpp:123) on a wrong index shows or hides another
  part of the shotgun; a wrong joint gets moved to the left hand [hypothesis]. If `_04` is missing the grab just logs
  (reload.cpp:449) — but the game's shell reload is still blocked, so the **M3 cannot be reloaded** [inferred-static].
- **:261 `pump_sfx`** — `spark_shot` folder is RE2-only; never reached in RE3 (no wp4300) [inferred-static].

### reload.cpp
- **:107 `g_claire = name starts with "pl1"`** — RE2: pl1000 Claire. RE3: Jill is pl2000, Carlos pl0000, so this is always
  false and **both Jill and Carlos get Leon's magazine hold** (`hand_pose`, :224) [inferred-static]. Fails safe (the
  magazine just sits wrong in the hand).
- **:108 `l_arm_wrist`** — RE engine human joint name; likely the same on pl2000/pl0000 [hypothesis]. If missing, the
  hand pose fails and nothing moves (safe).
- **:168, :232-262** — RE2 inventory calls (`reloadMainSlot`, `get_MainSlot`, `getMainWeaponReloadableBullet`,
  `getReloadableBulletMainSlot`, `executeReload(WeaponType,int)`, `executeEndReload`, `getBulletNumber`). The startup log
  shows the hooks on `reloadMainSlot` and both `executeReload` overloads went in, so those names exist in RE3
  [inferred-static, from the existing startup log]. The others are not hooked at startup and are unchecked [hypothesis];
  `call_direct` returns the default when missing, so `top_up` would add nothing and log "loaded x -> x" (no crash, but
  the magazine goes in empty).
- **:263** — a magazine into an empty gun calls `rack::need` (see rack.cpp below).

### rack.cpp
- **:62 slide/fore-end joint from `SLIDE_WEAPONS`**, :63 `r_arm_wrist`, :73 `l_arm_wrist` — as above.
- **:142 `blocks_fire()` + :146 `need()` + :153 `slide_lock_empty()`** — after a magazine into an empty gun (reload.cpp:263),
  or after each M3 shot with more shells in it (pump_native.cpp:339), **the gun refuses to fire until the hand racks the
  `_01` joint**. `hand_near_joint` (:71) returns false when the joint is missing, so the rack can never happen and the gun
  stays blocked until it is swapped [inferred-static]. **Misbehaves.** If `_01` is a real but different part, the rack
  works but moves the wrong part [hypothesis].
- **:123 `executeEndEject`** for pumps — RE2 Gun method, unchecked in RE3 [hypothesis]; missing = no-op.

### pump_native.cpp
- **:262 `is_pump_clip`** — matches clip names containing `wp1000`, `wp1001`, `wp1100`, `wp1200`, `wp1300`, `wp1500`,
  `sg02`, `_sg0`, `wp4300`. RE3 also has `wp1000` / `wp1001` (a variant folder), so RE3 shotgun clips with "reload",
  "pump", "cycle", "eject", "rack" or "blowback" in the name would be fast-forwarded to their end (:285-287) for 2.5 s
  after a shot [inferred-static]. RE3 clip names are unknown [hypothesis]. Misbehaves only if the M3's clips are named that
  way but are not a pump (e.g. its reload); the player-side check (:260, any "pump" clip) is game-wide.
- **:325 `ShellCartridgeController.generate`** hook went in on RE3 [inferred-static, startup log]; every shell eject on
  wp1000 is held back until our pull. If the rack never completes (above), no shells are ever ejected [inferred-static].
- **:247 `getMainWeaponRemainingBullet`** — hooked fine at startup in RE3 [inferred-static, startup log].

### reload_block.cpp
- **:20-22 hard-coded enum values** from RE2's type database: `KIND_SUPPORT_HOLD = 128`, `KIND_RELOAD = 512`,
  `PRECEDE_RELOAD = 8`, and ButtonBits offsets 0x10/0x18/0x20 [inferred-static]. Not re-read for RE3. If RE3's
  `offline.InputDefine.Kind` or `ActionOrder.Precede` differ, `inhibit_reload` (:37) would inhibit **another action** and
  `clear_bit` (:140) would wipe **another button** every frame while one of our guns is held [hypothesis]. **Could
  misbehave** (e.g. a lost dodge). Same constants in fire.cpp:21 (`KIND_ATTACK = 256`) and suppress.cpp:35-36, 109.
  Cheapest check: read the RE3 enum values from the type database the same way weapons.cpp reads WeaponType.
- **:169 `RemainingBulletBehavior.get_RequestDraw` not found in RE3** — the "ammo counter for 5 s after a reload" does
  nothing [inferred-static, startup log]. Safe.

### weapons.cpp
- **:18-39 table** — names fixed above. Holster sorting by range: 3100 (RAI-DEN) HANDGUN ok; 4200 probably not a held
  weapon; 4700 railgun as SPECIAL (a boss-fight weapon; holster grab may do odd things there) [hypothesis]. Unknown
  numbers return "unknown"/NONE (safe).
- **:47** reads `offline.EquipmentDefine.WeaponType` names; only names exactly `WPnnnn` (6 chars) are mapped. If RE3 names
  some entries differently (e.g. with a suffix), those weapons read as -1 = "bare hands" everywhere [hypothesis].

### holster.cpp / subweapon.cpp / shortcut.cpp / suppress.cpp / spread.cpp / spreadprobe.cpp (the "sub weapon" lists)
- **holster.cpp:280, subweapon.cpp:385, shortcut.cpp:16, suppress.cpp:141, spread.cpp:171, spreadprobe.cpp:41** — the
  knife/grenade list `{4500, 4510, 6200, 6300}` is hard-coded six times. RE3 adds **4520 (Hot Dogger)** which is in none of
  them [inferred-static]. Effects: with the Hot Dogger in hand, a right-grip press in a holster zone swaps weapons instead
  of leaving it to the game (holster.cpp:280); spread writes reticle fit for it (harmless); suppress does not treat it as a
  sub weapon. Mostly safe. Better: one `weapons::is_sub(wp)` from the table's `Holster::SUB`.
- **The whole sub-weapon idea is RE2's.** RE3 has no sub-weapon slot: `Inventory.equipSubSlot(Slot)`,
  `equipSubSlot(Shortcut)` and `equipSubSlotLastWeapon` are **not found** in RE3 [inferred-static, startup log]. Knives and
  grenades in RE3 are most likely ordinary shortcut weapons [hypothesis]. So:
  - shortcut.cpp:50-57 forcing `enableShortcut` = yes for knife/grenades is probably a no-op in RE3 (safe) [hypothesis].
  - shortcut.cpp:102 **skips `PlayerActionOrderer.set_RequestSubShortcut` entirely** (the hook went in on RE3). What that
  request does in RE3 is unknown; if RE3 uses it for something live (e.g. the knife quick action), it is now dead
  [hypothesis]. Could misbehave.
  - subweapon.cpp:385 `grenade_out` (6200/6300) and the back-holster "sub weapon out" latch feed praydog's VR layer
  (`openvr_input_to_re2_re3`, `re2_vr_grenade.lua`). Whether RE3's VR layer reads `visceral_vr_buttons` the same way is
  unchecked [hypothesis].

### fire.cpp / settings.h
- **settings.h:124 `FIRE_AUTOMATIC_WP = {2000, 2200, 4200, 4700, 8700, 4520, 4900}`** — RE2 automatics (MQ 11, LE 5,
  flamethrower, miniguns). In RE3: 2000 CQBR is automatic (right by luck); **2100 (the other rifle) is missing**, so it
  fires once per pull with RT alone; **4700 is the railgun**, now treated as automatic (RT held keeps forcing
  `enableAttack` yes) [inferred-static for the list, hypothesis for the effect]. 4520 is excluded anyway by
  `gun_in_hand` (SUB). 4200/8700/4900 do not exist as held guns in RE3 (harmless).
- **settings.h:89, spread.h** — reticle range "0-100, Matilda's" measured in RE2; spread reads the gun's own
  `ReticleParam` first, so it adapts if the field names exist [inferred-static]. If `_ReticleFitPoint` is missing it does
  nothing (safe).

### sfx.cpp
- **:275** sounds come from `<exe folder>\reframework\data\custom_sfx\<folder>\<kind>.ogg/.wav`. The RE3 install has the
  RE2 set copied there [inferred-static], so the folder names from reload_data.h resolve. Missing file = one warning, no
  sound (safe). Only the sounds are wrong-gun (MQ 11 sounds on the CQBR, W-870 on the M3).

## 3. Top five, ranked by how likely they bite in the headset

1. **Magazine / slide joint names `_04` / `_01` are RE2's.** If RE3's G19, G18s, MUP, CQBR or magnum lack them, those guns
   can no longer be reloaded (the game's reload is blocked, ours refuses). [hypothesis on the names; inferred-static on the
   lock-out]
2. **Rack / pump fire-block.** A magazine into an empty gun, or every M3 shot, blocks firing until the `_01` joint is
   racked; a missing or wrong joint leaves the gun dead until swapped. [inferred-static]
3. **All per-gun positions are for other guns** (G19 gets Matilda's magwell, CQBR rifle gets the MQ 11's, RE3 magnum gets
   RE2's), and both RE3 characters get Leon's hand hold because `"pl1"` means Claire. Wrong spot to insert, odd hand pose.
   [inferred-static]
4. **Shotgun shell part 31 on joint `_04`** may show/hide a different part of the M3, and RE2 pump clip names may cut
   RE3 shotgun clips. [hypothesis]
5. **RE2 enum numbers and the sub-weapon system:** input Kind 128/256/512 and Precede 8 are hard-coded; RE3 has no
   sub-weapon slot, `set_RequestSubShortcut` is skipped outright, and the Hot Dogger (4520) is in none of the knife lists.
   Could silently block an RE3 action. [hypothesis]

Cheapest next checks (all static or one flat run): log `getJointByName` for `_00`..`_10` on each held gun (one line per
gun), read `InputDefine.Kind` / `ActionOrder.Precede` values from the type database at startup, and log the M3's mesh
part count and names.
