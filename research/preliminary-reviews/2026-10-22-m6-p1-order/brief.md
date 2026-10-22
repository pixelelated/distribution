# Preliminary review: the proposed renovation order (M6.P1, #641)

You are one of three reviewers (Claude, Gemini, GPT) giving an **advisory
preliminary review**: no vote, no approval, not an audit and not a council.
You read the same four documents as the other two; they are embedded above
this brief, each with its path and verified sha256. You have no tools and no
other access to the repository: reason only from what is embedded, and say
so when a question cannot be settled from it.

## What you are reviewing

`docs/reviews/order.md` proposes the order in which a whole Linux
distribution for handheld gaming devices (a fork of ROCKNIX, itself built
on LibreELEC's build system) is renovated, slice by slice: 43 slices, each
one executing session's work, each reviewed under the per-slice procedure
of `plan-for-the-plan.md` § 6b. `inventory.md` is the generated survey the
order was cut from (every tracked path with its area, provenance tier, size
and reachability by the images the build makes). `areas.json` is the
hand-written map of paths to areas. `plan-for-the-plan.md` is the method the
order must follow: the seven questions (§ 4), the slicing bounds (§ 5), the
phases and ordering lenses (§ 6, § 6a), review depth (§ 6c), drift (§ 8).

The order is posted to the maintainer next, who says yes or asks for
changes. Your findings are answered by name in `order.md` before that.

## The questions

Answer each, citing the embedded documents by path and section or slice
number (T1 to T43). Where you would change the order, say exactly what moves
where and why.

1. **The gates and the first three.** Plan § 6a and D-WORKFLOW-102 require
   Tier 1's launch, control and state slice before release `0.1`, and the
   interface's launch-path slice before #336 Step 1, both among the first
   three slices, each of the first three about 12,000 read lines or one
   package group. Does the order meet that, and are T1 and T2's boundaries
   the right ones for what they gate?
2. **The argument from the lenses.** Is the order after the gates argued
   soundly from the six lenses (security, brittleness, nearest new
   functionality, nearest planned change, cost against value, reachability)?
   Name any slice placed too early or too late, with the lens that says so.
3. **Seams.** Plan § 5 keeps paths that share runtime state together,
   because interaction defects live at the seam. Which slice boundaries cut
   through a seam the order does not name as an interacting subsystem? Are
   the "interacting subsystems" entries sufficient for an executor reading
   one slice alone?
4. **Sizing and kinds.** Are the slice kinds (read, currency, table) applied
   consistently with plan § 2 and § 3 (provenance decides the lens)? Is any
   slice too large for one session, or so small it should be merged? Is T32's
   exception (one 14,238-line file kept whole) justified?
5. **Depth.** Are the review depths (Local, Independent, Extended, plan
   § 6c) assigned where the plan says they belong? Name any security,
   state-preservation or launch-path slice below Extended.
6. **Coverage and reachability.** `inventory.md` reports every tracked path
   in exactly one area and the order reports every path in exactly one
   slice. From what is embedded, do you see anything the survey's method
   would have mislabelled (for example a path called unreached that a build
   would use, or an area whose read size looks wrong)?
7. **Anything else** that would make an executor's slice fail, or the
   maintainer's yes premature.

## How to answer

Start with a two-line verdict: is the order ready to put to the maintainer,
ready with named changes, or not ready. Then one section per question, each
finding marked **material** (it should change the order or a slice before
the maintainer sees it) or **minor** (worth a note), with its evidence.
Keep to what the documents support; mark anything you infer beyond them as
an inference. End with a short list of the changes you would make, in
priority order.
