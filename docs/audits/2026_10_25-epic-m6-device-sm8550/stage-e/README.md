# T28 stage E: the stream's cases (#675)

One stream, S1, under `docs/reviews/briefs/t28-streams.md` at `ad168e6d55`. Each case runs on the host in `bwrap` against fixture paths, never on the Nova (D-QA-015, D-QA-027). `TMPDIR` must point under `/workspace/tmp/m6-t28/`.

| Stream | File | Driver | Cases | Bug |
| --- | --- | --- | --- | --- |
| S1 | `projects/ROCKNIX/devices/SM8550/bootloader/update.sh` | `s1/update-case.sh <update.sh> <unfixed\|fixed> <case>` | `updateabl-fail`, `updateabl-slow-fail`, `copy-fail` (each must fail closed when fixed) and `success` (unchanged) | #1109 |

```bash
# the unfixed side is the file at the stage-D tip b13d5d8074 (= 8ebaf8daad's bytes)
git show b13d5d8074:projects/ROCKNIX/devices/SM8550/bootloader/update.sh > "$TMPDIR/unfixed-update.sh"
docs/audits/2026_10_25-epic-m6-device-sm8550/stage-e/run-all.sh "$TMPDIR/unfixed-update.sh" projects/ROCKNIX/devices/SM8550/bootloader/update.sh
```

`run-all.sh` prints 9 rows: the four cases on each side, and the success path's console output compared between the two files. It ends `run-all: 9 rows, 0 unexpected, 0 could not run`. `s1/out-unfixed/` holds the test-first runs (the unfixed file against both expectations, the failing cases `UNEXPECTED` on the fixed side), and `s1/out-fixed/` the fixed file's runs.
