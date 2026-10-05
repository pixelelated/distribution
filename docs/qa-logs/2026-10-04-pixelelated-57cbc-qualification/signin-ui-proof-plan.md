# Remaining sign-in qualification

Owners #351/#362; delivery #383. Read against their live bodies/comments on
2026-10-05. Can this be done on the VM? **Yes**; an authenticated Dropbox
trust-page observation additionally needs dedicated QA account access.

The prepared memory05 owner invokes `tools/signin-memory` for 30 seconds.
That tool loads `https://example.org/`, checks that the window and WebKit
process appeared and that a page finished loading, and records peak memory.
It does not capture a provider login/finishing page, exercise redirects, or
assert a numerical memory ceiling. Preserve that exact scope in its report.
D-WORKFLOW-048 carries the earlier loaded-page memory comparison; do not
invent a previously enforced threshold or call a load-only result sign-in
completion.

After the sealed matrix and cloud-ui-01, run the fresh watched sign-in owner
`/workspace/tmp/pixelelated-m7-signin-ui-01` on frozen57cbc/bundled4007387.
Seven inputs are sealed and syntax-checked; it is unstarted. Preparation
script `/tmp/pixelelated-prepare-signin-ui-01.py` has already run: do not rerun.

- Exercise the installed `cloud-signin-window` against an isolated HTTP
  redirect/echo fixture. Read its actual Mobile user agent, CHASSIS=handset,
  successful redirected request and panel-sized frame. Keep synthetic pages
  explicitly distinct from provider pages.
- Load the public Dropbox login page over verified HTTPS with no account
  entered; inspect the actual frame. Trigger the binary's own finishing page
  with its documented done-file interface as a named stand-in, not an
  authenticated sign-in claim. Retain HTTP/TLS/redirect and current memory
  evidence with exact installed payload hashes.
- Serve the installed `cloud_oauth` phone page and render it at 390 CSS px in
  both Checking and Connected states. Measure the actual computed top/bottom
  state margins against .75rem and inspect the frames. A controlled delay in
  the probe response may expose Checking without changing the served page.
  Connected must come from the actual probe/window state, not text injection.
  Firefox's outer window floors at500px. Host probes actual45540/61056 both
  exited0: the latter measured an actual390px iframe viewport inside500px.
  Use the unchanged served page in that390px frame and WebDriver's element
  screenshot, asserting its PNG dimensions; do not claim the outer viewport
  was390px. The proof now checks the measured inner width before capture.
- The real Dropbox trust page remains pending QA access. An async text
  question was sent; no answer yet. Never substitute a local fixture for that
  provider-specific criterion or use a personal account without authorization.

Useful existing sources (read, do not rerun blindly):

- `tools/signin-memory` and the installed window source in
  `projects/ROCKNIX/packages/network/cloud-signin-window/sources/`.
- `/workspace/tmp/rocknix-session/proofs-351/phone-page-351.sh` and
  `phone-page-351b.sh`: historical routes. They use broad pkill patterns and
  one edits the served source; the new owner must use owned PIDs and the
  unchanged installed product instead.
- `docs/qa-frames/2026-10-01/351/README.md`: exact scope of earlier frames.
- Host tool probe actual16216 exited0: geckodriver0.37.1, Firefox157.0.
  Snap emitted mount-namespace warnings before the version, but the command
  completed. `/usr/bin/firefox` points at `/usr/lib/firefox/firefox`;
  `/snap/firefox/current/usr/lib/firefox/geckodriver` is the installed binary.
  Standard WebDriver HTTP can be driven with Python's standard library;
  Python playwright/selenium are absent. No packages were installed.

The existing documentation checkout remains local at
`/home/max/Development/rocknix.org`, commit4f6df54. Live org listing now shows
distribution, emulationstation, splash, world, art and hiring; no documentation
repository was found there. Do not create a fork or swap credentials to bypass
the recorded403/404 destination problem.

#362's old phrase “within its bound” remains unresolved acceptance wording.
It must be reconciled against D-WORKFLOW-048 and actual measurements before
closure; the prepared script does not invent a numerical pass threshold.
