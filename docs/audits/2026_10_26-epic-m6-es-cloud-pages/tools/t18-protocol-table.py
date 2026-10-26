"""T18 (#665): the protocol table, generated.

    python3 -I -B docs/audits/2026_10_26-epic-m6-es-cloud-pages/tools/t18-protocol-table.py \
        <es tree> <pin> <distribution rev>        (from the distribution worktree)

One row per ">>> " marker CloudText::classifyProtocolLine knows (pid, doing,
why, offer, tier, unit, removed) and per exit the two readers map (0, 9, 3/4,
5, 124, 7/8, 69, 75, 130, NoFolder, default): who prints or produces it (the
scripts at the distribution rev, or es-app/src at the pin), the line of each
reader that acts on it (CloudTransferJob::handleLine / run() for the page,
ThreadedCloudSync::run() for the card), and what the player sees, with the
string's own line. Every producer and reader cell is found by a search, not
typed; the spec below holds only the patterns and the sentence for the last
column. Asserted: 18 rows, and each row's producer and reader counts as stage
B read them -- a drift exits 1 and names the row. Exit 2 when a tree cannot
be read.
"""
import re
import subprocess
import sys

ES, PIN, REV = sys.argv[1:4]
SCRIPT_DIRS = ["projects/ROCKNIX/packages/network/rclone/sources",
               "projects/ROCKNIX/packages/rocknix/sources/scripts"]
JOB, CARD, PAGE, TEXT = ("es-app/src/CloudTransferJob.cpp", "es-app/src/ThreadedCloudSync.cpp",
                         "es-app/src/guis/GuiCloudTransfer.cpp", "es-app/src/CloudText.cpp")
EIGHT_CPP = [JOB, CARD, PAGE, TEXT]


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write("t18-protocol-table: git %s failed: %s\n" % (" ".join(args), r.stderr.strip()))
        sys.exit(2)
    return r.stdout


def es_file(path):
    return git("-C", ES, "show", "%s:%s" % (PIN, path)).split("\n")


def grep_scripts(pattern):
    """file:line of every non-comment line of the scripts matching pattern."""
    hits = []
    rx = re.compile(pattern)
    for path in [p for p in git("ls-tree", "-r", "--name-only", REV, "--", *SCRIPT_DIRS).split("\n") if p]:
        for n, line in enumerate(git("show", "%s:%s" % (REV, path)).split("\n"), 1):
            if line.strip().startswith("#"):
                continue
            if rx.search(line):
                hits.append("%s:%d" % (path.rsplit("/", 1)[-1], n))
    return hits


def grep_es(paths, pattern):
    hits = []
    rx = re.compile(pattern)
    for path in paths:
        for n, line in enumerate(es_file(path), 1):
            if line.strip().startswith("//"):
                continue
            if rx.search(line):
                hits.append("%s:%d" % (path.rsplit("/", 1)[-1], n))
    return hits


CALLERS = ["es-app/src/main.cpp", "es-app/src/guis/GuiMenu.cpp", "es-app/src/JourneyTiers.h",
           "es-app/src/CloudTransferJob.cpp", "es-app/src/ThreadedCloudSync.cpp"]

