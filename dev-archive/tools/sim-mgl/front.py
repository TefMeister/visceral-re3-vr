"""front.py <exe>: bring that program's main game window to the front (never by title alone)"""
import ctypes, os, sys, time
u = ctypes.windll.user32; k = ctypes.windll.kernel32
def exe(h):
    pid = ctypes.c_ulong(0); u.GetWindowThreadProcessId(ctypes.c_void_p(h), ctypes.byref(pid))
    hp = k.OpenProcess(0x1000, False, pid.value)
    if not hp: return ""
    b = ctypes.create_unicode_buffer(520); n = ctypes.c_ulong(520)
    k.QueryFullProcessImageNameW(ctypes.c_void_p(hp), 0, b, ctypes.byref(n)); k.CloseHandle(ctypes.c_void_p(hp))
    return os.path.basename(b.value).lower()
want = sys.argv[1].lower(); found = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(h, _):
    if u.IsWindowVisible(h) and exe(h) == want:
        t = ctypes.create_unicode_buffer(200); u.GetWindowTextW(h, t, 200)
        if "Simulator" not in t.value and t.value: found.append((h, t.value))
    return True
u.EnumWindows(cb, 0)
if not found: sys.exit("no window of " + want)
h = found[0][0]
u.keybd_event(0x12, 0, 0, 0); u.SetForegroundWindow(ctypes.c_void_p(h)); u.keybd_event(0x12, 0, 2, 0)
time.sleep(0.8); print("front:", found[0][1], u.GetForegroundWindow() == h)
