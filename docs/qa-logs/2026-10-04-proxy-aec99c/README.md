# Final pre-freeze proxy refresh (#419)

Upstream aec99ce05bc0b9761366543fe9f08ea34cd8bd7a at19:23:17UTC changes
five Android files and one documentation file. All270 raw and patched
Linux/native files exactly match ea9aba; all15 fork patches apply at fuzz0.
Archive c729d421f3d607521b8aec07e068c6c2d01025f17c4ddaf78fad94a28cf9c78e
is retained at /tmp/pixelelated-proxy-aec99c/upstream.tar.gz.

Comparison script/report retains each patched file hash. Prior199 upstream
and8 fork test results in ../2026-10-04-proxy-ea9aba/ therefore cover the
identical Linux source; this is source equivalence, not installed VM proof.
Current package lint and proxy schema-note check pass. The new build must
consume the new archive and still run installed preservation checks.
Freshness-after exits0 for proxy/rclone/libsoup/WebKitGTK. Later upstream
movement does not mutate the frozen candidate under test.
