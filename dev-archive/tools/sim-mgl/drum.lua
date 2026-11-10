local gun = E.eq:call("get_EquipWeapon")
local tf = gun:call("get_GameObject"):call("get_Transform")
local js = tf:call("get_Joints")
local t = { "loaded " .. show(gun:call("getBulletNumber")) }
for i = 0, js:get_size() - 1 do
  local j = js[i]; local n = j:call("get_Name")
  if n == "_01" or n == "_02" or n == "_06" or n == "_07" or n == "_11" or n == "_101" then
    local q = j:call("get_LocalRotation"); local s = j:call("get_LocalScale"); local p = j:call("get_LocalPosition")
    t[#t+1] = string.format("%s rot(%.3f %.3f %.3f %.3f) scale %.2f pos(%.3f %.3f %.3f)", n, q.x, q.y, q.z, q.w, s.x, p.x, p.y, p.z)
  end
end
return table.concat(t, "\n")
