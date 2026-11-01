"""t38-checks.py: the steps of t38-checks.sh (T38, #685), run by it after its refusals. See the .sh for usage.

Every failure is keyed `<path>:<line>` (line 0 for an absence that has no line), and an allowlist entry
`<path>:<line> <class> <reason>` suppresses the failures at its key. Classes:
  allow-legit.txt      A B C D H I (R1 C12's: an extraction artefact, another repository, a path named as absent
                       on purpose, an origin note, scaffold's documents cited as examples, a run-output path),
                       provenance (R3 § 2.3), contract (the item lives in the skill's other file), sentence (the
                       sentence names its skill on an earlier line); `*` may stand for every line of a file
  allow-inherited.txt  a lead of the export, L-30 to L-50 or L-76 to L-78 (ruling (d), #911); export paths only;
                       `*` allowed
  allow-findings.txt   a lead of this slice, L-01 to L-29 or L-51 to L-75 or L-79 to L-85; fork-adapted paths only;
                       exact lines only, so each entry is seen gone when its fix lands
An entry that matches no failure is itself a failure (an excuse for nothing). A malformed entry is a refusal. Only the text
checks (refs, stale, contract) are allowlistable, and a contract item is keyed by its name (`templates.md:01-research-notes.md`)
and never matched by `*`: inventory, front, roster and pins are never excused."""
import ast, hashlib, json, pathlib, re, subprocess, sys

TREE, REPO, COMMIT, ALLOW, OUT, WITHHOLD = sys.argv[1:7]
SKILLS = ["begin-delivery", "code-auditor", "council", "council-research", "developer-relations", "futro",
          "mini-retro", "release-notes", "session-resume", "session-stash"]
ACTIVE = {"claude", "gemini", "gpt", "kimi", "muse"}
INACTIVE = {"deepseek", "grok", "mistral"}
EXPORT = ("agents/", "skills/council/", "skills/council-research/")
LEGIT = {"A", "B", "C", "D", "H", "I", "provenance", "contract", "sentence"}
STALE = [("rubber-duck", r"rubber[- ]duck"), ("copilot", r"copilot"), (".github/instructions", r"\.github/instructions"),
         (".github/prompts", r"\.github/prompts"), ("test/qa-integration", r"test/qa-integration"),
         ("opus 4.8", r"opus[- ]4[.]8|claude-opus-4"), ("gpt-5.5", r"gpt-5[.]5"), ("fable 5", r"fable[- ]5(?![.\d])"),
         ("gpt-5.6", r"gpt-5[.]6"), ("trio-process", r"trio[- ]process"), ("trio-runs", r"trio-runs"),
         ("state-main", r"state-main"), ("an inactive seat as current", r"council-member-(deepseek|grok|mistral)|\(Claude, Gemini, GPT, Kimi, Mistral\)")]
ROOTED = r"(?<![\w./-])((?:\.claude|tools|scripts|docs|\.githooks|\.github|research|seed)/[A-Za-z0-9_./-]*[A-Za-z0-9_-])"
base = pathlib.Path(TREE) / ".claude"
out = pathlib.Path(OUT)


def refuse(msg):
    print(f"t38-checks: refused: {msg}; nothing checked")
    sys.exit(2)


