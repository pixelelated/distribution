# Research notes — M6.P2 T12, the VM harness (#659)

## Scope

- **The read hash:** `8ebaf8daad`. The 60 are read from its bytes, in the export `.qa-scratch/t12/at-hash/`. `reviewed-at` is `facb2ae523`, the branch `HEAD` at stage A, whose 60 paths equal the hash's: `tr '\n' '\0' < .qa-scratch/t12/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD --` is empty.
- **The filter:** brief § 2's block over `docs/reviews/inventory.json` (P1's `2174265e9c`). The area is `tooling-and-guards`; the names are `vm-*, vm-walks/**, frame-diff, time-to-play, emulator-exit-test, es-launch-memory, signin-memory, png-blackout, qa-accounts, ra-*, raofflineproxy-*, device-act, es-syntax-check, es-untranslated, font-stems`. Its output:

```
paths 60 lines 8790 {'fork-own': 60} {'n/a': 60} {'shell': 10, 'python': 20, 'markdown': 2, 'other': 22, 'text': 3, 'image': 3}
the glob also selects, in other areas: 0 paths (expect 0)
```

- **The counts,** equal to the brief:
  - 60 paths and 8,790 lines, all 60 fork-own;
  - 20 Python, 10 shell, 22 `.steps` (`other`), 3 text, 2 Markdown, 3 PNG (`image`);
  - reach `n/a` 60.
  - Bytes: 484,627 (`git cat-file -s` summed).
  - `wc -l` at the hash sums to 8,813: the three PNGs hold 23 newline bytes, and the inventory stores no line count for an image. The per-path list is `.qa-scratch/t12/lines-at-hash.txt`.
- **Provenance:** none of the 60 is on `upstream/next` (`git cat-file -e` fails for each). There are 145 fork commits since `c445081a59` (144 without merges).
- **The branch against the hash:** empty over the 60.
- **The interacting subsystems** (read-only context):
  - the image under test;
  - the cloud suites and `tools/cloud-test-backend` (another slice's);
  - `register-check`, `vocabulary-check` and `es-menu-map-check` (called by `vm-qa`);
  - the host's memory (`device-builds.md`);
  - the M7 lane's guests (the host file);
  - the fork CI (`fork-checks.yml:45-48`).

## Phase 1: what each tool is

To be written at stage B, from the export.

## The no-guest controls' baseline

The no-guest controls are recorded in `00` § Stage A: three controls rc 0, `vm-qa --list` with 17 names, the usage lines, and `es-syntax-check` rc 2, which is not a pass.
