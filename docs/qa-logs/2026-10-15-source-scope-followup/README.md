# Source scope follow-up — #528 and #601

Exact original bytes and host metadata are retained in `originals.tar.gz`, indexed by `members.json`; the archive and each live original were independently read back. No firmware or device changes occur in this packet.

- Remaining-component disposition: 143 files and four directories verified against seal `1653da5c`. Selection questions are resolved within its stated scope; named publication questions remain.
- Current FEX/Nix scope: three actual CMake roots map to 81 current database records. Of 61 direct derivations, 53 were retained and eight were absent. Database reads were immutable and before/after hashes match. These are build dependencies, not 81 shipped packages. Complete guest-thunk mapping remains separate.
- OpenABL: public upstream locators and Git-blob-verified texts identify a possible replacement with published source. The distinct SM8550 commit still needs matching against the actual asset before adoption. No source archive was downloaded or existing ABL gap cleared. The #601 comment and original responses are included. The upstream README remains recoverable from its API response; the local README is the dated intake summary.
- Published `64cc45e`: both wordlists succeeded; record CI failed only the external-audit cadence. Final logs are included.

Accepted engineering artifacts remain unchanged. Source retrieval, off-host custody, remaining terms and existing device/publication gates remain open.

The first verification script returned 1 because it compared permission bits with a full stat mode including the file type. That failure is retained. Independent readback verified the unchanged original archive against permission bits, ownership, timestamps and every original byte; no source collection was repeated.
