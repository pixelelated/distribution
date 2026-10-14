# #583 fixture-only correction after the first guest run

Original22cf probe stopped1 at the first XML write: ElementTree lazily imported
encodings.ascii after the strict file audit hook was installed. Decoder results
were already recorded but listing cases were not run. Preserve that FAIL.

This additive copy preloads only the standard-library ASCII codec before the
audit hook. It does not allow any extra path/event, change product candidates,
relax limits, or remove negative controls. Runtime UNRUN until the new owner.
Use alongside the original819source packet; same /run output contract.
