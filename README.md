# Visceral VR — Resident Evil 3 (2020)

**Work in progress.** Visceral for RE3 brings the features of
[Visceral RE2](https://github.com/TefMeister/visceral-re2-vr) over to Resident Evil 3, on top of praydog's
REFramework VR. Work began on 2026-10-10. The first build, 0.1.0 (2026-10-11), is on the
[Releases page](https://github.com/TefMeister/visceral-re3-vr/releases).

| Folder | What it holds |
| --- | --- |
| `dev-archive/native/` | the native plugin (`visceral_native.dll`), ported from RE2 with RE3's type names and weapon numbers |
| `dev-archive/reframework-patch/` | our changes to REFramework, applied to praydog's source and built for RE3 |
| `dev-archive/scripts/` | our REFramework Lua scripts for RE3 |
| `dev-archive/tools/re-engine/` | the animation-file tools (relaxed body pose, idle swap) |
| `modding-notes/` | the dated progress notes |
| `ideas/fresh/` | new ideas copied here from the private ideas repo, not yet picked |
| `ideas/chosen/` | ideas Tefa has chosen to keep for this mod |

The resume point and the open work live on the private status board (`claude-memory/status/visceral-re3-vr.md`).

## Credits

- **praydog**: REFramework and its VR mode, which this whole mod runs on.
- **Andyalpa**: the manual reload work and sounds that Visceral RE2 carries over.
- **Ekey**: REE.PAK.Tool and its RE3 file-name list.
- **[alphaZomega](https://github.com/alphazolam)**: [EMV Engine](https://github.com/alphazolam/EMV-Engine) (MIT), whose poser (freeze a joint, pose it by its local angles, re-apply it after the animation has run) is what our Hand Poser is modelled on; this mod's finger poses on the guns and at the grip spots come from that tool. Studied and written fresh; none of its code is included.
- Everyone in Visceral RE2's credits list, whose work this port reuses.

If someone should be credited here and is not, open an issue on GitHub and it will be fixed as soon as possible. We honour
correction and removal requests from rights holders.
