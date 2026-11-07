// game.cpp -- RE3's answers to game.h (the shared per-game layer; RE2's repo owns game.h).
#include "game.h"

namespace vn::game {

const char* ns() { return "offline."; }
std::string type(const char* rest) { return std::string(ns()) + rest; }
const char* project() { return "visceral-re3-vr"; }
// The gun holds' second set, as gen-1 RE3 had it (RE2's test kept): a player whose name starts "pl1". Which RE3 character
// that is has not been read yet; Andyalpa's holds are RE2's in both sets anyway.
bool second_character(MO* player) { return read_string(call_ptr(player, "get_Name")).rfind("pl1", 0) == 0; }

} // namespace vn::game
