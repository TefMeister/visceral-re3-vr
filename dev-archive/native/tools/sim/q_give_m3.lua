-- q_give_m3.lua (RE3, rv.py -f with RV_GAME_DIR set): put the M3 pump shotgun in Jill's hand. If the save owns it, the slot
-- holding it is equipped; if not, it is given (memory only: the game saves at typewriters; a full 16-slot inventory
-- silently refuses a gift, KNOWN.md). Ask twice: the gun object appears a frame or two after the equip. 2026-11-19.
local pl = sdk.get_managed_singleton("offline.PlayerManager"):call("get_CurrentPlayer")
if pl == nil then return "no player (not in gameplay)" end
local function gun()
    local w = pl:call("getComponent(System.Type)", sdk.typeof("offline.survivor.Equipment")):get_field("<EquipWeapon>k__BackingField")
    return w and w:call("get_GameObject"):call("get_Name") or "none"
end
if gun() == "wp1000" then E.m3_try = -1; return "the M3 is in hand" end
E.m3_try = (E.m3_try or -1) + 1
if E.m3_try <= 15 then
    pl:call("getComponent(System.Type)", sdk.typeof("offline.survivor.Inventory")):call("equipSlot(System.Int32)", E.m3_try)
    return "tried slot " .. E.m3_try .. " (was holding " .. gun() .. "): ask again"
end
local v = sdk.find_type_definition("offline.EquipmentDefine.WeaponType"):get_field("WP1000"):get_data(nil)
local ok = sdk.get_managed_singleton("offline.gamemastering.InventoryManager"):call("addAndEquipMainWeapon", v, 4, 0) ~= nil
E.m3_try = -1
return "not in any slot: M3 given: " .. tostring(ok)
