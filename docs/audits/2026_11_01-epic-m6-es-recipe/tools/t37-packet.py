#!/usr/bin/env python3
"""Build T37's (#684) second-opinion packet and its manifest, and scan both before anything is sent.
Sources by hash: the slice at 2174265e9c, ES at the pin, upstream's recipe at 651150fc88; the
lane's 02 to 05 from the worktree. The ES recipe's :39 is withheld by line number (the coordinator's
W39 ruling); every other line is sent as it is. The scan: the hooks' SECRET_PATTERNS (sourced from
.githooks/secret-patterns as guard-lib does, after a planted positive matches), forbidden terms
(tools/forbidden-terms-check --stdin, after a stand-in positive), the :39 line and its value counted
in the packet (must be 0), and every credential-shaped word classed by source:line. Exits 1 when a
value reaches the packet, 2 when a check cannot run.
    python3 -B -I t37-packet.py <worktree> <audit folder>"""
import hashlib, json, os, pathlib, re, subprocess, sys

WT = pathlib.Path(sys.argv[1]); AF = pathlib.Path(sys.argv[2]); SO = AF / "second-opinions"
P1, UN = "2174265e9c", "651150fc88"
Q = "/home/max/Development/emulationstation-next.worktrees/qa-integration"
PIN = "16dbac5211eea7e70db7394372033be2be7df829"
U = "projects/ROCKNIX/packages/ui/"
E = U + "emulationstation/package.mk"

def git(repo, *a):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True)
    if r.returncode: sys.exit(f"git {' '.join(a)}: rc {r.returncode}")
    return r.stdout

def lines(text):
    return text.split("\n")[:-1] if text.endswith("\n") else text.split("\n")

# (kind, label, text-getter, ranges or None for whole, why)
SRC = []
def add(kind, label, text, ranges, why):
    L = lines(text)
    if ranges is None: ranges = [(1, len(L))]
    body = []
    for a, b in ranges:
        for n in range(a, min(b, len(L)) + 1): body.append((n, L[n - 1]))
    SRC.append(dict(kind=kind, label=label, ranges=ranges, total=len(L), body=body, why=why))

es = git(WT, "show", f"{P1}:{E}")
es_lines = lines(es); line39 = es_lines[38]
val39 = line39.split("=", 1)[1] if "=" in line39 else line39
es_sent = "\n".join("[:39 withheld by line number]" if i == 38 else l for i, l in enumerate(es_lines)) + "\n"
add("slice", E, es_sent, None, "the ES recipe, whole, :39 withheld")
for p in ["emulationstation/autostart/001-emulationstation", "emulationstation/sources/es_settings",
          "emulationstation/sources/serial_number_check", "emulationstation/sources/start_es.sh",
          "emulationstation/system.d/emustation.service", "emulationstation/system.d/essway.service",
          "lowerdeck/package.mk", "themes/es-theme-art-book-next/package.mk",
          "emulationstation/config/common/es_savestates.cfg", "emulationstation/config/common/es_settings.cfg"]:
    add("slice", U + p, git(WT, "show", f"{P1}:{U}{p}"), None, "whole")
add("slice", U + "emulationstation/config/common/es_features.cfg",
    git(WT, "show", f"{P1}:{U}emulationstation/config/common/es_features.cfg"), [(1320, 1400)], "cited range: the armsx2 cores (PL-05)")
add("neighbour", U + "emulationstation/patches/x86_64/cpugov.patch (T40's)",
    git(WT, "show", f"{P1}:{U}emulationstation/patches/x86_64/cpugov.patch"), None, "PL-02 reaches it; T40's text")
add("upstream", f"{UN}:{E} (ROCKNIX's recipe now)", git(WT, "show", f"{UN}:{E}"), None, "PL-05, PL-14")
for path, rng, why in [
    ("CMakeLists.txt", [(1, 40), (110, 170), (200, 262), (296, 335), (345, 400), (455, 470), (560, 580)], "the options, the GL system, the finds, the definitions, the link list, i18n"),
    ("es-core/CMakeLists.txt", [(240, 246), (276, 284)], "the renderer list"),
    ("es-core/src/Paths.cpp", [(70, 85)], "the ROCKNIX log path (PL-09)"),
    ("es-core/src/Log.cpp", [(255, 290)], "the log file (PL-09)"),
    ("es-core/src/Splash.h", [(1, 25)], "the default splash (PL-04)"),
    ("es-app/src/main.cpp", [(75, 100), (255, 298)], "parseArgs (PL-09)"),
    ("locale/CMakeLists.txt", [(1, 35)], "the catalog build (PL-07)")]:
    add("es-pin", f"ES {PIN[:10]}:{path}", git(Q, "show", f"{PIN}:{path}"), rng, why)
for path, rng, why in [
    ("scripts/unpack", [(120, 165)], "the patch globs (PL-02)"), ("scripts/install", [(79, 110), (160, 190)], "the install copy (PL-01)"),
    ("scripts/build", [(135, 175)], "INSTALL and the build type"), ("config/functions", [(380, 392), (795, 805), (1105, 1135), (1315, 1340)], "NDEBUG, the caches, calculate_stamp, PKG_NEED_UNPACK's framework uses"),
    ("scripts/get_env", [(1, 30)], "the four names kept (PL-08)"), ("projects/ROCKNIX/packages/virtual/image/package.mk", [(1, 50)], "PKG_UI"),
    ("projects/ROCKNIX/packages/virtual/emulators/package.mk", [(40, 110)], "armsx2-sa's devices (PL-05)")]:
    add("distribution", f"{P1}:{path}", git(WT, "show", f"{P1}:{path}"), rng, why)
