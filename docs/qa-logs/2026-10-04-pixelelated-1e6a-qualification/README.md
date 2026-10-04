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
XML parses and matches corrected source. Its actual upgraded `/storage`
consumer and displayed rows remain assigned to runtime-05/ui-04.

The settings proof pauses the actual installed ES after recovery releases its
lock, lets actual `set_setting`/`chksysconfig` publish newer live and recovery
bytes, then resumes the same ES. Both newer files survive and remain 0600.
The 29 installed writer checks also cover private recovery records, permissive
staging files, restrictive group modes, and symlink/chmod/stat/producer/rename
refusals. Original settings and product hashes are restored/verified; the
actual RC2 backing disk remains unchanged. Prior failed probes and the old
02163 permission failure remain recorded in `2026-10-04-settings-race-and-modes/`.

Raw logs and frame hashes are indexed in `qa-artifacts.json`. The default
one-sample timing report retains its unresolved stamp caption; the later
isolated timing gate remains required. Remaining cloud, proxy, memory,
bilingual UI/boot and ordinary achievement evidence, followed by the approved
primary + Fable 5.1 review, still gate the RC call. No Daybreak coverage is
claimed. No personal-cloud or physical-device action was taken.
