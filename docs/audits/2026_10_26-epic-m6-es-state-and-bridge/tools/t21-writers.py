#!/usr/bin/env python3
"""T21 (#668): 02 § The writers, generated from the pin and from 8ebaf8daad.

    python3 -I -B t21-writers.py <es worktree> <distribution worktree> --expect-atomic N --expect-writeall N --expect-shell N

Three groups of rows, each found by a pattern rather than typed:

  1. every line naming `AtomicFile::` under es-app/src and es-core/src at
     16dbac5211 (the writer, its reads, its lock and its types);
  2. every call site of `writeAllText(` there (the definition and the
     declaration in FileSystemUtil are named and left out), each `sysfs`
     where the path is under /sys;
  3. every shell writer of system.cfg at 8ebaf8daad: a rename of
     ${J_CONF}.tmp in 001-functions, a copy of the image's seed over it, a
     chksysconfig rename, and a `sed -i` on system.cfg in post-update.

Each row: temp-and-rename or in place, fsync, the lock, the mode, the
positive check, and what a failure leaves. The classification is a rule per
call (below) with the context of the sites the lane read (SystemConf under
its PidLock, Settings under none, the journey record, the bookkeeper's
flock question). Exits 1 when a group's count differs from its --expect.
"""
import re, subprocess, sys

