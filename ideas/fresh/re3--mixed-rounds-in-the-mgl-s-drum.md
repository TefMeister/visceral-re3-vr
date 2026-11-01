# Mixed rounds in the MGL's drum

Order: 12001
From: the ideas repo, `games/re3.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/re3.md>), copied 2026-11-01

`[raw]` · `[looks doable]` — *judged from method names only (the game has a "change bullet" call on the weapon); NOT tried*

**What Tefa said (2026-11-01, MGL headset check):** load different round types into the same drum, and have the game
switch to the type of whichever chamber rotates up to fire. Same for any magazine, "if different ammo in the same mag is
doable".
**What it'd take:** keep our own list of which round sits in which chamber; before each shot, switch the gun's loaded
type to the next chamber's (RE2/RE3 have `Equipment.executeChangeBullet` / `requestChangeBullet`), without the game
emptying or refilling the drum when it switches. ⚠️ Whether a switch keeps the drum's count is the open question.

_Other categories appear as ideas arrive._

**To add one:** `[re3] your idea` — anywhere, any time.

🔗 Ideas for **all four** Resident Evil games at once — they share an engine and a modding framework — go on [`resident-evil-all.md`](resident-evil-all.md) (`[re games] your idea`).
