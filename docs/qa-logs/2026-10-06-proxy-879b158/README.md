# Android-only freshness update before replacement build

#361/#383/#457. The full frozen13 freshness check failed00:37:51/allfour1:
upstream b09d604 was one commit behind879b158995d412af434301ebdae581f66b8b6d57.
Observed00:37:54, actual cleanup00:38:16. Frozen13 source remains e4276a6743;
no cache copy or image build started. Preserve its exact input receipt and
failed freshness result. It was not a failed product compilation.

The new commit, published00:27:25, changes four Android files for update
notifications. Exact archive SHA256:
984957322337d1325f1b0fc11502336a80241ec511fd041c969bb0103c231664.
Entire pristine Linux tree219files and native/glue tree53files are identical
to b09; both coupled gitlinks are unchanged. All16 patches apply without fuzz,
and the entire patched Linux tree222files plus native53files are byte-identical
to the source qualified by818 native-enabled tests and both11-test predecessor
suites. The actual helper changes only its schema-review pin comment; reviewed
storage bytes are unchanged and package/schema guards pass.

[Full b09 source proof](../2026-10-06-proxy-consent/README.md) remains scoped to
its recorded inputs; the explicit full-tree equality establishes the unchanged
Linux runtime/tests, not a new test execution. Full scripts are not rerun for
an Android-only source delta. A newly frozen replacement14 and installed VM
proof are next. No RC or device-ready claim.