es, dist = sys.argv[1], sys.argv[2]
def opt(name):
    return int(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else None
PIN, BASE = "16dbac5211", "8ebaf8daad"

def grep(pattern, *paths, tree=None, repo=es, rev=PIN):
    r = subprocess.run(["git", "-C", repo, "grep", "-n", "-E", pattern, rev, "--", *paths], capture_output=True, text=True)
    out = []
    for line in r.stdout.splitlines():
        line = line[len(rev) + 1:]
        f, n, text = line.split(":", 2)
        out.append((f, int(n), text.strip()))
    return out

# ---- 1. AtomicFile:: ----
RULES = {
    "writeText": ("temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL)", "file and directory", "{lock}", "{mode}", "the rename's result; the write's and fsync's", "the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out)"),
    "copy": ("temp-and-rename, through writeText", "file and directory", "{lock}", "the source's mode", "the read's ok and the write's result", "as writeText"),
    "saveUnderLock": ("temp-and-rename, through writeText, onto the text read under the lock", "file and directory", "PidLock /tmp/.system.cfg.lock, 5 s", "the live file's, or every copy's on a recovery", "LockedSave::Written only after the rename", "the old file whole; the change kept in memory (LockBusy, Unreadable, WriteFailed)"),
    "loadUnderLock": ("a recovery written back through writeText", "file and directory", "PidLock, re-chosen under it", "every copy's shared bits", "RecoveryWrite::Written", "the chosen text read, the file as it was"),
    "PidLock": ("lock file linked into place holding the pid", "-", "is the lock", "0644 (the lock file)", "link() result; a stale holder by kill(pid, 0)", "a staging file `.new.<pid>.<n>` when killed between its create and the link"),
}
READS = {"readText": "read", "modeOf": "read (mode)", "chooseConfig": "read (the ladder)", "parseKeyValues": "read (the parse)",
         "isFlockHeld": "read (an flock question)", "pendingAfterReload": "read (pending changes)", "isUsableKeyValues": "read"}
TYPES = ("LoadedConfig", "LockedSave", "RecoveryWrite", "PendingChange")

def context(f, n, text):
    if f.endswith("SystemConf.cpp"):
        return "PidLock /tmp/.system.cfg.lock (5 s)", "-1: the live file's; recordLastGood: every copy's"
    if f.endswith("Settings.cpp"):
        return "none", "-1: the live file's, 0644 when new" if ":524" in f"{f}:{n}" or n == 524 else "modeOf(path, 0644)"
    if f.endswith("GuiMenu.cpp"):
        return "none (the journey record, written once per restore)", "-1: 0644 when new"
    return "-", "-"

atomic = []
for f, n, text in grep(r"AtomicFile::", "es-app/src", "es-core/src"):
    if f.startswith("es-core/src/utils/AtomicFileUtil"):
        continue   # the definitions themselves
    calls = re.findall(r"AtomicFile::(\w+)", text)
    call = next((c for c in calls if c in RULES), next((c for c in calls if c in READS), calls[0]))
    lock, mode = context(f, n, text)
    if call in RULES:
        how, fs, lk, md, check, rest = RULES[call]
        atomic.append((f"{f}:{n}", call, "write", how, fs, lk.format(lock=lock), md.format(mode=mode), check, rest))
    elif call in READS:
        atomic.append((f"{f}:{n}", call, READS[call], "-", "-", lock if "flock" not in READS[call] else "asks the cloud transfer's flock", "-", "-", "-"))
    elif call in TYPES:
        atomic.append((f"{f}:{n}", call, "type or comment", "-", "-", "-", "-", "-", "-"))
    else:
        atomic.append((f"{f}:{n}", call, "comment" if text.startswith("//") else "other", "-", "-", "-", "-", "-", "-"))

# ---- 2. writeAllText( ----
writeall, left_out = [], []
for f, n, text in grep(r"writeAllText\(", "es-app/src", "es-core/src"):
    if f.startswith("es-core/src/utils/FileSystemUtil"):
        left_out.append(f"{f}:{n}")
        continue
    sysfs = f == "es-app/src/ApiSystem.cpp"   # all sixteen write under /sys (the paths read at their lines)
    win32 = f.endswith("Win32ApiSystem.cpp")
    what = ("sysfs (a kernel attribute, not a file on the card)" if sysfs else
            "the Windows build only (not built on ROCKNIX)" if win32 else "a file on the card")
    writeall.append((f"{f}:{n}", what, "in place: fopen \"wb\" truncates (FileSystemUtil.cpp:1434)", "none", "none", "the umask's (0644)", "none: void, fwrite and fclose unchecked (:1442-1443)",
                     "-" if sysfs or win32 else "an empty or cut file where the old one was"))

# ---- 3. the shell writers at 8ebaf8daad ----
FN = "projects/ROCKNIX/packages/rocknix/profile.d/001-functions"
CK = "projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig"
PU = "projects/ROCKNIX/packages/rocknix/sources/post-update"
shell = []
for f, n, text in grep(r'mv -f "\$\{J_CONF\}\.tmp"', FN, repo=dist, rev=BASE):
    shell.append((f"{f.rsplit('/', 1)[-1]}:{n}", "a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings)", "temp-and-rename", "none", "wait_lock /tmp/.system.cfg.lock (the caller's)", "the live file's and the record's shared bits (prepare_settings_temp, #421)", "the pipeline's status under pipefail; mv's", "the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2)"))
for f, n, text in grep(r"cp -f /usr/config/system/configs/system\.cfg", FN, repo=dist, rev=BASE):
    shell.append((f"{f.rsplit('/', 1)[-1]}:{n}", "the image's seed copied over a missing system.cfg (set_setting, set_settings)", "in place: cp", "none", "none: before wait_lock", "the seed's (0644 shipped) through cp", "none", "the seed, which the interface's next load records over the player's record (shell-writers.out S1)"))
for f, n, text in grep(r'mv -f "\$\{dst\}\.tmp"|rsync -a --ignore-existing', CK, repo=dist, rev=BASE):
    kind = "put(): a whole copy through ${dst}.tmp (backup, restore, the reseed of system.cfg)" if "mv" in text else "the reseed of missing files under /storage/.config"
    shell.append((f"{f.rsplit('/', 1)[-1]}:{n}", kind, "temp-and-rename" if "mv" in text else "rsync's own temp-and-rename, missing files only", "none", "none (boot and shutdown, before and after the interface)", "prepare_settings_temp's for put()" if "mv" in text else "rsync -a: the image's", "the copy's and mv's status" if "mv" in text else "rsync's status", "the old file whole"))
for f, n, text in grep(r"sed -i", PU, repo=dist, rev=BASE):
    if "system.cfg" not in text:   # :101 edits a sysctl file (D-SYS-007), not system.cfg
        continue
    shell.append((f"{f.rsplit('/', 1)[-1]}:{n}", "post-update's edit at the update's first boot", "in place: busybox sed -i (its own temp and rename)", "none", "none", "sed -i's: the temp's, not always the file's", "none", "T1's PL-014 (cited)"))

def table(title, head, rows):
    print(f"### {title}\n")
    print("| " + " | ".join(head) + " |")
    print("| " + " | ".join("---" for _ in head) + " |")
    for r in rows:
        print("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    print()

table("1. `AtomicFile::` at the pin", ["Where", "Call", "Kind", "Temp-and-rename or in place", "fsync", "Lock", "Mode", "Positive check", "A failure leaves"], atomic)
table("2. `writeAllText(` call sites at the pin", ["Where", "What", "Temp-and-rename or in place", "fsync", "Lock", "Mode", "Positive check", "A failure leaves"], writeall)
print(f"Left out: the definition and the declaration, {', '.join(left_out)}.\n")
table("3. The shell writers of system.cfg at 8ebaf8daad (T1's files, read here)", ["Where", "What", "Temp-and-rename or in place", "fsync", "Lock", "Mode", "Positive check", "A failure leaves"], shell)
counts = {"atomic": len(atomic), "writeall": len(writeall), "shell": len(shell)}
print(f"Rows: AtomicFile {counts['atomic']} ({sum(1 for r in atomic if r[2] == 'write')} writes), writeAllText {counts['writeall']} ({sum(1 for r in writeall if r[1].startswith('sysfs'))} sysfs), shell {counts['shell']}.")
drift = [k for k, flag in (("atomic", "--expect-atomic"), ("writeall", "--expect-writeall"), ("shell", "--expect-shell")) if opt(flag) is not None and counts[k] != opt(flag)]
if drift:
    print("DRIFT: " + ", ".join(f"{k} {counts[k]}" for k in drift), file=sys.stderr)
    sys.exit(1)
