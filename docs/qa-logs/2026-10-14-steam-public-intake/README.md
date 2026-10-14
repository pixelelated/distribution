# Public Steam archive intake — original wrapper failure retained

One public fixed archive was fetched in23.9seconds:110373661bytes, verifiedTLS,
HTTP200,no redirect/retry/upload. The separate full-fileSHA256 child returned0
and matched8b31d0b0aa844d906b690283da41403b601a9b36b1f80b7819d1f85bb27854fc.
All children exited0 with no intervention or descendants. The final wrapper
returned1: it looked for curl metadata request_size instead of size_request.
That failure remains original evidence; it is not a failed transfer/hash and
must not cause a redundant download. No archive decoding or execution occurred.

The local archive remains only for the next immediate offline inspection.
Original private owner: /workspace/tmp/pix-steam-public-download-20261014.
This public record omits transport endpoint addresses and verbose certificates;
the sanitization lists fields and binds the unchanged private original hash.
The actual supervisor/launcher exits and host PID absence are consumed. A small
additive source correction and independent read-only recovery receipt are being
prepared; no original FAIL is relabelled. Offline parser/native-client proof is
still due. Refs #582.
