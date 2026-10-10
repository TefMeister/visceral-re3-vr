# 2026-10-10 — porting Visceral RE2 to RE3

## The day in order

1. **First run.** RE3 with praydog's March REFramework and the DLSS files (DLSS off) reached the menu. The music was
   muted and Tefa confirmed the window.
2. **Port 1+2: relaxed body pose.** Every weapon list for Jill (pl2000) and Carlos (pl0000) now uses the no-weapon
   (KFF_) motions, and the Hold look-at profiles are copies of Default (the hunch fix). Made by
   `dev-archive/tools/re-engine/relax_re3.py`.
3. **All of RE2 BASELINE 3 (b139).** The REFramework patch was rebuilt for RE3. The plugin was ported with `offline.`
   type names and RE3 weapon numbers (the names are a best guess). The body scripts went in unchanged, except for the
   game check.
4. **Worn: twist, hunch, torso push.** The log showed the loose-file loader never started. Cause
   `[verified-live 2026-10-10, n=1]`: our REFramework build reads **`re2_fw_config.txt`** even in RE3, because the name
   is fixed in `REFrameworkConfig.hpp`. It made that file with defaults (FirstPerson off, loose files off, DLSS on).
   Fixed: our settings now live in `re2_fw_config.txt` in the RE3 folder.
5. **Worn again.** Tefa: "body is the relaxed pose now, but torso still pushes out and stays out until i start walking".
   Every stop, armed or not, plays slot 0xa0 = `0160_KFF_Gazing_Idle_F_Loop`. Being tested: the idle slots now play
   `0161_KFF_Gazing_Idle_F_Relax_Loop` (`swap_idle_re3.py`, Jill only). `[hypothesis]`
6. **RE2 b145 brought over** (Tefa's reference build). REFramework gets the slide-rack hand dock. The plugin gets b141 to
   b145: motion slide racking, no shot with the magazine out, a dry click, the ammo counter after a reload, the shell
   hold, and the pick-up screen keeping the world camera. All the new RE3 names were found in re3.exe
   `[inferred-static]`. The rack's slide joints are RE2's and may not match RE3's guns. The title-screen scripts are
   RE2-only and were not brought over.

## Installed now (RE3 folder)

- dinput8.dll: REFramework 76298bd + `dev-archive/reframework-patch/2026-10-10-visceral-b145-for-re3.diff`
- visceral_native.dll: built from `dev-archive/native` (b145 level)
- autorun: visceral_bridge (b145), visceral_mute_music, the three body scripts, praydog's own scripts
- natives: the relaxed lists plus the idle swap for Jill

## 21:23 flat check (/lm, no headset)

- With no headset, REFramework could not open OpenXR and the game ran flat. The route from boot to Continue worked by
  keyboard: Insert, Enter, Space, Space. Recorded: `b145 port flat check_2026-10-10_21-23-34.mp4`.
- The loose-file loader starts now and RE3 loads our files: cmn/base_cmn_move (the idle swap), hdg hold/move, mle hold,
  smg hold, stg move, and all 11 look-at files `[verified-live 2026-10-10, n=1]`.
- Every new b145 hook went in, with one exception: `offline.gui.RemainingBulletBehavior.get_RequestDraw` is missing in
  RE3, so **the ammo counter after a reload will not show** until RE3's own way is found `[verified-live 2026-10-10, n=1]`.
  Missing as expected: equipSubSlot*, NewInventoryBehavior (menu tint).
- The rack found a slide joint on RE3's G19: "WP0000 joint _01 rests at local 0.000 0.073 0.062 (his rest 0.060)".
  Promising, but not tried.
- Still open: the motion-name log only runs in VR, so a flat run cannot show which idle actually plays. That needs
  Tefa's eyes in the headset.
- Evidence: `dev-archive/recon/2026-10-10-flat-b145/`.
