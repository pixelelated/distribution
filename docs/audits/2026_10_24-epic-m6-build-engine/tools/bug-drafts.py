#!/usr/bin/env python3
"""Draft the stage-D `bug` issue bodies from punch-items.py's list (#652). Writes <outdir>/PL-NN.md.
    python3 -I bug-drafts.py <outdir>
"""
import runpy, sys, pathlib
I = runpy.run_path(str(pathlib.Path(__file__).with_name("punch-items.py")))["I"]
out = pathlib.Path(sys.argv[1]); out.mkdir(exist_ok=True)
for n, x in enumerate(I, 1):
    if not x.get("tracked"): continue
    pl = f"PL-{n:02d}"
    body = f"""Found by the M6 renovation's T5 slice, the build engine (#652; audit `docs/audits/2026_10_24-epic-m6-build-engine/`, {x['f']}, punch item {pl}). D-WORKFLOW-187: a defect the renovation finds is a bug like any other.

## Code trace

- **How it was found:** {x['f']} in `02-forward-audit.md`, read at `8ebaf8daad`; evidence: {x['ev']}.
- **The defect at its source:** {x['t']}. Where: {x['where']}.
- **The fix's shape:** {x['what']}
- **Sibling sites:** named in the finding; any further site is listed here when the fix's stream brief hunts them.
- **What reading cannot prove:** what only a build shows; this issue's image proof is the coordinator's first build after the merge (`fix-pending-image`) unless the criterion below is a sandbox's.
- **Already written:** {x['aw']}

**Can this be done on the VM?** {x['vm']}

{"Upstream's code: a #585 candidate (D-WORKFLOW-164); submission deferred (D-WORKFLOW-165)." if x.get('upstream') else "The fork's code."}

## Acceptance criteria

- [ ] {x['acc']}
- [ ] The fix's commit cites this issue and names its sandbox or recorded-run artifact.
"""
    title = "Bug: " + x["t"].replace("`", "")
    (out / f"{pl}.md").write_text(f"<!-- title: {title} -->\n" + body)
    print(pl, len(title), title[:100])
