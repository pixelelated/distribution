# Durable submission controls (#444)

`tools/watch-build-submit` runs the existing frozen `watch-build` runner
with file-backed console output in a separate session. Its short submission
command returns before qualification completes. `launcher-submission.json`
records that distinction; `launcher-result.json` and `tool-wrapper.rc`
record the eventual observed runner return. The command's inner/outer
results and the runner's build result remain independent, unchanged files.

Actual control tool62077 returned0. `test-submit.py` executes real processes:
successful completion, exit7, duplicate-owner refusal while running, and
termination of the submitting process group while the detached job completes.
All three jobs retain matching standard terminal results and stopped child/
watcher processes. `controls.json` records the actual fixture and outcomes.

The launcher prevents loss of the submitting shell from taking its output
pipe and runner with it. It does not survive arbitrary host/worker death,
guarantee cleanup after SIGKILL, or deliver notifications after disconnection.
The standard watcher still detects runner death; an active observer must
check separately sessioned children/guests. No cause is attributed to the
original guest10 termination beyond the observed tool143/runner disappearance.

Fresh guest11 uses submission497141 and a retained launcher copy, with the
unchanged frozen candidate/runner/19 cloud cases. Its completion is separate
acceptance evidence and is not claimed by these short lifecycle controls.
`finish-submitted-owner.py` requires terminal matching result channels and
actual process cleanup; it never fills in a missing result file.
