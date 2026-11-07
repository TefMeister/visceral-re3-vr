// weapons.cpp -- see weapons.h. Names from RELOADED 1.0.1's data (re2_vr_reload.json / re2_vr_recoil.json);
// holster sorting is Tefa's (2026-10-05). The knife, grenades, EMF visualizer and the extra minigun numbers come
// from the RE Modding forum's ID thread (residentevilmodding.boards.net/thread/9864): its hex weapon list is the
// game's WeaponType enum value (01 handgun = WP0000, 0B shotgun = WP1000, 2E knife = WP4500 ...), which matches
// every weapon we could cross-check [inferred-static 2026-10-05]; the live log confirms each one when held.
#include "weapons.h"

#include <map>

namespace vn::weapons {

namespace {
struct Info { const char* name; Holster holster; };
const std::map<int, Info>& table() {
    // RE3 (port 2026-10-10): the WP numbers in RE3's own files (wp0000..wp6300). Names are the RE3 weapons as best known
    // [hypothesis]; the holster group follows RE2's rule by number range (0xxx/3xxx handguns and magnums, 1xxx/2xxx long
    // guns, 4xxx special, knives and grenades on the sub spot). The live log prints the game's own enum name when held.
    static const std::map<int, Info> t = {
        {0,    {"G19", Holster::HANDGUN}},
        {100,  {"G18 (burst)", Holster::HANDGUN}},
        {200,  {"G18", Holster::HANDGUN}},
        {300,  {"Samurai Edge", Holster::HANDGUN}},
        {600,  {"MUP", Holster::HANDGUN}},
        {1000, {"M3 Shotgun", Holster::LONG}},
        {2000, {"CQBR Assault Rifle", Holster::LONG}},
        {2100, {"CQBR Assault Rifle (other)", Holster::LONG}},
        {3000, {"Lightning Hawk", Holster::HANDGUN}},
        {3100, {"Magnum (other)", Holster::HANDGUN}},
        {4100, {"MGL Grenade Launcher", Holster::SPECIAL}},
        {4200, {"Special weapon 4200", Holster::SPECIAL}},
        {4400, {"Special weapon 4400", Holster::SPECIAL}},
        {4600, {"Rocket Launcher", Holster::SPECIAL}},
        {4700, {"Special weapon 4700", Holster::SPECIAL}},
        {4500, {"Combat Knife", Holster::SUB}},
        {4510, {"Combat Knife (other)", Holster::SUB}},
        {4520, {"Knife 4520", Holster::SUB}},
        {6200, {"Hand Grenade", Holster::SUB}},
        {6300, {"Flash Grenade", Holster::SUB}},
    };
    return t;
}

// WeaponType enum value -> WP number, read from the game's own enum names ("WP0000" = 1, BareHand = 0, ...)
std::map<int, int>& enum_to_wp() {
    static std::map<int, int> m;
    if (!m.empty()) return m;
    auto* td = API::get()->tdb()->find_type("offline.EquipmentDefine.WeaponType");
    if (td == nullptr) return m;
    for (auto* f : td->get_fields()) {
        if (f == nullptr || !f->is_static()) continue;
        const std::string n = f->get_name();
        if (n.size() == 6 && n[0] == 'W' && n[1] == 'P') m[f->get_data<int>(nullptr)] = std::stoi(n.substr(2));
    }
    LOGI("%s weapon types read from the game: %d", TAG, (int)m.size());
    return m;
}
} // namespace

int wp_of_enum(int v) {
    auto& m = enum_to_wp();
    auto it = m.find(v);
    return it == m.end() ? -1 : it->second;
}

int enum_of_wp(int wp) {
    for (auto& [e, w] : enum_to_wp()) if (w == wp) return e;
    return -1;
}

int current_id() {
    auto* pm = API::get()->get_managed_singleton("offline.PlayerManager");
    auto* go = call_ptr(pm, "get_CurrentPlayer");
    auto* eq = component(go, "offline.survivor.Equipment");
    if (eq == nullptr) return -1;
    return wp_of_enum(call_direct<int>(eq, "get_EquipType", -1));
}

const char* name(int wp) {
    auto it = table().find(wp);
    return it == table().end() ? "unknown" : it->second.name;
}

bool is_sub(int wp) { return holster_for(wp) == Holster::SUB; }

Holster holster_for(int wp) {
    auto it = table().find(wp);
    return it == table().end() ? Holster::NONE : it->second.holster;
}

const char* holster_name(Holster h) {
    switch (h) {
    case Holster::HANDGUN: return "right hip (handguns)";
    case Holster::LONG: return "right shoulder (long guns)";
    case Holster::SPECIAL: return "left shoulder (special weapons)";
    case Holster::SUB: return "left hip (sub weapon)";
    default: return "not sorted yet";
    }
}

} // namespace vn::weapons
