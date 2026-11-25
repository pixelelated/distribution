# M6's bugs for the M7 call: the list behind the question (2026-11-25, OS coordinator)

Made before the question goes to Max, at the steward's request. Read 2026-11-25 at 17:00 UTC from the tracker:
540 open `bug` issues; 320 under M6, 204 with no milestone (the 524), 16 under M7.

**Method, and its limits.** Shipped or not: by the paths each body cites (about 407 of the 524 cite code
the image ships, about 116 only tools, docs or process files). Severity: the body's Severity line (16 High,
66 Medium, 67 Low, 375 none). The two exposure and loss groups were selected from the titles (a leak or
loss word in one of the five areas: cloud, saves, settings, Wi-Fi, achievements), then read title by title;
test tools mislabelled as shipped were taken out. A bug whose title does not name its effect is not in
them. "Fix recorded" is from the subject of a commit on an M6 branch that cites the issue: a code commit
here, or M6's record naming an EmulationStation commit. Each one's code is read before it is taken.

## High, in code the image ships (14 of the 16 High; #969 and #970 are QA tools)

| Issue | Severity | Fix recorded on an M6 line | Title |
| --- | --- | --- | --- |
| #1170 | High | ES 698040b5c (M6 record 50b8f48175) | Bug: EmulationStation's game hasher uses and publishes a hasher its own threads may already have deleted |
| #1185 | High | T21 S1 (M6 record d3a9170e72) | Bug: EmulationStation: clearing the HOSTNAME row loses every setting (T21 PL-01) |
| #1187 | High | T21 S3 (06c5c4e685) | Bug: EmulationStation: a ROM's file name reaches `sh` inside double quotes before `7zr` runs, as root, for every `.7z` the scraper hashes; the same sh |
| #1189 | High | T21 S2 (1b2cbd2216) | Bug: EmulationStation: with `system.cfg` absent, `set_setting` copies the image's seed before the lock and without the record, and the interface's nex |
| #1208 | High | none found | Bug: the OS scripts' half of T21 PL-03: with `system.cfg` absent, `set_setting` copies the image's seed before the lock and without the record, and th |
| #1215 | High | T26 S1 (3fd5c88ffe) | Bug: EmulationStation: the REPAIR A CONNECTION picker calls `close()` on a page it already closed when the network drops before the press (T26 PL-01) |
| #1258 | High | ES e85735b0b | Bug: EmulationStation: a CANCEL as the batch scrape finishes writes through the freed `ThreadedScraper` and marks the completed run cancelled (T32 PL- |
| #1259 | High | ES b52245036 | Bug: EmulationStation: a scrape that reached nothing reads as COMPLETED: IO errors, spent 429s and failed media read as done, and the count is short b |
| #1260 | High | ES 0404e76cc | Bug: EmulationStation: a response of the wrong shape is a wild read in the shipped build: TheGamesDB's `"boxart": "x"` and IGDB's or HfsDB's numeric t |
| #1271 | High | ES dd86d7ce2 | Bug: EmulationStation: a `gamelist.xml` restored from the cloud while ES runs is overwritten by the next save with the changed entries alone (T33 PL-0 |
| #1359 | High | none found | EmulationStation: a failed font-atlas allocation leaves a dangling pointer (Font.cpp, T36 PL-06) |
| #1360 | High | none found | EmulationStation: a date format over 256 bytes overruns a stack buffer (TimeUtil.cpp, T36 PL-07) |
| #1361 | High | none found | EmulationStation: copyFile onto the same inode destroys the source (FileSystemUtil.cpp, T36 PL-08) |
| #1408 | High | none found | Bug: carried MSM resource-cleanup patches write through an uninitialized pointer |

## A password, token or Wi-Fi key exposed, in shipped code (14)

