"""Compose 02-forward-audit.md from its template and the generators' tables (#678).

    python3 -I t31-02.py <audit folder>

Substitutes, in stage-b/02-template.md:
  {{COVERAGE}}  one row per path (76), from stage-a/membership.txt's rows: the
                lines, the inventory's tier, the read's tier (the three files
                absent at cada856d86 are fork-own; the other fork-touched nine
                fork-modified), how the file was read, and the leads naming it
                (parsed from the template's own § Leads table);
  {{PAGES}} {{DIALOGS}} {{ROWS}} {{TITLES}}  the stage-b tables, verbatim;
  {{READS}}     stage-b/reads.md's 26 rows, each joined with its writer and
                what a failure reads as (WRITERS below, read at each line); a
                site without an entry, or an entry without a site, fails;
  {{NUMSTAT}}   the fork's 12 numstat pairs (stage-a/runs.txt's run).
Asserts: 76 coverage rows, 37 pages, 50 dialogs, 48 rows, 26 reads, 37 titles,
12 numstat pairs. Exits 1 on any difference, writing nothing.
"""
import re
import sys
from pathlib import Path

A = Path(sys.argv[1])
tpl = (A / "stage-b/02-template.md").read_text()

FORK_ADDED = {"GuiScraperRun.cpp", "GuiScraperRun.h", "WifiScanProcess.h"}
FORK_TOUCHED = FORK_ADDED | {"GuiBios.cpp", "GuiBios.h", "GuiGameOptions.cpp", "GuiImageViewer.cpp", "GuiSaveState.cpp",
                             "GuiSaveState.h", "GuiScraperStart.cpp", "GuiSettings.cpp", "GuiSettings.h"}
WHOLE = FORK_ADDED | {"GuiSaveState.cpp", "GuiScraperStart.cpp", "GuiBios.cpp", "GuiSettings.cpp", "GuiSettings.h", "GuiLoading.h"}
NUMSTAT = [("GuiBios.cpp", 172, 88), ("GuiBios.h", 6, 7), ("GuiGameOptions.cpp", 2, 2), ("GuiImageViewer.cpp", 16, 1),
           ("GuiSaveState.cpp", 330, 23), ("GuiSaveState.h", 23, 0), ("GuiScraperRun.cpp", 258, 0), ("GuiScraperRun.h", 67, 0),
           ("GuiScraperStart.cpp", 105, 7), ("GuiSettings.cpp", 8, 1), ("GuiSettings.h", 18, 0), ("WifiScanProcess.h", 202, 0)]

# The writer of each read and what a failure reads as, read at each line.
WRITERS = {
    "GuiFavoriteMusicSelector.cpp:19": ("a music folder", "the player (a copy over USB or the network)", "a folder added while ES runs is not listed until a restart"),
    "GuiGameOptions.cpp:41": ("the game's marquee", "the scraper", "no logo on the options menu until a restart, if the miss was remembered first"),
    "GuiGameOptions.cpp:53": ("the game's manual", "the scraper", "VIEW THIS GAME'S MANUAL absent after a scrape until a restart"),
    "GuiGameOptions.cpp:54": ("the game's magazine", "the scraper", "the magazine row absent after a scrape until a restart"),
    "GuiGameOptions.cpp:55": ("the game's map", "the scraper", "the map row absent after a scrape until a restart"),
    "GuiGameOptions.cpp:56": ("the game's video", "the scraper", "the video row absent after a scrape until a restart"),
    "GuiImageViewer.cpp:415": ("a page extracted from an archive", "this process (`zipFile.extract`)", "the extraction reported failed if its path was asked about before"),
    "GuiImageViewer.cpp:629": ("an image added to the viewer", "RetroArch (screenshots), the scraper", "a new capture not shown until a restart"),
    "GuiImageViewer.cpp:660": ("the image to show", "RetroArch, the scraper", "the viewer opens nothing for a capture made this session, if missed before"),
    "GuiImageViewer.cpp:723": ("the video to play", "the scraper", "the video does not play until a restart"),
    "GuiNetPlay.cpp:679": ("the game's image", "the scraper", "the cartridge icon in place of a scraped image"),
    "GuiNetPlaySettings.cpp:70": ("`:/community_relay_servers.xml`", "none (a resource)", "harmless"),
    "GuiSaveState.cpp:33": ("`/var/run/cloud_sync.lock`", "the cloud scripts (flock)", "any open failure but ENOENT reads as A SYNC IS ALREADY RUNNING (L-14); ES is root, so EACCES is hard to reach"),
    "GuiAnalogSticksLedControls.cpp:20": ("`analogsticks.led` token 0", "the page itself", "guarded by `tokens.size() == 7`; a non-number is 0"),
    "GuiAnalogSticksLedControls.cpp:21": ("token 1", "the page", "as above"),
    "GuiAnalogSticksLedControls.cpp:22": ("token 2", "the page", "as above"),
    "GuiAnalogSticksLedControls.cpp:23": ("token 3", "the page", "as above"),
    "GuiAnalogSticksLedControls.cpp:24": ("token 4", "the page", "as above"),
    "GuiAnalogSticksLedControls.cpp:25": ("token 5", "the page", "as above"),
    "GuiAnalogSticksLedControls.cpp:26": ("token 6", "the page", "as above"),
    "GuiKeyMappingEditor.cpp:156": ("a tab's value, \"0\" to \"3\"", "the page", "positive"),
    "GuiUpdate.cpp:213": ("the updater's `>>> N%` line", "`updateSystem`'s script", "a non-number is 0% on the card; upstream's OS update card (D-UI-079)"),
    "GuiGamelistOptions.cpp:389": ("a grid size's two dimensions (the seat's EP-27; the first reading said ratings)", "the theme or the player's choice", "a non-number is 0"),
    "GuiMetaDataEd.cpp:600": ("the stored rating", "the gamelist", "positive"),
    "GuiMetaDataEd.cpp:601": ("the edited rating", "the editor", "positive"),
}

