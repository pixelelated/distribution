"""t39-checks.py: the steps of t39-checks.sh (T39, #686), run by it after its refusals. See the .sh for usage.

Every text failure is keyed `<path>:<line>` (the line in --tree's copy of the file), and an allowlist entry
`<path>:<line> <class> <reason>` excuses the failures at its key in the steps its class covers. `*` for the
line excuses every line of the file (allow-legit.txt and allow-inherited.txt only). Classes:

  allow-legit.txt      what is not a defect (brief § 5, step 4 and step 6):
                       external      another repository's path, page, branch or tool (X02)  links paths tools
                       pattern       an elided or illustrative path, not a claim it exists   links paths tools
                       historical    a name or path in a dated record (NAMING.md:47-51)       every text step
                       character     the character or the handle keeps its name (NAMING.md:19) identity
                       provenance    the record of where a thing came from                    identity retired paths tools
                       interim-name  `rasteratops-*` tools, `RASTERATOPS_*` variables (#509)  identity paths tools
  allow-inherited.txt  `L-NN`: a finding owned elsewhere; the reason names its owner, one of the coordinator,
                       #528, #585, #509, #511, #270, #947, #1013, the interface lanes or the next upstream
                       base merge (brief § 6's set)                                           every text step
  allow-findings.txt   `L-NN`: this slice's own stage-B finding, on a path of the edit scope (the carve's
                       edit-scope or edit-under-naming class), at its exact line, never `*`; emptied as
                       stage E fixes each                                                     every text step

An entry that excuses nothing is itself a failure (step `allowlists`). An entry with no class, an unknown
class or no reason is a refusal (exit 2). inventory, scope, untouched, generated and binaries are never
excused. `leads` (step 12) is the § 3 check line of each fix candidate a text check can hold, so the run with
allow-findings.txt withheld names each stage-B finding; only an allow-findings.txt or allow-inherited.txt entry
excuses it. Counts are the script's own; the last line is `TOTAL: <passed> of <checks> steps`."""
import collections, hashlib, json, pathlib, posixpath, re, subprocess, sys, urllib.parse

TREE, REPO, COMMIT, SINCE, PATHS, ALLOW, OUT, WITHHOLD = sys.argv[1:9]
tree = pathlib.Path(TREE)
out = pathlib.Path(OUT)

# The slice's fixed figures (brief § 2, ruling (h), and the stage-A CARVE lines, brief :1297): a drift FAILs.
EXPECT_PATHS, EXPECT_TEXT, EXPECT_BINARY = 254, 223, 31
EXPECT_CARVE = {"art-bytes": 18, "edit-scope": 68, "edit-under-naming": 1, "ledger-binary": 31, "ledger-named": 6,
                "ledger-plan": 1, "ledger-reviews": 12, "read-only-528": 1, "read-only-585": 27,
                "read-only-upstream": 88, "tabled-generic-x64": 1}
NAMED = {"docs/releases/catalog.md", "docs/pr-series/map.txt", "docs/releases/rc-accept.txt", "docs/vm-qa-log.md",
         "docs/cloud-sync-changelog.md", "docs/rasteratops/p0-sweep-hits.txt"}
AUDIT = "docs/audits/2026_11_01-epic-m6-doctrine-reference/"
POINTER = ".github/sessions/saved-session-state-feature-m6-doctrine-reference-686.md"
APPEND_ONLY = ("docs/decision-register.md", "docs/blindspot-register.md", "docs/friction-log.md")
CATALOG = "docs/releases/catalog.md"
# The runs block's retired list (brief § 5, :1353), case-insensitive.
RETIRED = ["cloud_migrate_layout", "migrate.?layout", "rebase --onto", "rclonectl", r"\.github/instructions",
           "copilot", "rubber[- ]duck", r"\brclone config\b", r"rocknix\.worktrees"]
# Step 6: the capitalised brand, Rasteratops as a name, the fork's repository under its retired owner.
IDENTITY = [("brand-case", r"\bPixelelated\b|PIXELELATED"), ("Rasteratops", r"Rasteratops|RASTERATOPS"),
            ("maxengel/rocknix", r"maxengel/rocknix")]
