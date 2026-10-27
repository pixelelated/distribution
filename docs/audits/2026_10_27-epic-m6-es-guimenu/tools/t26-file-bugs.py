#!/usr/bin/env python3
"""T26 (#673): the bodies and titles of the 19 bugs the stage-D ruling names, from 05-punch-list.md.

    python3 -I t26-file-bugs.py <05-punch-list.md> <out dir>

Writes <out dir>/PL-NN.title and PL-NN.md for each; the filing is a loop over
them with `gh issue create`. Each body is the item's section of 05, copied,
between an introduction and the acceptance criteria every T26 bug shares.
"""
import os, re, sys
PLS = ["PL-01", "PL-02", "PL-03", "PL-04", "PL-05", "PL-06", "PL-07", "PL-08", "PL-09", "PL-10", "PL-11", "PL-12",
       "PL-13", "PL-14", "PL-16", "PL-18", "PL-25", "PL-28", "PL-29"]
text = open(sys.argv[1], encoding="utf-8").read()
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
INTRO = ("Found by T26 (#673), the audit of EmulationStation's main menu, GuiMenu (`docs/audits/2026_10_27-epic-m6-es-guimenu/`; "
         "the audit issue #1213), read at the ES pin `16dbac5211` and the scripts at `8ebaf8daad`. The section below is the item's "
         "in `05-punch-list.md`, copied; its leads and proofs are in `02-forward-audit.md`.")
for pl in PLS:
    m = re.search(r"^## (%s): (.*?)\n(.*?)(?=^## PL-|^---\n)" % pl, text, re.S | re.M)
    assert m, pl
    title = re.sub(r"\s*\((a `bug` proposed|a design item|recorded|latent)[^)]*\)\s*$", "", m.group(2)).strip()
    stream = re.search(r"stream (S\d+) of", m.group(3)).group(1)
    body = "\n".join([INTRO, "", "## " + pl, m.group(3).rstrip(), "",
                      "**Stream:** %s of `docs/reviews/briefs/t26-streams.md` (the coordinator's, at `4bd066551a`), on the ES branch `feature/m6-es-guimenu-673`." % stream,
                      "", "## Acceptance criteria", "",
                      "- [ ] The item's positive FAILs on the pin and PASSes on the stream's commit: `stage-e/%s-before.txt` and `-after.txt` in the audit folder, as the item's **Acceptance** lines above describe." % stream.lower(),
                      "- [ ] `02` § The streams carries the stream's row with this bug's `Already written:` answer, and the bug's `fixed-at-es` is filled.", ""])
    full = "Bug: EmulationStation: %s (T26 %s)" % (title, pl)
    open(os.path.join(out, pl + ".title"), "w").write(full + "\n")
    open(os.path.join(out, pl + ".md"), "w").write(body)
    print(pl, stream, len(full), len(body))
