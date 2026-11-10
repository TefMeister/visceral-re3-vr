local im = S("offline.gamemastering.InventoryManager"); E.im = im
local p = S("offline.PlayerManager"):call("get_CurrentPlayer")
E.eq = C(p, "offline.survivor.Equipment")
local inv = im:call("get_CurrentInventory") or im:get_field("<CurrentInventory>k__BackingField"); E.inv = inv
for _, i in ipairs({13, 12, 10, 9, 7, 5, 3, 2}) do inv:call("removeSlot(System.Int32)", i) end
im:call("addAndEquipMainWeapon", 42, 6, 37)
for _, id in ipairs({37, 38, 39, 36}) do im:call("addItemCount", id, 6) end
return "set up"
