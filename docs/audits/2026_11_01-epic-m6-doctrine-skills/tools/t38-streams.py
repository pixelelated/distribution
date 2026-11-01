"""t38-streams.py: T38 (#685) stage E's tables, read from the records `tools/t38-fix.sh` wrote under stage-e/, so
the fix table, the description lengths, the import-unchanged list and the outcomes are the records' and never retyped.

    python3 -I t38-streams.py fix          -- 02 § The streams' fix table: one row per lead per commit
    python3 -I t38-streams.py streams      -- per stream: its items, its commits, the checker's TOTAL at its last
    python3 -I t38-streams.py lengths      -- the description lengths before and after (Q5's unit and the line's)
    python3 -I t38-streams.py imports      -- every fix whose changed sentence is the import's, unchanged since
    python3 -I t38-streams.py outcomes     -- JSON {PL: [commits]} for tools/t38-punch.py

Refuses (exit 2) a record without its FAIL, PASS, fix or TOTAL line, or a stage-e/ that holds none."""
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent.parent / "stage-e"
NAME = re.compile(r"^(S\d)-(PL-\d\d)([b-f]?)\.txt$")


def records():
    out = []
    for p in sorted(HERE.iterdir()):
        m = NAME.match(p.name)
        if not m:
            continue
        t = p.read_text()
        def one(rx):
            r = re.search(rx, t, re.M)
            if not r:
                sys.exit(f"t38-streams: refused: {p.name} has no line matching {rx!r}")
            return r
        head = one(r"^# (PL-\d\d) \(([^)]*)\), (S\d): (.*)$")
        fix = one(r"^parent: (\S+) .*; fix: (\S+) \(tree")
        out.append({
            "file": p.name, "sid": m.group(1), "pl": m.group(2), "suffix": m.group(3),
            "leads": [x.strip() for x in head.group(2).split(",")], "subject": head.group(4),
            "parent": fix.group(1), "commit": fix.group(2),
            "fail": one(r"^FAIL at the parent \(rc=\d+\): (.*)$").group(1),
            "pass": one(r"^PASS at the fix \(rc=\d+\): (.*)$").group(1),
            "total": one(r"^TOTAL: .*$").group(0),
            "desc": re.findall(r"^Description, (.*)$", t, re.M),
            "imp": one(r"^import-unchanged: (yes|no) \((.*)\)$"),
        })
    if not out:
        sys.exit("t38-streams: refused: stage-e/ holds no item record")
    return out


_ORDER = {}


def order(c):
    """A commit's place in the lane's history since the dispatch tip, so a lead's commits sort as they landed."""
    if not _ORDER:
        log = subprocess.run(["git", "-C", str(HERE), "rev-list", "--reverse", "--abbrev=10", "--abbrev-commit", "87c2ab0fed..HEAD"],
                             capture_output=True, text=True)
        if log.returncode:
            sys.exit("t38-streams: refused: git rev-list failed")
        _ORDER.update({h: i for i, h in enumerate(log.stdout.split())})
    if c not in _ORDER:
        sys.exit(f"t38-streams: refused: {c} is not in the lane's history since 87c2ab0fed")
    return _ORDER[c]


def cell(s):
    return s.replace("|", "\\|")


def main():
    rs = records()
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "fix":
        print("| Item | Lead | The check at the parent | The check at the fix | Commit | Description |")
        print("| --- | --- | --- | --- | --- | --- |")
        for r in sorted(rs, key=lambda r: (r["pl"], order(r["commit"]))):
            d = "; ".join(x.split(":", 1)[0] + ": " + re.sub(r" characters of the scalar.*", "", x.split(": ", 1)[1]) for x in r["desc"]) or "--"
            for lead in r["leads"]:
                print(f"| {r['pl']} | {lead} | FAIL: {cell(r['fail'])} | PASS: {cell(r['pass'])} | `{r['commit']}` | {cell(d)} |")
        n = sum(len(r["leads"]) for r in rs)
        print(f"\n{n} rows: {len(rs)} commits over {len({r['pl'] for r in rs})} items and {len({l for r in rs for l in r['leads']})} leads.")
    elif cmd == "streams":
        by = {}
        for r in rs:
            by.setdefault(r["sid"], []).append(r)
        for sid in sorted(by):
            xs = sorted(by[sid], key=lambda r: order(r["commit"]))
            print(f"{sid}: {len({r['pl'] for r in xs})} items, {len(xs)} commits: " + ", ".join(f"`{r['commit']}` {r['pl']}" for r in xs))
            print(f"    the checker at {xs[-1]['commit']}: {xs[-1]['total']}")
    elif cmd == "lengths":
        print("| Item | Line | Before | After | Unit |")
        print("| --- | --- | ---: | ---: | --- |")
        for r in sorted(rs, key=lambda r: (r["pl"], order(r["commit"]))):
            for x in r["desc"]:
                where, rest = x.split(": ", 1)
                m = re.match(r"(\d+) -> (\d+) characters of the scalar \(tools/t38-tables.py q5\); (\d+) -> (\d+) bytes", rest)
                if not m:
                    sys.exit(f"t38-streams: refused: {r['file']}'s description line is not the helper's shape")
                print(f"| {r['pl']} (`{r['commit']}`) | `{where}` | {m.group(1)} | {m.group(2)} | the scalar's characters (`t38-tables.py q5`) |")
                print(f"| {r['pl']} (`{r['commit']}`) | `{where}` | {m.group(3)} | {m.group(4)} | the line's bytes (`sed -n 3p \\| wc -c`) |")
    elif cmd == "imports":
        for r in sorted(rs, key=lambda r: (r["pl"], order(r["commit"]))):
            if r["imp"].group(1) == "yes":
                print(f"{r['pl']} `{r['commit']}` {r['sid']}: {r['imp'].group(2)} -- {r['subject']}")
    elif cmd == "outcomes":
        o = {}
        for r in sorted(rs, key=lambda r: (r["pl"], order(r["commit"]))):
            o.setdefault(r["pl"], []).append(r["commit"])
        print(json.dumps(o, indent=1, sort_keys=True))
    else:
        sys.exit("t38-streams: refused: fix | streams | lengths | imports | outcomes")


main()