def git_show(path):
    r = subprocess.run(["git", "-C", REPO, "show", f"{COMMIT}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


_exists = {}


def at_commit(path):
    if path not in _exists:
        _exists[path] = subprocess.run(["git", "-C", REPO, "cat-file", "-e", f"{COMMIT}:{path}"], capture_output=True).returncode == 0
    return _exists[path]


def lead_num(cls):
    m = re.fullmatch(r"L-(\d+)", cls)
    return int(m.group(1)) if m else None


def load(name, kind):
    p = pathlib.Path(ALLOW) / name
    if kind == "findings" and WITHHOLD == "findings":
        return []
    if not p.is_file():
        refuse(f"{p} is missing (withhold it with --withhold findings, never by deleting it)")
    entries = []
    for n, line in enumerate(p.read_text().split("\n"), 1):
        if not line.strip() or line.startswith("#"):
            continue
        m = re.fullmatch(r"(\.claude/\S+):(\d+|\*|[A-Za-z0-9][A-Za-z0-9_.-]*) (\S+) (\S.*)", line)
        if not m:
            refuse(f"{name}:{n} is not `<path>:<line> <class> <reason>`")
        path, ln, cls, reason = m.groups()
        rel = path[len(".claude/"):]
        num = lead_num(cls)
        if kind == "legit" and cls not in LEGIT:
            refuse(f"{name}:{n} has class {cls!r}, not one of {sorted(LEGIT)}")
        if kind == "inherited" and not (num and (30 <= num <= 50 or 76 <= num <= 78) and rel.startswith(EXPORT)):
            refuse(f"{name}:{n} must name an export lead (L-30 to L-50, L-76 to L-78) on an export path")
        if kind == "findings" and not (num and (num <= 29 or 51 <= num <= 75 or num >= 79) and not rel.startswith(EXPORT)):
            refuse(f"{name}:{n} must name this slice's lead on a fork-adapted path")
        if kind == "findings" and ln == "*":
            refuse(f"{name}:{n}: a finding is allowed at its exact line, never `*`")
        entries.append({"file": name, "n": n, "path": path, "line": ln, "cls": cls, "reason": reason, "used": 0})
    return entries


ALLOWS = load("allow-legit.txt", "legit") + load("allow-inherited.txt", "inherited") + load("allow-findings.txt", "findings")
results = []  # (step, passed)
ALLOWABLE = {"refs", "stale", "contract"}  # text checks; inventory, front, roster and pins are never excused (stage C: a `*` entry once excused a pin)
detail = {}


def record(step, ok, key="", what=""):
    """One assertion. A failure at an allowlisted key passes, with the entry it used."""
    if not ok and step in ALLOWABLE:
        path, _, ln = key.rpartition(":")
        hit = next((e for e in ALLOWS if e["path"] == path and (e["line"] == ln or (e["line"] == "*" and step != "contract"))), None)
        if hit:
            hit["used"] += 1
            detail.setdefault(step, []).append(f"allowed  {key}  {what}  [{hit['file']}:{hit['n']} {hit['cls']}]")
            results.append((step, True, "allowed"))
            return
    if not ok:
        detail.setdefault(step, []).append(f"FAIL     {key}  {what}")
        results.append((step, False, "fail"))
        return
    results.append((step, True, "ok"))


def files():
    return sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file())


def text(rel):
    return (base / rel).read_text(errors="replace")


def front(src):
    """Top-level front-matter keys -> (value, line); a `model:` list keeps its items."""
    lines = src.split("\n")
    if not lines or lines[0] != "---":
        return {}
    out_, key = {}, None
    for i, line in enumerate(lines[1:], 2):
        if line == "---":
            break
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out_[key] = {"value": m.group(2).strip(), "line": i, "items": []}
        elif key and line.startswith("  - "):
            out_[key]["items"].append(line[4:].strip())
    return out_


def scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        v = v[1:-1]
    return v


paths = files()

# 1. inventory
lines_total = 0
for p in paths:
    record("inventory", p.startswith(("agents/", "skills/")), f".claude/{p}:0", "a path outside .claude/agents and .claude/skills")
    lines_total += text(p).count("\n")
(out / "inventory.txt").write_text("\n".join(paths) + f"\ninventory: {len(paths)} paths, {lines_total} lines\n")
print(f"inventory: {len(paths)} paths, {lines_total} lines under {TREE}/.claude")

# 2. front
lens = []
for s in sorted({p.split("/")[1] for p in paths if p.startswith("skills/")}):
    rel = f"skills/{s}/SKILL.md"
    if rel not in paths:
        record("front", False, f".claude/{rel}:0", "no SKILL.md")
        continue
    src = text(rel)
    fm = front(src)
    record("front", src.startswith("---\n"), f".claude/{rel}:1", "does not open ---")
    name = fm.get("name", {"value": "", "line": 0})
    record("front", scalar(name["value"]) == s, f".claude/{rel}:{name['line']}", f"name {scalar(name['value'])!r} is not its directory {s!r}")
    record("front", bool(re.fullmatch(r"[a-z][a-z0-9-]*", scalar(name["value"]))), f".claude/{rel}:{name['line']}", "name not lowercase and hyphenated")
    d = fm.get("description", {"value": "", "line": 0})
    dv = scalar(d["value"])
    record("front", bool(dv) and dv not in (">", "|", ">-", "|-"), f".claude/{rel}:{d['line']}", "no one-line description")
    lens.append(f"{rel}: description {len(dv)} characters (the YAML scalar, its quotes removed)")
for p in [p for p in paths if p.startswith("agents/")]:
    src = text(p)
    fm = front(src)
    stem = pathlib.Path(p).name[: -len(".agent.md")]
    name = fm.get("name", {"value": "", "line": 0})
    record("front", scalar(name["value"]) == stem, f".claude/{p}:{name['line']}", f"name {scalar(name['value'])!r} is not its stem {stem!r}")
    for k in ("description", "tools", "argument-hint"):
        record("front", k in fm and bool(scalar(fm[k]["value"])), f".claude/{p}:{fm.get(k, {'line': 0})['line']}", f"no {k}")
    model = fm.get("model", {"value": "", "line": 0, "items": []})
    record("front", model["value"] == "" and len(model["items"]) == 1, f".claude/{p}:{model['line']}", f"model: is not a list of one item ({len(model['items'])} items)")
    lens.append(f"{p}: description {len(scalar(fm.get('description', {'value': ''})['value']))} characters")
(out / "front.txt").write_text("\n".join(lens) + "\n")

# 3. refs
named_skill = {s: re.compile(r"(?<![\w-])%s(?![\w-])" % re.escape(s)) for s in SKILLS}
for p in paths:
    if not p.endswith(".md"):
        continue
    own = p.split("/")[1] if p.startswith("skills/") else None
    for i, line in enumerate(text(p).split("\n"), 1):
        for m in re.finditer(ROOTED, line):
            tok = m.group(1)
            nxt = line[m.end():m.end() + 1]
            if nxt in "<{*" and nxt != "" or "..." in tok or tok.endswith(("-", "_")):
                continue  # a placeholder path, written to be filled
            tok = tok.rstrip("./")
            if tok.startswith((".claude/agents/", ".claude/skills/")):
                ok = (base / tok[len(".claude/"):]).exists()
            else:
                ok = at_commit(tok)
            record("refs", ok, f".claude/{p}:{i}", f"`{tok}` does not resolve at {COMMIT}")
        for m in re.finditer(r"(?<![\w/.-])references/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", line):
            ref = m.group(0).rstrip(".")
            if line[m.end():m.end() + 1] in "<{*" and line[m.end():m.end() + 1] != "":
                continue
            cands = ([own] if own else []) + [s for s, rx in named_skill.items() if rx.search(line)]
            ok = any((base / "skills" / c / ref).exists() for c in cands)
            record("refs", ok, f".claude/{p}:{i}", f"`{ref}` resolves under none of {cands or ['no skill named']}")
        for m in re.finditer(r"\]\(([^)#\s]+)", line):
            link = m.group(1)
            if link.startswith(("http:", "https:", "mailto:", "/", "#")) or not link.startswith("../") or any(c in link for c in "<{*"):
                continue  # a relative link climbing out of the skill: resolved from the file's own directory
            target = (pathlib.PurePosixPath(".claude") / p).parent.joinpath(link)
            parts = []
            for part in target.parts:
                if part == "..":
                    if not parts:
                        parts = None
                        break
                    parts.pop()
                elif part != ".":
                    parts.append(part)
            if parts is None:
                record("refs", False, f".claude/{p}:{i}", f"link `{link}` climbs out of the repository")
                continue
            t = "/".join(parts).rstrip("/")
            ok = (base / t[len(".claude/"):]).exists() if t.startswith((".claude/agents", ".claude/skills")) else at_commit(t)
            record("refs", ok, f".claude/{p}:{i}", f"link `{link}` (`{t}`) does not resolve at {COMMIT}")
(out / "refs.txt").write_text("")

# 4. stale
for p in paths:
    for i, line in enumerate(text(p).split("\n"), 1):
        for name, rx in STALE:
            if name == "an inactive seat as current" and p.startswith("agents/council-member-") and re.search(r"council-member-(deepseek|grok|mistral)", line):
                if not re.search(r"\(Claude, Gemini, GPT, Kimi, Mistral\)", line):
                    continue  # an inactive agent naming itself is not a seat presented as current
            if re.search(rx, line, re.I):
                record("stale", False, f".claude/{p}:{i}", f"retired term `{name}`")
record("stale", True)  # the step ran over every line

# 5. roster
rule = (git_show(".claude/rules/adversarial-council.md") or b"").decode()
rule_rows = {r.group(1).lower(): (r.group(2), r.group(3)) for r in re.finditer(r"^\| (Claude|GPT) \| `([^`]+)` \| `([^`]+)` \|", rule, re.M)}
record("roster", set(rule_rows) == {"claude", "gpt"}, ".claude/rules/adversarial-council.md:0", f"the rule's seat rows are {sorted(rule_rows)}")
mr_rel = "skills/council/references/member-roster.md"
roster = text(mr_rel) if mr_rel in paths else ""
mr_rows = {r.group(1): (r.group(2), r.group(3)) for r in re.finditer(r"^\| `council-member-(\w+)`\s*\| `([^`]+)`[^|]*?effort=`(\w+)`", roster, re.M)}
active = set()
for a in sorted(ACTIVE | INACTIVE):
    p = f"agents/council-member-{a}.agent.md"
    if p not in paths:
        record("roster", False, f".claude/{p}:0", "missing")
        continue
    fm = front(text(p))
    desc = scalar(fm.get("description", {"value": ""})["value"])
    if not re.search(r"do not invoke|inactive|outside every run profile", desc, re.I):
        active.add(a)
    if a in INACTIVE:
        record("roster", bool(re.search(r"do not invoke", desc, re.I)), f".claude/{p}:{fm.get('description', {'line': 0})['line']}", "an inactive seat whose description does not say do not invoke")
        continue
    model = fm.get("model", {"items": [], "line": 0})
    mm = re.match(r'"?([^ "]+) \(.*effort=(\w+)', model["items"][0] if model["items"] else "")
    got = (mm.group(1), mm.group(2)) if mm else None
    record("roster", got is not None and got == mr_rows.get(a), f".claude/{p}:{model['line'] + 1}", f"{got} against member-roster.md's {mr_rows.get(a)}")
    if a in rule_rows:
        record("roster", got == rule_rows[a], f".claude/{p}:{model['line'] + 1}", f"{got} against adversarial-council.md's {rule_rows[a]}")
record("roster", active == ACTIVE, ".claude/agents/council-member-claude.agent.md:0", f"the active seats are {sorted(active)}, not {sorted(ACTIVE)}")

# 6. pins
pins = json.loads(git_show("verifier-pins.json"))["pins"]
under = sorted(p for p in pins if p.startswith(".claude/"))
record("pins", len(under) == 8, "verifier-pins.json:0", f"{len(under)} pins under .claude/, not 8")
for p in under:
    f = base / p[len(".claude/"):]
    h = hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else ""
    record("pins", h == pins[p]["sha"], f"{p}:0", f"sha256 {h[:16]} against the pin {pins[p]['sha'][:16]}")

# 7. contract
lint = git_show("tools/lint-audit-artifacts").decode()
consts = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(lint).body
          if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("REQUIRED", "ANALYSIS_SECTIONS")}
