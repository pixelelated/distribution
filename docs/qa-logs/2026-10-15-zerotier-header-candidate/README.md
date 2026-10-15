# ZeroTier client header-isolation candidate

This source-only candidate guards three nonfree includes and their pointer
lifetimes with the existing controller macros. It includes upstream's narrow
controller-destructor fix and preserves enabled-mode source semantics. The
latest stable and current upstream files still have the broader header issue.

Patch SHA256: `5fe6dcc77910a0faf40fa2e9bcb09e918632d0ed2880fd7b30efdeb335c34ad5`.
No product source, package pin or accepted image changed. Compilation from a
fresh input with nonfree/ absent is still required before integration.

The complete three nonfree header copies are excluded from this public-selection
packet. Their exact hashes and private diagnostic references remain recorded;
the original source manifest deliberately names those unbundled private files.
Historical evidence is preserved. No permission, legal clearance or source-bundle
publication decision is inferred from this proposed technical fix.
