// re3check.h -- read-only checks of the numbers and names the port carried over from RE2 (2026-10-15, /pd).
//   Once per launch: the input Kind bits and ActionOrder.Precede values the code hard-codes, read back from RE3's own
//   type database (MATCH / DIFFERS / NOT FOUND). Once per gun: every joint name on the held gun, so the RE2 magazine
//   (_04) and slide (_01) joints can be checked against RE3's meshes. Logs only, changes nothing.
#pragma once

namespace vn::re3check {
void frame();   // once per frame (UpdateBehavior pre); does its work once and then only on a new gun
} // namespace vn::re3check