record("contract", set(consts) == {"REQUIRED", "ANALYSIS_SECTIONS"}, "tools/lint-audit-artifacts:0", "the lint's constants not found")
tpl_rel = "skills/code-auditor/references/templates.md"
tpl = text(tpl_rel) if tpl_rel in paths else ""
for v in consts.get("REQUIRED", []):
    record("contract", v in tpl, f".claude/{tpl_rel}:{v}", f"REQUIRED `{v}` named nowhere in templates.md")
norm = lambda s: re.sub(r"[-\s]+", " ", s.lower()).strip()
for v in consts.get("ANALYSIS_SECTIONS", []):
    ok = v.lower() in tpl.lower()  # the lint's own comparison
    ln = next((i for i, l in enumerate(tpl.split("\n"), 1) if l.startswith("#") and norm(v) in norm(l)), 0)
    record("contract", ok, f".claude/{tpl_rel}:{ln}", f"ANALYSIS_SECTIONS `{v}` fails the lint's lower-case comparison")

# 8. bundle (informational: never a FAIL, ruling (d))
sums_rel = "skills/council/COUNCIL-BUNDLE.SHA256SUMS"
bm = bd = ba = 0
if sums_rel in paths:
    for l in text(sums_rel).splitlines():
        if not l.strip():
            continue
        h, p = l.split(None, 1)
        p = p.lstrip("*")
        if p.startswith(".claude/"):
            f = base / p[len(".claude/"):]
            b = f.read_bytes() if f.is_file() else None
        else:
            b = git_show(p)
        if b is None:
            ba += 1
        elif hashlib.sha256(b).hexdigest() == h:
            bm += 1
        else:
            bd += 1
