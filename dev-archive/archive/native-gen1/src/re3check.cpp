// re3check.cpp -- see re3check.h. Written from the 2026-10-10 reader note (engine-research: "RE2-only assumptions left
// in the RE3 port"), whose cheapest checks were exactly these two.
#include "re3check.h"
#include "common.h"
#include "inputbits.h"
#include "joints.h"
#include "weapons.h"

#include <cstring>
#include <set>
#include <string>

namespace vn::re3check {

namespace {
// the RE2 numbers in the code today (fire.cpp, reload_block.cpp, suppress.cpp, inputbits.h)
struct Expect { const char* field; uint64_t ours; };
constexpr Expect KIND[] = {{"HOLD", inputbits::HOLD}, {"SUPPORT_HOLD", inputbits::SUPPORT_HOLD},
                           {"ATTACK", inputbits::ATTACK}, {"RELOAD", inputbits::RELOAD}};
constexpr Expect PRECEDE[] = {{"ATTACK", 4}, {"RELOAD", 8}};
constexpr int START_FRAMES = 300;    // wait until the player and input system exist
constexpr int MAX_JOINT_NAMES = 64;  // per gun, one log line each block

// the enum type of parameter `index` of method `name` on the object's type (the code passes these numbers there)
API::TypeDefinition* param_type(MO* o, const char* name, uint32_t index) {
    auto* m = o ? find_method_deep(o->get_type_definition(), name) : nullptr;
    if (m == nullptr) return nullptr;
    auto params = m->get_params();
    return index < params.size() ? (API::TypeDefinition*)params[index].t : nullptr;
}

void check_enum(API::TypeDefinition* td, const char* what, const Expect* list, size_t n) {
    if (td == nullptr) { LOGW("%s re3check: %s enum type NOT FOUND (the method or its parameter is missing)", TAG, what); return; }
    const uint32_t size = td->get_underlying_type() ? td->get_underlying_type()->get_valuetype_size() : 8;
    LOGI("%s re3check: %s = %s (%u-byte values)", TAG, what, td->get_full_name().c_str(), size);
    for (size_t i = 0; i < n; ++i) {
        API::Field* f = nullptr;
        for (auto* c : td->get_fields()) if (c != nullptr && c->is_static() && std::strcmp(c->get_name(), list[i].field) == 0) { f = c; break; }
        if (f == nullptr) { LOGW("%s re3check: %s.%s NOT FOUND (ours %llu)", TAG, what, list[i].field, (unsigned long long)list[i].ours); continue; }
        uint64_t v = 0;
        std::memcpy(&v, f->get_data_raw(nullptr), size <= 8 ? size : 8);
        LOGI("%s re3check: %s.%s game %llu, ours %llu: %s", TAG, what, list[i].field, (unsigned long long)v,
             (unsigned long long)list[i].ours, v == list[i].ours ? "MATCH" : "DIFFERS -- this code would hit another action");
    }
}

void check_enums() {
    // isOn takes a plain UInt64, so the Kind enum is found by name (offline.* is RE3's namespace for RE2's app.ropeway.*)
    API::TypeDefinition* kind = nullptr;
    for (const char* n : {"offline.InputDefine.Kind", "offline.input.InputDefine.Kind", "offline.InputSystem.Kind"})
        if ((kind = API::get()->tdb()->find_type(n)) != nullptr) break;
    check_enum(kind, "InputDefine.Kind", KIND, std::size(KIND));
    auto* go = call_ptr(API::get()->get_managed_singleton("offline.PlayerManager"), "get_CurrentPlayer");
    auto* orderer = call_ptr(component(go, "offline.survivor.SurvivorCondition"), "get_ActionOrderer");
    check_enum(param_type(orderer, "setInhibitPrecede", 1), "ActionOrder.Precede (setInhibitPrecede)", PRECEDE, std::size(PRECEDE));
}

bool list_joints(int wp) {
    auto* go = call_ptr(API::get()->get_managed_singleton("offline.PlayerManager"), "get_CurrentPlayer");
    auto* gun = field_obj(component(go, "offline.survivor.Equipment"), "<EquipWeapon>k__BackingField");
    auto* tf = call_ptr(call_ptr(gun, "get_GameObject"), "get_Transform");
    auto* arr = call_ptr(tf, "get_Joints");
    const int n = call_direct<int>(arr, "get_Length", 0);
    if (n <= 0) return false;
    std::string names;
    for (int i = 0; i < n && i < MAX_JOINT_NAMES; ++i) {
        auto* j = call_ptr(arr, "GetValue(System.Int32)", {(void*)(intptr_t)i});
        auto* s = call_ptr(j, "get_Name");
        if (!names.empty()) names += ' ';
        names += s ? read_string(s) : "?";
    }
    LOGI("%s re3check: WP%04d %s has %d joints: %s", TAG, wp, weapons::name(wp), n, names.c_str());
    for (const char* want : {"_01", "_04"})
        LOGI("%s re3check: WP%04d joint %s %s", TAG, wp, want,
             joints::joint_by_name(tf, joints::widen(want).c_str()) ? "present" : "MISSING (the RE2 slide/magazine joint)");
    return true;
}
} // namespace

void frame() {
    static int frames = 0;
    static bool enums_done = false;
    static std::set<int> guns_done;
    if (++frames < START_FRAMES) return;
    if (!enums_done) { enums_done = true; check_enums(); }
    const int wp = weapons::current_id();
    if (wp < 0 || weapons::is_sub(wp) || guns_done.count(wp)) return;
    if (list_joints(wp)) guns_done.insert(wp);   // nothing read yet (gun still being drawn): try again next frame
}

} // namespace vn::re3check
