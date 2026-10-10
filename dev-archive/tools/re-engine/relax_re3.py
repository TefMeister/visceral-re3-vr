"""relax_re3.py -- Visceral RE2's first two golden steps, made for RE3 (2026-10-10).

  RE2 2026-10-04 "Leon pose fix" + 2026-10-05 "all weapons relaxed, every character":
    every weapon moves and aims with the no-weapon (KFF_) body pose: straight body, no hunch, normal aim-walk speed.
  RE2 lookat: every Hold* look-at profile replaced by a copy of Default (the RE2 golden files are byte-identical
    copies of RE2's Default.user.2, checked 2026-10-10), so the spine does not bend toward the aim.

RE3 differences, measured 2026-10-10:
  - lists live in natives/stm/escape/character/player/<plNNNN>/animation/list/<wp>/  (RE2: sectionroot/animation/player/<plNN>/list)
  - characters: pl2000 Jill, pl0000 Carlos; motion names are plNNNN_..., so the prefix is six characters
  - slot numbers and the KFF_/OFF_ naming are the same as RE2 (0x6e..0x99 walk/raise slots, 0x0a0 idle)
  - RE3 also has <wp>_move_* override lists; they get the same treatment as <wp>_hold_* overrides (walk slots emptied)
  - look-at profiles are shared: natives/stm/escape/userdata/character/survivor/common/lookat/

The motlist code (motlist_splice.py, motlist_relax.py, pak_pull.py) is copied unchanged from visceral-re2-vr
dev-archive/tools/re-engine at 1c96419.

  py relax_re3.py --game-dir "<RE3>" --names <RE3 file-name list> --out <folder> [--character pl2000 pl0000]
The file-name list is Ekey's public REE.PAK.Tool Projects/RE3_RT_STM_Release.list (names only, no game data).
Legitimacy: reads the player's own paks, writes only into --out; no game data in this file.
"""
import argparse, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motlist_splice as ms
import motlist_relax as mr
import glob, struct
import mmh3

ROOT = "natives/stm/escape/character/player/%s/animation/list/"
LOOKAT = "natives/stm/escape/userdata/character/survivor/common/lookat/"
HOLD_LOOKAT = ["hold", "hold_gg", "hold_hacktool", "hold_hg", "hold_hg_hp", "hold_rl", "hold_sg", "hold_smg",
               "hold_wp0800", "holdgrenade", "holdknife"]


def prefix_of(m):
    """RE3 motion names start plNNNN_ (six characters); the most common one in base_cmn_move is the character's."""
    count = {}
    for n in m.entry_name.values():
        g = n and re.match(r"(pl\d{4})_", n)
        if g:
            count[g.group(1)] = count.get(g.group(1), 0) + 1
    if not count:
        raise SystemExit("no plNNNN_ motion names in %s" % m.path)
    return max(count, key=count.get)


mr.prefix_of = prefix_of


def h32(s):
    return mmh3.hash(s.encode("utf-16-le"), 0xFFFFFFFF, signed=False)


def in_archive(game, names):
    """Keep the names whose hash pair is in the game's paks (pak_pull.py runs on import, so it is not imported)."""
    keys = set()
    for p in glob.glob(os.path.join(game, "re_chunk_000.pak*")):
        if os.path.getsize(p) < 16:
            continue
        with open(p, "rb") as f:
            total = struct.unpack("<IBBHII", f.read(16))[4]
            raw = f.read(total * 48)
        for i in range(total):
            keys.add(struct.unpack_from("<II", raw, i * 48))
    return [n for n in names if (h32(n.lower()), h32(n.upper())) in keys]


def classify(path, wp):
    name = path.rsplit("/", 1)[1].split(".")[0]
    if name == "base_%s_hold" % wp:
        return "base-hold"
    if name == "base_%s_move" % wp:
        return "base-move"
    if name.startswith(("%s_hold_" % wp, "%s_move_" % wp)):
        return "override"
    return None


def pull(game, work, paths):
    r = subprocess.run([sys.executable, os.path.join(HERE, "pak_pull.py"), game, work] + paths, capture_output=True, text=True)
    if r.returncode or "MISS" in r.stdout:
        raise SystemExit("pull failed:\n" + r.stdout + r.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game-dir", required=True)
    ap.add_argument("--names", required=True)
    ap.add_argument("--character", nargs="+", default=["pl2000", "pl0000"])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    work = os.path.join(a.out, "_originals")
    names = [l.strip() for l in open(a.names, encoding="utf-8", errors="replace") if l.strip()]
    local = lambda p: os.path.join(work, p.replace("/", os.sep))
    quiet = lambda *x: None

    for pl in a.character:
        root = ROOT % pl
        cands = [n for n in names if n.lower().startswith(root) and n.endswith(".motlist.524") and n.count("/") == root.count("/") + 1]
        cands = in_archive(a.game_dir, cands)
        cmn = root + "cmn/base_cmn_move.motlist.524"
        lists = []
        for p in cands:
            wp = p[len(root):].split("/")[0]
            if wp in ("cmn", "fce", "face", "actor"):
                continue
            mode = classify(p, wp)
            if mode:
                lists.append((mode, p))
        pull(a.game_dir, work, [cmn] + [p for _, p in lists])
        cm = ms.Motlist(local(cmn))
        done, skipped = [], []
        for mode, p in lists:
            src, dst = local(p), os.path.join(a.out, p.replace("/", os.sep))
            name = p.rsplit("/", 1)[1].replace(".motlist.524", "")
            if mode == "override":
                out, changed = mr.override(open(src, "rb").read(), quiet)
            else:
                lst = ms.Motlist(src)
                if lst.num == 0 or not any(lst.slots):
                    skipped.append(name); continue
                out, changed = (mr.base_hold if mode == "base-hold" else mr.base_move)(lst, cm, quiet)
                if not ms.verify(out, lst, cm, changed, quiet):
                    raise SystemExit("VERIFY FAIL on " + name)
            if not changed:
                skipped.append(name); continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "wb").write(out)
            done.append("%-36s %2d slots" % (name, len(changed)))
        print("%s: %d lists found, %d written, %d need nothing (%s)" % (pl, len(lists), len(done), len(skipped), " ".join(skipped)))
        for d in done:
            print("  wrote", d)

    # look-at: every Hold profile becomes a copy of Default
    paths = [LOOKAT + "default.user.2"] + [LOOKAT + f + ".user.2" for f in HOLD_LOOKAT]
    pull(a.game_dir, work, paths)
    default = open(local(paths[0]), "rb").read()
    for f in HOLD_LOOKAT:
        dst = os.path.join(a.out, (LOOKAT + f + ".user.2").replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(default)
    print("lookat: %d Hold profiles = Default (%d bytes)" % (len(HOLD_LOOKAT), len(default)))


if __name__ == "__main__":
    main()
