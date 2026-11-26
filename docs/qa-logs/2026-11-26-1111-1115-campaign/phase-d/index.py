#!/usr/bin/env python3
# #1111/#1115 phase D: write evidence-index.json (schema 1) from the frames
# under build13-<res>/<lang>/<screen>/, with each screen's trigger, expected
# state and the criteria it feeds. A frame is "reviewed" only when its
# <res>/<lang>/<screen> is listed in reviewed.txt (one per line), which is
# written as the sheets are actually looked at; the rest stay "captured".
#   python3 -I index.py
import hashlib, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SOURCES = {
    "build13": {"es": "c0fd03e1b (local m7/rc-round-es-20261125; route m7-20261126-16a1ec4e624a)",
                "distribution": "bc81894fa826e118d43f19ce9d3e5e94709ea4c5 (local build/m7-rc-round-20261125, build 13)",
                "image": "pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261126T161646Z.gbc81894fa826-from-ROCKNIX",
                "walk": "docs/qa-logs/2026-11-26-1111-1115-campaign/phase-d/phase-d.sh"},
    "build15": {"es": "334ee42b8 (local m7/rc-round-es-20261125; route m7-20261126-3817c3c0b12f)",
                "distribution": "90b95f7259c107d17a90e73b6d62999a06eb56c0 (local build/m7-rc-round-20261125, build 15)",
                "image": "pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261126T214410Z.g90b95f7259c1-from-ROCKNIX",
                "walk": "docs/qa-logs/2026-11-26-1111-1115-campaign/phase-d/phase-d.sh"},
    "build14": {"es": "6cdcb7a64 (local m7/rc-round-es-20261125; route m7-20261126-552f3815e4b4)",
                "distribution": "ed61fe8e5922f3106cb35230fed0027f4f7fc431 (local build/m7-rc-round-20261125, build 14)",
                "image": "pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261126T192845Z.ged61fe8e5922-from-ROCKNIX",
                "walk": "docs/qa-logs/2026-11-26-1111-1115-campaign/phase-d/phase-d.sh"},
}
SOURCE = {"es": "c0fd03e1b (local m7/rc-round-es-20261125; route m7-20261126-16a1ec4e624a)",
          "distribution": "bc81894fa826e118d43f19ce9d3e5e94709ea4c5 (local build/m7-rc-round-20261125, build 13)",
          "image": "pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261126T161646Z.gbc81894fa826-from-ROCKNIX",
          "walk": "docs/qa-logs/2026-11-26-1111-1115-campaign/phase-d/phase-d.sh"}
