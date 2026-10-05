# Sign-in display comparison before and after the pixelelated rename

Issue #447; requested by the maintainer on2026-10-05. Can this be done on the
VM? **Yes.** Both immutable images ran on the current host with the same
launcher/profile and local redirect/finishing/capture procedure. No provider
credentials, injected input, resize or compositor override in this comparison.

| Image | Software graphics | Accelerated graphics |
| --- | --- | --- |
| Pre-pixelelated RASTERATOPS, October3, source61b64817bf / bundle87b8c01d | Diagnostic08: host HMP/VNC old at0seconds, partial at5, correct15; native correct throughout | Diagnostic09: all nine native/HMP/VNC frames agree exactly |
| pixelelated, sourcecf511ce79b / bundle79d56004 | Diagnostic05: same old/partial/correct sequence; native correct throughout | Diagnostic06: all nine native/HMP/VNC frames agree exactly |

These are declared offsets after the existing initial capture sequence, not
latencies measured directly from the navigation request. Each sample records
its actual elapsed time. Full canonical sign-in11 separately qualifies27
checks and six intended frames; diagnostic runs do not replace it.

The earlier image reproduces the discrepancy on today's host. Therefore the
pixelelated migration is not necessary to reproduce it. This does not establish
what the host did on October3, or prove that a physical handheld has the issue.
The remaining investigation belongs to the software virtual-display path;
its exact faulty component is not established. #447 remains open.

## Source and configuration comparison

`source-comparison.json` verifies twelve real git objects, not empty diffs of
nonexistent paths: sign-in window, WebKit/libsoup, Sway/wlroots, Mesa, kernel
recipes/config, VM launcher/profile and capture tool are identical between
61b648 and cf511ce. `nearby-source.diff` retains the quiet boot option, OS_NAME
export and settings-temporary permissions changes. ES and other whole-image
changes are not declared identical.

The older ROCKNIX RC2→61b648 source difference is the earlier #351 finishing-page
styling change, retained in `prior-rc2-signin.diff`. That change predates the
pixelelated rename. The actual RC2 image has now run the matched comparison: software host
frames are stale initially while native is correct; all accelerated frames
agree. Its original September29 suite report records accelerated virgl and
no browser finishing-transition comparison. See [RC2 evidence](rc2/README.md).

`graphics-argv-comparison.json` compares actual QEMU arguments for old/current
accelerated guests. They are exactly equal after replacing only the owner
path; QEMU version is recorded. Earlier software08's actual argv verifies its
software GPU. Both historical guests preserve the image's own compositor
configuration. Old installed sign-in/OAuth hashes derive from the verified
old update SYSTEM, and the booted guest's identity and hashes match them.
Current frozen source and old bundle verify before/after both tests.

The actual installed sign-in executable is also byte-for-byte identical in both
images (SHA256fc9a3473490f52e8da76d473a2265e56d1dd362977351b4b732ed2bcd1419990).
The OAuth wrapper differs; this local rendering comparison calls the window
directly and does not use that wrapper. See installed-payload-comparison.json.

## Receipts

- Historical software08: submission943159, durable17:17:13/all four rc0;
  actual2f5df8 cleanup17:17:37. All nine frames reviewed;119artifact hashes,
  115public files retained in `../signin-render-diagnostic-08/`.
- Historical accelerated09: submission2f5df8, durable17:18:48/all four rc0;
  actualf4b65f cleanup17:19:03. All nine frames directly reviewed and exact
  decoded RGB matches;287artifact hashes/283public files retained in
  `../signin-render-diagnostic-09/`.
- Earlier legacy-DRM experiment07: selected mode and llvmpipe proved, but
  the discrepancy persisted. It is a rejected remedy, retained separately;
  no runtime override is proposed for the product.

All guests and owned processes are stopped. No product bytes were changed.
Normal publication and current M7/checkpoint reconciliation follow these
artifact-scoped observations; no RC/device-ready claim follows.
