# 2026-11-16: opening doors with the hand: how SH2 does it, and what RE3 / RE2 doors are (Developer PC, Opus)

Tefa: *"can you play sh2 and see how doors open with a hand stretched out and see if any of these can be ported over to re
games, or is that something that is just not doable in re games, like collision between game world and vr hands"*; then
*"the doors in re3 sewer save file, latest save, there is a door right behind Jill"*.

## SH2 (read from the pack's scripts, not run) `[inferred-static 2026-11-16]`
`mod/UnrealVRMod/SHProto-Win64-Shipping/scripts/libs/collision.lua` moves a small collider with each controller every frame
by a sweep (`K2_SetWorldLocation(loc, sweep=true, hit)`); a blocking hit goes to `main.lua`'s contact callback (~line 3817):
if the hit component's owner has a `DoorMovement` (`USHDoorMovementComponent`), the hand's speed along the swing direction
around the hinge (up x radius) becomes `DoorMovement:AddPhysicForce(force * 0.1)`. It works because SH2's doors are
angle-driven by a force the game itself already understands.

## RE3's door behind Jill in the latest sewer save `[verified-live 2026-11-16, simulator, n=1 door]`
`Door_3_602_603_00_gimmick`, 2.6 m behind Jill. Parts: `offline.gimmick.action.InteractBehavior` + `GimmickControl`
(`requestStartGimmick`...) + `offline.escape.gimmick.action.EsGimmickDoor`, `MotionFsm2` and `MotionJackFsm2` (the open is a
matched animation of Jill and the door), colliders `Fixed`, `FixedB`, `Moving`, `ForceClose`, a `SceneLoader` child (the next
room is streamed as it opens), `AIMapShape`, `DoorOpened`. Joints `root`, `_00`, `_01`. The leaf (`_01`) is a rigid body,
210 kg, in the body set `sm_door_steel_heavy.rbs`, whose only mode is `KeyFramedStates`: it follows the animation, it does not
swing by itself; the set has `addForce`, `setDesiredMotor...`, but no free-swinging mode to switch to. RE2's doors near its
save are the same family (`Door_2_1_..._gimmick` with `CollidersFixed / FixedB / Moving`).

## What can be ported
- **Hands meeting the world**: yes. RE Engine casts rays into the physics world from script (Village's `re8_vr.lua`
  `via.physics.System castRay`, our `visceral_re8_magthrow.lua`); a sphere or ray from the shoulder to the hand finds what
  the hand touches, and which object it is (a door gimmick, a wall).
- **Touch-to-open (recommended)**: the hand pushed into a door's collider with some speed starts the door's own open, the
  same thing A does (`GimmickControl` / the interaction). The game then plays its door, loads the next room and keeps its
  enemies and AI map right. It will not swing with the hand: it opens the game's way once pushed.
- **The door following the hand like SH2**: turning the leaf joint ourselves is possible to draw, but the game would not
  know the door is open (its collision, the next room's loading, enemies, the AI map), so walking through could fail or
  show an unloaded room. Not recommended; maybe for doors already standing open.
- **A free-swinging physics door**: not available: the door's own body file has only the follow-the-animation mode.

## Tefa's option C, measured (same afternoon): "touching a door opens it just a little, like pressing A ... and after that the door follows hand collision, like it does follow leons body"
`[verified-live 2026-11-16, simulator, n=1 each]` on the same door (hinge = joint `_00`, local yaw; `_01` is its child):
- **A**: the door's motion bank 0 / id 20 starts with layer speed 0 (its frame is SET by the game, not played): 0 to ~61
  degrees in ~0.7 s (frames 10-41), then it holds or creeps on slowly (~5 degrees a second, to 90 by ~6 s).
- **The body pushes it**: Jill nudged through the doorway (1.6 m over 80 frames): the door went 62 -> 90 degrees in ~0.8 s,
  following her, then **closed by itself** (90 -> 0 in ~2 s) once she was past. So the door does follow the body, as Tefa said.
- **Our own write did not take**: `layer:set_Frame(60)` every LateUpdateBehavior for 2 s (180 writes): the door kept its own
  slow creep (67 -> 78 degrees) and the frame read back 0 during the writes. The angle is set deeper than the motion layer's
  frame (the door's behaviour tree / its push logic), after or instead of our write.
- A closed door blocks the body (pushed into it, Jill stopped at it). From the far side A did not open it (3 tries).
- Driving it: A only fired with Jill WALKED into place (stick), not when she was only moved there by script.
**So option C looks possible in principle (the game already turns the door by the body), but needs the place where the
game works out the door's angle from the body, to give it the hand instead. That is the undocumented-engine part:
`MODEL: FABLE`.** A cheaper first test (Opus): turn the hinge joint ourselves after the game, just before drawing, and
see whether its collision follows (if it does, the hand can push it visually on top of the game's own opening).
