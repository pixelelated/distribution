# T46 — Correct current audit guidance, then finish E–H

Version 1 candidate, coordinator, 2026-11-03. This is a proposed stream
under plan §6b, D-WORKFLOW-189/225/236. It does not accept D or start E.
Root must reconcile D, obtain the unfamiliar-executor proof, publish any
corrections and explicitly dispatch this exact version on #693 first.

## 1. Owner, start and outcome boundary

Existing T3, m6-t3-emulators wN:p6, session
01a19d12-29e3-7fe0-9f41-038dac0a5deb, owns
`/workspace/repos/pixelelated/distribution.worktrees/m6-records-693`,
branch `feature/m6-records-693`. Start at clean published D
`a0d4c4fda7a0c16c04d57edf921ffeb741eff19b`, direct child of execution seed
`8710a6210a40de0110244d03a886161ee06faf29`. Source cutoff remains
`d707c82ab8c48b674acc1f95a9571f0cb24d226a`. Read the complete #693 thread,
audit #1417, bug #1416, records.md v2 and this supplement.

One S1 corrects PL-001 / Low bug #1416. This is a current documentation
correction, not a change to the historical input census or rule policy.
After explicit dispatch proceed S1/E–H continuously, then stop at one
clean published handback. Root retains final acceptance, completion marker,
audit/slice closure and actual ordered integration. All18 #693 criteria
remain root-owned; no coordinator merge is authorized.

## 2. Reuse D and preserve its limitations

D has311 audit files and314 total changed paths, including its pointer,
day log and INDEX. Source census127469/2190843187,95 routes/89 targets,
99 reading records,71 selected sections/15 fallbacks and86 index alignments
remain dated results. Counts are not full semantic reading, disk savings
or integrated-next coverage. T39's48 accepted corrections and #1407's
33-document/2770-line boundary retain their existing owners.

Freeze all original stage-a/b/c/d subdirectories, all17 original tools,
Local plan,01 and03. Six narrative files may receive the dated correction
and outcome:00/02/04/05/06/07. Preserve the D account and its original
failures; distinguish later resolution from the prior Open outcome.
That leaves305 of311 D audit files byte/mode exact. No original producer,
reader, parser, generator, control, lint fixture or scanner is replayed.

Twenty-nine D record files use lossless JSON transport. Preserve stored
bytes, manifest, original-stream identities and recovery rules exactly.
Decode only for new immutable reconciliation; do not execute decoded
content. Original receipts bind decoded streams. Initial incomplete Local
fixtures, tracker message mismatch, staged whitespace refusal and normal
pre-commit refusal stay failures with their actual evidence. Existing
nonblocking ceremony warning remains a warning. Earlier snapshot gates
are not newly attributed to final bytes or resolution. Root's D readback
and any additional qualifications will be appended before dispatch.

## 3. Literal stream binding

Run the block once for the new stream, in the assigned checkout or a
private no-checkout proof clone. It inspects immutable objects only;
it neither creates an export nor invokes an audit producer.

```bash
taskset -c 8-23 python3 -B - <<'PY'
import hashlib, subprocess
D='a0d4c4fda7a0c16c04d57edf921ffeb741eff19b'
S='8710a6210a40de0110244d03a886161ee06faf29'
A='docs/audits/2026_11_03-epic-m6-records/'
def git(*args):
    return subprocess.check_output(['git', *args])
assert git('rev-parse', D+'^{commit}').decode().strip() == D
assert git('show', '-s', '--format=%P', D).decode().strip() == S
paths=[p for p in git('ls-tree','-r','--name-only','-z',D,'--',A).split(b'\0') if p]
assert len(paths) == 311
for path, digest in [
    ('docs/audits/README.md','17269ce0820878e809890a9f737cd665c77d32ff07a20e779aed4fac1b745d79'),
    ('.claude/rules/instruction-files.md','ca638c32b6bbf991c02a865b9c3ab19279416806e7baa0a320713989610da845')]:
    assert hashlib.sha256(git('show',D+':'+path)).hexdigest() == digest
print('PASS T46 stream binding: D a0d4c4fda7a0 / 311 audit files / 1 owned documentation path')
PY
```