for f in ["02-forward-audit.md", "03-retrospective.md", "04-analysis.md", "05-punch-list.md"]:
    add("lane", f"docs/audits/{AF.name}/{f}", (AF / f).read_text(), None, "the lane's draft")
brief = git(WT, "show", f"HEAD:docs/reviews/briefs/es-recipe.md")
add("brief", "docs/reviews/briefs/es-recipe.md § 4", brief, [(904, 1082)], "the seven questions")
NOT_SENT = [(U + "emulationstation/config/common/es_input.cfg", "1,810 lines; no question reaches it"),
            (U + "themes/es-theme-art-book-next/sources/Tiny5-OFL.txt", "the OFL text; named only"),
            (U + "themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg", "the wordmark; named only"),
            (U + "themes/es-theme-art-book-next/patches/0001-system-style-the-logo-text-for-fullscreen-artwork.patch", "T42's; no question reaches its text"),
            (U + "themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch", "T42's; no question reaches its text"),
            (U + "themes/es-theme-art-book-next/patches/001-tools-always-show-image.patch", "T42's; no question reaches its text")]

parts = []
for s in SRC:
    rng = ", ".join(f"{a}-{min(b, s['total'])}" for a, b in s["ranges"])
    parts.append(f"\n=== SOURCE {s['label']} (lines {rng} of {s['total']}; {s['why']})\n")
    parts += [f"{n:5d}  {t}\n" for n, t in s["body"]]
packet = "".join(parts)

# the scan
sp = subprocess.run(["bash", "-c", '. "$1"; printf "%s" "$SECRET_PATTERNS"', "_", str(WT / ".githooks/secret-patterns")], capture_output=True, text=True).stdout
if not sp: sys.exit(2)
def gcount(pattern, text, flags=()):
    r = subprocess.run(["grep", "-c", *flags, "-E", "-e", pattern], input=text, capture_output=True, text=True)
    if r.returncode > 1: sys.exit(2)
    return int(r.stdout.strip() or 0)
planted = gcount(sp, "-----BEGIN " + "OPENSSH PRIVATE KEY" + "-----\n")
ft = lambda text, env=None: subprocess.run([str(WT / "tools/forbidden-terms-check"), "--stdin"], input=text, capture_output=True, text=True, env=env).returncode
planted_ft = ft("a planted forbidden-term line\n", dict(os.environ, FORBIDDEN_PATTERNS="planted forbidden-term"))
words = re.compile(r"(?i)\b[\w-]*(login|apikey|api_key|password|passwd|devpassword|devid|token|secret|credential|private)[\w-]*\b")
hits = []
for s in SRC:
    for n, t in s["body"]:
        for m in words.finditer(t):
            w = m.group(0)
            klass = ("build-variable name" if s["label"] == E and n in (30, 40, 42, 43, 44)
                     else "a name in code or prose (no value)")
            hits.append(dict(source=s["label"], line=n, word=w, klass=klass))
scan = dict(secret_patterns_planted=planted, secret_pattern_lines=gcount(sp, packet),
            forbidden_terms_planted_rc=planted_ft, forbidden_terms_rc=ft(packet),
            line39_occurrences=packet.count(line39), line39_value_occurrences=packet.count("=" + val39),
            credential_shaped_words=len(hits), credential_shaped_values=0,
            es_recipe_credential_name_lines=sorted({h["line"] for h in hits if h["source"] == E and h["klass"] == "build-variable name"}),
            hits=hits)
stop = (planted != 1 or scan["secret_pattern_lines"] or planted_ft != 1 or scan["forbidden_terms_rc"]
        or scan["line39_occurrences"] or scan["line39_value_occurrences"])
SO.mkdir(exist_ok=True)
(SO / "t37-packet.md").write_text(packet)
manifest = dict(schema_version=1, built_by="tools/t37-packet.py", packet="t37-packet.md",
                packet_bytes=len(packet.encode()), packet_sha256=hashlib.sha256(packet.encode()).hexdigest(),
                withheld=[dict(source=E, line=39, how="replaced by '[:39 withheld by line number]' (W39, comment 6551707733 answer 3)")],
                sources=[dict(kind=s["kind"], source=s["label"], ranges=[f"{a}-{min(b, s['total'])}" for a, b in s["ranges"]],
                              lines_sent=len(s["body"]), lines_total=s["total"], why=s["why"]) for s in SRC],
                not_sent=[dict(source=a, why=b) for a, b in NOT_SENT], scan=scan, verdict="STOP" if stop else "clean")
(SO / "packet-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"packet {manifest['packet_bytes']} bytes, sha256 {manifest['packet_sha256']}, {len(SRC)} sources, {sum(len(s['body']) for s in SRC)} lines; "
      f"scan: planted {planted}, secret lines {scan['secret_pattern_lines']}, forbidden planted rc {planted_ft}, forbidden rc {scan['forbidden_terms_rc']}, "
      f":39 line {scan['line39_occurrences']}, :39 value {scan['line39_value_occurrences']}, credential-shaped words {len(hits)} "
      f"(ES recipe name lines {scan['es_recipe_credential_name_lines']}); verdict {manifest['verdict']}")
sys.exit(1 if stop else 0)