def table(name):
    lines = [l for l in (A / "stage-b" / name).read_text().splitlines() if l.startswith("|")]
    return lines

def rows_of(lines):
    return [l for l in lines if l.startswith("| `")]

fail = []
def expect(what, got, want):
    if got != want:
        fail.append("%s %d, expected %d" % (what, got, want))

# leads per file, from the template's Leads table
leads = {}
sect = tpl[tpl.index("## Leads"):tpl.index("## Positives")]
for l in sect.splitlines():
    m = re.match(r"\| \*\*(L-\d+)\*\* \| [^|]* \| ([^|]*) \|", l)
    if m:
        for f in re.findall(r"`([A-Za-z]+\.(?:cpp|h))[:`]", m.group(2)):
            leads.setdefault(f, []).append(m.group(1))

cov = ["| Path | Lines | Inventory | Read tier | How read | Leads |", "| --- | ---: | --- | --- | --- | --- |"]
for l in (A / "stage-a/membership.txt").read_text().splitlines():
    m = re.match(r"^(\d+) (c\+\+|c-header) (\S+) (es-app/src/guis/(\S+))$", l)
    if not m:
        continue
    n, _, inv, path, f = m.groups()
    tier = "fork-own" if f in FORK_ADDED else "fork-modified" if f in FORK_TOUCHED else "upstream-carried"
    how = "whole" if f in WHOLE else ("the fork's diff whole, the rest at the leads' lines" if tier == "fork-modified" else
                                      "the censuses; at the leads' lines" if f in leads else "the censuses")
    cov.append("| `%s` | %s | %s | %s | %s | %s |" % (path, n, inv, tier, how, ", ".join(sorted(set(leads.get(f, [])), key=lambda x: int(x[2:]))) or "-"))
expect("coverage rows", len(cov) - 2, 76)

pages, dialogs, rowsT, titles, reads = table("pages.md"), table("dialogs.md"), table("rows.md"), table("titles.md"), table("reads.md")
expect("pages", len([r for r in rows_of(pages) if "(header only)" not in r]), 37)
expect("dialogs", len(rows_of(dialogs)), 50)
expect("rows", len(rows_of(rowsT)), 48)
expect("titles", len(rows_of(titles)), 37)
rd = ["| Site | Kind | Argument(s) | Cache | The file | Its writer while ES runs | What a failure reads as |", "| --- | --- | --- | --- | --- | --- | --- |"]
seen = set()
for r in rows_of(reads):
    site = re.match(r"\| `([^`]+)`", r).group(1)
    if site in seen:
        continue  # GuiGamelistOptions.cpp:389's two atof on one line: one row
    seen.add(site)
    if site not in WRITERS:
        fail.append("no writer entry for " + site)
        continue
    cells = [c.strip() for c in r.strip("|").split("|")]
    rd.append("| %s | %s | %s | %s | %s | %s | %s |" % (cells[0], cells[1], cells[2], cells[3], *WRITERS[site]))
for k in WRITERS:
    if k not in seen:
        fail.append("a writer entry without a site: " + k)
expect("read sites", len(rd) - 2, 25)
ns = ["| File | Added | Removed |", "| --- | ---: | ---: |"] + ["| `%s` | %d | %d |" % x for x in NUMSTAT]
expect("numstat pairs", len(ns) - 2, 12)
if sum(a for _, a, _ in NUMSTAT) != 1207 or sum(r for _, _, r in NUMSTAT) != 129:
    fail.append("the numstat pairs do not sum to 1207/129")

if fail:
    for f in fail:
        print("FAIL t31-02: " + f)
    sys.exit(1)
out = tpl
for key, lines in (("COVERAGE", cov), ("PAGES", pages), ("DIALOGS", dialogs), ("ROWS", rowsT), ("READS", rd), ("TITLES", titles), ("NUMSTAT", ns)):
    out = out.replace("{{%s}}" % key, "\n".join(lines))
if "{{" in out:
    print("FAIL t31-02: a placeholder is left"); sys.exit(1)
(A / "02-forward-audit.md").write_text(out)
print("t31-02: coverage 76, pages 37, dialogs 50, rows 48, reads 25 sites (26 calls), titles 37, numstat 12; wrote 02-forward-audit.md")
