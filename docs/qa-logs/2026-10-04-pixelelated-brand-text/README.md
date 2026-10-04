# Player text and Tools XML corrections — #416/#417

Can this be done on the VM? Yes. Preliminary staging/source reads exposed
seven stale display/help strings and one malformed XML entity. Frozen1600
continues its own tests unchanged; these corrections are not in that image.

Five Tools descriptions now use pixelelated or neutral wording. Cloud help
points to the actual Game Settings > Cloud Settings interface. The memory
status heading and bucket-name example use lowercase pixelelated. Existing
paths, command names, names, developer/publisher credits and other metadata
are retained. XML comparison verifies only those five descriptions changed.

The inherited touchHLE description's literal ampersand made strict XML parsing
fail at line392/column277. Escaping it preserves the displayed `iOS 2 & 3`.
The existing identity guard now parses Tools metadata and checks its name/desc
fields. The original XML fails; well-formed XML with old player text fails;
corrected source passes. Shell syntax and vocabulary pass. These are source
controls; installed-byte/frame and full artifact-sweep criteria remain open.

The `install-rocknix.svg` filename is retained compatibility metadata: its
actual rendered icon says Install to Internal, with a neutral drive symbol.
The source SVG was rendered with the exact ES NanoSVG code for inspection;
its PNG is an inspection proof, not a replacement asset. An initial attempt
incorrectly invoked the specialized Ocean validator as a renderer and was
rejected by its argc assertion; the separate retained preview source is the
actual renderer. No product asset changed.