SCREENS = {
    "s01": ("the hub, CHANGE CLOUD FOLDER LOCATIONS, USE pixelelated DEFAULTS, NO",
            "SET CLOUD FOLDER LOCATIONS names the connection; three locations; the defaults preview names the connection and the three paths; NO leaves the page as it was",
            ["1111 C03", "1111 C18", "1111 C20", "1111 C21", "1111 C24"]),
    "s02": ("a custom saves folder set by cloud_remote set-folder, then USE pixelelated DEFAULTS, YES",
            "the editor shows /Custom/Saves; after YES the three defaults", ["1111 C21", "1111 C20"]),
    "s03": ("the content folder set to / by cloud_remote set-folder", "ROMS, BIOS, AND GAME CONTENT FOLDER reads CLOUD ROOT (/)", ["1111 C19"]),
    "s04": ("an explicit empty selection (active-connection emptied)",
            "the hub: NO CONNECTION SELECTED, and CHANGE CLOUD FOLDER LOCATIONS gives the choose-a-connection sentence; the editor: FOLDER LOCATIONS UNAVAILABLE with MANAGE CLOUD CONNECTIONS",
            ["1111 C10", "1111 C11", "1111 C03", "1480 c1"]),
    "s05": ("SAVES_REMOTE in cloud_sync.conf changed behind the profile (a restored pointer)",
            "the hub names the connection with CONFIRM THIS CONNECTION'S FOLDER LOCATIONS...; the editor shows REVIEW FOLDER LOCATIONS",
            ["1111 C11", "1480 c2"]),
    "s06": ("SYNC SAVES WHEN EXITING A GAME switched on on the hub, then USE pixelelated DEFAULTS",
            "the refusal: TURN OFF BOTH AUTOMATIC SAVE SYNC OPTIONS...; the switch off again", ["1111 C06", "1111 C22", "1111 C03"]),
    "s07": ("one saved connection", "MANAGE CLOUD CONNECTIONS: AVAILABLE CONNECTIONS, QA-CLOUD IN USE, ADD A NEW CONNECTION", ["1111 C12", "1111 C03"]),
    "s08": ("a second connection added through the installed module (conn.py add-two)",
            "AVAILABLE CONNECTIONS lists QA-CLOUD IN USE and QA-TWO; ADD A NEW CONNECTION below", ["1111 C12"]),
    "s09": ("the connection's own page", "CLOUD CONNECTION with CHANGE CLOUD FOLDER LOCATIONS", ["1111 C18", "1111 C03"]),
    "s10": ("CLOUD FOLDER ACTIONS, CHECK CLOUD FOLDERS with the default categories, each instruction page",
            "CLOUD FOLDER CHECK COMPLETED: five categories with paths, NOT CHECKED for the three unselected; a category-specific instruction page each; CLOUD FOLDERS has CHANGE CLOUD FOLDER LOCATIONS",
            ["1111 C16", "1111 C17", "1111 C18", "1111 C24", "1115 C04"]),
    "s11": ("4,097 files in the QA cloud's settings backup folder", "COULDN'T FINISH; SETTINGS BACKUPS CHECK INCOMPLETE with FOLDER ACCESSIBLE; saves still found",
            ["1115 C02", "1115 C04"]),
    "s12": ("the WebDAV URL pointed at a dead port", "COULDN'T FINISH; each folder COULDN'T READ THIS FOLDER", ["1115 C04"]),
    "s13": ("CHECK CLOUD SETUP", "CLOUD SETUP CHECK: the connection, CLOUD ANSWERED..., the local folders, the sync switches, the folder checks", ["1111 C18"]),
    "s14": ("MANAGE CLOUD CONNECTIONS, LINK FROM A COMPUTER", "CLOUD STORAGE SETUP with CHANGE CLOUD FOLDER LOCATIONS and the saves path", ["1111 C18"]),
    "s15": ("no saved connection (rclone.conf moved aside)", "the hub, MANAGE CLOUD CONNECTIONS and (from build 14) CHECK CLOUD SETUP with nothing saved; from build 14 the line is ADD A CONNECTION BEFORE USING CLOUD TOOLS.", ["1111 C12", "1482 c1", "1482 c2"]),
    "s16": ("CHECK CLOUD SETUP, to the bottom of the page", "CHANGE CLOUD FOLDER LOCATIONS, CHECK OTHER CLOUD FOLDERS, MANAGE CLOUD CONNECTIONS", ["1111 C18"]),
    "s17": ("cloud_remote set-folder saves / (refused by the profile module: Choose a separate folder for saves or settings backups.)",
            "the hub's line and the editor unchanged at /pixelelated/Saves: a saves folder at the cloud root cannot be set",
            ["1480 c1"]),
    "s18": ("a second connection (qa-two) removed from its own page: REMOVE CONNECTION, CANCEL, then REMOVE CONNECTION",
            "the confirmation says cloud files stay and what an active connection needs; CANCEL leaves the page; after removal QA-CLOUD alone, still IN USE",
            ["1111 C01", "1111 C08"]),
    "s19": ("EDIT CONNECTION on qa-two after its endpoint stopped answering: backed out of, then SAVE CONNECTION, UPDATE CONNECTION",
            "backing out changes nothing; the update re-verifies, fails with THE CONNECTION COULDN'T BE SAVED. and its reason, and the section is kept byte for byte (two-hash before and after in s19.arm.log)",
            ["1111 C03", "1111 C06", "1111 C08"]),
    "s20": ("a line before rclone.conf's first section (an unreadable setup)",
            "each page says the setup could not be read rather than no selection or a connection failure",
            ["1111 C11"]),
    "s21": ("the saves folder changed while CLOUD FOLDERS is open, then CHECK CLOUD FOLDERS",
            "THE CLOUD CHECK IS NO LONGER CURRENT. REOPEN CLOUD FOLDERS AND CHECK AGAIN.: the stale wording, for the context change only",
            ["1111 C11", "1111 C14"]),
    "s22": ("the selection emptied while CLOUD FOLDERS is open, then CHECK CLOUD FOLDERS",
            "not the stale wording: the no-selection case is told apart from a changed context",
            ["1111 C11"]),
    "s23": ("a connection saved but the selection emptied: MANAGE CLOUD CONNECTIONS and CHECK CLOUD SETUP",
            "both pages still read CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS. (#1482 leaves this case as it was)", ["1482 c3", "1111 C10"]),
    "s25": ("a fresh device: no rclone.conf and no folder-profiles.json (both restored after)",
            "setup-info STATE=no-connections; CHECK CLOUD SETUP and MANAGE CLOUD CONNECTIONS read ADD A CONNECTION BEFORE USING CLOUD TOOLS.", ["1482 c1", "1482 c2", "1111 C12"]),
    "s26": ("every connection removed through cloud_connections.remove (all files restored after)",
            "setup-info STATE=no-connections; the same two pages read ADD A CONNECTION BEFORE USING CLOUD TOOLS.", ["1482 c1", "1482 c2", "1111 C01", "1111 C12"]),
    "s27": ("diagnosis: after s15, the four files' hashes, then adding qa-two, a bare listing of qa-cloud and the state (values never printed)",
            "add rc and the listing in s27.arm.log; the hub frame only", ["1111 C06"]),
    "s28": ("EDIT CONNECTION saved on a working qa-two, which is not the active connection",
            "CONNECTION SAVED (YOUR CURRENT CONNECTION HAS NOT CHANGED...), then back to the connection's page; the section's hash unchanged", ["1483 c2", "1111 C08"]),
    "s29": ("SIGN IN AGAIN on an OAuth-tier connection (qa-oauth, type dropbox, no sign-in), then back from the choice page; no typing method is chosen, so nothing reaches the provider",
            "on build 14 back skips the connection's page to MANAGE CLOUD CONNECTIONS (#1486, before the fix); from build 15 it returns to the connection's page", ["1486 c1", "1486 c2"]),
    "s30": ("LINK FROM THIS DEVICE, AMAZON S3 AND COMPATIBLE, its first service, the form and its lower half; nothing submitted",
            "from build 15 the mapped row labels read in French in French (#1485); in English as before", ["1485 c1"]),
    "s31": ("a working copy of qa-cloud added to rclone.conf as qa-ext outside the interface, after the profile store exists; then USE THIS CONNECTION on QA-EXT",
            "from build 16: the hub, CHECK CLOUD SETUP and MANAGE CLOUD CONNECTIONS read CLOUD CONNECTIONS CHANGED, QA-EXT reads NOT CHECKED YET, and USE THIS CONNECTION checks it and adds it (IN USE)", ["1489 c1", "1489 c2"]),
    "s24": ("LINK FROM THIS DEVICE, WEBDAV, then back on the provider form",
            "where the add-a-connection wizard lands on back, unchanged by #1483", ["1483 c3"]),
}
reviewed = set()
rf = HERE / "reviewed.txt"
if rf.exists():
    reviewed = {l.strip() for l in rf.read_text().splitlines() if l.strip() and not l.startswith("#")}
