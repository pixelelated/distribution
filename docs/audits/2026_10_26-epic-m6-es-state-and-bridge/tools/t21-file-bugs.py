# Build T21's bug bodies from the coordinator's 05, verbatim, one file per bug.
import re, sys, json
src, out = sys.argv[1], sys.argv[2]
t = open(src).read()
secs = dict(re.findall(r"^## (PL-\d+): .*?\n(.*?)(?=^## )", t, re.S | re.M))
heads = dict(re.findall(r"^## (PL-\d+): (.*)$", t, re.M))
stream = {"PL-01":"S1","PL-10":"S1","PL-11":"S1","PL-09":"S2","PL-03":"S2 (the recorder half)","PL-02":"S3",
          "PL-17":"S3 (the hash halves) and S13 (the scraper halves)","PL-04":"S4","PL-05":"S5","PL-06":"S6 (the page half)",
          "PL-07":"S7","PL-08":"S7","PL-19":"S7","PL-12":"S8 (and S5 for its modes)","PL-13":"S9","PL-14":"S10",
          "PL-15":"S11","PL-18":"S12","PL-16":"none here: its page half waits for the OS round (one change across the page and `wifictl`)"}
t1 = {"PL-03":"the `set_setting` / `set_settings` seed copy in `001-functions`",
      "PL-06":"`wifictl`'s missing-device guard","PL-16":"the key on argv in `wifictl` and `001-functions`",
      "PL-13":"`chksysconfig backup`'s temporary name"}
def title(pl):
    h = re.sub(r"\s*\(a `bug` proposed[^)]*\)\s*$", "", heads[pl]).strip()
    return h
plan = []
pre = ("Found by T21 (#668), the audit of EmulationStation's state primitives and its bridge to the OS "
       "(`docs/audits/2026_10_26-epic-m6-es-state-and-bridge/`; the audit issue #1184), read at the ES pin `16dbac5211` and "
       "the scripts at `8ebaf8daad`. The section below is {pl} of `05-punch-list.md` as the coordinator wrote it "
       "(D-WORKFLOW-212), copied verbatim; it carries the code trace, the VM line and the `Already written:` line.\n\n")
for n in range(1, 20):
    pl = f"PL-{n:02d}"
    b = pre.format(pl=pl) + f"## {pl}\n\n" + secs[pl].strip() + "\n\n"
    b += f"**Stream:** {stream[pl]} of `docs/reviews/briefs/t21-streams.md` (the coordinator's, at `e3c07a9c30`), on the ES branch `feature/m6-es-state-and-bridge-668`.\n\n"
    if pl in t1:
        b += f"**The OS scripts' half** ({t1[pl]}) is filed separately under #695 and changes nothing here.\n\n"
    b += ("## Acceptance criteria\n\n"
          f"- [ ] The item's positive FAILs on the pin and PASSes on the stream's commit: `stage-e/{stream[pl].split()[0].lower() if stream[pl].startswith('S') else 'none'}-before.txt` and `-after.txt` in the audit folder, as the item's **Acceptance** line above describes.\n"
          "- [ ] `02` § The streams carries the stream's row with this bug's `Already written:` answer, and the bug's `fixed-at-es` is filled.\n")
    if not stream[pl].startswith("S"):
        b = b.replace(f"- [ ] The item's positive FAILs on the pin and PASSes on the stream's commit: `stage-e/none-before.txt` and `-after.txt` in the audit folder, as the item's **Acceptance** line above describes.\n",
                      "- [ ] The page half lands with the OS round's `wifictl` change, its positive recorded beside that change as the item's **Acceptance** line above describes.\n")
    open(f"{out}/{pl}.md", "w").write(b)
    plan.append({"pl": pl, "file": f"{out}/{pl}.md", "title": "Bug: " + title(pl), "parent": 668})
for pl, what in t1.items():
    b = pre.format(pl=pl) + (f"**This issue is the OS scripts' half: {what}.** It is T1's file and is fixed in the integration's fix round under #695 (the coordinator's stage-D ruling on #668); the EmulationStation half is its own bug under #668.\n\n"
         f"## {pl}\n\n" + secs[pl].strip() + "\n\n## Acceptance criteria\n\n"
         "- [ ] The scripts' half's positive (the item's fixture or `tools/settings-modes-test`-shaped case run against the shell at the fixing commit) FAILs before and PASSes after, recorded beside the fix in the integration's fix round.\n")
    open(f"{out}/{pl}-os.md", "w").write(b)
    plan.append({"pl": pl + "-os", "file": f"{out}/{pl}-os.md", "title": "Bug: the OS scripts' half of T21 " + pl + ": " + title(pl), "parent": 695})
json.dump(plan, open(f"{out}/plan.json", "w"), indent=1)
print(len(plan), "bodies;", "max title", max(len(p["title"]) for p in plan))
