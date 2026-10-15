# PPSSPP selected-state checker: #599 source and host controls

This packet retains the exact released checker/test source and upstream-source comparison, the three original host runs, and all 14 public PPSSPP defaults used by the passing suite. The correction is limited to the fork policy checker and its fixtures; frozen product f863 and the H700 firmware were not changed.

The generic parser rejected the valid spaced key `Enable Logging`, present in every shipped profile. The same review found that the checker did not recognize PPSSPP's actual `AchievementsUserName` and `AchievementsToken` keys. The PPSSPP-specific parser/classifier now handles these forms while preserving case/section semantics, conservative syntax refusal, duplicate/include controls, recovery siblings and private-value suppression. Other emulator grammars remain unchanged. Detailed pinned-source/upstream findings and lookup limits are retained inside `source/README.md` in the archive.

| Original host run | Command / monitor / runner | Scope and outcome |
| --- | --- | --- |
| 20261015T063603Z-569772e6 | 2 / 0 / 2 | Full-suite attempt stopped at the required-tool precondition; no fixture ran. |
| 20261015T063732Z-ab3404de | 2 / 0 / 2 | Unchanged-source diagnostic traced the same precondition at line 767; no fixture ran. |
| 20261015T063831Z-c75018f3 | 0 / 0 / 0 | All 212 controls passed, including 40 PPSSPP controls and all 14 shipped profiles. |

The first two failures are preserved. Root diagnosed absent host `mcopy` in PATH, with the seven other prerequisites available. For run03, root created only a private `bin/mcopy` link to the existing H700 buildroot host tool. Its target resolves to `build.pixelelated-H700.aarch64/toolchain/bin/mtools`, SHA256 `2949bcce7f951f571d32f5d5d915d86d5a582a633f31b4ebef5b8d97a68ad0f6`. The original link, hash file and metadata are retained; the binary is not duplicated. No source correction was needed between these attempts.

Root executed and supervised the suite. This retaining worker only read source/original results, checked hashes and metadata, and created this compact archive. Original runner-result.json, build.rc, build logs, watcher copies and diagnostics remain exact. Root reported short exec session62150 completed with original exit0 (tool chunk2199e3), then observed four recorded PIDs absent and scratch empty (chunk5a190d). No separately persisted outer-exec producer receipt exists; `evidence-readback.json` labels that information as a root observation. The retaining worker independently found the recorded numeric /proc paths absent and all three scratch directories empty at custody time; this is not a whole-host process or descriptor census. Historical terminal status files are unchanged, including their then-current `alive=yes` text.

The archive has 88 members: 74 regular files, 13 directories and one symlink, totaling 612,397 regular-file bytes. It preserves the original source seals, three owner/watch trees, and public defaults. `member-manifest.json` maps every archive member to its original source path, hash, permission mode, UID/GID and exact nanosecond mtime. Verification used `stat.S_IMODE` and exact decimal PAX timestamps, with no float conversion. Original bytes and metadata were rechecked unchanged after archiving. The private mcopy symlink is archived without following it; archive custody does not authorize executing its target.

Source seal: `ab24bb4b4ec48c2db03ffde9fc3acc2b42eed5402241cc4205f03f0bcf588ecb`.
Released checker SHA256: `65ab515ec2c0ccdf474f08128cabf1dea774846a8add3725cd05d334b2e1eba6`.
Released test SHA256: `6e0b2eb945b913ad0c176dd532586463493e6984240e128ff771ce6264fd3eec`.

The sealed source packet's UNRUN/source-only status describes its preparation time; the later root-owned host results are additive evidence. Root independently verified every archived member against original bytes/modes/ownership/nanosecond times and confirmed the finite review in `local-review.md`. The original draft and outer seal remain in the private root-review record. Independent external review was not run. Actual H700 update-payload acceptance and the separately hash-bound SM8550 reader remain pending; passing synthetic host controls and public defaults do not establish either firmware result or physical-device behavior. The original H700 acceptance failure is retained separately at `/tmp/pix-m7-h700-state-failure-20261015` and is not relabeled here.

No VM, compiler, target runtime, admission, registry, original receipt or shared tracker was changed during custody. The outer SHA256SUMS binds this README, local review, evidence readback, member manifest and archive. No disk, build cache or private player configuration is included.