Root compared README mode/blob/content at source, seed, D, coordinator
f92bc2f372c0c0ed32018975e903ac83b33bf3a5 and accepted T39
4eb5dfab8e745914a55e7de3e5a43c5b91ebc608: all are identical. No T39
correction must be copied or reverted here. Exact comparison and proposed
replacement bytes are retained in
`docs/qa-logs/2026-11-03-m6-records-disposition/source-disposition-inputs.json`.

## 4. S1 — The one current-document correction

**Verdict:** D05 PL-001, D02/04 L-01, bug #1416. The final paragraph of
docs/audits/README.md uses `applyTo` for current rule selection. The named
canonical instruction-files.md:9,27,37–47 defines `paths:` and every-session
behavior. D's bounded duplicate check found no owner for this correction;
the canonical guide being reachable limits the risk to Low.

**Fix specification:** Replace only the final three-line paragraph with
these exact six lines, preserving the rest of the README byte-for-byte:

```markdown
The skill grounds work against this project's own doctrine rather than a single
rubric file: every-session rules (no `paths:` key or a `**` glob), instruction
files whose `paths:` globs match the changed paths, `docs/blindspot-register.md`,
and the invariants those files state. See the
[rule-selection convention](../../.claude/rules/instruction-files.md).
<!-- #1416 -->
```

The before file is666 bytes, SHA256
17269ce0820878e809890a9f737cd665c77d32ff07a20e779aed4fac1b745d79.
Expected after file is813 bytes, SHA256
410e4432c01a38cda578a68fdaa730129c15a8e3e60c7305001bb40bd5a71b6c.
Keep LF and the existing blank lines; no other paragraph changes.
Canonical rules, other READMEs and historical audit contents are not edited.

**Test first:** Add a small new audit-local source/record proof with separate
before and candidate inputs. The desired current-wording predicate must
fail against immutable D, then pass against the candidate README. Bind the
whole-file before/after hashes, exact paragraph delta and relative link's
existing canonical target. This is a new documentary proof, not replay of
the D table/link controls. Retain actual input/program/argv/cwd/time/exit
and both raw streams/hash identities. No elaborate product test suite is
needed for this prose correction. Any new guard must demonstrate a relevant
refusal before its positive.

**Already written:** The source guidance and historical audit receipts
already exist. No device/cloud state or migration is affected. Historical
authorship, decoded input receipts and source cutoff remain unchanged.
Can this be done on the VM? A bounded documentary source comparison and
current record checks prove this correction; no runtime behavior is claimed
and no VM, image or device action is needed.

**Commit shape:** One S1 source-and-proof commit after green candidate
scope/rules/record checks. Stage named files and inspect status before
committing. The source cites bug #1416, never a coordinator register row
missing from the lane. Cite #693/#1416 in commits. Record the actual commit
after it exists; do not type a predicted own hash into its receipts.

## 5. Exact write ownership and new confinement

Own only docs/audits/README.md's specified paragraph; new audit-local
stage-e/f/g/h records and separately named tools; the six narratives above;
the exact T46 lane pointer; actual UTC execution-day worklog(s), INDEX;
and `docs/retros/<actual-UTC-date>-m6-records.md`. Bind date paths explicitly
from recorded execution dates, not a glob over all logs or retros. Existing
source paths outside the README and original305 frozen audit files cannot
change mode/type/blob. No deletions, renames, unsafe record modes or merges.

The D confinement.py admits only the audit root, pointer, November3 log and
INDEX; it intentionally cannot certify this source correction or G retro.
Preserve it. Add a separately named E–H guard, with its own inputs and new
tiny-Git controls. It inspects every commit from D to tip plus candidate
working changes, rejects source edits and edit-then-revert outside the one
README, rejects changed frozen D artifacts, unrelated retro/day paths,
unsafe modes/symlinks and merges. Any commit changing the README must leave
the exact specified after blob, so a wrong edit followed by a repair still
refuses. Its positive includes the exact README, authorized dated retro/log
and allowed new records. Tiny synthetic metadata fixtures copy no product
tree and execute no product behavior. Keep all original D tools unchanged.

