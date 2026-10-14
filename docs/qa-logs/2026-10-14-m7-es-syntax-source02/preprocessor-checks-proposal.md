# Scoped tool-fix controls — proposal only, UNRUN

No compiler/preprocessor/fixture has run during retry preparation. The recorded original run01 already supplies the real product negative compile result; do not replay it merely to reproduce the same error.

Static checks performed here:

1. Read ThreadedHasher.cpp's actual angled include, and bind both source headers. Current header declares `bool gameCubeRvzHashEnabled();` unconditionally; current implementation defines it. No source modification is needed to provide that declaration.
2. Read the bound cached Ninja object stanza and enumerate its -I roots in order. Neither selected-tree app/core header farm can supply `libcheevos/cheevos.h`. The first matching cached root resolves to the old header, which lacks the declaration. Adding only the existing -iquote external root leaves this angle lookup unchanged (negative control).
3. Add the selected full tree's external root to PRE before the cached -I roots. The first matching angle include resolves to the exact current header (positive selection). The same header's relative rcheevos include then resolves inside the same current external subtree. All other command flags/source bytes and --with parsing are unchanged.

Optional future admitted preprocessor controls when integrating the durable tool fix:

- Use the actual ThreadedHasher.cpp command from the bound Ninja object stanza and the existing helper's source/header-farm remapping. Record the complete evaluated argv. For a diagnostic-only invocation, remove object/dependency-output flags and select `-E -H` instead of syntax parsing; retain stdout/stderr under the private owner. Never invoke a different system compiler or an invented declaration test stub.
- With the original quote-only external addition, the compiler's include trace must select cached c8dc `external/libcheevos/cheevos.h`; its preprocessed output must not contain the capability declaration. This checks header choice, not syntax PASS.
- With the exact proposed --tree PRE addition, the trace must select c045 `external/libcheevos/cheevos.h`, whose full bytes/hash must match the binding; the output must contain the real declaration. Compare all other compiler arguments and feature defines unchanged.
- Keep the original finite container family, memory/CPU/storage boundaries and original-result ownership. These diagnostics are not necessary to replay all accepted product tests, and do not replace the actual five-TU syntax retry. A failed/unavailable preprocessor invocation is not evidence of correct header selection.

The prepared retry02 itself uses the existing real syntax child with five exact ordered OK lines and one PASS required. The helper prints the selected external root before its compiler invocations. Runtime success remains UNRUN; no compiler trace or corrected PASS is claimed.
