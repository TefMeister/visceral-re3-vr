-- visceral_title_level.lua -- Visceral RE3: the title / main menu camera made level and raised (2026-11-01; Tefa, worn:
-- "the main menu in re3 has to be tilted so it sits right and the camera raised so i can't see through the floor").
-- Only while there is no player (title and its menus): each frame, after the game has moved its title camera, the camera's
-- tilt and roll are taken out (its heading kept) and it is lifted. The lift and an extra pitch live in
-- reframework/data/visceral_title_level.txt ("<up metres> <pitch degrees>"), re-read every 2 s, so it can be tuned live.
if reframework:get_game_name() ~= "re3" then return end
local FILE = "visceral_title_level.txt"
local up, pitch_extra, last_read, logged = 0.6, 0.0, -10, 0
local base, wrote = nil, nil   -- the game's own camera place, and what we last wrote (the game may not move it every frame)
local function read_file()
    local f = io.open("reframework/data/" .. FILE, "r")
    if not f then return end
    local a, b = f:read("*n", "*n"); f:close()
    if type(a) == "number" then up = a end
    if type(b) == "number" then pitch_extra = b end
end
local function in_title()
    local pm = sdk.get_managed_singleton("offline.PlayerManager")
    return not (pm and pm:call("get_CurrentPlayer"))
end
local function yaw_of(q)   -- the heading of a quaternion's forward (-z), radians
    local fx = -(2 * (q.x * q.z + q.w * q.y)); local fz = -(1 - 2 * (q.x * q.x + q.y * q.y))
    return math.atan(fx, fz) -- Lua 5.4 two-argument atan
end
local function level()
    if not in_title() then base, wrote = nil, nil; return end
    local cam = sdk.get_primary_camera(); if not cam then return end
    local go = cam:call("get_GameObject"); local tf = go and go:call("get_Transform"); if not tf then return end
    local q = tf:call("get_Rotation"); local p = tf:call("get_Position")
    if wrote and math.abs(p.x - wrote.x) + math.abs(p.y - wrote.y) + math.abs(p.z - wrote.z) < 1e-4 and base then
        p, q = base.p, base.q          -- still ours from last frame: work from the game's own place, not from ours
    else
        base = {p = p, q = q}          -- the game moved it: that is its own place now
    end
    if logged < 3 then
        logged = logged + 1
        log.info(string.format("[visceral_title_level] title camera at y %.2f, rotation %.3f %.3f %.3f %.3f; lifting %.2f m", p.y, q.x, q.y, q.z, q.w, up))
    end
    local yaw = yaw_of(q)
    local hy, hp = yaw / 2, math.rad(pitch_extra) / 2
    local qy = Quaternion.new(math.cos(hy), 0, math.sin(hy), 0)         -- (w, x, y, z)
    local qp = Quaternion.new(math.cos(hp), math.sin(hp), 0, 0)
    tf:call("set_Rotation", qy * qp)
    wrote = Vector3f.new(p.x, p.y + up, p.z)
    tf:call("set_Position", wrote)
end
re.on_pre_application_entry("BeginRendering", function()
    if os.clock() - last_read > 2 then last_read = os.clock(); read_file() end
    pcall(level)
end)