No full-tree export or checkout is needed for E–H. If a tiny Git proof
needs scratch, record its creation/content/owner and retain it through H.
No registry, rule, selector, inventory, brief, other lane or shared-kit write.

## 6. F — Resolution and new current-record checks

After the actual S1 commit and its new proof, record PL-001 **Resolved for
the current documentary correction** in new stage-e/disposition.md and
05/YAML/Phase7 plus dated02/04/06/07 addenda. The finding's historical trace
remains intact. Update audit #1417's one checkbox only when its committed
source trace and required checks actually meet the predicate. Update bug
#1416 with exact source/proof evidence; its two criteria may then be checked.
Both issues remain open for root acceptance/integration; no marker yet.
Keep the18 #693 criteria unchanged for root.

Run both existing resolution lints (normal and `--issue 1417`), current
rules/register/index/ceremony/forbidden/hooks and owning issue checks,
new E–H per-commit confinement, exact305 frozen-artifact identity and
protected source comparisons. Use original D producer receipts as evidence
without invoking their producers. New final gates must bind current input
and program versions; original incomplete metadata remains incomplete.

Before each commit, the whole applicable new record/source harness must
be green; expected old-source/refusal fixtures remain explicitly expected.
Before H, retain an enumerated exact-current-record scan. After final
commit, bind the exact committed changed paths externally with scanner
stdin/hash/exit and source/frozen manifest identities. Explicitly state
self-receipt exclusions. Do not claim a prior snapshot is final-byte proof.

## 7. G — Learning and preserved decisions

Write/post the actual-date T46 retro on #693 and read it back exactly.
Cover finite reading versus metadata coverage, masks/fallbacks, historical
status versus current guidance, source/seed separation, lossless transport
and failed publication attempts, and the small current README correction.
Include Instruction File Recommendations: this corrects a reference to an
existing rule; it does not justify another global rule. Both time-to-play
quantities remain unmeasured. Append the dated worklog and regenerate INDEX.
Root owns any actual rule/register change.

## 8. H — Retain scratch and publish once

This stream authorizes **no deletion**. Record a bounded retained-only
census of the two D-named owned roots `/tmp/m6-t46-inputs.svbcPP` and
`/tmp/m6-t46-confinement-s69_op77`, plus newly created E–H proof scratch.
Inspect only these exact own-lane roots with non-symlink traversal; an
inaccessible or ambiguous path is retained with its limitation. Record
current identities/counts only where available; never invent historical
inode/creation/process evidence. No global /tmp/process/host/cache census.
Do not open any held or unrelated directory. Existing ordinary D publication
receipts at `/tmp/m6-t46-d-publication-pqw4z0xj` and all new final receipts
are retained and named separately, not cleanup targets. Root is the next
owner for any later retirement decision.

Normal commit/push/remote equality/empty status, external exact-final scan
and tracker readbacks precede the single handback. Use reviewed-at=source
d707c82ab8c48b674acc1f95a9571f0cb24d226a, execution-seed=8710a6210a40de0110244d03a886161ee06faf29,
fixed-at=actual final record tip. Keep final publication receipts outside
the observed commit, with a confined ordinary-file manifest and hashes;
do not create a receipt-only commit loop. Stop for root's exact-tip
integration simulation and acceptance. No actual coordinator/next merge.

## 9. Runtime and authority limits

All subprocesses and children use CPUs8–23. No accepted-stage replay,
source acquisition/fetch, package/config evaluation, product/source export,
build/guest/runtime, model/provider/reviewer, host-ledger or physical/cloud
action, cleanup or other-agent permission answer. Normal repository hooks
are required. Successful E/F/G steps are not new approval gates; report a
substantive result or concrete blocker and continue to H under dispatch.
No outcome or execution starts from this candidate alone.

## 10. Proof and final-version record

The unfamiliar executor checks the literal block, exact replacement/delta,
canonical link,311/305 preservation counts, new guard scope, resolution
tool interfaces, dates/retro ownership and retained-only custody without
running old producers or source-reading stages. At most ten top-level
commands, private metadata/text and tiny Git only, no product checkout.
Root records corrections and D reconciliation here before explicit dispatch.
