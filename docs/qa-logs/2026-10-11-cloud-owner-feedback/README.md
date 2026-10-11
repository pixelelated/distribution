# Cloud owner feedback — #536 / #537

The authorized RG SP compositor capture was directly reviewed at720×480.
It shows Dropbox's first screen, the hand over Continue with Google, and the
Apple/Microsoft buttons. A hand is normal hover feedback; the image alone
cannot establish which click was lost. The private image stays local.

A bounded read of window.log counts three refused navigations to
login.microsoftonline.com. No URL path/query, account, credential, or full log
was displayed or published. cloud-signin-window.c filters gesture-initiated
cross-host navigations; this is concrete evidence for the Microsoft path,
not a general diagnosis of every control. The source does not set a tablet
user agent; tablet_pad is the gamepad classification. Actual UA is unmeasured.
The phone pad uses separate move and command queues and a60ms tap timer;
latency ordering remains a separate hypothesis needing a synthetic negative
control. No speculative user-agent or navigation-policy relaxation was made.

#537 source trace at ES1d76b3da7: openCloudAddRemote/provider search invokes
cloudOAuthStart(backend, backend.name). Dropbox therefore requests dropbox.
Session._create_remote_locked refuses that exact name if present. It neither
reauthorizes that existing remote nor allocates a dropbox2 name. If the older
connection has another name, creating dropbox can add a separate connection.
The current CONNECT OR REPAIR description is broader than this native path.
An existing-connections list and repair chooser are available only behind
USE A COMPUTER INSTEAD, leading to SSH instructions. cloud_remote exposes
list/create but no native edit/remove command. The proposed management flow
must preserve selected paths, cloud bytes, unrelated connections and disabled
automation, and define transactional failure/cancellation before implementation.

Can this be done on the VM? Yes for both behavior fixes and lifecycle tests.
Only the exact transient owner panel was captured on hardware, under explicit
screenshot authority. No input, sign-in submission, configuration change,
restart, cloud transfer or new firmware. Source hashes and sanitized readback
are in readback.json. The source trace is not installed-behavior qualification.

#536 next: credential-free installed browser/phone-path fixture, link/button/
input events and navigation-policy cases; retain actual failure and negative
controls before any fix. #537 next: canonical IA/flow and backend transaction
contract, implementation, clean/retained VM proof, reviewed exact-source frames
and applicable review. No known bug may remain when declaring an RC.
