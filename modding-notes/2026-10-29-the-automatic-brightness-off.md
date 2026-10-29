# 2026-10-29 — the game's automatic brightness kept off (home PC, Fable, desk; not run yet)

Tefa: *"remove the adaptive lighting from RE8 and 3"*. RE2's switch of 2026-10-28 (`exposure.cpp`) is ported as it stood after
b192, brightness part only (no colour-grading or contrast change): every frame at BeginRendering the main camera's
`via.render.ToneMapping` gets AutoExposure = Disable and its AutoExposureMinEV / MaxEV pinned to the area's own EV, so the
adaptation has no room even when the game's controller switches it back on. NUM7 toggles it; the REFramework menu's
"Visceral: brightness" tree has a tick box "Let the game adjust the brightness by itself" (bridge slot 56) to compare.

Built a9fae9a8 `[compile-verified 2026-10-29]`, installed in the Steam game; the files it replaced are in
`D:/RE3 REFramework builds/_backup-2026-10-29-2209-before-brightness-off/`. **Nothing checked live in RE3 yet**: the first
run's log must show `exposure: Disable = N, kept` and then `kept off (... UseAutoExposure 0, EV x, limits x..x)` with a
steady EV; RE2 in the headset still has to prove the pinned limits hold there (its b192 is unworn).
