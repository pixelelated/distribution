"""02 § Coverage: one row per path of the 96, both tiers (#682).

    python3 -I t35-coverage.py <es worktree> <commit> <paths.txt> [rows=96 added=1 modified=12 upstream=83 inv_fork=13 inv_up=83 lines=22575]

Run from the distribution worktree (it reads docs/reviews/inventory.json there). The
read tier is `git diff --name-status bccd715707 <commit>` over the paths: A fork-added,
M fork-modified, neither upstream-carried. The inventory tier is the inventory's own
`tier` column. Lines are `grep -c ''`'s rule (an unterminated last line counts).
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-coverage.py <es worktree> <commit> <paths.txt> [key=value ...]")
inv = json.load(open("docs/reviews/inventory.json"))
cols = inv["columns"]
rows_inv = {r["path"]: r for r in (dict(zip(cols, x)) for x in inv["rows"]) if r["tree"] == "es"}
ns = subprocess.run(["git", "-C", c.W, "diff", "--name-status", "bccd715707", c.ref, "--"] + c.paths, capture_output=True, text=True, check=True).stdout
status = {l.split("\t")[1]: l.split("\t")[0] for l in ns.splitlines() if l}
num = subprocess.run(["git", "-C", c.W, "diff", "--numstat", "bccd715707", c.ref, "--"] + c.paths, capture_output=True, text=True, check=True).stdout
stat = {l.split("\t")[2]: f"+{l.split(chr(9))[0]}/-{l.split(chr(9))[1]}" for l in num.splitlines() if l}

GROUPS = [
    ("es-core/CMakeLists.txt", "the build lists"),
    ("es-core/src/Window.", "the window and its surfaces"),
    ("es-core/src/Input", "the input manager and its config"),
    ("es-core/src/GunManager", "the light guns"),
    ("es-core/src/Log", "the log"),
    ("es-core/src/Scripting", "the script runner"),
    ("es-core/src/Splash", "the splash"),
    ("es-core/src/guis/", "the es-core dialogs"),
    ("es-core/src/watchers/", "the watchers"),
    ("es-core/src/math/", "the math"),
    ("es-core/src/anim/", "the storyboards"),
    ("es-core/src/animations/", "the animations"),
    ("es-core/src/playlists/", "the playlists"),
    ("es-core/src/GuiComponent", "the component base"),
    ("es-core/src/Theme", "the theme parser"),
    ("es-core/src/Help", "the help prompts"),
    ("es-core/src/BindingManager", "the theme bindings"),
]
DEVICE = ("AudioManager", "Sound", "VolumeControl", "CECInput", "TextToSpeech", "PowerSaver", "FavoriteMusicManager")


def group(p):
    for prefix, g in GROUPS:
        if p.startswith(prefix):
            return g
    if any(p.startswith("es-core/src/" + d) for d in DEVICE):
        return "the device and audio layer"
    return "the rest"


def count_lines(t):
    return t.count("\n") + (1 if t and not t.endswith("\n") else 0)


out = []
cnt = {"rows": 0, "added": 0, "modified": 0, "upstream": 0, "inv_fork": 0, "inv_up": 0, "lines": 0}
for p in c.paths:
    t = c.text(p)
    n = count_lines(t)
    r = rows_inv.get(p)
    if r is None:
        c.fail.append(f"{p} is not in the inventory")
        continue
    if r["lines"] != n:
        c.fail.append(f"{p}: {n} lines at {c.ref}, inventory {r['lines']}")
    s = status.get(p, "")
    read = {"A": "fork-added", "M": "fork-modified"}.get(s, "upstream-carried")
    if s not in ("", "A", "M"):
        c.fail.append(f"{p}: name-status {s}")
    cnt["rows"] += 1
    cnt["lines"] += n
    cnt[{"fork-added": "added", "fork-modified": "modified", "upstream-carried": "upstream"}[read]] += 1
    cnt["inv_fork" if r["tier"] == "fork-own" else "inv_up"] += 1
    out.append([f"`{p}`", n, read, r["tier"], stat.get(p, "--"), group(p), "tree"])
print(table(["Path", "Lines", "Read tier", "Inventory tier", "Fork stat (vs `bccd715707`)", "What", "proved:"], out))
c.finish("t35-coverage", cnt, f"{cnt['rows']} rows, {cnt['lines']} lines (grep -c rule); read tiers fork-added {cnt['added']} / fork-modified {cnt['modified']} / upstream-carried {cnt['upstream']}; inventory fork-own {cnt['inv_fork']} / upstream-carried {cnt['inv_up']}")
