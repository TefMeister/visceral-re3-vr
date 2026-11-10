// guns_table.cpp -- RE3's per-gun numbers for the reload by hand (declared in guns/gun_data.h).
//
// The numbers are Andyalpa's RE2 data (RE2VRMODRELOADED 1.0.1, used with his permission 2026-09-04; credit: Andyalpa), keyed by
// WP id exactly as gen-1 RE3 used them since 2026-10-10. RE3's ids name other guns: 0 the G19, 100 / 200 the G18, 600 the MUP,
// 2000 / 2100 the CQBR, 3000 the Lightning Hawk, 1000 the M3. Checked so far `[2026-11-07]`: the M3's joints _01 / _04 exist
// (re3check, 2026-11-02); the G19's slide (_01) racked and locked in the headset (2026-11-01). The magazine numbers were never
// checked in RE3: the simulator drive's magreport shows whether each magazine joint sits where this table says.
// Changes from gen-1: the CQBR is a long-magazine gun (LG on it + LT pulls it out), the CQBR 2100 takes 2000's numbers, and
// RE2-only guns (the LE 5 2200, the Samurai Edge 7000, the other shotguns, the Spark Shot) are gone.
#include "gun_data.h"

namespace vn::guns {

namespace {
constexpr Hold HOLD_GENERIC = {0.115f, -0.135f, 0.010f, -180.0f, -92.0f, 2.5f};
constexpr Hold HOLD_GENERIC_2 = {0.092f, -0.074f, 0.010f, -180.0f, -92.0f, 2.5f};

constexpr MagGun MAG_GUNS[] = {
    {0,    "_04", {-0.004f, -0.110f, -0.026f}, 0.05f, "handgun",  2.0f, {0.099f, -0.024f, 0.056f, 72.5f, 15.0f, 106.5f}, HOLD_GENERIC},
    {100,  "_04", { 0.001f, -0.093f, -0.016f}, 0.03f, "handgun",  2.0f, {0.127f, -0.030f, 0.052f, -106.5f, 156.0f, -61.0f}, HOLD_GENERIC},
    {200,  "_04", { 0.000f, -0.089f, -0.023f}, 0.03f, "handgun",  2.0f, {0.100f, -0.032f, 0.028f, -82.5f, -180.0f, -53.5f}, HOLD_GENERIC},
    {600,  "_04", { 0.000f, -0.103f, -0.035f}, 0.05f, "handgun",  2.0f, HOLD_GENERIC, HOLD_GENERIC},
    {2000, "_04", {-0.002f, -0.108f,  0.006f}, 0.02f, "smg_mq11", 1.0f, {0.093f, -0.021f, 0.045f, -90.0f, 172.5f, -72.5f}, HOLD_GENERIC_2},
    {2100, "_04", {-0.002f, -0.108f,  0.006f}, 0.02f, "smg_mq11", 1.0f, {0.093f, -0.021f, 0.045f, -90.0f, 172.5f, -72.5f}, HOLD_GENERIC_2},
    {3000, "_04", { 0.000f, -0.103f, -0.022f}, 0.05f, "magnum",   1.0f, HOLD_GENERIC_2, HOLD_GENERIC_2},
};

constexpr SlideGun SLIDE_GUNS[] = {
    {0,    "_01", 0.060f, 0.038f,  0.013f},
    {100,  "_01", 0.101f, 0.057f,  0.007f},
    {200,  "_01", 0.101f, 0.072f,  0.044f},
    {600,  "_01", 0.098f, 0.060f,  0.025f},
    {2000, "_01", 0.004f, 0.003f, -0.072f},
    {2100, "_01", 0.004f, 0.003f, -0.072f},
    {3000, "_01", 0.098f, 0.058f,  0.030f},
    {1000, "_01", 0.000f, 0.000f, -0.080f},   // the M3's fore-end
};

constexpr ShellGun SHELL_GUNS[] = {
    {1000, "_04", 31, {-0.001f, -0.030f, 0.148f}, 0.22f, "shotgun_w870", 2.0f},
    // the MGL: no round of its own to show yet; the port is the middle of the drum (joints _01 + _02, read 2026-11-10)
    {4100, "",    -1, { 0.000f,  0.051f, 0.261f}, 0.22f, "shotgun_w870", 2.0f},
};

// RE3 item numbers (read from the running game 2026-11-10): 37 Explosive, 38 Acid, 39 Flame, 36 Mine Rounds
constexpr RoundGun ROUND_GUNS[] = {
    // the drum is joint _02 (under _01); its six chambers _06 .. _11, _06 at the barrel at rest (read 2026-11-10)
    {4100, {37, 38, 39, 36}, "_02", 1.0f, {"_06", "_07", "_08", "_09", "_10", "_11"},
     "_01", -100.0f, "shotgun_w870", 2.0f},   // the drum swings out on _01, 100 degrees, to the gun's left (toward the loading hand)
};
} // namespace

const MagGun* mag_gun(int wp) { for (const auto& m : MAG_GUNS) if (m.wp == wp) return &m; return nullptr; }
const RoundGun* round_gun(int wp) { for (const auto& r : ROUND_GUNS) if (r.wp == wp) return &r; return nullptr; }
const SlideGun* slide_gun(int wp) { for (const auto& s : SLIDE_GUNS) if (s.wp == wp) return &s; return nullptr; }
const ShellGun* shell_gun(int wp) { for (const auto& s : SHELL_GUNS) if (s.wp == wp) return &s; return nullptr; }
bool is_pump(int wp) { return wp == 1000; }
const char* pump_sfx(int) { return "shotgun_w870"; }
bool long_mag(int wp) { return wp == 2000 || wp == 2100; }   // the CQBR: the magazine sits ahead of the grip

} // namespace vn::guns
