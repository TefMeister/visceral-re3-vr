E.lift = E.lift or {}
if not E.lift_hooked then
  re.on_application_entry("LateUpdateBehavior", function()
    local ok = pcall(function()
      if not E.lift.on then return end
      local gun = E.eq:call("get_EquipWeapon")
      local tf = gun:call("get_GameObject"):call("get_Transform")
      for name, p in pairs(E.lift.pos) do
        local j = tf:call("getJointByName", name)
        if j then j:call("set_LocalPosition", Vector3f.new(p[1], p[2], p[3])) end
      end
    end)
  end)
  E.lift_hooked = true
end
E.lift.pos = { ["_06"] = { 0.0, 0.30, -0.111 }, ["_101"] = { 0.15, 0.25, 0.10 } }
E.lift.on = true
return "lifting _06 and _101"
