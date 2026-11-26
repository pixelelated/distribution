# #1484: the ES cloud page-lifetime test, back in service

OS coordinator, 2026-11-26.

- **The test.** `tests/cloud-oauth-lifetime.py` in the ES tree extracts `cloudSetupPresent` and the sign-in choice page from `GuiMenu.cpp`. It compiles them with host `g++` and AddressSanitizer against small doubles, and drives real deletion over four routes.
- **The fault.** It had not compiled since the composed M7 source (`409704f3b`, #1462) changed the functions it extracts. Nothing ran it, so nothing reported that.

| File | Source under test | Result |
| --- | --- | --- |
| `round-6cdcb7a64-fixed-test.out` | the ES round `6cdcb7a64`, with the test fixed in `b80e59646` | 4 of 4 PASS |
| `old-source-0ee5b28a6.out` | the test's own commit's `GuiMenu.cpp` | 4 of 4 PASS: the fixed harness still runs older source |
| `planted-use-after-free.out` (+ `.diff`) | a scratch copy reading the closed page after `cloudSetupPresent` closes it | 4 of 4 FAIL, ASan `heap-use-after-free`, rc 1 |
| `es-syntax-check-round.out` | `tools/es-syntax-check --tree` on the round's `GuiMenu.cpp` | OK, plus "lifetime test, 4 routes", rc 0 |
| `es-syntax-check-planted.out` | the same on the planted copy | FAIL with the ASan lines, rc 1 |

**A first plant proved nothing.** It assigned the page's tag to itself after the close. A string self-assignment compares addresses and never reads the freed object, so ASan stayed quiet and the test passed. The kept plant reads the string's size. A plant has to touch the freed memory before its silence means anything.

Before the fix, the round's source gave 10 compile errors, rc 1, for example `'OfflineRecoveryNotice' has not been declared` and `'struct GuiSettings' has no member named 'getTag'`. That output was read at the time and not kept; the issue body quotes it.
