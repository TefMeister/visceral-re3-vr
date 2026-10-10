-- Visceral RE3 (2026-10-10) -- TORSO PROBE, read-only. Tefa: "torso still pushing forward" when Jill stops, also
-- with the relaxed idle (0161) playing. Twice a second this logs, in the view's own frame (forward = where the
-- camera looks, flattened), how far ahead / below the camera each spine/neck/head joint sits, plus the player's speed.
-- Walking vs standing numbers side by side name the cause. Remove after the test.

if reframework:get_game_name() ~= "re3" then return end

local TAG = "[torso_probe]"
local NS = sdk.game_namespace
local last_t, last_pos = 0, nil
local names = nil

local function safe(fn) local ok, r = pcall(fn); if ok then return r end return nil end

local function player_tf()
    local pm = sdk.get_managed_singleton(NS("PlayerManager")); if not pm then return nil end
    local p = safe(function() return pm:call("get_CurrentPlayer") end); if not p then return nil end
    return safe(function() return p:call("get_Transform") end)
end

local function joint_names(tf)
    local out = {}
    local joints = safe(function() return tf:call("get_Joints") end)
    if not joints then return out end
    local n = safe(function() return joints:call("get_Length") end) or 0
    for i = 0, n - 1 do
        local j = safe(function() return joints:call("GetValue(System.Int32)", i) end)
        local nm = j and safe(function() return j:call("get_Name") end)
        if nm then
            local l = nm:lower()
            if l:find("spine") or l:find("neck") or l:find("head") or l:find("chest") or l == "hip" or l == "cog" then
                out[#out + 1] = nm
            end
        end
    end
    return out
end

re.on_frame(function()
    local now = os.clock()
    if now - last_t < 0.5 then return end
    last_t = now
    local tf = player_tf(); if not tf then return end
    local cam = sdk.get_primary_camera(); if not cam then return end
    local ctf = safe(function() return cam:call("get_GameObject"):call("get_Transform") end); if not ctf then return end
    local cp = safe(function() return ctf:call("get_Position") end)
    local cr = safe(function() return ctf:call("get_Rotation") end)
    if not cp or not cr then return end
    -- RE Engine cameras look down -Z
    local fwd = cr * Vector3f.new(0, 0, -1)
    local fl = math.sqrt(fwd.x * fwd.x + fwd.z * fwd.z); if fl < 1e-4 then return end
    local fx, fz = fwd.x / fl, fwd.z / fl
    if not names then names = joint_names(tf); log.info(TAG .. " joints: " .. table.concat(names, ",")) end
    local pp = safe(function() return tf:call("get_Position") end)
    local speed = 0
    if pp and last_pos then
        local dx, dz = pp.x - last_pos.x, pp.z - last_pos.z
        speed = math.sqrt(dx * dx + dz * dz) / 0.5
    end
    last_pos = pp
    local parts = {}
    for _, nm in ipairs(names) do
        local j = safe(function() return tf:call("getJointByName", nm) end)
        local p = j and safe(function() return j:call("get_Position") end)
        if p then
            local dx, dy, dz = p.x - cp.x, p.y - cp.y, p.z - cp.z
            parts[#parts + 1] = string.format("%s fwd %.3f up %.3f", nm, dx * fx + dz * fz, dy)
        end
    end
    -- the root too: where the body stands relative to the view
    if pp then
        local dx, dz = pp.x - cp.x, pp.z - cp.z
        parts[#parts + 1] = string.format("root fwd %.3f", dx * fx + dz * fz)
    end
    log.info(string.format("%s speed %.2f m/s | %s", TAG, speed, table.concat(parts, " | ")))
end)
