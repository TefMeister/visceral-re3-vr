local scene = sdk.call_native_func(sdk.get_native_singleton("via.SceneManager"), sdk.find_type_definition("via.SceneManager"), "get_CurrentScene")
local arr = scene:call("findComponents(System.Type)", sdk.typeof("via.gui.GUI"))
local t = {}
for i = 0, arr:get_size() - 1 do
  local g = arr[i]
  local name = g:call("get_GameObject"):call("get_Name")
  local l = string.lower(name)
  if string.find(l, "bullet") or string.find(l, "weapon") or string.find(l, "ammo") or string.find(l, "equip") or string.find(l, "remain") or string.find(l, "shortcut") or string.find(l, "hud") then t[#t + 1] = name end
end
return arr:get_size() .. " GUIs; matching: " .. table.concat(t, ", ")
