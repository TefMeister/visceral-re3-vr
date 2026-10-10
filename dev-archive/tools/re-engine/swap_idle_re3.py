"""Visceral RE3 (2026-10-10): give the standing-still slots a different idle motion.

Why: Tefa, port build worn 2026-10-10 ~20:00: "torso still pushes out and stays out until i start walking". The log
shows every stop lands on slot 0xa0 = pl2000_0160_KFF_Gazing_Idle_F_Loop, with or without a weapon. Jill's no-weapon
list also carries 0161_KFF_Gazing_Idle_F_Relax_Loop (slot 0xa1). This writes that motion (or any --idle) into the
full-length idle slots (0xa0, 0xa6) of the given lists, and of cmn/base_cmn_move itself. The short raise slots
(0x8c..0x99, trimmed copies of 0160) are left alone.

  python swap_idle_re3.py --cmn <original cmn/base_cmn_move> --idle 0161_KFF_Gazing_Idle_F_Relax_Loop \
      --out <natives root> LIST [LIST ...]

Each LIST is rewritten in place under --out at its own natives path (the part after 'natives/').
"""
import argparse, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motlist_splice as ms
import motlist_relax as mr

IDLE_SLOTS = (0x0a0, 0x0a6)


def swap(lst_path, cmn, idle, log):
    lst = ms.Motlist(lst_path)
    pre = mr.prefix_of(cmn)
    hit = [i for i, o in enumerate(lst.slots)
           if o and lst.slot_number(i) in IDLE_SLOTS and "Gazing_Idle_F_Loop" in lst.entry_name[o]]   # not cmn 0xa6 dummy_loop
    if not hit:
        return None
    d = bytearray(lst.data)
    for i in hit:
        struct.pack_into("<Q", d, lst.ptrs + 8 * i, 0)
    tmp = lst_path + ".idle.tmp"
    open(tmp, "wb").write(d)
    try:
        cp = ms.Motlist(tmp)
        fill = {cp.slot_number(i): idle for i in hit}
        out, rep = ms.build(cp, cmn, {}, pre, log, fill=fill)
        if not ms.verify(out, cp, cmn, rep, log):
            raise SystemExit(2)
    finally:
        os.unlink(tmp)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cmn", required=True, help="the ORIGINAL cmn/base_cmn_move.motlist.524 of the character")
    ap.add_argument("--idle", default="0161_KFF_Gazing_Idle_F_Relax_Loop")
    ap.add_argument("--out", required=True, help="folder that holds natives/ (usually the game folder)")
    ap.add_argument("lists", nargs="+")
    a = ap.parse_args()
    mr.prefix_of = lambda m: max({n[:6] for n in m.entry_name.values() if n and n.startswith("pl")},
                                 key=lambda p: sum(1 for n in m.entry_name.values() if n and n.startswith(p + "_")))
    cmn = ms.Motlist(a.cmn)
    quiet = lambda s: None
    for p in a.lists + [a.cmn]:
        out = swap(p, cmn, a.idle, quiet)
        rel = p.replace("\\", "/").split("natives/", 1)[1]
        if out is None:
            print("no idle slot: %s" % rel)
            continue
        dst = os.path.join(a.out, "natives", rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(out)
        print("idle -> %s: %s" % (a.idle, rel))


if __name__ == "__main__":
    main()
