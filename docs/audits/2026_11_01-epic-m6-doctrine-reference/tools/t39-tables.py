"""t39-tables.py: T39 (#686) stage C's table generator (brief § 6, the Tools row).

    python3 -I t39-tables.py <table> --export <dir> --repo <worktree> --commit <ref> --probes <dir>
                             [--allow <dir>] [--issues <tsv>] [--fixed-at <ref>]

<table> is one of coverage, binaries, art, q4, q5, q6. The Markdown goes to stdout; `ok` / `FAIL` lines and a
last `COUNTS ...` line go to stderr. Exit 1 when an assertion fails, so a missing row fails here rather than
printing an empty cell (T40's generator), 2 on a usage error.

--probes is t39-checks.sh's --out from the baseline run (probes.tsv and read-<step>.tsv: one definition of each
probe, the checker's). Every table first checks that each file it reads in --export is byte-identical to its
blob at --commit, so the tables are about the tree the checker read; a drifted export fails here.
--issues is a snapshot of `gh api repos/pixelelated/distribution/issues?state=all --paginate` as
number<TAB>state<TAB>kind<TAB>title, its read time in stage-c/. --fixed-at fills the binaries' and the art bytes'
second sha256 column (stage E)."""
import argparse, collections, hashlib, json, pathlib, posixpath, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("table", choices=("coverage", "binaries", "art", "q4", "q5", "q6"))
ap.add_argument("--export", required=True)
ap.add_argument("--repo", required=True)
ap.add_argument("--commit", required=True)
ap.add_argument("--probes", required=True)
ap.add_argument("--allow")
ap.add_argument("--issues")
ap.add_argument("--fixed-at")
a = ap.parse_args()
E, R, C = pathlib.Path(a.export), a.repo, a.commit
fails = []


def ok(msg):
    print(f"ok    {msg}", file=sys.stderr)


def bad(msg):
    fails.append(msg)
    print(f"FAIL  {msg}", file=sys.stderr)


