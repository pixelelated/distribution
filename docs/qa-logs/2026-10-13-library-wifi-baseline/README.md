# M7 library-copy and Wi-Fi baseline — October 13, 2026

The owner's testing-first request is quoted in `plan.md`. These are unchanged-image
controls and defect reproductions, not fixed-source or release-candidate qualification.
No handheld, personal account, cloud transfer or game launch was used. No compiler
or full build-cache copy ran; #493 mandatory launch enforcement precedes compilation.

## Source, allocation and lifecycle

Accepted VM20 distribution `1a026648442321609b2288c2c9c06803817f9df2`, ES
`c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`; installed ES SHA256
`db136580f0a46442bb3fe7ac9e31606b38b816c78efc8f9b4e267284daca6502`.
The compressed image's adjacent SHA256 was verified before expansion. The
standard 8192MiB/4vCPU guest used a 16GiB sparse disk, first 640×480 then,
serially, 1280×800. Both boot identities and the unchanged binary hash are
retained in the compressed identity receipts. Wi-Fi uses a bind-mounted synthetic
`wifictl`; it cannot join a network and never invokes NetworkManager.

Eight watched stages are consumed in `consumption-retirement.json`: six return0;
`library-owner` and `collection-library02-owner` retain their original failures1.
The four collection controls inside the latter completed0 before its subsequent
library fixture hit a service start limit. Actual host owner/launcher/command/
watcher exits are verified separately from terminal status text. The old status
files' `alive=yes` was their final sampling instant, not a current liveness claim.
The enumeration bind was removed, exact VM stopped, disk/UEFI/temporary SSH
material retired: **2,247,536,640 allocated bytes** released. Original compact
owner records remain under `/workspace/tmp/pix-m7-baseline-tests-20261013`.
That owner is COMPLETE/RETIRED; do not replay it or its hard-coded paths.

## #565 — ROM folders can carry play history

`library03-result.json` and both full synthetic API results establish:

| Imported files | Play count | Last played | Recent membership |
| --- | --- | --- | --- |
| Same 37-byte synthetic ROM stub only | 0 | 0 | absent |
| Same stub plus ROM-side `gamelist.xml` | 5 | 20260908T031024 | present |

Recent was explicitly enabled with `favorites,recent` for this comparison.
The same stub SHA256 is recorded in both cases. No emulator launched. Selected
RetroAchievements/ScreenScraper/rclone account settings, connection files and
cloud activity-stamp files were equal before and after both imports. Values and
secret-derived hashes are not emitted. The fixture compares these named surfaces;
it is not a proof that arbitrary ROM-directory content can never affect settings,
a USB transfer test, or a complete image scan.

Together with the Nova's previously observed ROM-side metadata, this establishes
a credible copy mechanism. It does **not** prove the exact historical copy,
identify the original account writer or attribute the account fields to ROMs.
Final candidate payload and genuine retained-storage upgrade gates remain open.

The original library fixture wrongly interpreted Recent HTTP404 as an empty
collection. Its ROM-only PASS line is invalid as membership evidence; its overall
failure1 remains in `library-result.json`. The corrected fixture requires an
existing, empty Recent collection. A second attempt exceeded systemd's five
starts per ten seconds; `library02-service-failure.txt.gz` records
`start-limit-hit`, not an ES crash. After recording that condition, the disposable
service was reset and only the owned stub/gamelist removed. The fresh third owner
passed both cases. Pace future fixture restarts and preserve preconditions.

## #578 — an inherited default disables Recent

Four controls in `collection-result.json`:

| `CollectionSystemsAuto` | Recent API | Result |
| --- | --- | --- |
| No explicit override | 404 | default omits Recent |
| `favorites, recent` | 404 | space prevents exact match |
| `favorites,recent` | 200 | imported history appears |
| `favorites` explicitly | 404 | deliberate choice respected |

`Settings.cpp` supplies the spaced default; `CollectionSystemManager` splits on
commas and compares exact names, and `StringUtil::split` does not trim spaces.
Source history identifies `401d97370d55e3161437c2f38182224ed1322dac`.
The official ROCKNIX source check still found the same default, recorded in
`upstream-settings-check.json`. No product fix has been compiled or installed.
Correct the default narrowly and retain explicit player choices; actual fixed
binary, clean/retained behavior and same-source frames are still required.

## #577 — reproduced UI and outcome defects

Twelve English frames are indexed with the exact installed source in
`frame-index.json`. All have been reviewed. This is the accepted-source baseline;
French and fixed-source frames remain due.

- At640×480, initial search has a blank list with a separate centered searching
  overlay. Screen/footer bounds remain full-screen.
- On populated refresh, old rows **remain visible, dimmed behind the overlay**.
  An early commentary and GitHub plan note overstated this as disappearing;
  the reviewed frames correct that claim. Do not count it as a reproduced loss
  of existing rows. Search status is still outside the list.
- A successful empty scan and a failed scan (exit2) produce byte-identical
  `NO WI-FI NETWORKS FOUND` completion frames. `wifi-calls.jsonl` binds the two
  distinct command outcomes. Failure has no distinct message.
- At1280×800, initial search shows a short title/button dialog with no reserved
  list area; the dialog grows and its footer moves when three rows arrive.
  Loading appears in a separate card below the short dialog.

Use the native picker with a stable scrolling viewport and in-list status;
preserve prior rows/focus while refreshing. Carry enumeration success separately
from its rows so error is distinct from empty. Qualify duplicate refresh, pending
exit, late completion, safe focus and existing saved/open/manual/forget flows.
This baseline did not exercise all those branches and closes none of the fix's
acceptance criteria. No Wi-Fi credential, real radio or actual join was involved.

## Reproduction and remaining gates

`fixtures/` and `walks/` preserve exact executed bytes, including failed attempts.
They contain historical absolute owner paths. For a new run, allocate a fresh
QA-only owner/guest, translate those paths, provision a synthetic key through the
canonical VM helper, and post the VM-first plan before execution. Never run these
fixtures on a player's handheld. Do not reuse the retired key or replay owners.
`library-fixture03.py` requires untouched stub/gamelist paths, a ready frontend
and an explicitly enabled empty Recent collection. The collection control resets
its synthetic override deliberately; record fixture reset and service readiness
between phases. Stub ROMs are never playable inputs.

Next: #493 launch/retirement enforcement before compilation; actual #570 allocator
trim source/binary qualification; #565 next-payload/clean/retained upgrade proof;
#566/#567, #571/#577/#578, #574/#575 and stable20261001/#564; renewed combined VM
qualification and audit, then H700 followed bySM8550. Source-only memory experiments
are not product fixes, and this baseline does not allocate a new RC number.

`SHA256SUMS` binds this packet. Raw text captures/logs are losslessly compressed;
`raw-byte-identities.json` retains original hashes. Temporary key material, guest
disks and unrelated private device/provider evidence are excluded.