LEGIT = {"external": {"links", "paths", "tools"}, "pattern": {"links", "paths", "tools"},
         "historical": {"links", "paths", "tools", "identity", "retired", "cites"}, "character": {"identity"},
         "provenance": {"identity", "retired", "paths", "tools"}, "interim-name": {"identity", "paths", "tools"}}
TEXT_STEPS = {"links", "paths", "tools", "identity", "retired", "cites", "leads"}
OWNERS = ("coordinator", "#528", "#585", "#509", "#511", "#270", "#947", "#1013", "the interface lanes",
          "the next upstream base merge")
PLACEHOLDER = re.compile(r"[<>{}*$\[\]]|\.\.\.|\u2026")


def refuse(msg):
    print(f"t39-checks: refused: {msg}; nothing checked")
    sys.exit(2)


def git(*args, ok=(0,)):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    return r.stdout if r.returncode in ok else None


_exists = {}


def at(ref, path):
    k = (ref, path)
    if k not in _exists:
        _exists[k] = subprocess.run(["git", "-C", REPO, "cat-file", "-e", f"{ref}:{path}"],
                                    capture_output=True).returncode == 0
    return _exists[k]


def blob_sha(ref, path):
    b = git("show", f"{ref}:{path}")
    return hashlib.sha256(b).hexdigest() if b is not None else None


paths = [l.strip() for l in open(PATHS) if l.strip()]
if len(paths) != EXPECT_PATHS or len(set(paths)) != EXPECT_PATHS:
    refuse(f"--paths holds {len(paths)} lines, {len(set(paths))} distinct, not {EXPECT_PATHS}")

# The inventory at --commit: tier and lines for the carve (one definition, the stage-A CARVE rule).
inv = json.loads(git("show", f"{COMMIT}:docs/reviews/inventory.json"))
cols = inv["columns"]
ix = {k: i for i, k in enumerate(cols)}
invrow = {}
for r in inv["rows"]:
    if r[ix["tree"]] == "distribution":
        invrow[r[ix["path"]]] = {"tier": r[ix["tier"]], "lines": r[ix["lines"]]}


def carve(p):
    r = invrow.get(p)
    if r is None:
        return "not-in-inventory"
    if r["lines"] is None:
        return "ledger-binary"
    if r["tier"] == "upstream-carried":
        return "read-only-upstream"
    if p.startswith("docs/reviews/"):
        return "ledger-reviews"
    if p in NAMED:
        return "ledger-named"
    if p.startswith("plans/"):
        return "ledger-plan"
    if p.startswith("docs/upstream/"):
        return "read-only-585"
    if p == "LICENSE.md":
        return "read-only-528"
    if p.startswith("documentation/"):
        return "tabled-generic-x64"
    if "/art/" in p and not p.endswith(".md"):
        return "art-bytes"
    if p == "TRADEMARK.md":
        return "edit-under-naming"
    return "edit-scope"


CLASS = {p: carve(p) for p in paths}
EDIT = {p for p in paths if CLASS[p] in ("edit-scope", "edit-under-naming")}