bundle_line = f"BUNDLE match={bm} diff={bd} absent={ba}"

# the allowlists: an entry that excused nothing is a failure
for e in ALLOWS:
    record("allowlists", e["used"] > 0, f"{e['path']}:{e['line']}", f"{e['file']}:{e['n']} ({e['cls']}) excused nothing")

order = ["inventory", "front", "refs", "stale", "roster", "pins", "contract", "allowlists"]
for step in order:
    rs = [r for r in results if r[0] == step]
    f = [r for r in rs if not r[1]]
    a = [r for r in rs if r[2] == "allowed"]
    (out / f"{step}.txt").write_text("\n".join(detail.get(step, [])) + "\n")
    print(f"{'ok  ' if not f else 'FAIL'}  {step:<10} {len(rs) - len(f)} of {len(rs)} passed" + (f", {len(a)} allowlisted" if a else ""))
    for d in detail.get(step, []):
        if d.startswith("FAIL"):
            print("      " + d)
print(f"info  bundle     {bundle_line} (informational, never a FAIL)")
used = {k: sum(1 for e in ALLOWS if e["file"] == k) for k in ("allow-legit.txt", "allow-inherited.txt", "allow-findings.txt")}
print("allowlists read: " + ", ".join(f"{k} {v}" for k, v in used.items()) + (" (allow-findings.txt withheld)" if WITHHOLD else ""))
passed = sum(1 for r in results if r[1])
print(f"TOTAL: {passed} of {len(results)} assertions")
sys.exit(0 if passed == len(results) else 1)
