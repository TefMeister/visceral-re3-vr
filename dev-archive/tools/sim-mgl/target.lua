-- E.port = where the joint named E.tj sits now, in the gun's own space
local function qrot(q, v)
  local x, y, z, w = q.x, q.y, q.z, q.w
  local tx, ty, tz = 2 * (y * v.z - z * v.y), 2 * (z * v.x - x * v.z), 2 * (x * v.y - y * v.x)
  return { x = v.x + w * tx + (y * tz - z * ty), y = v.y + w * ty + (z * tx - x * tz), z = v.z + w * tz + (x * ty - y * tx) }
end
local gtf = E.eq:call("get_EquipWeapon"):call("get_GameObject"):call("get_Transform")
local gp, gq = gtf:call("get_Position"), gtf:call("get_Rotation")
local p = gtf:call("getJointByName", E.tj):call("get_Position")
E.port = qrot({ x = -gq.x, y = -gq.y, z = -gq.z, w = gq.w }, { x = p.x - gp.x, y = p.y - gp.y, z = p.z - gp.z })
return string.format("%s at (%.3f %.3f %.3f)", E.tj, E.port.x, E.port.y, E.port.z)