# A walk that did not finish keeps its frame as the record of the failure; it
# is never "reviewed", and it names the run that redid the screen.
FAILED = {"1280x800/fr/s13": "walk rc 3: the key up after the setup check was not seen; redone in build13-1280x800-extra",
          # The walk assumed back on EDIT CONNECTION returns to the connection page; on build 13 it returns to
          # the list (#1483), so the next presses opened the page again and removed qa-two. Redone on build 14.
          "640x480-more/en/s19": "walk went astray: back on EDIT CONNECTION returned to the list (#1483), and the next presses removed qa-two; no edit was saved",
          "640x480-more/fr/s19": "walk went astray: back on EDIT CONNECTION returned to the list (#1483), and the next presses removed qa-two; no edit was saved"}
FAILED.update({f"build14/640x480/{lang}/s19": "arm failed: adding qa-two could not be verified right after s15 (s19.arm.log); the walk ran on regardless, opened MEGA's form and pressed CONNECT. The driver now skips the walk of a screen whose arm failed" for lang in ("en", "fr")})
FAILED["build15/640x480/fr/s29"] = ("walk went astray: the English pass had left a profile store, so qa-oauth added behind it read as review-folders (#1489); "
                                      "the extra row moved the cursor to qa-cloud and the walk opened its EDIT form (nothing saved). Redone alone in build15-640x480-b")
