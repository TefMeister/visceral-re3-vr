Description


Both eyes get the same lighting in VR when REFramework draws with Single Frame Multipass.

Without it, one eye is drawn with the game's automatic brightness and the other without it, so one eye looks brighter than the other.

What it does, every frame:
- holds the game's automatic brightness at each area's own level, so both eyes get the same picture

The game's own colours and contrast are left as they are. In the REFramework menu, under "Visceral: steady light", the per-area colour tint can be switched off and the contrast changed.

Caution: Resident Evil 3 in VR is still being worked on. VR can cause motion sickness and discomfort; stop and rest if you feel unwell.


Installation instructions


STEP 1 - The game and REFramework VR

1.1  Resident Evil 3 (Steam) with praydog's REFramework and its VR files already installed and working in the headset.

1.2  In the REFramework menu > VR, set the rendering technique to Single Frame Multipass. (This mod is the fix for that mode; with Two Frame Sequential it is not needed.)


STEP 2 - This mod

2.1  With Fluffy Mod Manager: put this zip in Fluffy's RE3 mods folder, open Fluffy, choose Resident Evil 3 and tick "Visceral Steady Light - RE3 VR".

2.2  By hand instead: copy the "reframework" folder from this zip into the game folder (the folder that contains re3.exe), and say yes to merging folders.

2.3  Start the game. In the REFramework menu, "Visceral: steady light" shows the settings.


Settings


Light: "area" (default) holds each area's own brightness. "hold" uses one brightness everywhere (the "Held EV" slider). "game" switches the mod's lighting off, to compare.

Per-area colour grading: "game" (default) or "off".

Contrast: 0 (default) leaves the game's own; 1.2 is what Visceral RE2 uses.

The settings are saved in reframework/data/visceral_steady_light.json.


Requirements


Resident Evil 3 (Steam)

praydog's REFramework with VR

Works beside Visceral RE3 VR (its own older light fix does the same job less fully).


UNINSTALL


Untick it in Fluffy Mod Manager, or delete these two files from the game folder:

reframework/autorun/visceral_steady_light.lua

reframework/data/visceral_steady_light.json


Shout outs


praydog - REFramework and its VR mode, which this runs on

FluffyQuack - Fluffy Mod Manager