# (row, script producer pattern, es producer pattern, job reader, card reader, sees, expected counts)
# expected counts: (script producers, es producers, job readers, card readers)
SPEC = [
    ("`>>> pid`", None, r'echo \\">>> pid \$\$', r"ProtocolKind::Pid:", r"ProtocolKind::Pid:",
     "nothing: the process group a stop signals (`deliverStop`, `cancelForLaunch`)", (0, 2, 1, 1)),
    ("`>>> doing`", r'echo ">>> doing ', r">>> doing (unpack|archive|network|receive|send)", r"ProtocolKind::Doing:", r"ProtocolKind::Doing:",
     "card: `CHECKING THE CONNECTION...` / `WAITING FOR A NETWORK...` (network), the half's word and bar (receive, send); page row 3: `PACKING UP YOUR SETTINGS...`, `PUTTING YOUR SETTINGS BACK...`, the scan's sentence, `COMPARING WITH THIS DEVICE...`; `copy`/`verify`/`remove` have no producer (the retired folder move)", (6, 5, 1, 1)),
    ("`>>> why`", r'(echo ">>> why|say_why "|\bwhy "|echo ">>> why \$)', None, r"ProtocolKind::Why:", r"ProtocolKind::Why:",
     "card: the outcome line's why (`COULDN'T FINISH - <why>`), translated by `localizedWhy`; page: line 4 beside the items it stopped (§ The why table)", (None, 0, 1, 1)),
    ("`>>> offer`", r'>>> offer ', None, r"ProtocolKind::Offer:", r"ProtocolKind::Offer:",
     "`CloudOffer::present` after the run: the card only when it completed and was not an automatic sync's no-folder skip; the page on dismissal of a completed run with no completed action", (3, 0, 1, 1)),
    ("`>>> tier`", None, r">>> tier ", r"ProtocolKind::Tier:", r"ProtocolKind::Tier:",
     "card: a run whose parts disagree reads `COULDN'T FINISH - <the failing part's why>`; page: line 2 `N OF M ITEMS DID NOT FINISH`, line 4 the parts", (0, None, 1, 1)),
    ("`>>> unit`", r'echo ">>> unit ', r"'>>> unit ", r"ProtocolKind::Unit:", None,
     "page rows 1 and 2: the item and `ITEM i OF n` (the card drops it: `default:` at its switch)", (None, 2, 1, 0)),
    ("`>>> removed`", r'>>> removed ', None, r"ProtocolKind::Removed:", None,
     "page line 3 `REMOVED N FILES FROM THIS DEVICE`, line 4 per system (the card drops it)", (3, 0, 1, 0)),
    ("exit 0", r"clean_exit 0\b", None, r"mExit == 0|ret == 0|rc == 0", r"ret == 0",
     "`COMPLETED`", (None, 0, None, None)),
    ("exit 9", None, None, r"== 9", r"== 9",
     "`COMPLETED` (rclone's nothing needed moving)", (0, 0, None, None)),
    ("exit 3 / 4", r"3\|4\)\s+echo", None, r"whyForCode", r"case 3: case 4:",
     "`COULDN'T FINISH - COULDN'T FIND YOUR CLOUD FOLDER`", (None, 0, None, 2)),
    ("exit 5", r"^\s*5(\|124)?\)\s+echo", None, r"whyForCode", r"case 5: case 124:",
     "`COULDN'T FINISH - YOUR CLOUD STOPPED ANSWERING`", (None, 0, None, 2)),
    ("exit 124", r"clean_exit 124|10\|124\)|5\|124\)", None, r"whyForCode", r"case 5: case 124:",
     "`COULDN'T FINISH - YOUR CLOUD STOPPED ANSWERING`, or the scripts' `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` on an automatic run", (None, 0, None, 2)),
    ("exit 7 / 8", r"7\|8\)\s+echo", None, r"whyForCode", r"case 7: case 8:",
     "`COULDN'T FINISH - YOUR CLOUD WOULDN'T TAKE THE FILES`", (None, 0, None, 2)),
    ("exit 69", r"EXIT_NO_NETWORK=69", None, r"CloudExit::NoNetwork", r"CloudExit::NoNetwork",
     "`SKIPPED - YOU'RE NOT ONLINE` when nothing moved; `COULDN'T FINISH - YOU WENT OFFLINE PART-WAY THROUGH` when the script stamped the cut", (None, 0, None, None)),
    ("exit 75", r"EXIT_LOCK_HELD=75|exit 75", None, r"CloudExit::LockHeld", r"CloudExit::LockHeld",
     "`SKIPPED - A SYNC IS ALREADY RUNNING`; a scan's `SKIPPED - ANOTHER CLOUD CHECK IS RUNNING` (eight wordings in all, § The why table)", (None, 0, None, None)),
    ("exit 130", r"clean_exit 130|exit 130", None, r"CloudExit::Stopped", r"CloudExit::Stopped",
     "a stop this process made: `SKIPPED - YOU CANCELLED IT` / `SKIPPED - YOU STARTED A GAME`; another's: `COULDN'T FINISH - IT WAS STOPPED`", (None, 0, None, None)),
    ("NoFolder (78)", r"exit 78", r"mOffer == \"create-saves-folder\"", r"CloudExit::NoFolder", r"CloudExit::NoFolder",
     "`SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET` with `SET IT UP: GAME SETTINGS > MANAGE CLOUD STORAGE` (the card computes it from the offer; no script exits 78)", (0, 1, None, None)),
    ("default", r"\*\)\s+echo \"SOMETHING WENT WRONG\"", None, r"whyForCode", r"default:\s+return _\(\"SOMETHING",
     "`COULDN'T FINISH - SOMETHING WENT WRONG`", (None, 0, None, 1)),
]


def main():
    print("| # | Marker or exit | Printed or produced by | Page reader (`CloudTransferJob.cpp`, `GuiCloudTransfer.cpp`) | Card reader (`ThreadedCloudSync.cpp`) | What the player sees |")
    print("| ---: | --- | --- | --- | --- | --- |")
    drift = []
    for i, (row, sp, ep, jr, cr, sees, expect) in enumerate(SPEC, 1):
        scripts = grep_scripts(sp) if sp else []
        es = grep_es(CALLERS, ep) if ep else []
        job = grep_es([JOB, PAGE], jr) if jr else []
        card = grep_es([CARD], cr) if cr else []
        got = (len(scripts), len(es), len(job), len(card))
        for k, (want, have) in enumerate(zip(expect, got)):
            if want is not None and want != have:
                drift.append("%s %s=%d (expected %d)" % (row, ("scripts", "es", "page", "card")[k], have, want))
        if row.startswith("`>>>") and row not in ("`>>> unit`", "`>>> removed`") and (not job or not card):
            drift.append("%s has no reader on one side" % row)
        def cell(hits, cap=8):
            if not hits:
                return "--"
            shown = ", ".join(hits[:cap])
            return shown + (" (+%d more)" % (len(hits) - cap) if len(hits) > cap else "")
        produced = "; ".join(x for x in (("scripts: " + cell(scripts)) if scripts else "",
                                         ("es-app: " + cell(es)) if es else "") if x) or "rclone's code, or a script's own success, passed through"
        print("| %d | %s | %s | %s | %s | %s |" % (i, row, produced, cell(job), cell(card), sees))
    print()
    print("Rows: %d (expected 18)." % len(SPEC))
    if len(SPEC) != 18:
        drift.append("rows=%d" % len(SPEC))
    if drift:
        sys.stderr.write("t18-protocol-table: DRIFT %s\n" % "; ".join(drift))
        sys.exit(1)


main()
