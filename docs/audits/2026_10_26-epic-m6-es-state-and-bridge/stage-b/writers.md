### 1. `AtomicFile::` at the pin

| Where | Call | Kind | Temp-and-rename or in place | fsync | Lock | Mode | Positive check | A failure leaves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| es-app/src/SaveStateBookkeeper.cpp:64 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-app/src/SaveStateBookkeeper.cpp:71 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-app/src/SaveStateBookkeeper.cpp:85 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-app/src/guis/GuiMenu.cpp:5066 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none (the journey record, written once per restore) | -1: 0644 when new | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-app/src/guis/GuiSaveState.cpp:33 | isFlockHeld | read (an flock question) | - | - | asks the cloud transfer's flock | - | - | - |
| es-core/src/Settings.cpp:524 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | -1: the live file's, 0644 when new | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/Settings.cpp:533 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | modeOf(path, 0644) | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/Settings.cpp:617 | copy | write | temp-and-rename, through writeText | file and directory | none | the source's mode | the read's ok and the write's result | as writeText |
| es-core/src/Settings.cpp:626 | readText | read | - | - | none | - | - | - |
| es-core/src/Settings.cpp:629 | modeOf | read (mode) | - | - | none | - | - | - |
| es-core/src/Settings.cpp:630 | readText | read | - | - | none | - | - | - |
| es-core/src/Settings.cpp:631 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | none | modeOf(path, 0644) | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/SystemConf.cpp:75 | parseKeyValues | read (the parse) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:77 | parseKeyValues | read (the parse) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:91 | PidLock | write | lock file linked into place holding the pid | - | is the lock | 0644 (the lock file) | link() result; a stale holder by kill(pid, 0) | a staging file `.new.<pid>.<n>` when killed between its create and the link |
| es-core/src/SystemConf.cpp:94 | chooseConfig | read (the ladder) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:96 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:108 | readText | read | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:110 | writeText | write | temp-and-rename (`path`.tmp.<pid>.<n>, O_EXCL) | file and directory | PidLock /tmp/.system.cfg.lock (5 s) | -1: the live file's; recordLastGood: every copy's | the rename's result; the write's and fsync's | the old file whole; a kill before the rename leaves its temporary, which nothing sweeps (stage-b/positives/kill-writer.out) |
| es-core/src/SystemConf.cpp:120 | chooseConfig | read (the ladder) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:128 | PendingChange | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:133 | PendingChange | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:173 | pendingAfterReload | read (pending changes) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.cpp:217 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:218 | loadUnderLock | write | a recovery written back through writeText | file and directory | PidLock, re-chosen under it | every copy's shared bits | RecoveryWrite::Written | the chosen text read, the file as it was |
| es-core/src/SystemConf.cpp:223 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:225 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:232 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:243 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:248 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:253 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:262 | RecoveryWrite | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:267 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:277 | LoadedConfig | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:304 | saveUnderLock | write | temp-and-rename, through writeText, onto the text read under the lock | file and directory | PidLock /tmp/.system.cfg.lock, 5 s | the live file's, or every copy's on a recovery | LockedSave::Written only after the rename | the old file whole; the change kept in memory (LockBusy, Unreadable, WriteFailed) |
| es-core/src/SystemConf.cpp:309 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:312 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:315 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:320 | LockedSave | type or comment | - | - | - | - | - | - |
| es-core/src/SystemConf.cpp:328 | parseKeyValues | read (the parse) | - | - | PidLock /tmp/.system.cfg.lock (5 s) | - | - | - |
| es-core/src/SystemConf.h:21 | pendingAfterReload | read (pending changes) | - | - | - | - | - | - |

### 2. `writeAllText(` call sites at the pin

| Where | What | Temp-and-rename or in place | fsync | Lock | Mode | Positive check | A failure leaves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| es-app/src/ApiSystem.cpp:1017 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1020 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1718 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1796 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1936 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1948 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1955 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1970 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1971 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:1972 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2104 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2107 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2128 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2130 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2132 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/ApiSystem.cpp:2141 | sysfs (a kernel attribute, not a file on the card) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/CaptureRotation.cpp:175 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/FileData.cpp:2213 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/KeyboardMapping.cpp:426 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/KeyboardMapping.cpp:429 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/ThreadedCloudSync.cpp:944 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/Win32ApiSystem.cpp:979 | the Windows build only (not built on ROCKNIX) | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | - |
| es-app/src/guis/GuiKeyboardLayout.cpp:164 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/guis/GuiMenu.cpp:11587 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |
| es-app/src/services/HttpApi.cpp:258 | a file on the card | in place: fopen "wb" truncates (FileSystemUtil.cpp:1434) | none | none | the umask's (0644) | none: void, fwrite and fclose unchecked (:1442-1443) | an empty or cut file where the old one was |

Left out: the definition and the declaration, es-core/src/utils/FileSystemUtil.cpp:1429, es-core/src/utils/FileSystemUtil.h:71.

### 3. The shell writers of system.cfg at 8ebaf8daad (T1's files, read here)

| Where | What | Temp-and-rename or in place | fsync | Lock | Mode | Positive check | A failure leaves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 001-functions:435 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:467 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:498 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:603 | a rename of ${J_CONF}.tmp (write_setting_line, del_setting, sort_settings, set_settings) | temp-and-rename | none | wait_lock /tmp/.system.cfg.lock (the caller's) | the live file's and the record's shared bits (prepare_settings_temp, #421) | the pipeline's status under pipefail; mv's | the old file whole and the shared .tmp (stage-b/positives/shell-writers.out K1, K2) |
| 001-functions:542 | the image's seed copied over a missing system.cfg (set_setting, set_settings) | in place: cp | none | none: before wait_lock | the seed's (0644 shipped) through cp | none | the seed, which the interface's next load records over the player's record (shell-writers.out S1) |
| 001-functions:595 | the image's seed copied over a missing system.cfg (set_setting, set_settings) | in place: cp | none | none: before wait_lock | the seed's (0644 shipped) through cp | none | the seed, which the interface's next load records over the player's record (shell-writers.out S1) |
| chksysconfig:70 | put(): a whole copy through ${dst}.tmp (backup, restore, the reseed of system.cfg) | temp-and-rename | none | none (boot and shutdown, before and after the interface) | prepare_settings_temp's for put() | the copy's and mv's status | the old file whole |
| chksysconfig:324 | the reseed of missing files under /storage/.config | rsync's own temp-and-rename, missing files only | none | none (boot and shutdown, before and after the interface) | rsync -a: the image's | rsync's status | the old file whole |
| post-update:160 | post-update's edit at the update's first boot | in place: busybox sed -i (its own temp and rename) | none | none | sed -i's: the temp's, not always the file's | none | T1's PL-014 (cited) |
| post-update:202 | post-update's edit at the update's first boot | in place: busybox sed -i (its own temp and rename) | none | none | sed -i's: the temp's, not always the file's | none | T1's PL-014 (cited) |

Rows: AtomicFile 41 (9 writes), writeAllText 25 (16 sysfs), shell 10.
