local gun = E.eq:call("get_EquipWeapon")
local mesh = gun:call("get_Mesh")
local n = mesh:call("get_MaterialNum")
local t = { "materials " .. tostring(n) }
for i = 0, (n or 0) - 1 do
  local name = mesh:call("getMaterialName", i)
  local vn = mesh:call("getMaterialVariableNum", i)
  local vars = {}
  for v = 0, math.min((vn or 0) - 1, 40) do vars[#vars + 1] = mesh:call("getMaterialVariableName", i, v) end
  t[#t + 1] = i .. ": " .. tostring(name) .. " (" .. tostring(vn) .. " vars) " .. table.concat(vars, ",")
end
return table.concat(t, "\n")
