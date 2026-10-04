# Replacement05: default, upgrade, content and settings qualification

Refs #383, #344, #409, #320, #420, #421, #416, #417, #419.
Can this be done on the VM? **Yes:** clean boot, actual retained ROCKNIX RC2
upgrade, and a disposable copy-on-write guest for the installed settings race.
Image content analysis reads the emitted bytes without executing them.

Frozen distribution `1e6a156b5477650e298b6a4dfff996673bf33fb1`;
immutable bundle `a179bd73a732f49c4219177c89a860d561dad4d16a3467aae2cbafc15152b3ea`.
Input manifest and complete build provenance are retained beside this directory
in `2026-10-04-pixelelated-replacement-05/`. No product input changed during QA.

| Owner | Actual tool result | Observed outcome |
| --- | --- | --- |
| qa-05 | 43844, exit 0 | All 15 defaults, 16 visual walks/78 frames, baseline comparison, actual RC2 upgrade, exact clean/upgraded payloads and source/bundle custody pass. Finished 20:30:56 UTC. |
| image-06 | 37162, exit 0 | Raw-image and update SYSTEM are byte-identical; extracted without executing image binaries. |
| sweep-03 | 97815, exit 0 | Complete content classification and localisation checks pass, including 10 scanner controls and consumed pugixml 1.16 theme parsing. |
| settings-05 | 48514, exit 0 | Actual installed ES race: 20 checks. Installed writers: 29 mode/refusal checks. Exact restoration and backing-disk rehash pass. Finished 20:33:53 UTC. |
| link-05 | 32413, exit 0 | Seven WebDAV and seven S3 interruption/retry cases pass (494s/460s). Cleanup, candidate/source custody and actual owned process/container exits pass. Finished 20:51:28 UTC. |
| guest-05 | 59664, exit 0 | All19 independently reset cases,249 checks/0failures.87 walk frames/1467 total captures;15 selected frames inspected and retained. Exact custody and owned exits pass. Terminal watcher21:33:30UTC. |
| runtime-05 | 70320, exit 0 | Actual RC2 archive recovery14, timing4, installed identity/Tools consumer13 assertions pass. Five measured transfers per layout, medians266/237ms (29ms difference, limit30ms); every transfer hash matches, no source override. Actual exits/backing rehash pass. |
| proxy-04 | 35719, exit 0 |20 installed-module checks preserve predecessor database/cache/sign-in/images and queued base/subset awards, including the real offline HTTP service. Source/bundle custody and actual exits pass. Terminal21:36:18UTC. |
| optins-04 |83669, exit0| S3 roundtrip PASS110s; actual RC2/fresh pair42PASS/0FAIL with upgrade, shared data move/follow, byte-exact save exchange and provider refusal. All result channels/custody/owned exits pass. |
| memory-04 |86046, exit0| Virgl10/software10/software50 with exit-sync pass unchanged limits: VmSize growth0KiB, RSS growth608/280/620KiB.30s HTTPS sign-in load passes; actual cleanup/custody verified. |

Each completion JSON reconciles command/inner/outer/wrapper results and records
actual host process exit. A terminal status file's last `alive=yes` observation
is not an indication that the recorded process remains alive.

The image/update SYSTEM SHA256 is
`14f75c8ef576b19f0d79c8ddd2a1a93b24055f4fd38a52e1643dcf4bad7d2b24`.
The content scan reads 57,292 regular entries and 1,345 symlinks. All 8,589
branding contexts are classified, with zero FIX or UNKNOWN findings. Seventy
broad credential-pattern matches are reviewed public constants/self-test data,
with zero unclassified matches; this is not a claim of zero regex matches or a
universal security audit. Only the owned extracted shadow copy changed mode
0000 to 0400 for analysis; the immutable image was unchanged and no matching
credential value was printed.

French reconciliation retains 794 current translations, 57 retired IDs,
2 removed IDs and 95 XML entries, with zero active orphans. Installed Tools
XML parses and matches corrected source. Its actual upgraded `/storage` consumer also passes bytes and strict XML
parsing in runtime-05. Displayed Tools rows remain assigned to ui-04.

The settings proof pauses the actual installed ES after recovery releases its
lock, lets actual `set_setting`/`chksysconfig` publish newer live and recovery
bytes, then resumes the same ES. Both newer files survive and remain 0600.
The 29 installed writer checks also cover private recovery records, permissive
staging files, restrictive group modes, and symlink/chmod/stat/producer/rename
refusals. Original settings and product hashes are restored/verified; the
actual RC2 backing disk remains unchanged. Prior failed probes and the old
02163 permission failure remain recorded in `2026-10-04-settings-race-and-modes/`.

Raw logs and frame hashes are indexed in `qa-artifacts.json`. The default
one-sample timing report retains its unresolved stamp caption; runtime-05 supplies the separate
isolated timing gate recorded above. Remaining bilingual UI/boot, inherited RC2-script recovery, synthetic subset flush and ordinary achievement evidence, followed by the approved
primary + Fable 5.1 review, still gate the RC call. No Daybreak coverage is
claimed. No personal-cloud or physical-device action was taken.

Proxy preservation is synthetic predecessor data on packaged Python3.14 with
no source override, external networking removed and upstream loopback port9.
It verifies queued base100/subset200 state without attempting a live award or
flush. The original terminal echo still says replacement01; exact BUILD_ID,
source/bundle verification and artifact provenance identify replacement05.
The executed harness and its original output remain unchanged. The new pin's
270 Linux/native files are byte-identical to the refreshed tested source;
upstream preservation fix remains present and duplicate017 retired. See the
current-pin receipts under ../2026-10-04-proxy-aec99c/ and source preservation
under ../2026-10-03-proxy-refresh/.
