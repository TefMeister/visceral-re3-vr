-- how far the shell in the left hand is from the launcher's port, in the head's own axes (x right, y up, z back)
local function qrot(q, v)
  local x, y, z, w = q.x, q.y, q.z, q.w
  local tx, ty, tz = 2 * (y * v.z - z * v.y), 2 * (z * v.x - x * v.z), 2 * (x * v.y - y * v.x)
  return { x = v.x + w * tx + (y * tz - z * ty), y = v.y + w * ty + (z * tx - x * tz), z = v.z + w * tz + (x * ty - y * tx) }
end
local function qinv(q) return { x = -q.x, y = -q.y, z = -q.z, w = q.w } end
local p = S("offline.PlayerManager"):call("get_CurrentPlayer")
local ptf = p:call("get_Transform")
local lw = ptf:call("getJointByName", "l_arm_wrist")
local gun = E.eq:call("get_EquipWeapon")
local gtf = gun:call("get_GameObject"):call("get_Transform")
local gp, gq = gtf:call("get_Position"), gtf:call("get_Rotation")
local PORT = E.port or { x = 0.000, y = 0.051, z = 0.261 }
local HOLD = { x = 0.108, y = -0.042, z = 0.032 }
local r = qrot(gq, PORT)
local port = { x = gp.x + r.x, y = gp.y + r.y, z = gp.z + r.z }
local wp, wq = lw:call("get_Position"), lw:call("get_Rotation")
local h = qrot(wq, HOLD)
local shell = { x = wp.x + h.x, y = wp.y + h.y, z = wp.z + h.z }
local cam = sdk.get_primary_camera()
local cq = cam:call("get_GameObject"):call("get_Transform"):call("get_Rotation")
local e = qrot(qinv(cq), { x = port.x - shell.x, y = port.y - shell.y, z = port.z - shell.z })
local d = math.sqrt(e.x * e.x + e.y * e.y + e.z * e.z)
return string.format("%.4f %.4f %.4f %.4f", e.x, e.y, e.z, d)