def git(*args):
    r = subprocess.run(["git", "-C", R, *args], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def blob(ref, p):
    return git("show", f"{ref}:{p}")


def sha(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None


def tsv(name):
    f = pathlib.Path(a.probes) / name
    if not f.is_file():
        bad(f"{f} is missing (run t39-checks.sh with --out {a.probes} first)")
        return []
    rows = f.read_text().rstrip("\n").split("\n")
    head = rows[0].split("\t")
    return [dict(zip(head, r.split("\t"))) for r in rows[1:] if r]


PROBES = tsv("probes.tsv")
PATHS = [r["path"] for r in PROBES]
CLASS = {r["path"]: r["class"] for r in PROBES}
TEXT = [r["path"] for r in PROBES if r["kind"] == "text"]
inv = json.loads(git("show", f"{C}:docs/reviews/inventory.json"))
ix = {k: i for i, k in enumerate(inv["columns"])}
INV = {r[ix["path"]]: {k: r[ix[k]] for k in ("tier", "lines", "language")} for r in inv["rows"] if r[ix["tree"]] == "distribution"}
EDIT = [p for p in PATHS if CLASS[p] in ("edit-scope", "edit-under-naming")]


def same_as_commit(paths):
    """Each file in --export is its blob at --commit: the tables describe the tree the checker read."""
    n = 0
    for p in paths:
        f = E / p
        if not f.is_file():
            bad(f"{p} is absent from --export")
            continue
        if sha(f.read_bytes()) != sha(blob(C, p)):
            bad(f"{p} in --export differs from its blob at {C}")
            continue
        n += 1
    return n


def grp(p):
    q = p.split("/")
    if len(q) == 1:
        return p
    if q[0] == "docs":
        if len(q) == 2:
            return "docs/*"
        if q[1] == "reviews" and len(q) > 3:
            return "docs/reviews/" + q[2] + "/"
        return "docs/" + q[1] + "/"
    return q[0] + "/"


# The leads of brief § 3 on paths of the 254, with their Coverage disposition and questions (02 § The table).
LEADS = {
    "L-01": (["docs/reviews/README.md", "docs/reviews/plan-for-the-plan.md", "docs/reviews/briefs/p1-survey.md", "docs/reviews/build-path-read.md"], "ledger", "Q6"),
    "L-02": (["README.md"], "fix", "Q4 Q7"),
    "L-03": (["docs/device-testing-policy.md"], "fix", "Q4"),
    "L-04": (["docs/rasteratops/cloud-layout.md", "docs/releases/pr/08-saves.md"], "fix", "Q1 Q3"),
    "L-05": (["docs/device-flashing-runbook.md"], "fix", "Q2 Q4"),
    "L-06": (["docs/cloud-save-integrity.md"], "fix", "Q4"),
    "L-07": (["docs/backup-contents.md"], "fix", "Q2 Q4"),
    "L-08": (["docs/es-menu-map.md"], "fix", "Q4 Q7"),
    "L-09": (["docs/releases/next-candidate-work.md"], "fix", "Q4"),
    "L-10": (["docs/pixelelated/cloud-folders.md"], "fix", "Q7"),
    "L-11": (["docs/rasteratops/release-readiness.md", "docs/releases/next-candidate-work.md", "docs/releases/next-candidate-scope.md",
              "docs/es-menu-map.md", "docs/pixelelated/cloud-folder-flow-review.md", "docs/rasteratops/support-matrix.md",
              "docs/releases/device-facts.md", "docs/releases/versioning.md", "docs/releases/0.0.1-release-preparation.md"], "fix", "Q7"),
    "L-11u": (["docs/upstream/README.md"], "#585", "Q7"),
    "L-12": (["docs/council-mistral-counter.md"], "fix", "Q5 Q6"),
    "L-13": (["docs/technical-appendix-cloud-sync-and-offline-achievements.md", "docs/pixelelated/site-plan.md",
              "docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md", "docs/ra-offline/rocknix-org-offline-achievements.md"], "fix", "Q6"),
    "L-14": (["docs/pixelelated/art/README.md"], "none", "Q6"),
    "L-15": (["docs/releases/device-facts.md"], "fix", "Q4 Q6"),
    "L-16": (["docs/device-testing-policy.md"], "fix", "Q3"),
    "L-17": (["docs/conflict-wizard-ia.md"], "inherited:the interface lanes", "Q4"),
    "L-19": (["docs/rasteratops/art/README.md"], "ledger", "Q6"),
    "L-20": (["docs/rasteratops/p0-read.md", "docs/rasteratops/p0-sweep.md"], "ledger", "Q6"),
    "L-21": (["docs/rasteratops/raofflineproxy-refresh.md", "docs/rasteratops/cloud-folder-state-table.md"], "ledger", "Q2"),
    "L-22": (["docs/pixelelated/site-plan.md"], "fix", "Q4"),
    "L-23": (["docs/cloud-sync-changelog.md"], "ledger", "Q2"),
    "L-24": (["plans/conflict-resolution/vita-style-conflict-resolution.md"], "ledger", "Q1 Q5"),
    "L-25": (["docs/releases/rc-accept.txt"], "inherited:coordinator", "Q2"),
    "L-26": (["docs/releases/rc-accept.txt"], "ledger", "Q4"),
    "L-27": (["docs/pr-series/map.txt"], "inherited:coordinator", "Q6"),
    "L-28": (["docs/reviews/plan-for-the-plan.md"], "inherited:coordinator", "Q4"),
    "L-29": (["docs/reviews/order.md"], "inherited:coordinator", "Q7"),
    "L-30": (["docs/rasteratops/release-readiness.md", "docs/rasteratops/support-matrix.md"], "inherited:#509", "Q2 Q7"),
    "L-31": (["documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md"], "inherited:coordinator", "Q5 Q6"),
    "L-32": (["docs/es-menu-map.md"], "inherited:the interface lanes", "Q4"),
    "L-36": (["docs/device-testing-policy.md"], "inherited:coordinator", "Q7"),
    "L-39": (["docs/releases/versioning.md"], "inherited:#1013", "Q4"),
    "L-42": (["LICENSE.md"], "inherited:coordinator", "Q4"),
    "L-43": (["TRADEMARK.md", "LICENSE.md"], "#528", "Q2"),
    "L-44": (["licenses/AETHERSX2.pdf"], "#528", "Q1"),
    "L-45": (["LICENSE.md", "TRADEMARK.md"], "#528", "Q4"),
    "L-46": (["docs/upstream/README.md", "docs/upstream/raofflineproxy/pixelelated-identity/README.md",
              "docs/upstream/raofflineproxy/image-completeness/fix.patch"], "#585", "Q4"),
}
RANK = ["fix", "inherited", "#528", "#585", "ledger", "none"]


def rank(d):
    return RANK.index(d.split(":")[0])


def inbound():
    """R/O/D/W inbound names (brief § 4 Q5, R2 C21's columns): files in .claude/, the root documents, the 254's
    text rows outside the ledgers, and the October work logs whose text names the document's path (or, from the
    254, a relative Markdown link that resolves to it)."""
    ls = (git("ls-tree", "-r", "--name-only", C) or b"").decode().split("\n")
    pops = {"R": [p for p in ls if p.startswith(".claude/")],
            "O": [p for p in ls if "/" not in p and p.endswith(".md")],
            "W": [p for p in ls if p.startswith("docs/work-logs/2026_10-work_logs/")],
            "D": [p for p in TEXT if not CLASS[p].startswith("ledger")]}
    text = {}
    for k, ps in pops.items():
        for p in ps:
            if p not in text:
                b = (E / p).read_bytes() if k == "D" else blob(C, p)
                text[p] = (b or b"").decode(errors="replace")
    links = collections.defaultdict(set)
    for p in pops["D"]:
        for t in re.findall(r"\]\(\s*<?([^)\s>#?]+)", text[p]):
            if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", t):
                links[p].add(posixpath.normpath(posixpath.join(posixpath.dirname(p), t)))
    def named(doc, t):
        """The path, or the file name where it is distinctive (R2 C21 named documents by their file names)."""
        base = posixpath.basename(doc)
        d = posixpath.dirname(doc)
        return (doc in t or (base not in GENERIC and re.search(r"(?<![\w.-])" + re.escape(base) + r"(?![\w-])", t) is not None)
                or (d.count("/") >= 2 and re.search(re.escape(d) + r"/?(?![\w.-])", t) is not None))

    names = collections.Counter(posixpath.basename(p) for p in TEXT)
    GENERIC = {b for b, c in names.items() if c > 1} | {"README.md", "LICENSE.md", "SUPPORTED_EMULATORS_AND_CORES.md"}
    out = {}
    for doc in TEXT:
        row = {}
        for k, ps in pops.items():
            row[k] = sum(1 for p in ps if p != doc and (named(doc, text[p]) or (k == "D" and doc in links[p])))
        out[doc] = row
    return out


def low_set(inb):
    """R2 C26's rule: no inbound name from .claude/, the root documents or the October work logs, at most one from
    docs/ outside the ledgers. The population is the reference documents proper and the plan (L-18's list names
    it): #585's drafts and the art bytes are not documents a reader is sent to."""
    pop = [p for p in TEXT if p in EDIT or CLASS[p] == "ledger-plan"]
    low = [p for p in pop if inb[p]["R"] == 0 and inb[p]["O"] == 0 and inb[p]["W"] == 0 and inb[p]["D"] <= 1]
    return pop, low


MONTH = r"(January|February|March|April|May|June|July|August|September|October|November|December)"


def dated(p):
    """A record that says its date: in its file name, or in its first three lines."""
    if re.search(r"20\d\d[-_]?\d\d[-_]?\d\d", posixpath.basename(p)):
        return True
    head = "\n".join((E / p).read_text(errors="replace").split("\n")[:3])
    return re.search(r"20\d\d-\d\d-\d\d|" + MONTH + r" \d{1,2},? 20\d\d|\d{1,2} " + MONTH + r" 20\d\d|" + MONTH + r" 20\d\d", head) is not None


def dispositions(low):
    by = collections.defaultdict(list)
    for lead, (ps, d, q) in LEADS.items():
        for p in ps:
            if p in CLASS:
                by[p].append((lead.rstrip("u"), d, q))
    for p in low:
        if p not in EDIT:
            by[p].append(("L-18", "ledger", "Q5 Q7"))
        elif not dated(p):
            by[p].append(("L-18", "fix", "Q5 Q7"))
        else:
            by[p].append(("L-18", "none", "Q5"))
    up = {}
    for p in PATHS:
        if p.startswith("documentation/") and INV[p]["tier"] == "upstream-carried":
            up[p] = git("rev-parse", f"651150fc88:{p}") != git("rev-parse", f"{C}:{p}")
    for p, differs in up.items():
        if differs:
            by[p].append(("L-41", "inherited:the next upstream base merge", "Q4"))
    return by


def cover_default(p):
    c = CLASS[p]
    if c.startswith("ledger"):
        return "ledger", "a ledger, not a reference (ruling (a))"
    if c == "art-bytes":
        return "none", "art bytes, tabled and never edited (ruling (o))"
    if c == "read-only-upstream":
        return "none", "upstream-carried, byte-identical to the merge base, read-only (ruling (a))"
    if c == "read-only-585":
        return "none", "#585's queue, read-only (ruling (n)); nothing misleads at the tip"
    if c == "read-only-528":
        return "#528", "legal (ruling (k))"
    if c == "tabled-generic-x64":
        return "inherited:coordinator", "ruling (j)"
    return "none", "no lead and no unexcused probe hit at the tip"


def probe_cell(r):
    parts = []
    for k, dk in (("links", "links_dead"), ("paths", "paths_dead"), ("tools", "tools_absent"), ("cites", "cites_unresolved")):
        n = int(r[k])
        if n:
            d = int(r[dk])
            name = {"cites": "IDs"}.get(k, k)
            parts.append(f"{name} {n}" + (f" ({d} {'unresolved' if k == 'cites' else 'dead' if k != 'tools' else 'absent'})" if d else ""))
    for k in ("identity", "retired"):
        if int(r[k]):
            parts.append(f"{k} {r[k]}")
    return " · ".join(parts) or "--"


out = []
counts = ""
if a.table == "coverage":
    n = same_as_commit(PATHS)
    for lead, (ps, d, q) in LEADS.items():
        for p in ps:
            if p not in CLASS:
                bad(f"{lead} names {p}, not one of the 254")
    inb = inbound()
    pop, low = low_set(inb)
    by = dispositions(low)
    out.append("| path | group | tier | lines | kind | class | probes | Q1-Q7 | disposition |")
    out.append("| --- | --- | --- | ---: | --- | --- | --- | --- | --- |")
    dc = collections.Counter()
    for r in PROBES:
        p = r["path"]
        if not (E / p).is_file():
            continue
        leads = by.get(p, [])
        if leads:
            d = sorted({x[1] for x in leads}, key=rank)[0]
            q = "; ".join(f"{x[2]} {x[0]}" for x in sorted(set(leads))) + "; the rest n/a (no other lead)"
        else:
            d, why = cover_default(p)
            q = f"n/a: {why}"
        dc[d.split(":")[0] if d.startswith("inherited") else d] += 1
        lines = INV[p]["lines"]
        out.append(f"| `{p}` | {grp(p)} | {INV[p]['tier']} | {lines if lines is not None else '--'} | {r['kind']} | {CLASS[p]} | {probe_cell(r)} | {q} | {d} |")
    rows = len(out) - 2
    (ok if rows == 254 else bad)(f"coverage rows {rows}, expected 254")
    (ok if sum(dc.values()) == rows else bad)(f"dispositions sum {sum(dc.values())}, rows {rows}")
    counts = "DISPOSITIONS " + " ".join(f"{k} {dc[k]}" for k in sorted(dc)) + f" total {sum(dc.values())}"

elif a.table in ("binaries", "art"):
    want = {"binaries": ("ledger-binary", 31), "art": ("art-bytes", 18)}[a.table]
    ps = [p for p in PATHS if CLASS[p] == want[0]]
    same_as_commit(ps)
    out.append("| path | size | sha256 at the dispatch tip | sha256 at fixed-at |")
    out.append("| --- | ---: | --- | --- |")
    for p in ps:
        f = E / p
        if not f.is_file():
            continue
        b = blob(C, p)
        fx = "(stage E)"
        if a.fixed_at:
            s2 = sha(blob(a.fixed_at, p))
            fx = f"`{s2}`" + ("" if s2 == sha(b) else " **differs**")
            (ok if s2 == sha(b) else bad)(f"{p}: fixed-at equals the dispatch tip")
        out.append(f"| `{p}` | {len(b)} | `{sha(b)}` | {fx} |")
    rows = len(out) - 2
    (ok if rows == want[1] else bad)(f"{a.table} rows {rows}, expected {want[1]}")
    counts = f"{a.table.upper()} {rows}"

elif a.table == "q4":
    same_as_commit(TEXT)
    reg = git("show", f"{C}:docs/decision-register.md").decode()
    cut = reg.find("\n## Open decisions")
    decided = set(re.findall(r"^\| (D-[A-Z]+-\d+)", reg[:cut] if cut > 0 else reg, re.M))
    opened = set(re.findall(r"^\| (D-[A-Z]+-\d+)", reg[cut:], re.M)) if cut > 0 else set()
    cites = tsv("read-cites.tsv")
    # cross-check: the export's IDs are the checker's
    mine = collections.Counter()
    for p in TEXT:
        for i, l in enumerate((E / p).read_text(errors="replace").split("\n"), 1):
            for d in set(re.findall(r"\bD-[A-Z]+-\d+\b", l)):
                if not re.search(r"-0+$", d):
                    mine[(p, str(i), d)] += 1
    theirs = collections.Counter((c["path"], c["line"], c["item"]) for c in cites)
    (ok if mine == theirs else bad)(f"the export's {sum(mine.values())} citations equal the checker's {sum(theirs.values())}")
    files = collections.defaultdict(set)
    for c in cites:
        files[c["item"]].add(c["path"])
    st = {}
    for d in files:
        st[d] = "decided" if d in decided else "open" if d in opened else "UNRESOLVED"
        if st[d] == "UNRESOLVED":
            bad(f"{d} names no register row")
    out.append("#### (a) The decision IDs the 223 cite, with their rows' state\n")
    out.append("| area | distinct IDs cited | decided | open | unresolved | citations |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    areas = collections.defaultdict(collections.Counter)
    for d, s in st.items():
        ar = d.split("-")[1]
        areas[ar]["n"] += 1
        areas[ar][s] += 1
    ncit = collections.Counter(c["item"].split("-")[1] for c in cites)
    for ar in sorted(areas):
        x = areas[ar]
        out.append(f"| {ar} | {x['n']} | {x['decided']} | {x['open']} | {x['UNRESOLVED']} | {ncit[ar]} |")
    tot = collections.Counter()
    for x in areas.values():
        tot.update(x)
    out.append(f"| **Total** | {tot['n']} | {tot['decided']} | {tot['open']} | {tot['UNRESOLVED']} | {len(cites)} |")
    op = sorted((d for d in st if st[d] == "open"), key=lambda d: (d.split("-")[1], int(d.split("-")[2])))
    out.append("\nThe IDs cited whose rows sit under `## Open decisions` (a document citing one as settled would mislead):\n")
    out.append("| ID | cited by |")
    out.append("| --- | --- |")
    for d in op:
        out.append(f"| {d} | {', '.join(f'`{p}`' for p in sorted(files[d]))} |")
    if not op:
        out.append("| -- | none |")
    # (b) tools
    tools = tsv("read-tools.tsv")
    tf = collections.defaultdict(set)
    tex = {}
    for t in tools:
        tf[t["item"]].add(t["path"])
        tex[t["item"]] = t["resolves"] == "1"
    out.append("\n#### (b) Every `tools/<name>` the 223 name, with its existence at the tip\n")
    out.append("| tool | exists | named by (files) |")
    out.append("| --- | --- | ---: |")
    for t in sorted(tf):
        out.append(f"| `{t}` | {'yes' if tex[t] else '**no**'} | {len(tf[t])} |")
    absent_tools = sum(1 for t in tex if not tex[t])
    # (c) issues
    if not a.issues or not pathlib.Path(a.issues).is_file():
        bad("--issues (the issue-state snapshot) is required for q4")
        states = {}
    else:
        states = {}
        for l in pathlib.Path(a.issues).read_text().split("\n"):
            f = l.split("\t")
            if len(f) >= 3 and f[0].isdigit():
                states[int(f[0])] = (f[1], f[2])
    refs = collections.defaultdict(set)
    for p in TEXT:
        if CLASS[p] in ("read-only-upstream", "read-only-585"):
            continue  # upstream's own text and #585's drafts number other repositories' issues
        for l in (E / p).read_text(errors="replace").split("\n"):
            for n in re.findall(r"(?<![\w/#&-])#(\d{1,4})\b", l):
                refs[int(n)].add(p)
    sc = collections.Counter()
    for n in refs:
        sc[states.get(n, ("absent", ""))[0] + " " + states.get(n, ("", "absent"))[1]] += 1
    out.append("\n#### (c) The issues the reference documents cite, against their state (snapshot of 2026-11-02 00:25:51Z)\n")
    out.append("| state | distinct numbers |")
    out.append("| --- | ---: |")
    for k in sorted(sc):
        out.append(f"| {k} | {sc[k]} |")
    out.append(f"| **Total** | {sum(sc.values())} |")
    edit_open = sorted(n for n in refs if states.get(n, ("", ""))[0] == "open" and any(p in EDIT for p in refs[n]))
    out.append(f"\nOpen issues cited by a reference document proper: {len(edit_open)} "
               f"({', '.join('#%d' % n for n in edit_open)}).")
    # (d) paths
    pr = tsv("read-paths.tsv")
    allow = {}
    if a.allow:
        for fn in ("allow-legit.txt", "allow-inherited.txt", "allow-findings.txt"):
            fp = pathlib.Path(a.allow) / fn
            if fp.is_file():
                for l in fp.read_text().split("\n"):
                    m = re.fullmatch(r"(\S+):(\d+|\*) (\S+) .*", l)
                    if m and not l.startswith("#"):
                        allow[(m.group(1), m.group(2))] = m.group(3)
    pc = collections.Counter()
    for r in pr:
        cls = "resolves" if r["resolves"] == "1" else allow.get((r["path"], r["line"]), allow.get((r["path"], "*"), "UNCLASSED"))
        pc[cls] += 1
        if cls == "UNCLASSED":
            bad(f"dead path {r['item']} at {r['path']}:{r['line']} has no allowlist class")
    out.append("\n#### (d) The backticked repository paths, resolved, in the `paths` step's classes\n")
    out.append("| class | references |")
    out.append("| --- | ---: |")
    for k in sorted(pc):
        out.append(f"| {k} | {pc[k]} |")
    out.append(f"| **Total** | {sum(pc.values())} |")
    # (e) counts and baselines, (f) the lines issues cite
    def show(p, n):
        ls = (E / p).read_text(errors="replace").split("\n")
        return ls[n - 1].strip()[:110].replace("|", "\\|") if 0 < n <= len(ls) else "(no such line)"
    cat = (E / "docs/releases/catalog.md").read_text()
    rca = [l for l in (E / "docs/releases/rc-accept.txt").read_text().split("\n") if l.strip() and not l.startswith("#")]
    out.append("\n#### (e) Every baseline, catalog row or count a lead names, against its artifact\n")
    out.append("| lead | the statement | the artifact, read now |")
    out.append("| --- | --- | --- |")
    out.append(f"| L-09 | `next-candidate-work.md:4-5`: {show('docs/releases/next-candidate-work.md', 5)} | `device-facts.md` records the 2026-10-16 transfer to `077197` |")
    out.append("| L-15 | `device-facts.md:7`: the cuts are in `catalog.md` | " + ", ".join(f"`{h}` {cat.count(h)}" for h in ("bc9dfe8141", "077197", "8b511", "a0f60255ab")) + " occurrences in the catalog |")
    out.append(f"| L-26 | `rc-accept.txt`: the acceptances stay as the record | {len(rca)} non-comment lines |")
    out.append("| L-41 | the per-device tables | " + str(sum(1 for p in PATHS if p.startswith('documentation/') and INV[p]['tier'] == 'upstream-carried'
                                                     and git('rev-parse', f'651150fc88:{p}') != git('rev-parse', f'{C}:{p}'))) + " of 15 upstream-carried tables differ from `upstream/next` `651150fc88` |")
    out.append("\n#### (f) Every line number an issue cites in a reference document, against the line\n")
    out.append("| issue | cites | the line at the tip |")
    out.append("| --- | --- | --- |")
    for iss, p, ns in (("#1100", "docs/releases/device-facts.md", (17, 18, 19)), ("#1126", "docs/releases/device-facts.md", (31,)),
                       ("#682", "docs/es-menu-map.md", (134,)), ("#1216", "docs/es-menu-map.md", (405,)), ("#667", "docs/es-menu-map.md", (595,))):
        for n in ns:
            out.append(f"| {iss} | `{p}:{n}` | {show(p, n)} |")
    counts = (f"Q4 ids {len(st)} (decided {tot['decided']}, open {tot['open']}, unresolved {tot['UNRESOLVED']}); "
              f"tools {len(tf)} (absent {absent_tools}); issues {len(refs)}; path references {sum(pc.values())}")

elif a.table == "q5":
    same_as_commit(TEXT)
    inb = inbound()
    pop, low = low_set(inb)
    by = dispositions(low)

    def role(p):
        for pre, rl in (("README.md", "the front page"), ("TRADEMARK.md", "a redistributor's notice"),
                        ("docs/releases/pr/", "a dated PR description"), ("docs/releases/", "a release record"),
                        ("docs/pixelelated/art/", "the art's reference"), ("docs/pixelelated/", "identity and the site"),
                        ("docs/rasteratops/", "a dated record under the retired folder"), ("docs/ra-offline/", "offline achievements design"),
                        ("docs/council-", "a council note"), ("docs/es-", "an interface reference"), ("docs/conflict-", "an interface reference"),
                        ("docs/device-", "a device procedure"), ("docs/cloud-", "a cloud reference"), ("docs/save", "a save-format reference"),
                        ("docs/", "a reference document")):
            if p.startswith(pre):
                return rl
        return "a reference document"

    out.append("| document | lines | last commit | R | O | D | W | role | read by | verdict |")
    out.append("| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- |")
    for p in EDIT:
        if not (E / p).is_file():
            continue
        lc = (git("log", "-1", "--format=%h %cs", C, "--", p) or b"").decode().strip()
        i = inb[p]
        readers = [n for n, k in (("the rules", "R"), ("the root documents", "O"), ("other documents", "D"), ("the October logs", "W")) if i[k]]
        fixes = [x[0] for x in by.get(p, []) if x[1] == "fix"]
        if p in low:
            v = "§ 4 question 2: date its first line or retire"
        elif fixes:
            v = "keep; fix " + ", ".join(sorted(set(fixes)))
        else:
            v = "keep"
        out.append(f"| `{p}` | {INV[p]['lines']} | {lc} | {i['R']} | {i['O']} | {i['D']} | {i['W']} | {role(p)} | {', '.join(readers) or 'nobody named'} | {v} |")
    rows = len(out) - 2
    (ok if rows == 69 else bad)(f"q5 rows {rows}, expected 69 (edit-scope 68, edit-under-naming 1)")
    lowlines = sum(INV[p]["lines"] or 0 for p in low)
    out.append(f"\n`LOW-INBOUND files={len(low)} lines={lowlines}` over R2's reference population ({len(pop)} documents); "
               "R2 C26 printed `files=17 lines=2135`.\n")
    out.append("| low-inbound document | lines | class | R | O | D | W |")
    out.append("| --- | ---: | --- | ---: | ---: | ---: | ---: |")
    for p in low:
        i = inb[p]
        out.append(f"| `{p}` | {INV[p]['lines']} | {CLASS[p]} | {i['R']} | {i['O']} | {i['D']} | {i['W']} |")
    counts = f"Q5 rows {rows}; LOW-INBOUND files={len(low)} lines={lowlines}; population {len(pop)}"

elif a.table == "q6":
    same_as_commit(TEXT)
    allow = {}
    if a.allow:
        for fn in ("allow-legit.txt", "allow-inherited.txt", "allow-findings.txt"):
            fp = pathlib.Path(a.allow) / fn
            if fp.is_file():
                for l in fp.read_text().split("\n"):
                    m = re.fullmatch(r"(\S+):(\d+|\*) (\S+) (.*)", l)
                    if m and not l.startswith("#"):
                        allow[(m.group(1), m.group(2))] = (m.group(3), m.group(4))
    out.append("| what the document points at | where | resolves at the tip | class | reason |")
    out.append("| --- | --- | --- | --- | --- |")
    dead = [r for r in tsv("read-paths.tsv") + tsv("read-tools.tsv") if r["resolves"] == "0"]
    for r in dead:
        p, n, item = r["path"], r["line"], r["item"]
        if git("cat-file", "-e", f"{C}:{item}") is not None:
            bad(f"{item} at {p}:{n} resolves at {C}: the probes are stale")
        ls = (E / p).read_text(errors="replace").split("\n")
        if not (0 < int(n) <= len(ls) and item in ls[int(n) - 1]):
            bad(f"{item} is not at {p}:{n} in --export")
        cls, why = allow.get((p, n), allow.get((p, "*"), ("UNCLASSED", "")))
        if cls == "UNCLASSED":
            bad(f"{item} at {p}:{n} has no allowlist class")
        out.append(f"| `{item}` | `{p}:{n}` | no | {cls} | {why.replace('|', '/')} |")
    for item, where, lead in (("projects/ROCKNIX/packages/network/rclone/sources/post-update", "docs/pr-series/map.txt:112", "L-27"),
                              ("projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout", "docs/pr-series/map.txt:174", "L-27"),
                              ("docs/graphics-memory-testing.md", "#576 :7, #620 :16", "L-33")):
        gone = git("cat-file", "-e", f"{C}:{item}") is None
        (ok if gone else bad)(f"{lead}: {item} absent at {C}")
        out.append(f"| `{item}` | {where} | {'no' if gone else 'yes'} | {lead} | inherited:coordinator |")
    rows = len(out) - 2
    counts = f"Q6 dead {len(dead)} (paths and tools) plus 3 inherited; rows {rows}"

print("\n".join(out))
print(f"COUNTS {counts}", file=sys.stderr)
sys.exit(1 if fails else 0)
