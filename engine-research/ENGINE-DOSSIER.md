# ENGINE-DOSSIER — Visceral RE3 VR

RE Engine (RE3 2020), praydog's REFramework VR (v1.5.9.1 + the 76298bd DLSS files + our patch). Same engine and
REFramework as Visceral RE2, so RE2's dossier (`visceral-re2-vr/engine-research/ENGINE-DOSSIER.md`) is the main
reference; this file holds only what is different or unknown in RE3. Started 2026-10-15 (`/pd`), from the 2026-10-10
reader note on the port.

## 1. Names: RE3 uses `offline.*` where RE2 uses `app.ropeway.*`

- `offline.PlayerManager`, `offline.InputSystem`, `offline.survivor.Equipment`, `offline.survivor.SurvivorCondition`,
  `offline.survivor.Inventory`, `offline.EquipmentDefine.WeaponType` all resolve `[inferred-static 2026-10-10, re3.exe
  strings + the startup log]`.
- Not found in RE3: `gui.NewInventoryBehavior` (menu tint), `Inventory.equipSubSlot(Slot)`, `equipSubSlot(Shortcut)`,
  `equipSubSlotLastWeapon`, `get_IsSubWeapon`, `offline.gui.RemainingBulletBehavior.get_RequestDraw` `[inferred-static
  2026-10-10]`. RE3 has no sub-weapon slot; knives and grenades are most likely ordinary shortcut weapons `[hypothesis]`.
- Our REFramework build reads `re2_fw_config.txt` and writes `re2_framework_log.txt` even in RE3 (name hard-coded in
  REFrameworkConfig.hpp) `[verified-live 2026-10-10, n=1]`.

## 2. Weapon numbers (from the RE3 file list's mesh names) `[inferred-static 2026-10-10]`

| WP | RE3 mesh | most likely |
| --- | --- | --- |
| 0000 | `wp0000_g19` | G19 (Jill's handgun) |
| 0100 / 0200 | `wp0100_g18` / `wp0200_g18` | G18 burst / G18 |
| 0300 | `wp0300_samuraiedge` | Samurai Edge |
| 0600 | `wp0600_mup` | MUP |
| 1000 | `wp1000_shotgun` | M3 shotgun |
| 2000 / 2100 | `wp2000_assaultrifle` / `wp2100_assaultrifle` | CQBR / a second rifle `[hypothesis]` |
| 3000 / 3100 | `wp3000_magnum` / `wp3100_lightning` | Lightning Hawk / RAI-DEN `[hypothesis]` |
| 4100 | `wp4100_grenadelauncher` | MGL |
| 4400 / 4600 | rocket launchers | second one infinite? `[hypothesis]` |
| 4500 / 4510 / 4520 | knives (`wp4520_knife` + `knife_hot_msk3`) | 4520 = Hot Dogger `[hypothesis]` |
| 4700 | `wp4700_railgun` | the boss-fight railgun |
| 6200 / 6300 | grenade / flash | hand / flash grenade |
| 4200 | no held mesh | not a held gun `[hypothesis]` |

**Same number does not mean same gun**: RE2 wp0000 Matilda vs RE3 G19, RE2 wp2000 MQ 11 vs RE3 CQBR. Every per-gun
number copied from RE2 (magwell spots, slide travel, hand holds, sound folders) is for a different gun.

## 3. RE2 assumptions still in the port (reader note 2026-10-10, ranked)

1. **Magazine / slide joints `_04` / `_01` are RE2's.** If an RE3 gun lacks them, the game's reload is blocked while
   ours refuses ("joint not found"), so that gun cannot be reloaded at all with the headset on `[inferred-static]` for the
   lock-out, `[hypothesis]` for the names. Against the worst case: the 2026-10-10 19:40 VR run found `_01` on WP0000 and
   WP2000 and the magazine-out block worked `[verified-live 2026-10-10, n=1]`.
2. **Rack / pump fire-block**: after a magazine into an empty gun, or each M3 shot, the gun will not fire until the
   `_01` joint is racked; a missing joint leaves it dead until swapped `[inferred-static]`.
3. **Per-gun positions are other guns'**, and both RE3 characters get Leon's hand hold (`"pl1"` = Claire in RE2; RE3 is
   pl2000 Jill, pl0000 Carlos) `[inferred-static]`.
4. **M3 shell = mesh part 31 on `_04`**, from RE2's W-870; may show/hide another part `[hypothesis]`.
5. **Hard-coded RE2 enum numbers**: InputDefine.Kind HOLD 64, SUPPORT_HOLD 128, ATTACK 256, RELOAD 512; ActionOrder
   Precede ATTACK 4, RELOAD 8. If RE3's differ, the code inhibits or clears another action `[hypothesis]`.

Also: `set_RequestSubShortcut` is skipped outright (unknown what it does in RE3) `[hypothesis]`; custom_sfx holds RE2's
recordings, so RE3 guns play RE2 sounds `[inferred-static]`.

## 4. Built 2026-10-15 (`/pd`), plugin fef6cbb3, installed on the home PC, UNRUN `[compile-verified 2026-10-15]`

- `re3check.cpp`, logs only: once per launch reads items 5's numbers back from RE3's own type database
  (`re3check: InputDefine.Kind.ATTACK game N, ours 256: MATCH / DIFFERS`; the Precede type is taken from
  `setInhibitPrecede`'s own parameter); once per gun lists every joint on the held gun and says whether `_01` and `_04`
  are present. Answers items 1, 2 and 5 on the first launch that draws each gun.
- One sub-weapon list: the five hard-coded `{4500, 4510, 6200, 6300}` checks (holster, shortcut, spread, spread probe,
  suppress) now ask the weapons table (`weapons::is_sub`), so 4520 counts as a knife like the table already says.
- `FIRE_AUTOMATIC_WP` gains 2100 (the second rifle fires full-auto like the CQBR) `[hypothesis]`.

## 5. Where things live

- Game: `C:/Steam/steamapps/common/RE3` (home PC). Music muted, window confirmed by Tefa 2026-10-10.
- Plugin history: `D:/RE3 REFramework builds/plugin-history/` (+ MANIFEST.sha256).
- No type dump for RE3 on disk yet; RE2's `il2cpp_dump.json` covers the shared `via.*` engine types.
