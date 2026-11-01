#!/usr/bin/env bash
# T38 stage B (#685): the council family's lines the leads name, printed through the read mask, for the record.
export LC_ALL=C; C=.claude/skills/council/references; R=.claude/skills/council-research/references
M='s/((token|key|pass(w[a-z]*)?|psk|user|login|apikey) *[=:] *)[^ "]*/\1***/Ig; s/(--(token|key|pass(w[a-z]*)?|psk|user)[= ]+)[^ ]+/\1***/Ig'
show() { f=$1; shift; for r in "$@"; do printf -- '-- %s:%s\n' "${f#.claude/skills/}" "$r"; git show "HEAD:$f" | sed -n "${r}p" | sed -E "$M" | cut -c1-220; done; }
show $C/model-verification.md 16 63,69 336,340 385 538,542
show $C/pipeline.md 62,64 155,157 202,206 458,460 468 496,497
show $C/context-loading.md 47 60 120,126 198,199
show $C/output-conventions.md 25 131 452
show $R/methodology-primitives.md 224
show $R/phase-1-independent-research.md 107,122 142 150,154 266,268 285
show $R/phase-2-clinical-synthesis.md 110 246
show $R/phase-3-adversarial-review.md 104,111 170 584
show $R/phase-4-council-deliberation.md 59
show $R/phase-5-deliverable.md 118 172
show $R/model-roster.md 3,6 26,27
show $R/provenance-schema.md 424 587 594 640
show $R/output-directory-structure.md 36 53
