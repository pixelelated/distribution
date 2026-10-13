# #571 French phone keyboard follow-up — source only

Prepared 2026-10-13 for coordinator w4:p2. The French companion keyboard now
translates its field, key controls, pointer instruction, help/trust note,
Show/Hide action, and unsupported-character warnings. Input and arrow controls
also have accessible names. English visible copy remains identical.

Only `projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth` and this new
packet change. The requested phone-status packet was cherry-picked first; its
files, the accepted library/browser-failure packet and ES commits are immutable.
Integrate **only this new follow-up commit**, not the worker's historical branch.
There is no ES, package pin, shared reference, GitHub, or runtime change here.

## Exact source binding

[source.json](source.json) records the full prerequisite commit, local parent,
coordinator comparison, and baseline/candidate blobs and SHA256s. The product at
`a824edbd209d1971b2c814cf86528bae0add9c51` is byte-identical to the product at
coordinator `0d69fca540c7a75833e26054463145635c121b00`; that equality was read from
Git, not inferred from a report. Candidate product blob:
`78c343771a0ad500ba894d58f728375f3911cdf1`.

The user's #571 frame review and the accepted phone-status packet are the
assignment evidence. This follow-up did not contact GitHub or reread the live
issue over the network. Its scope follows that explicit coordinator handoff.

## Behavior and preservation

Static French text extends `phone_page`'s existing literal replacement table.
Dynamic text extends the existing `phoneMessages[phoneLanguage]` dictionary.
Both still inherit the handheld locale through `signin_language`; browser locale
does not select another language. Translation happens before escaped service-name
insertion, so a service named “Show” or “Type here” remains data.

The masked-warning branch selects only singular/count messages. Character
interpolation occurs only in the revealed branch. Toggling back to password
immediately calls the same warning renderer; neither action sends input. Warning
output remains `textContent`. The ASCII filter and its existing UTF-16 counting
behavior are unchanged; this does not fix grapheme counting or unsupported input.

The five French keys use `⌫ / Tab / ↵ / Vider / Voir`, with `Cacher` while revealed.
The symbols have full French accessible names. French key rows use an automatic
flex basis so the short symbols leave room for the longer text, keeping the
existing 16 px font, padding, and order. The scroll controls read `Monter` and
`Descendre` and explicitly name scrolling in their accessible labels. Arrow keys
are named as arrow keys, not as mouse movement. No handler or key identifier changes.
320 px fit and symbol rendering still require actual frames.

[static-result.json](static-result.json) records Python AST/literal inspection and
EN/FR JavaScript syntax checks. After normalizing exactly the dictionary additions,
warning text expression, and toggle text expression, the entire JavaScript is
byte-identical to the accepted source. Queueing, movement/tap batching, readiness,
navigation resets, probes, status presentation, and Close/Keep handlers therefore
have no code changes. Other Python AST is identical after excluding page literals
and the added translation-table entries; broker/PIN/network/security behavior is
unchanged. The CSS delta is exactly one French-only key-row rule and its comment.

## Criteria and next coordinator experiment

Can this be done on the VM? **Yes.** Locale selection, synthetic input, masking,
layout, and installed companion behavior require no physical device or account.
All runtime here is **UNRUN**. Earlier four-case/32-frame status evidence reported
by the coordinator covers the earlier source only.

| Criterion | Source/static evidence | Next-source evidence required, UNRUN |
| --- | --- | --- |
| French field/buttons/help/toggle/warnings | Exact [copy.md](copy.md), literal markup and dictionary inspection | EN/FR 320/768 frames; no English fallback in the keyboard controls |
| Fit on 320 px | Short labels, French content-sized key cells, same font | Text-range bounds for every first-row label including Cacher, no overlaps or horizontal overflow; glyph legibility |
| Masked characters never disclosed | Exact guarded expression, no character placeholder in masked messages | Singular/plural reveal → rehide frames and warning assertions; no extra POST |
| Input/pointer/probe unchanged | Full JavaScript equivalence after the three copy-only substitutions | Coordinator component/regression and installed VM synthetic proof |
| Accessible control names | Static input/arrow/Backspace/Enter labels | Accessibility-tree review, keyboard focus and translated-name activation |

[locale-cases.json](locale-cases.json) prepares nine groups of exact inputs,
actions, and expected outcomes, including eight synthetic locale environments,
masked single/multiple characters, reveal/rehide, clear, ASCII/markup, Unicode
counting, direction/scroll keys, and next-source regression. It is data for the
coordinator's existing harness, not a launched fixture or new browser dependency.

Before a separately allocated next-source run, coordinator should:

1. Bind its current component fixture (including its explicit browser executable
   option) to `source.json`'s candidate bytes. Do not run the old immutable packet's
   candidate-bound fixture against new bytes, or edit its old binding/results.
2. Extend the existing isolated synthetic EN/FR × 320/768 cases with the prepared
   locale cases. Capture initial masked controls, single/multiple masked warnings,
   revealed and rehidden warnings, plus the pointer/help surface in each locale.
   Review button text bounds and readable wrapping, not merely screenshot creation.
3. Run the coordinator-owned component/regression and then the installed VM proof
   under its runtime allocation. Verify the installed product SHA256 before the
   flow; retain the first result, exit status, new source identity, and frame index.
   Reuse synthetic pages/data and the existing lifecycle/input controls.

No worker runtime, fixture import, compiler, browser, service, device, provider,
dependency install, build, or push occurred. No new runtime was allocated.

## Static verification and reference handoff

Executed static checks only:

```sh
python3 docs/qa-logs/2026-10-13-phone-locale-source/static_check.py
git diff --check
# From this packet directory:
sha256sum --check SHA256SUMS
```

The static checker never imports or executes the product, and passes only literal
extracted scripts to `node --check`. The fixture data is parsed, never executed.
No static failure or commit approval blocker remains at handoff.

Proposed canonical companion-flow addition, for the coordinator after reviewing
new-source frames: “The phone keyboard uses the handheld's language for controls,
instructions, and warnings. Unsupported characters are counted while hidden and
named only while visible. Voir/Cacher reveals or masks the local field; it does
not resend it.” No ES menu row or wizard transition changes. [copy.md](copy.md)
provides exact EN/FR reference additions; no `.po` edits are needed for this page.

Boundary: this is the authenticated `REMOTE_PAGE` keyboard surface identified by
the reviewed frames. The separate legacy redirect/PIN pages, provider-owned text,
and browser-supplied error details are unchanged. It is not a claim that every
HTTP error/fallback/provider surface is translated, or that assistive-technology
and phone-browser behavior has been exercised.
