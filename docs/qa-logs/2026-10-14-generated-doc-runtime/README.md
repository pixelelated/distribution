# Generated documentation versus frozen source — #493

Corrected host control02 passes all seven environment/documentation cases.
Actual runner/launcher exits0; host owners exited. Original control01 remains1
because its fixture lacked PROJECT_DIR before the source-time XML query.
The derivative uses real, hash-bound SDK XML tooling and actual project config;
no source function or admission guard is substituted.

The baseline reproduces nested admission refusal after tracked documentation
changes. The candidate emits byte-identical documentation under BUILD and leaves
tracked source unchanged. Direct/manual output remains unchanged. GENERIC_X64,
H700 arm/aarch64, missing BUILD refusal, real tracked-source mutation refusal and
actual environment-export forwarding are covered. This is synthetic host build-
tool proof, not a full-image run. The actual image build remains integration proof.

The exact eight-line candidate is now integrated into distribution functions;
the admission tool is unchanged. Original records, source packet and manifests
remain. Both tiny synthetic Git fixtures were retired after original exits.