| Issue | Severity | Fix recorded on an M6 line | Title |
| --- | --- | --- | --- |
| #724 | - | e5e3a36c1f | Bug: `system.cfg` is world-readable and world-executable |
| #861 | - | T30 S3 (3429d4f29e) | Bug: Five achievements scripts keep the previous RetroAchievements session when the switch is on and the token empty, and leave the token at rest when |
| #865 | - | T30 S0 (6efdc07c2c) | Bug: gopher64 receives the RetroAchievements password on its command line, unquoted; an empty password makes the ROM path its value |
| #866 | - | none found | Bug: melonDS's script writes the RetroAchievements password in plain text into melonDS.ini every launch, with an incomplete sed escape |
| #870 | - | none found | Bug: Low: the achievements scripts write sign-in values unescaped and token files without a private mode |
| #887 | - | c60cdddf8b (fix/m6-887-melonds-toml-blank) | Bug: settings backups carry the RetroAchievements password and token from melonDS.toml |
| #889 | - | 828472eb59 (fix/m6-889-scan-toml) | Bug: backuptool's credential scan never reads a .toml for a key and value |
| #1157 | - | none found | Bug: the offline proxy's login answers any request naming the account with the cached sign-in and its session token |
| #1158 | - | 76658dd062 | Bug: every file the offline achievements proxy writes is world-readable, the store with the session token included |
| #1171 | Medium | T20 S2 (23f0f05170) | Bug: EmulationStation's RetroAchievements sign-in puts the password in the URL, and follows a redirect to http |
| #1193 | Medium | T21 S5 (63c7e8a0b6) | Bug: EmulationStation: `system.cfg`, its record and the shipped seed are 0645 on the image with `wifi.key`, `root.password` and the RetroAchievements  |
| #1204 | Low | none found | Bug: EmulationStation: the Wi-Fi key on argv (T21 PL-16) |
| #1210 | Low | none found | Bug: the OS scripts' half of T21 PL-16: the Wi-Fi key on argv (T21 PL-16) |
| #1288 | Medium | T33 S4a (c154c3e0bf) | Bug: EmulationStation: a token check in flight writes the token back after the player turned achievements off (T33 PL-23) |

## A player's saves or settings lost, in shipped code (10)

| Issue | Severity | Fix recorded on an M6 line | Title |
| --- | --- | --- | --- |
| #740 | - | none found | Bug: Engineering-image blocks overwrite the owner's `authorized_keys` and Wi-Fi files |
| #863 | - | none found | Bug: Start scripts delete a real directory before linking it, with no copy: a save state made in DuckStation from the Tools launcher is deleted by the |
| #1129 | - | none found | Bug: a flag in RCLONE_NET_OPTS reaches the content match's deleting sync unfiltered, and --delete-excluded there deletes saves (Medium) |
| #1131 | - | none found | Bug: cloud_connections.save() passes an option-shaped key to rclone as a flag, so --config= writes a connection outside rclone/; a killed save's stagi |
| #1136 | - | none found | Bug: backuptool restore plants a symlink an archive carries, and a revert over a restored-into directory fails and leaves the mark |
| #1236 | Medium | none found | Bug: EmulationStation: START (CLOSE) and a click outside the menu delete settings pages without `close()`, dropping their deferred choices (T31 PL-01) |
| #1243 | Low | ES 82f80693d | Bug: EmulationStation: USE RELAY SERVER and SHOW CONTROLLER ACTIVITY replace their pages without `save()`, dropping the deferred switches changed befo |
| #1285 | Medium | T33 S4b (5fb170a465) | Bug: EmulationStation: the other in-place writers: the rotation record, the key maps, and `saveToXml`'s remove-then-save (T33 PL-16) |
| #1299 | - | 38cf8c9d10 | Bug: cloud_restore: a stopped restore leaves the saves it was replacing absent, and the next completed restore deletes the only copies |
| #1301 | - | 38cf8c9d10 | Bug: cloud_restore, cloud_saves_root, cloud_capture: SAVESPATH's readers disagree, and an empty one reaches rclone and is blamed on the cloud |

**Totals:** 38 bugs; 22 with a fix recorded on an M6 line, 16 without.

**How a fix would be taken without touching M6** (Max, 2026-11-24: *"It's good for us to leave the milestone 6
work untouched"*): read from M6's pushed commit and applied by content onto the M7 source round, as #1012's
runner fix was today (`560188d9d4`). No M6 branch, worktree or lane is changed, and nothing is dispatched to M6.

