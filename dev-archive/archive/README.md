# Archive: files tried and taken out of the game folder
- `visceral_title_level.lua` (2026-11-01, sha256 5ca46d7da158): levels and lifts the primary camera on the title screen. NO EFFECT on the simulator: the primary camera's transform reads (0,0,0), unrotated, at the title; the title scene is drawn through another camera or a matrix set directly. Taken out.
