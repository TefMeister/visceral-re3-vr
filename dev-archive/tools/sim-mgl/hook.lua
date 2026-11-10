if not E.hooked then
  E.shots = {}
  local td = T("offline.weapon.generator.ShellGeneratorBase")
  local m = td:get_method("generateShell")
  sdk.hook(m, function(args)
    local kind = sdk.to_int64(args[3]) & 0xFFFFFFFF
    local ud = sdk.to_managed_object(args[5])
    local name = "?"
    pcall(function() name = ud:get_type_definition():get_full_name() end)
    local bt = "?"
    pcall(function() bt = tostring(E.eq:call("get_BulletType")) end)
    E.shots[#E.shots + 1] = "kind " .. tostring(kind) .. " userdata " .. name .. " gunType " .. bt
  end, function(r) return r end)
  E.hooked = true
end
return "hooked, shots so far " .. #E.shots
