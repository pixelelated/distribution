# Lowercase cloud-folder frame claims — #415

The original b137 run correctly failed three editor regions. Actual baseline
and candidate pairs are retained under baseline/ and candidate/. Each was
visually inspected: /ROCKNIX/Saves becomes the approved /pixelelated/Saves;
the keyboard, title and other layout remain unchanged. The earlier claims
still described /Rasteratops/Saves and missed the lowercase text at x183.

Only those three claims change, to half-open183,226–416,268 against the same
d72084ccad baseline. No mask or baseline changes. The original failed report
is in ../2026-10-04-pixelelated-qualification/initial-frame-diff.md.

Recomparison of the actual78 frames passes21 changed regions,0 unclaimed and
0 missing. Old, missing and one-pixel-undersized claims fail. An8x8 change
outside the text in a disposable frame copy fails too. Original frame and
baseline hashes remain unchanged; proof.json records all of them. This is
image-derived comparison evidence, not generated artwork or a new VM run.

Replay with the existing Pillow12.3.0 environment:
`/tmp/pixelelated-fontenv/bin/python docs/qa-logs/2026-10-04-pixelelated-folder-claims/check-claims.py`.
The first attempt under system Python could not import Pillow and performed
no comparison; the retained controls use the documented environment.

The original image still fails scripts on #414 and is not qualified. Renew
all required image evidence after rebuilding corrected bytes. This claim
correction changes no installed code, settings or cloud data.
