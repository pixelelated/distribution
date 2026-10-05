# First transfer status sample (#439)

Directly inspected baseline/current first frame and current completed frame.
Baseline shows SAVES / ITEM1OF4; current09 first frame shows PREPARING, and
later COMPLETED,24files/640KB, elapsed0:04. This is an expected sampled phase;
no single performance cause is inferred. The source captures immediately after
wait-for-change: t02 is a historical filename. The comment now states that.

One baseline/issue-bound claim covers557,288–723,339 (half-open),2778 changed
pixels. Actual44269=0: removing it fails1, shrinking x1 by one pixel fails1,
corrected78-frame comparison passes0 with20claimed/0unclaimed/0missing,
substituting an unrelated actual screen fails1, and a missing frame fails1.
Full original baseline/candidate hashes, engine/masks digests and outputs are
retained. No baseline acceptance, mask expansion, product or frozen QA edit.

Original QA11 actual64718/allrc1 and its fourteen preceding suite passes stay
separate. New QA13 binds their hashes, these controls and its copied claims;
it reruns the corrected comparison before the previously unrun upgrade proof.
QA12 was refused before start for a missing activity directory (#440); its
console/rc2 remain separate. QA13 prepares that directory and runs under the
ordinary5s/5min recursive watcher. No RC qualification is inferred here.
