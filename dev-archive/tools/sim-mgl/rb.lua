local go = G("GUI_RemainingBullet")
E.rbgo = go
local comps = go:call("get_Components")
local t = {}
for i = 0, comps:get_size() - 1 do
  local c = comps[i]
  local n = c:get_type_definition():get_full_name()
  t[#t + 1] = n
  if string.find(n, "Bullet") then E.rb = c end
end
local out = "components: " .. table.concat(t, ", ")
if E.rb then
  out = out .. "\n" .. string.sub(F(E.rb), 1, 1500)
end
return out