def load(name, kind):
    f = pathlib.Path(ALLOW) / name
    if kind == "findings" and WITHHOLD == "findings":
        return []
    if not f.is_file():
        refuse(f"{f} is missing (withhold it with --withhold findings, never by deleting it)")
    entries = []
    for n, line in enumerate(f.read_text().split("\n"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        m = re.fullmatch(r"(\S+):(\d+|\*) (\S+) (\S.*)", line)
        if not m:
            refuse(f"{name}:{n} is not `<path>:<line> <class> <reason>` (a class and a reason are required)")
        path, ln, cls, reason = m.groups()
        if path not in CLASS:
            refuse(f"{name}:{n} names {path}, not one of the 254")
        lead = re.fullmatch(r"L-(\d{2})", cls)
        if kind == "legit":
            if cls not in LEGIT:
                refuse(f"{name}:{n} has class {cls!r}, not one of {sorted(LEGIT)}")
            steps = LEGIT[cls]
        else:
            if not lead or not 1 <= int(lead.group(1)) <= 46:
                refuse(f"{name}:{n} has class {cls!r}, not a lead L-01 to L-46")
            steps = TEXT_STEPS
        if kind == "inherited" and not any(o in reason for o in OWNERS):
            refuse(f"{name}:{n} names no owner of {OWNERS}")
        if kind == "findings":
            if ln == "*":
                refuse(f"{name}:{n}: a finding is allowed at its exact line, never `*`")
            if path not in EDIT:
                refuse(f"{name}:{n}: {path} is {CLASS[path]}, outside the edit scope; a finding there is inherited")
        entries.append({"file": name, "n": n, "path": path, "line": ln, "cls": cls, "steps": steps, "used": 0})
    return entries


ALLOWS = load("allow-legit.txt", "legit") + load("allow-inherited.txt", "inherited") + load("allow-findings.txt", "findings")
results = []      # (step, passed, allowed)
probe = collections.defaultdict(collections.Counter)   # per path: what each text step read and found (probes.tsv)
seen = collections.defaultdict(list)                   # per step: every item read, for the table generator
detail = collections.defaultdict(list)


def record(step, passed, key, msg):
    allowed = False
    if not passed and step in TEXT_STEPS:
        p, _, ln = key.rpartition(":")
        for e in ALLOWS:
            if e["path"] == p and (e["line"] == "*" or e["line"] == ln) and step in e["steps"]:
                e["used"] += 1
                allowed = True
        if allowed:
            detail[step].append(f"allowed {key} {msg}")
    if not passed and not allowed:
        detail[step].append(f"FAIL {key} {msg}")
    results.append((step, passed or allowed, allowed))


# 1. inventory: the 254, each at --commit and in --tree; text and binary by a NUL byte, agreeing with the inventory.
text, binary = [], []
for p in paths:
    f = tree / p
    record("inventory", at(COMMIT, p), f"{p}:0", "absent at --commit")
    if not f.is_file():
        record("inventory", False, f"{p}:0", "absent from --tree")
        continue
    b = f.read_bytes()
    isbin = b"\0" in b
    (binary if isbin else text).append(p)
    inv_bin = invrow.get(p, {}).get("lines", 0) is None
    record("inventory", isbin == inv_bin, f"{p}:0", f"NUL-byte binary={isbin} but the inventory's lines is None={inv_bin}")
record("inventory", len(text) == EXPECT_TEXT, "-:0", f"text rows {len(text)}, expected {EXPECT_TEXT}")
record("inventory", len(binary) == EXPECT_BINARY, "-:0", f"binary rows {len(binary)}, expected {EXPECT_BINARY}")
inventory_line = f"paths {len(paths)} text {len(text)} binary {len(binary)}"

# 2. scope: ruling (a)'s carve, the class sizes printed and held to the stage-A CARVE lines.
cc = collections.Counter(CLASS.values())
for k in sorted(set(cc) | set(EXPECT_CARVE)):
    record("scope", cc.get(k, 0) == EXPECT_CARVE.get(k, 0), f"-:0", f"CARVE {k} {cc.get(k, 0)}, expected {EXPECT_CARVE.get(k, 0)}")
scope_line = "CARVE " + " ".join(f"{k} {cc[k]}" for k in sorted(cc)) + f" total {sum(cc.values())}"

lines_of = {p: (tree / p).read_text(errors="replace").split("\n") for p in text}


def strip_code(lines):
    """Lines with fenced blocks blanked (a link or a span inside a fence is an example, not a claim)."""
    outl, fence = [], None
    for l in lines:
        m = re.match(r"\s*(```+|~~~+)", l)
        if m:
            fence = None if fence and m.group(1)[0] == fence[0] else (fence or m.group(1))
            outl.append("")
            continue
        outl.append("" if fence else l)
    return outl


# 3. links: every relative Markdown link resolves at --commit, `./x`, `../x` and bare `x`; schemes and anchors excluded.
LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
nlinks = 0
for p in text:
    if not p.endswith(".md"):
        continue
    for i, l in enumerate(strip_code(lines_of[p]), 1):
        l = re.sub(r"`[^`]*`", "", l)
        for t in LINK.findall(l) + REFDEF.findall(l):
            if SCHEME.match(t) or t.startswith("#"):
                continue
            target = urllib.parse.unquote(t.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue
            nlinks += 1
            rp = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(p), target))
            good = not rp.startswith("..") and (rp in (".", "") or at(COMMIT, rp.rstrip("/")))
            probe[p]["links"] += 1; probe[p]["links_dead"] += not good
            record("links", good, f"{p}:{i}", f"link {t} -> {rp} absent at --commit")

# 4. paths: every backticked repository path resolves after a :N / :N-M suffix is stripped; placeholders skipped.
top = set((git("ls-tree", "--name-only", COMMIT) or b"").decode().split())
SPAN = re.compile(r"`([^`\n]+)`")
PATHISH = re.compile(r"^(?:\./)?([A-Za-z0-9_.@+-]+(?:/[A-Za-z0-9_.@+-]*)+)(?::L?\d+(?:-L?\d+)?(?:,\s*L?\d+(?:-L?\d+)?)*)?$")
npaths = 0
for p in text:
    for i, l in enumerate(lines_of[p], 1):
        for s in SPAN.findall(l):
            s = s.strip()
            if PLACEHOLDER.search(s):
                continue
            m = PATHISH.match(s)
            if not m:
                continue
            cand = m.group(1).rstrip("/")
            if cand.split("/", 1)[0] not in top:
                continue
            if re.fullmatch(r"tools/[^/]+", cand):
                continue  # a bare tools/<name> is step 5's, so one planted tool name fails one step
            npaths += 1
            good = at(COMMIT, cand)
            probe[p]["paths"] += 1; probe[p]["paths_dead"] += not good
            seen["paths"].append((p, i, cand, int(good)))
            record("paths", good, f"{p}:{i}", f"path `{cand}` absent at --commit")

# 5. tools: every tools/<name> a text row names exists at --commit (L-14, L-19). A name followed by a glob or
#    placeholder character (`tools/cloud-*`) or cut by a generator's ellipsis (`tools/device-ac…`) is a pattern,
#    skipped as step 4 skips one.
TOOL = re.compile(r"(?<![\w./~-])tools/([A-Za-z0-9_][A-Za-z0-9_.-]*[A-Za-z0-9_])(?![A-Za-z0-9_.-]*[*?{\[<\u2026])")
ntools = 0
for p in text:
    for i, l in enumerate(lines_of[p], 1):
        for name in sorted(set(TOOL.findall(l))):
            ntools += 1
            good = at(COMMIT, f"tools/{name}")
            probe[p]["tools"] += 1; probe[p]["tools_absent"] += not good
            seen["tools"].append((p, i, f"tools/{name}", int(good)))
            record("tools", good, f"{p}:{i}", f"tools/{name} absent at --commit")

# 6. identity and 7. retired: one failure per line per term.
for step, terms, flags in (("identity", IDENTITY, 0), ("retired", [(t, t) for t in RETIRED], re.I)):
    for p in text:
        for i, l in enumerate(lines_of[p], 1):
            for name, rx in terms:
                if re.search(rx, l, flags):
                    probe[p][step] += 1
                    seen[step].append((p, i, name, 0))
                    record(step, False, f"{p}:{i}", f"{name}: {l.strip()[:120]}")
    if not any(r[0] == step for r in results):
        results.append((step, True, False))

# 8. cites: every D-<AREA>-<n> in the text rows names a register row at --commit; a -0+ placeholder skipped.
reg = git("show", f"{COMMIT}:docs/decision-register.md").decode()
ids = set(re.findall(r"^\| (D-[A-Z]+-\d+)", reg, re.M))
ncites = 0
for p in text:
    for i, l in enumerate(lines_of[p], 1):
        for d in sorted(set(re.findall(r"\bD-[A-Z]+-\d+\b", l))):
            if re.search(r"-0+$", d):
                continue
            ncites += 1
            probe[p]["cites"] += 1; probe[p]["cites_unresolved"] += d not in ids
            seen["cites"].append((p, i, d, int(d in ids)))
            record("cites", d in ids, f"{p}:{i}", f"{d} names no register row")
cites_line = f"register IDs {len(ids)}, citations {ncites}"

# 9. untouched: no non-merge commit in --since..--commit touches a path outside the edit scope, the audit
#    folder, the retro, the pointer, the work logs, or (append-only) the three registers.
log = (git("log", "--no-merges", "--format=%x00%h", "--name-only", f"{SINCE}..{COMMIT}") or b"").decode()
ncommits = 0
for chunk in log.split("\0")[1:]:
    h, *files = [x for x in chunk.split("\n") if x.strip()]
    ncommits += 1
    for f in files:
        okp = (f in EDIT or f.startswith(AUDIT) or f == POINTER
               or f.startswith(".github/sessions/archived/saved-session-state-feature-m6-doctrine-reference-686-")
               or f.startswith("docs/work-logs/")
               or re.fullmatch(r"docs/retros/\d{4}-\d\d-\d\d-m6-doctrine-reference\.md", f) or f in APPEND_ONLY)
        record("untouched", okp, f"{f}:0", f"{h} touches {f} ({CLASS.get(f, 'outside the 254')})")
for f in APPEND_ONLY:
    d = (git("diff", SINCE, COMMIT, "--", f) or b"").decode()
    removed = [l for l in d.split("\n") if l.startswith("-") and not l.startswith("---")]
    record("untouched", not removed, f"{f}:0", f"{len(removed)} removed line(s): the registers take appends only")
if not any(r[0] == "untouched" for r in results):
    results.append(("untouched", True, False))

# 10. generated: the catalog begins with its Generated-by header (in --tree and at --commit) and is unchanged since --since.
cat_tree = (tree / CATALOG).read_text().split("\n")[:4] if (tree / CATALOG).is_file() else []
record("generated", any(l.startswith("Generated by `tools/release-catalog --write`") for l in cat_tree), f"{CATALOG}:0",
       "--tree's catalog lacks its Generated-by header")
record("generated", blob_sha(COMMIT, CATALOG) == blob_sha(SINCE, CATALOG), f"{CATALOG}:0", "changed between --since and --commit")
tsha = hashlib.sha256((tree / CATALOG).read_bytes()).hexdigest() if (tree / CATALOG).is_file() else None
record("generated", tsha == blob_sha(SINCE, CATALOG), f"{CATALOG}:0", "--tree's catalog differs from --since's")

# 11. binaries: the 31 binaries and the 18 art text files, in --tree and at --commit, equal --since (ruling (o)).
held = [p for p in paths if CLASS[p] in ("ledger-binary", "art-bytes")]
for p in held:
    s = blob_sha(SINCE, p)
    record("binaries", blob_sha(COMMIT, p) == s, f"{p}:0", "sha256 at --commit differs from --since")
    f = tree / p
    record("binaries", f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == s, f"{p}:0", "sha256 in --tree differs from --since")
binaries_line = f"held {len(held)} (ledger-binary {cc.get('ledger-binary', 0)}, art-bytes {cc.get('art-bytes', 0)})"

# 12. leads: the § 3 check line of each fix candidate a text check can hold, run over --tree, one failure per
#     defect line (`:0` where the defect is an absence), so the stage-B findings are named by the run with
#     allow-findings.txt withheld and seen gone after stage E. Not here, with the reason: L-11 (a heuristic, not
#     a check: brief :1049), L-13 (the fix's shape is the stream brief's), L-17 (conditional; the text against
#     the four rows is unread), L-18 (the dated-first-line set waits on § 4 question 2), L-21 (ledger unless its
#     tense presents the identity as current), L-22 (the identity step holds it).
def lead_lines(p, rx, flags=0):
    return [i for i, l in enumerate(lines_of.get(p, []), 1) if re.search(rx, l, flags)]


def has(p, rx, flags=0):
    return bool(lead_lines(p, rx, flags))


LEADS = []  # (lead, path, failing line numbers)
LEADS.append(("L-02", "README.md", lead_lines("README.md", r"instructions attached")))
LEADS.append(("L-03", "docs/device-testing-policy.md", lead_lines("docs/device-testing-policy.md", r"Open:.*D-QA-016")))
for p in ("docs/rasteratops/cloud-layout.md", "docs/releases/pr/08-saves.md"):
    LEADS.append(("L-04", p, [] if has(p, r"D-CLOUD-175") else lead_lines(p, r"cloud_migrate_layout|layout migration")))
LEADS.append(("L-05", "docs/device-flashing-runbook.md", [] if has("docs/device-flashing-runbook.md", r"pixelelated") else [0]))
LEADS.append(("L-06", "docs/cloud-save-integrity.md", lead_lines("docs/cloud-save-integrity.md", r"M7 order remains")))
LEADS.append(("L-07", "docs/backup-contents.md", lead_lines("docs/backup-contents.md", r"CONFIGURATIONS|EVERYTHING")))
LEADS.append(("L-08", "docs/es-menu-map.md", lead_lines("docs/es-menu-map.md", r"^#+ .*(Pending|under qualification)")))
ncw = "docs/releases/next-candidate-work.md"
LEADS.append(("L-09", ncw, [i for i in lead_lines(ncw, r"baseline is")
                            if re.search(r"20261011T222153Z", " ".join(lines_of[ncw][i - 1:i + 1]))]))
LEADS.append(("L-10", "docs/pixelelated/cloud-folders.md", lead_lines("docs/pixelelated/cloud-folders.md", r"prepared release documentation")))
LEADS.append(("L-12", "docs/council-mistral-counter.md",
              [] if has("docs/council-mistral-counter.md", r"sealed|retired|scaffold#915", re.I) else [0]))
LEADS.append(("L-15", "docs/releases/device-facts.md", lead_lines("docs/releases/device-facts.md", r"themselves are \[catalog\.md\]")))
dtp = "docs/device-testing-policy.md"
LEADS.append(("L-16", dtp, [] if has(dtp, r"--\(token") else (lead_lines(dtp, r"^## Reading a device's output") or [0])))
for lead, p, bad_lines in LEADS:
    for i in bad_lines:
        record("leads", False, f"{p}:{i}", f"{lead}: its § 3 check prints the defect")
    if not bad_lines:
        results.append(("leads", True, False))
leads_line = f"{len(LEADS)} lead checks, {sum(1 for _, _, b in LEADS if b)} printing a defect"

for e in ALLOWS:
    record("allowlists", e["used"] > 0, f"{e['path']}:{e['line']}", f"{e['file']}:{e['n']} ({e['cls']}) excused nothing")
if not ALLOWS:
    results.append(("allowlists", True, False))

# What the text steps read, for tools/t39-tables.py (written under --out only).
PROBES = ["links", "links_dead", "paths", "paths_dead", "tools", "tools_absent", "identity", "retired", "cites",
          "cites_unresolved"]
with open(out / "probes.tsv", "w") as fh:
    fh.write("path\tclass\tkind\t" + "\t".join(PROBES) + "\n")
    for p in paths:
        kind = "text" if p in lines_of else "binary"
        fh.write(f"{p}\t{CLASS[p]}\t{kind}\t" + "\t".join(str(probe[p][k]) for k in PROBES) + "\n")
for step, rows in seen.items():
    with open(out / f"read-{step}.tsv", "w") as fh:
        fh.write("path\tline\titem\tresolves\n")
        for r in rows:
            fh.write("\t".join(map(str, r)) + "\n")

info = {"inventory": inventory_line, "scope": scope_line, "links": f"{nlinks} relative links",
        "paths": f"{npaths} backticked repository paths", "tools": f"{ntools} tools/ names",
        "cites": cites_line, "untouched": f"{ncommits} non-merge commits since {SINCE}", "binaries": binaries_line, "leads": leads_line}
order = ["inventory", "scope", "links", "paths", "tools", "identity", "retired", "cites", "untouched", "generated",
         "binaries", "leads", "allowlists"]
passed_steps = 0
for step in order:
    rs = [r for r in results if r[0] == step]
    f = [r for r in rs if not r[1]]
    a = [r for r in rs if r[2]]
    (out / f"{step}.txt").write_text("\n".join(detail.get(step, [])) + "\n")
    passed_steps += not f
    extra = (f"; {len(a)} allowlisted" if a else "") + (f"; {info[step]}" if step in info else "")
    print(f"{'ok  ' if not f else 'FAIL'}  {step:<10} {len(rs) - len(f)} of {len(rs)} assertions{extra}")
    for d in detail.get(step, []):
        if d.startswith("FAIL"):
            print("      " + d)
used = {k: sum(1 for e in ALLOWS if e["file"] == k) for k in ("allow-legit.txt", "allow-inherited.txt", "allow-findings.txt")}
print("allowlists read: " + ", ".join(f"{k} {v}" for k, v in used.items()) + (" (allow-findings.txt withheld)" if WITHHOLD else ""))
print(f"TOTAL: {passed_steps} of {len(order)} steps")
sys.exit(0 if passed_steps == len(order) else 1)
