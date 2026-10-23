# Argon audit receipt compatibility — #638

The artifact checker now admits only the explicitly selected `gemini-argon`
route at google/gemini-4-argon/high, with verified Google provider identity.
The council roster stays unchanged. A current Facilitator receipt stores its
output hash in final.file_artifact_sha256; the checker now verifies that exact
field and additionally verifies the older top-level hash when present. It never
creates or rewrites provider provenance.

Nine synthetic controls pass: valid current receipt, wrong model/provider,
unverified provider, wrong effort, missing hash, conflicting legacy hash,
same-lab reviewer and missing refutation. Run `python3 check.py` from the repo
root using this file's path. Fixtures contain no live review and cannot satisfy
its evidence gate. The Argon blind invocation runs separately on unchanged
product evidence; this checker is not an in-flight process or its dependency.
