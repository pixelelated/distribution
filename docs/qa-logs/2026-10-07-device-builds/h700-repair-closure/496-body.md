The #495 SPIRV-Tools host package now compiles and installs successfully in the pinned build container. H700 arm03 then completed its nine assembly/validation/roundtrip commands, but its new smoke-result writer failed before publishing a result because container Python3.10 lacks `hashlib.file_digest` (introduced in Python3.11). The overall run remains failed with return code2; the full compatibility build did not begin. No product failure is inferred from this observer exception.

Can this be done on the VM? Yes: run the unchanged shader controls against the actual installed host executables inside the same pinned container. No hardware is required.

## Acceptance criteria

- [x] Preserve arm03 original traceback, shader logs, sealed script, terminal channels and exited owner evidence.
- [x] A fresh owner uses a streaming SHA256 implementation available in the pinned Python and passes the identical positive and negative shader controls, producing independently verified executable/stamp hashes.
- [x] The H700 compatibility build resumes only after that successful result; retain the new watched owner in #492.

Already written: installed local host tools exist with a successful build stamp. No H700 firmware image, player storage or cloud state was changed. Keep the failed observer record intact and reuse only the verified, unchanged package inputs.


## Verified completion

Published on next `63ef759ad508d27b0bebc4337a1ed7868cc180c5`, including recipe `f5f815faff4e18808d2c1c0298e4335cc0b20fe7`. [Original arm03 traceback and unchanged shader logs](https://github.com/pixelelated/distribution/tree/63ef759ad508d27b0bebc4337a1ed7868cc180c5/docs/qa-logs/2026-10-07-device-builds/h700-arm03-failed); [fresh04 portable hasher, nine passing shader commands, independently verified executable/stamp hashes and live build readback](https://github.com/pixelelated/distribution/tree/63ef759ad508d27b0bebc4337a1ed7868cc180c5/docs/qa-logs/2026-10-07-device-builds/h700-arm04-start). Failed arm03 has four2/seven unchanged seals/exited owners. Fresh04 host stage is independently accepted while its full H700 compatibility build remains running under #492. No terminal success is claimed for that continuing build.
