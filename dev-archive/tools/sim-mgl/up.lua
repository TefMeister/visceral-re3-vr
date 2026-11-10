local function qrot(q, v)
  local x, y, z, w = q.x, q.y, q.z, q.w
  local tx, ty, tz = 2 * (y * v.z - z * v.y), 2 * (z * v.x - x * v.z), 2 * (x * v.y - y * v.x)
  return { x = v.x + w * tx + (y * tz - z * ty), y = v.y + w * ty + (z * tx - x * tz), z = v.z + w * tz + (x * ty - y * tx) }
end
local gtf = E.eq:call("get_EquipWeapon"):call("get_GameObject"):call("get_Transform")
local f = qrot(gtf:call("get_Rotation"), { x = 0, y = 0, z = 1 })
return string.format("gun +Z in the world: (%.2f %.2f %.2f)", f.x, f.y, f.z)
