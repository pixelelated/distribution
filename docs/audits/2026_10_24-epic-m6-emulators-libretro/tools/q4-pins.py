#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""q4-pins.py -- the libretro recipes' pins against ROCKNIX and against their
projects (M6 T3, #650; brief section 4 Q4 (a) and (b)).

    python3 -I q4-pins.py <tree> <read-hash> <upstream-ref> <out.json> <out.md> [cache.json]

For each of the 151 package.mk under projects/ROCKNIX/packages/emulators/
libretro/ (the two globs of brief section 5), at <read-hash> and at
<upstream-ref>: PKG_VERSION, PKG_SITE, PKG_URL. For a github.com recipe, three
GitHub API calls through `gh api` (no clone, no download): the pin's commit
date (commits/<pin>), the repository's default branch (repos/<o>/<r>) and that
branch's head date (commits/<branch>), and whether the pin is on the branch
(compare/<pin>...<branch>: `ahead` or `identical` means it is; `diverged` or a
404 means it is not). The three non-GitHub recipes are classed by hand in the
table that reads this output; they get `class: by-hand` here, never an empty
cell.

One class per row, in this order of precedence:
  repo-missing        the repository answers 404
  pin-not-on-project  the pin's commit is absent, or not on the default branch
  behind-upstream     upstream-ref pins another version (actionable: to merge)
  current             the pin is the default branch's head
  behind-project      the default branch is ahead of the pin (informational
                      for an upstream-carried recipe; ROCKNIX's to take)
and a separate column `upstream` reading `same` or `differs` (the brief's
`upstream-same`, beside either class). The script asserts every row has a
class and every GitHub row a pin date before it writes, and exits 1 when one
does not (an empty cell is the scan's own FAIL, blindspot 39). A rate limit
or an API error is recorded in the row's `error`, never skipped.
"""
import json, os, re, subprocess, sys, datetime

tree, read_hash, up_ref, out_json, out_md = sys.argv[1:6]
cache_path = sys.argv[6] if len(sys.argv) > 6 else None
cache = json.load(open(cache_path)) if cache_path and os.path.exists(cache_path) else {}
env = dict(os.environ, GH_PAGER="")

def git(*a):
    return subprocess.run(["git", "-C", tree, *a], capture_output=True, text=True)

def api(path):
    if path in cache:
        return cache[path]
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, env=env)
    if r.returncode == 0:
        v = {"ok": True, "data": json.loads(r.stdout)}
    else:
        msg = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
        v = {"ok": False, "error": msg[0][:200], "notfound": "404" in (r.stderr + r.stdout)}
    cache[path] = v
    return v

def fields(text):
    g = lambda k: (re.search(rf'^{k}="([^"]*)"', text, re.M) or [None, None])[1]
    return g("PKG_VERSION"), g("PKG_SITE"), g("PKG_URL")

files = git("ls-tree", "-r", "--name-only", read_hash, "--", "projects/ROCKNIX/packages/emulators/libretro").stdout.split()
files = [f for f in files if re.fullmatch(r"projects/ROCKNIX/packages/emulators/libretro/[^/]+(/[^/]+)?/package\.mk", f)]
rows = []
for f in files:
    name = f.split("/")[-2]
    v, site, url = fields(git("show", f"{read_hash}:{f}").stdout)
    ut = git("show", f"{up_ref}:{f}")
    uv = fields(ut.stdout)[0] if ut.returncode == 0 else None
    row = {"recipe": name, "path": f, "pin": v, "site": site, "url": url,
           "upstream_pin": uv if ut.returncode == 0 else "(absent upstream)",
           "upstream": "same" if (ut.returncode == 0 and uv == v) else "differs"}
    s = " ".join(x for x in (site, (url or "").replace("${PKG_SITE}", site or "")) if x)
    m = re.search(r"https?://github\.com/([^/\s]+)/([^/\s]+?)(?:\.git)?(?:/|\s|$)", s)
    if not m:
        row["class"] = "by-hand"; row["host"] = (re.search(r"https?://([^/]+)/", s) or [None, "?"])[1]
        rows.append(row); continue
    o, r = m.group(1), m.group(2); row["repo"] = f"{o}/{r}"; row["host"] = "github.com"
    repo = api(f"repos/{o}/{r}")
    if not repo["ok"]:
        row["class"] = "repo-missing" if repo.get("notfound") else "error"; row["error"] = repo.get("error")
        rows.append(row); continue
    branch = repo["data"]["default_branch"]; row["branch"] = branch
    row["repo_moved_to"] = repo["data"]["full_name"] if repo["data"]["full_name"].lower() != f"{o}/{r}".lower() else ""
    row["archived"] = repo["data"].get("archived", False)
    head = api(f"repos/{o}/{r}/commits/{branch}")
    if head["ok"]:
        row["head"] = head["data"]["sha"]; row["head_date"] = head["data"]["commit"]["committer"]["date"]
    else:
        row["error"] = head.get("error")
    ref = v
    if v and v.startswith("$("):
        row["class"] = "by-hand"; row["note"] = "PKG_VERSION is another recipe's"; rows.append(row); continue
    pin = api(f"repos/{o}/{r}/commits/{ref}") if ref else {"ok": False, "notfound": True, "error": "no PKG_VERSION"}
    if not pin["ok"]:
        row["class"] = "pin-not-on-project"; row["error"] = pin.get("error"); rows.append(row); continue
    row["pin_sha"] = pin["data"]["sha"]; row["pin_date"] = pin["data"]["commit"]["committer"]["date"]
    cmp = api(f"repos/{o}/{r}/compare/{row['pin_sha']}...{branch}")
    status = cmp["data"]["status"] if cmp["ok"] else "error"
    if not cmp["ok"]:
        row["error"] = cmp.get("error")
        # GitHub's answer when the pin shares no history with the branch
        # (a rewritten history, or a pin from another line of work).
        if "No common ancestor" in (cmp.get("error") or ""):
            status = "no-common-ancestor"
    row["compare"] = status; row["ahead_by"] = cmp["data"].get("ahead_by") if cmp["ok"] else None
    if "head_date" in row:
        d = lambda x: datetime.datetime.fromisoformat(x.replace("Z", "+00:00"))
        row["days"] = (d(row["head_date"]) - d(row["pin_date"])).days
    if status in ("diverged", "error", "behind", "no-common-ancestor"):
        row["class"] = "pin-not-on-project" if status != "error" else "error"
    elif row["upstream"] == "differs":
        row["class"] = "behind-upstream"
    elif status == "identical":
        row["class"] = "current"
    else:
        row["class"] = "behind-project"
    rows.append(row)

# A recipe whose PKG_VERSION is $(get_pkg_version <other>) builds <other>'s
# pin from the same repository, so it takes that row's dates and class.
byname = {r["recipe"]: r for r in rows}
for r in rows:
    m = re.fullmatch(r"\$\(get_pkg_version ([^)]+)\)", r["pin"] or "")
    if m and m.group(1) in byname:
        src = byname[m.group(1)]
        for k in ("pin_sha", "pin_date", "head", "head_date", "days", "compare", "class"):
            if k in src: r[k] = src[k]
        r["note"] = f"PKG_VERSION is {m.group(1)}'s"
if cache_path:
    json.dump(cache, open(cache_path, "w"))
bad = [r["recipe"] for r in rows if not r.get("class") or r["class"] == "error" or (r.get("host") == "github.com" and r["class"] not in ("repo-missing", "pin-not-on-project", "by-hand") and not r.get("pin_date"))]
json.dump({"read_hash": read_hash, "upstream_ref": up_ref, "run": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "rows": rows}, open(out_json, "w"), indent=1)
with open(out_md, "w") as fh:
    fh.write("| Recipe | Pin | Pin date | Project head date | Days | Class | Upstream | Upstream pin (if it differs) |\n| --- | --- | --- | --- | ---: | --- | --- | --- |\n")
    for r in sorted(rows, key=lambda r: r["recipe"]):
        up = "" if r["upstream"] == "same" else f"`{(r['upstream_pin'] or '')[:12]}`"
        fh.write(f"| `{r['recipe']}` | `{(r['pin'] or '')[:12]}` | {(r.get('pin_date') or '-')[:10]} | {(r.get('head_date') or '-')[:10]} | {r.get('days', '-')} | {r['class']} | {r['upstream']} | {up} |\n")
print(f"q4-pins: {len(rows)} rows; classes " + json.dumps(dict(sorted(__import__('collections').Counter(r['class'] for r in rows).items()))) + f"; empty or errored: {bad}")
sys.exit(1 if bad or len(rows) != 151 else 0)
