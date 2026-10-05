# Original ROCKNIX RC2 display comparison

Issues #447 and #448. The maintainer asked whether the last ROCKNIX build
already had the problem and the tests missed it. VM-first: yes. The actual
September29 image was replayed on the current host with its original binary,
unstyled finishing page, desktop user agent and compositor configuration.
No provider credentials, input, forced resize or product change.

## Results

| Original RC2 image | Native compositor | Host HMP and VNC |
| --- | --- | --- |
| Software GPU, diagnostic12 | Correct at all three samples | Previous form at offset0; correct original finishing page at5/15 |
| Accelerated GPU, diagnostic13 | Correct at all three samples | Correct at all three; all nine decoded RGB frames equal |

All eighteen comparison frames were directly reviewed. Offsets0/5/15 start
after the initial finishing capture sequence, not at navigation; actual
elapsed values are retained. The old page reads `Finishing up…`; it is not
the newer Connected card. Original RC2 image SHA256:
`e2b662ba728a22cfb05b16779e4475d631b71645a91506261d4c09c3917a67d6`.
Its installed window hash is
`78f9a727f8a100e81da090bf88d787bd2386844587b8239c1cc20152b57a1113`.
Both image/update hashes and current frozen source were verified before/after.

The discrepancy is therefore reproducible without the subsequent branding,
finishing-page styling, WebKit2.54.1/libsoup3.8 or Mesa lifetime changes.
This identifies reproduction scope, not the exact defective component.
Today's replay cannot establish precisely what the September29 host displayed.

## Why the old qualification did not expose it

The retained original report explicitly records GL through virgl on
`/dev/dri/renderD128`, corroborated by its guest's `renderer: virgl` entry.
That is the accelerated route, which also passes the new matched comparison.
The actual walk log lists sixteen menu/transfer/manager walks; it has no
browser finishing-transition native-versus-host capture. The default runner
at source69e6039f8f likewise has no such suite. These are concrete differences
in renderer and coverage, rather than evidence that the software path was
healthy then. The original two suite failures and successful reruns are
retained verbatim beside this file; they are not reclassified as this fault.

## Historical fixture correction

Diagnostic10 failed before browser launch because the current harness required
`CHASSIS=handset`. RC2 has no `/etc/machine-info`; commit98e1a30362 added it
later to select WebKit's mobile UA. Failure10's original four rc1 channels,
log and actual cleanup remain under `../../signin-render-diagnostic-10-failed/`.
Prepared11 was never started and is superseded.

Fresh12/13 derive metadata presence/hash from the verified old SYSTEM and
check it on the guest; wrong presence/hash controls reject. They assert the
original desktop HTTP/navigator UA and exact original finishing URI.
Current-candidate mobile qualification predicates remain unchanged. No
handset metadata was injected into RC2. This corrects the diagnostic's scope,
not the image.

Software12: submission909cbf; durable18:27:28/all four rc0;
actual a56ea5 cleanup18:27:55. Accelerated13: submissiona56ea5;
durable18:29:06/all four rc0; actual5f2fbc cleanup18:29:22.
Both guests and their owner processes were verified absent before the next
guest started. Diagnostic success does not qualify an RC or resolve #447.

`historical-record-hashes.json` binds the six original records; the adjacent
diff records relevant RC2-to-RASTERATOPS changes. New run artifacts and sealed
harnesses are under `../../signin-render-diagnostic-12/` and13.