# A reviewed screen whose frames show a defect says what was seen, not "as expected".
OBSERVED = {k: v for lang in ("en", "fr") for k, v in (
    (f"build14/640x480/{lang}/s15", "connections page as #1482 asks (ADD A CONNECTION...); the setup check reads SETUP COULD NOT BE READ because this arm moves only rclone.conf and leaves a profile store naming qa-cloud, an inconsistent store, not a fresh device. s25 (fresh) and s26 (all removed) are the faithful cases"),
    ("build14/640x480-c/fr/s19", "back on the edit form returns to CONNEXION AU CLOUD; the failed save ends in LA CONNEXION N'A PAS PU ÊTRE ENREGISTRÉE and the section is kept; the form's row labels are English (#1485)"),
    ("build14/640x480-b/en/s19", "back on the edit form returns to CLOUD CONNECTION qa-two; the failed save ends in THE CONNECTION COULDN'T BE SAVED and the section is kept byte for byte"),
    ("build14/640x480-d/en/s15", "s15 first after seeding: no profile store yet, so setup-info reads no-connections and both pages read ADD A CONNECTION BEFORE USING CLOUD TOOLS."),
    ("build14/640x480-d/fr/s15", "the English pass left a profile store naming qa-cloud: the setup check reads RÉGLAGES ILLISIBLES (an inconsistent store; see s25/s26 for the faithful cases)"),
    (f"build14/640x480-oauth/{lang}/s29", "before the fix: back from the choice page lands on MANAGE CLOUD CONNECTIONS, not qa-oauth's page (#1486)"),
    (f"build15/640x480/{lang}/s30", "the S3 form's mapped labels" + (" in French (#1485); SERVER SIDE ENCRYPTION and SSE KMS KEY ID are unmapped and keep rclone's names; the subtitle AMAZON S3 AND COMPATIBLE is #1490" if lang == "fr" else "")),
    (f"build15/640x480/{lang}/s24", "back on the WebDAV form lands on the provider chooser" + ("; the form's labels in French (#1485)" if lang == "fr" else "")),
    ("build15/640x480/en/s29", "after the fix: back from the choice page returns to CLOUD CONNECTION qa-oauth (#1486); oauth status idle"),
    ("build15/640x480-b/fr/s29", "after the fix: back from the choice page returns to CONNEXION AU CLOUD qa-oauth (#1486); oauth status idle"),
    (f"build14/640x480/{lang}/s24", "back on the WebDAV form lands on the provider chooser with WEBDAV focused" + ("; the form's row labels are English in French (#1485)" if lang == "fr" else "")),
    (f"640x480-more/{lang}/s20", "defect, build 13: the hub reads NO CONNECTION SELECTED and CLOUD FOLDERS asks to choose a connection for an unreadable setup; the setup check and connections page name it. Fixed in ES 6cdcb7a64 (#1111 C11)"),
    (f"640x480-more/{lang}/s22-b", "defect, build 13: a selection emptied while CLOUD FOLDERS is open gives COULDN'T CHECK YOUR FOLDERS. CHECK YOUR CONNECTION; not the stale wording, but it names a connection fault. Fixed in ES 6cdcb7a64 (#1111 C10, C20)"))}
entries = []
import sys
SKIP = set(sys.argv[sys.argv.index("--skip") + 1:]) if "--skip" in sys.argv else set()   # a run still writing
for res_dir in sorted(d for d in HERE.glob("build1[345]-*") if d.name not in SKIP):
    build, _, run = res_dir.name.partition("-")            # build13|build14, <res>[-extra|-root|-more]
    run = run if build == "build13" else f"{build}/{run}"  # build 13 keys stay as reviewed.txt has them
    res = run.split("/")[-1].split("-")[0]; w, h = (int(v) for v in res.split("x"))
    for lang_dir in sorted(p for p in res_dir.iterdir() if p.is_dir()):
        # <sNN>-b/ holds the second walk of a screen that changes state part-way.
        for scr_dir in sorted(p for p in lang_dir.iterdir() if p.is_dir() and p.name.split("-")[0] in SCREENS):
            trigger, expected, criteria = SCREENS[scr_dir.name.split("-")[0]]
            key = f"{run}/{lang_dir.name}/{scr_dir.name}"
            status = "walk-failed" if key in FAILED else "reviewed" if key in reviewed else "captured"
            for frame in sorted(scr_dir.glob("*.png")):
                entries.append({"flow_id": "cloud-folders-and-connections", "branch_id": f"{key}/{frame.stem}",
                                "document": "docs/es-menu-map.md", "anchor": "cloud", "criteria": criteria,
                                "trigger": trigger, "expected_state": expected, "source": SOURCES[build],
                                "locale": lang_dir.name, "width": w, "height": h,
                                "frame": str(frame.relative_to(HERE)), "sha256": hashlib.sha256(frame.read_bytes()).hexdigest(),
                                "status": status,
                                **({"note": FAILED[key]} if key in FAILED else {}),
                                **({"review": {"reviewer": "OS coordinator (claude-opus-5-5)", "observed": OBSERVED.get(key, "as expected"), "date": "2026-11-26"}}
                                   if status == "reviewed" else {})})
(HERE / "evidence-index.json").write_text(json.dumps({"schema_version": 1, "issue": [1111, 1115, 1480], "entries": entries}, indent=1) + "\n")
print(f"{len(entries)} frames, {sum(e['status'] == 'reviewed' for e in entries)} reviewed")
