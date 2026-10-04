# Proxy schema-note preflight — #414

The first pixelelated image's default scripts suite found one stale review
comment after the final upstream refresh: package ec60fdd, note5866cd9.
The preceding assertion successfully read the database written by the actual
current Storage implementation. The original full log stays at the immutable
run path named and hashed by source-proof.json; the failure is not waived.

Both checksum-verified upstream archives have identical storage.py and
cache_keys.py bytes. The current consumed schema's api_cache and pending_awards
columns and the ctl's SQL/cache-key uses were read. Updating the note changes
no noncomment script line; source-proof.json records this comparison and the
old/new script hashes. No account, cache or award migration is introduced.

The added rc-preflight check runs in the ordinary preflight and through
`--only proxy-schema`. It reads the selected tree without executing its recipe,
requires one full pin and one header note before the profile import, and
refuses unreadable, missing, malformed, duplicate or mismatched observations.
Its PASS claims note consistency only. The full current-Storage assertion is
unchanged; a scoped invocation cannot claim RC readiness.

Run `python3 docs/qa-logs/2026-10-04-proxy-schema-note/check-guard.py`:
15 controls pass, including the ordinary dispatcher with unrelated checks
stubbed. The same15 controls with only the stale-note condition disabled
produce13 PASS/2 FAIL (scoped and ordinary dispatch). Retained logs include
that negative control and the actual frozen tree's failure. No network or
VM is used by these controls.

The shipped two-line comment correction needs a replacement image and renewed
script-suite evidence. The frozen b137 tree/bundle and running QA files were
not edited. No replacement image or RC claim follows from these source checks.
