# #905: `ceremony-check` reads every dated friction entry

Fixture and outputs for the packet `fix/m6-905-ceremony-check-friction`
(brief `docs/reviews/briefs/fix-packet-905-ceremony-friction.md` at
`ee029004c6`), cut from `next` at `8ebaf8daad` on 2026-10-24.

## The counts, reproduced at `8ebaf8daad`

```bash
grep -c -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2}' docs/friction-log.md      # 445 dated entries
python3 -c "import re; L=open('docs/friction-log.md').read().splitlines(); \
  print(sum(bool(re.match(r'- (\d{4}-\d\d-\d\d) .*issue:\s*(#\d+|none|guard)', l.strip(), re.I)) for l in L))"
                                                                       # 320 the old regex read
grep -E '^- [0-9]{4}-[0-9]{2}-[0-9]{2}' docs/friction-log.md | grep -vic 'issue:'
                                                                       # 116 without the field
```

445 - 320 = 125 never read: 116 without an `issue:` field, 9 with one in a
shape the old regex refused (a colon or a `T` straight after the date).
Every dated line sits after `## Entries` (line 18). Of the 125, only lines
37 and 38 name no `#N`; both name a guard path that exists.

## The fixture

`friction-log.md` is `docs/friction-log.md` at `8ebaf8daad` with one line
appended: an entry dated four days before the run (`date -u -d '4 days
ago' +%F`, 2026-10-20), in the no-field shape, naming no `#N` and no
guard path.

`tools/ceremony-check` finds the log from its own location, so each run
uses a scratch tree: `tools/`, `.githooks/` and `.claude/` copied from the
worktree (so the guard paths the log names exist), the tool under test at
`tools/ceremony-check`, and the log under test at `docs/friction-log.md`.

```bash
T=<scratch>/tree; mkdir -p $T/docs
cp -a tools .githooks .claude $T/
cp <tool under test> $T/tools/ceremony-check
cp docs/qa-logs/2026-10-24-905-ceremony-friction/friction-log.md $T/docs/friction-log.md
$T/tools/ceremony-check --no-gh
```

The scratch tree is not a git checkout and has no work logs, so its
`issues`, `monthly`, `index`, `register` and `rules` lines fail; only the
`friction` line is the evidence.

| File | Tool | Log | `friction` |
| --- | --- | --- | --- |
| `fixture-before.txt` | `8ebaf8daad` | fixture | `ok` -- the added entry is never read (fails open) |
| `fixture-after.txt` | fixed | fixture | `OVERDUE: 1`, naming the added entry; 446 entries read |
| `live-before.txt` / `live-after.txt` | `8ebaf8daad` / fixed | live, in the worktree, `--no-gh` | `ok` both; the diff is the one added count line |
| `live-gate-before.txt` / `live-gate-after.txt` | `8ebaf8daad` / fixed | live, `--gate` | identical |
| `tip-before.txt` / `tip-after.txt` | `ee029004c6`'s / fixed | `ee029004c6`'s (463 dated) | `ok` both; 463 entries read |
| `noheading-before.txt` / `noheading-after.txt` | `8ebaf8daad` / fixed | live with `## Entries` renamed, `--gate` | nothing / `BLOCK` |

`live-*.txt` also show the `weekly` line overdue at `8ebaf8daad` (no
2026-W42 summary); that is the tree's, before and after alike.

The 37 lines under `## Entries` that are not entries are the five prose
blocks' headings and paragraphs (171-177, 488-502, 519-534, 719-725). The
fixed check names them on its count line; it does not move them. Indented
lines straight after an entry (508-512, 537-540) are read as that entry's
continuation, so an owner written there counts.
