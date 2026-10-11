# Proxy integration discovery — #543

Direct readback of original proof74/regression75/regression79 logs shows **11 tests**
each. Earlier work-log and #541 summary claims of 12 were incorrect. The declared
PreparationCadence test was omitted from the manually selected class list; the
original logs and results remain unchanged.

The CLI now discovers the module's tests, including PreparationCadence. Fresh
proof01 ends0 at18:14:47UTC: all **12 tests pass**, with the named pause-boundary
assertion checking games50/100 and30-second pauses. A scratch helper changing the
pause to0seconds fails exactly that assertion:12 tests,1 failure, expected exit1.
Both outcomes are retained. The shipped helper's hash is unchanged; no firmware
source or installed behavior changes. Native866-test evidence remains separate.

This corrects the harness and the evidence count; it does not replace installed
proxy service/retained-state qualification under #344/#541. No account contacted.
