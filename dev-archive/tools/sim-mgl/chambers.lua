local function qrot(q, v)
  local x, y, z, w = q.x, q.y, q.z, q.w
  local tx, ty, tz = 2 * (y * v.z - z * v.y), 2 * (z * v.x - x * v.z), 2 * (x * v.y - y * v.x)
  return { x = v.x + w * tx + (y * tz - z * ty), y = v.y + w * ty + (z * tx - x * tz), z = v.z + w * tz + (x * ty - y * tx) }
end
local gun = E.eq:call("get_EquipWeapon")
local gtf = gun:call("get_GameObject"):call("get_Transform")
local gp, gq = gtf:call("get_Position"), gtf:call("get_Rotation")
local inv = { x = -gq.x, y = -gq.y, z = -gq.z, w = gq.w }
local t = {}
for _, n in ipairs({ "_06", "_07", "_08", "_09", "_10", "_11" }) do
  local p = gtf:call("getJointByName", n):call("get_Position")
  local l = qrot(inv, { x = p.x - gp.x, y = p.y - gp.y, z = p.z - gp.z })
  t[#t + 1] = string.format("%s (%.3f %.3f %.3f)", n, l.x, l.y, l.z)
end
return table.concat(t, "  ")
