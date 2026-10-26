# Analysis — M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

## Executive summary

- **What it read.** The 14 files the cloud's setup, sign-in, connections, content and settings archives run on: 11,180 lines, every one read, all shipped. Thirteen are the fork's own; `backuptool` is the fork's rewrite of an identical 68-line upstream script. **Lens: security. Depth reason: state preservation.**
- **What holds.**
  - One writer of `rclone.conf` (`cloud_connections.atomic()`, 0600 observed), locked, verified before install, rolled back on failure.
  - Provider diagnostics never forwarded.
  - The only deleting path behind an ordered set of refusals, with the preview's count as `--max-delete`.
  - A settings archive named only after it lists back whole and is scanned for credentials.
  - Probes that report absence honestly: the validator's and the scan's `stop_on`. The setup probe does not (F-21).
  - A log scrub recorded only when every file was rewritten whole.
- **Three candidate bugs, each shown by a host fixture running the product's own code:**
  - **F-01** (Low): the phone listener counts a browser's own icon requests as wrong PINs, and ten lock the right PIN out for the serve.
  - **F-02** (Low; the only deleting path): `RCLONE_NET_OPTS` reaches `--match --apply`'s deleting `sync` unfiltered. With the donor's real rclone, `--delete-excluded` there deletes a save. T16's `cloud_restore` takes the same value the same way.
  - **F-03** (Low): `cloud_content_backup`'s explicit names are not checked as the restore's are, and `'../.config'` uploads `/storage/.config`.
  - **F-20** (Low; found by both seats independently, A-45 and R-40, and confirmed by fixture): `save()` passes an option-shaped key to rclone as a flag. `--config=<path>` writes the new connection, its secret included, into `<path>`, and the save refuses.
  - **Both seats propose Medium for F-02 and F-03** (A-27, A-28, R-47). The coordinator rules.
- **One candidate refuted by fixture:** F-04. A symlink member passes `backuptool`'s name check, and the image's busybox `tar` refuses it.
- **Info and design notes:** secrets on argv and a 0644 state file holding the PIN (F-05); staged credentials a kill leaves behind (F-06); rclone's words and the root password on a screen (F-07); the match's and the listener's smaller edges (F-08, F-09); unchecked or unlocked writes (F-10); a reversible device-id hash (F-11); the window (F-12); the tools' drift (F-13); two why sentences the interface cannot translate (F-14).
- **Twenty-three findings:** 5 Low (F-01, F-02, F-03, F-14, F-20), 18 Info, Design or Renovation. F-20 to F-23 came from the first seat (§ Second opinion), and the seat proposes raising F-10's selection write to Low. **Removals: none.** **Nothing on a person's device or cloud.**
- **Stage E and the guest window.**
  - Six streams fixed #1128 to #1133 (`02` § The streams).
  - The window (07:59:26 to 08:06:04 UTC) proved F-02 and F-03 on the guest's real paths against the QA backend. With F-03, 3,418 files of `/storage/.config`, `rclone.conf` among them, reached the cloud.
  - PL-18's full restore found **F-24**: a standalone symlink an archive carries is restored, and a revert can fail and leave the mark. It is a Low candidate for the coordinator (`05` PL-23).

## Acceptance-criteria scorecard

#664's seventeen, at stage C before the punch-list issue. *Met* names its artifact; *waits* names the stage that ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C |
| 2 | the lint `PASS` | pre-issue at stage C; resolution at the close |
| 3 | the plan, two reviewers, provenance, the manifest's scans | stage C |
| 4 | every punch item at a Phase 7 outcome | waits: stage D onward |
| 5 | `reviewed-at:` and `fixed-at:`; the 14 at `8ebaf8daad`'s bytes; nothing changed at A to D | the diffs are empty (r39, r40); the header lines wait for the hand-back |
| 6 | `01` § Scope | met (`64ff2f519f`), with four deltas |
| 7 | coverage, 14 rows | met |
| 8 | § The writers, generated with asserts | met (`tools/t17-tables.py writers`, 32 rows: 31 at stage B, and the marker the seat found, A-20) |
| 9 | § The secrets' paths, the scrubber's families with *writes it today* | met (28 rows, three families) |
| 10 | § The deletions, the two deleting statements and the refusals | met |
| 11 | § The runs | met (40 generated rows, and the host tools) |
| 12 | § The guest cycle | run 07:59:26 to 08:06:04 UTC (`guest-cycle/`); five of the checkbox's named proofs were not run in the window and are put to the coordinator (`02` § The guest cycle) |
| 13 | `00`'s never-run list, four keyed invokes | met through stage B; the four at stage C |
| 14 | `04` § Q3, Q2, Q4, Q6, Q7 | met |
| 15 | every proof's cell; every punch item's `question:`; every `bug` `box-check` | 27 `proved:` cells and 27 `PROOF:` lines; 23 items with `question:`; six bugs at 0 fail |
| 16 | the retro | waits: stage G |
| 17 | the five checkers | waits: the hand-back |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A player is locked out of the phone keyboard mid sign-in | Medium (every page load may request icons) | Low (the handheld's own sign-in still works; a new serve resets it) | F-01 |
| A match deletes the saves beside the ROMs | Low (needs a non-shipped value in `RCLONE_NET_OPTS`) | High (saves, not recoverable locally) | F-02; the guard is missing, not the loss |
| `/storage/.config`, `rclone.conf` among it, uploaded to the cloud | Low (needs a direct command line) | High (credentials in the player's cloud) | F-03 |
| A connection, its secret included, written outside `rclone/` by an option-shaped key | Low (needs a caller passing such a key) | Medium (a credential at rest where nothing cleans up) | F-20 |
| A partial system selection installed on a full card | Low | Low (systems drop from `--selected`) | F-10 |
| A kill mid sign-in leaves new credentials staged | Low | Low (0600, never archived) | F-06 |
| A French player reads an English refusal | Low | Low | F-14 |

## Coverage boundary

- **Read in full:** all 14 (`stage-b/read-notes.md`). `001-functions`'s `redact_credentials` (outside the 14) was read for what the scrubber relies on. The rule `rclone-cloud-sync.md` was read for its `--delete-excluded` lines and its naming of the setup scripts.
- **Read at the ES pin, under the coordinator's word:** `CloudText.cpp`'s why table, the `cloud_remote create` logging line and the `es_settings` credential keys. `tools/vocabulary-check` ran against it.
- **Read by name only:** the interface's setup, connection, transfer and scan pages; T16's scripts, beyond the `RCLONE_NET_OPTS` lines quoted; T1's `chksysconfig`.
- **Not run:** a guest (the window is asked for); a provider's sign-in page with an account (D-QA-058); the phone page from the host (`CANNOT` under user-mode networking).

## Second opinion

### The packet and the plan

- **The packet** (`second-opinions/packet.md`, 294,779 bytes; `stage-c/packet.py`; `second-opinions/manifest.json`) was trimmed from the start, D-WORKFLOW-195's shape. A first build of 437,469 bytes sat at the size where Argon failed on T30, so this one was cut down before either seat read it. The seats saw:
  - 02, 03 and 04 whole;
  - four of the 14 whole: `package.mk`, `cloud_connections.py`, `cloud_remote` and `cloud_content_transfer`;
  - the other ten **as excerpts**, each covering every cited line with eight lines of context.
  - So an item a seat marked *outside the packet* is settled from the artifact, not from either reading. The lane read all 14 whole at stage B.
- **The scan.**
  - `forbidden-terms-check --stdin`: 0 hits in 94 sections and on the whole file.
  - `SECRET_PATTERNS`: 0 lines, shown to fire on a fake line built at run time.
  - 20 lines masked, and 343 credential-word hits classed. 16 were read by shape only and dispositioned by name in `packet.py`. No value.
- **The plan:** `second-opinions/review-plan.json`, extended, written before the first call.

### GPT-6 Astra (`gpt`, `openai/gpt-6-astra`, `max`)

- **The probe:** 06:51:29 to 06:51:46 UTC. `http=200 model=openai/gpt-6-astra providers=["OpenAI"] effort=max finish=stop`; verification PASS.
- **The refutation:** 06:52:05 to 07:11:33 UTC, one attempt, `finish=stop`, verification PASS. 84,627 prompt tokens and 37,210 completion tokens, 29,303 of them reasoning.
- **What it returned:** `second-opinions/astra-audit.md`, 50 items. By its own labels: 7 confirmed, 35 narrowed, 1 refuted (A-4), 1 refuted in part (A-11) and 6 new (A-45 to A-50).
- **How each was graded:** every item was re-read at its lines at `8ebaf8daad` (`stage-c/rereads/rereads.sh`, `c01` to `c14`, all rc 0). A-45 was settled by a fixture (`c13`).

| Item | Seat | The lane's grade | Evidence | Effect |
| --- | --- | --- | --- | --- |
| A-1 | narrowed | **accepted** | `c01`, `cloud_connections.py:161-180`, `cloud_remote:83-88` | F-05: the token rides `config create`'s argv only, not `lsd`'s, and `cloud_remote`'s own argv holds a typed secret for its whole run |
| A-2 | narrowed | accepted as a packet limit (`excerpt`) | `stage-b/read-notes.md` § cloud_oauth | the lane read `read_state` and the failure paths whole: `error` carries only `_write_config`'s fixed sentences (`:594`) |
| A-3 | narrowed | accepted | `cloud_oauth:2437-2457` | the phone keyboard and `cloud_remote`'s argv are two paths, not one; § The secrets' paths keeps them apart |
| A-4 | refuted | **accepted** | `c03`, `cloud_setup:495-543` | F-07 and its secrets row corrected: nothing masks rclone's ERROR text |
| A-5 | confirmed | accepted, no leak | `c14`, `cloud_oauth:448`, `:594` | the F2 prefix is still written, with fixed sentences only |
| A-6 | narrowed | accepted | `cloud_device_id:133-145` | F-11: 40 bits truncated, several preimages; the machine-id fallback is another case |
| A-7 | narrowed | **accepted** | `cloud_content_restore:886-890` | § The deletions corrected: read, then spent; per-system refusals, not one transaction |
| A-8 | confirmed | **accepted** | `c12` | F-02 widened: six call sites, any flag |
| A-9 | narrowed | accepted | `c12` | every call site passes a literal verb (`copy`, `sync`); flags are the open input |
| A-10 | narrowed | accepted (`excerpt`) | delta 2 of 02 | `backuptool:224` sweeps every staging-prefix object, as the delta says |
| A-11 | refuted | **accepted** | `c09` | F-23, new |
| A-12 | confirmed | accepted | `stage-b/fixture-pin.txt` | F-01 proves the handler; how often a real phone asks is the guest's and the community's to see |
| A-13 | narrowed | accepted as a packet limit | `c08`: `MAX_CONNECTIONS 16`, `REQUEST_TIMEOUT 15`, `MAX_BODY` at `:2399`, the serve's 600 s at `:2681` | the bounds stand as 02 states them |
| A-14 | narrowed | accepted | `c07`, `cloud_oauth:2279-2290`, `:480-488` | F-09: the raw render is reached only on the no-browser branch; the POST accepts a code on both; no script execution shown |
| A-15 | narrowed | **accepted** | `c06`, `cloud_content_backup:711`, `:484-489` | F-03: the destination read; what lands is the guest's proof |
| A-16 | confirmed | accepted | `c12`, `cloud_content_backup:230-232` | F-03 and F-02: the backup's `RCLONE_NET_OPTS` is unchecked too |
| A-17 | narrowed | **accepted** | `c10`, `cloud_connections.py:218-224` | 03 § 3.1 corrected: `select()` is a third writer of `active-connection`; `atomic()` takes no lock |
| A-18 | narrowed | accepted | `c10` | F-06: kill states between the publishes |
| A-19 | narrowed | **accepted** | `c02`, `cloud_content_restore:1405-1406` | F-10: a partial selection can be installed |
| A-20 | narrowed | **accepted** | `c14`, `cloud_oauth:2708` | the writers table gains the `phone-keyboard` marker (32 rows) |
| A-21 | narrowed | **accepted** | `c04` | the scan rows' modes relabelled *by construction* |
| A-22 | narrowed | accepted | `c14`, `cloud_log_scrub:181-187` | F-10: `record()` keeps only `printf`'s status; harmless |
| A-23 | narrowed | accepted as theoretical; **re-graded by Argon's R-46: accepted as an Info hardening** | `c05`, `backuptool:1342`, `:655`, `:1611` | F-10: `mv -fT` and a check that `TARGET` is the file |
| A-24 | narrowed | accepted as a packet limit | `stage-b/read-notes.md` § backuptool | the revert is the guest's proof (F-04) |
| A-25 | confirmed | accepted | `backuptool:1885`, `cloud_setup:69-112` | F-10 as written |
| A-26 | confirmed | accepted | `cloud_oauth:2322-2344` | F-01's fix: ASCII digits checked before `compare_digest`, on GET and POST, which also ends F-09's `TypeError` |
| A-27 | confirmed; proposes Medium | recorded | -- | F-02's severity is the coordinator's |
| A-28 | narrowed; proposes Medium | recorded | -- | F-03's severity is the coordinator's |
| A-29 | narrowed | accepted | -- | F-04: one member shape tested |
| A-30 | narrowed | accepted | -- | F-05 |
| A-31 | narrowed | accepted | -- | F-06 |
| A-32 | narrowed | accepted | -- | F-07's disposition |
| A-33 | narrowed | accepted | `c02`, `cloud_content_restore:436-442` | F-08: no reach today |
| A-34 | narrowed | accepted | -- | F-09 |
| A-35 | narrowed | accepted | `c02` | F-10 |
| A-36 | narrowed | accepted | -- | F-11 |
| A-37 | narrowed | **accepted** | `c14`, `cloud-signin-window.c:532` | F-12: `g_getenv`, so any value turns it on |
| A-38 | narrowed | accepted | -- | F-13: host verdicts, #1127 |
| A-39 | confirmed | accepted | -- | F-14 |
| A-40 | narrowed | accepted | `c10` | F-15, with A-17 |
| A-41 | narrowed | accepted as a packet limit | `stage-a/runs.sh` r02 to r05 | the census ran on the whole files |
| A-42 | narrowed | accepted | -- | Q7: the tables are a map, not proof that the inventory is complete |
| A-43 | narrowed | **accepted** | `rclone/autostart/102-cloud-saves:29` | F-18 corrected: the scrubber runs at boot |
| A-44 | narrowed | accepted | -- | F-19 |
| A-45 | new | **accepted; confirmed by fixture** | `c13_option_key.out` | **F-20**, a candidate bug |
| A-46 | new | **accepted** | `c02`, `cloud_content_restore:1271` | F-21 |
| A-47 | new | **accepted** | `c03`, `cloud_setup:495-498` | F-21 |
| A-48 | new | **accepted** | `c04`, `cloud_scan:315-353` | F-21 |
| A-49 | new | rejected; **re-graded by Argon's R-45: accepted as an Info hardening** | `c05`, `c15`, `backuptool:1285-1292` | a short count is refused; a count that is not a number (only if `wc` fails) skips the refusal. F-10 |
| A-50 | new | **accepted** | `c01`, `cloud_remote:263`, `cloud_connections.py:141` | **F-22** |

**Astra's effect:**
- one new candidate bug, F-20;
- three new Info findings, F-21 to F-23;
- nine first-draft claims corrected: F-05, F-07, F-10, F-12 and F-18; the writers table, the scan modes and the plan's order; and 03 § 3.1;
- two severities proposed for the coordinator, F-02 and F-03 at Medium;
- one item rejected, A-49, then re-graded after Argon (R-45).

### Gemini 4 Argon (`gemini-argon`, `google/gemini-4-argon`, `high`)

- **The probe:** 07:18:19 to 07:18:31 UTC. `http=200 model=google/gemini-4-argon providers=["Google"] effort=high finish=stop`; verification PASS.
- **The refutation:** 07:18:36 to 07:27:05 UTC, one attempt, `finish=stop`, verification PASS. 100,141 prompt tokens and 42,135 completion tokens, 26,651 of them reasoning.
- **What it read:** the same packet, with the lane's grades of Astra appended (`second-opinions/argon-brief.md`, 302,486 bytes). That was 7,707 bytes more than Astra's: the grades table and an eighth question. It did not see Astra's text.
- **What it returned:** `second-opinions/argon-audit.md`, 49 items: R-1 to R-44 on the packet, and R-45 to R-49 on the lane's grades.
- **How each was graded:** re-read at its lines (`c01` to `c15`; `c15` added for R-4, R-6, R-44, R-45 and R-49).

| Item | Seat | The lane's grade | Evidence | Effect |
| --- | --- | --- | --- | --- |
| R-1 | narrowed | accepted | as A-1 | F-05, already corrected |
| R-2 | narrowed | **accepted** | `cloud_oauth:2437-2458` | § The secrets' paths: the phone keyboard's rows are now *sign-in page password*, a sixth kind |
| R-3 | refuted | accepted | as A-4 | F-07, already corrected |
| R-4 | narrowed | accepted; its open question settled | `c15`: `log_message` overridden at `cloud_oauth:2260` | request paths, `?pin=` among them, are not logged to stderr |
| R-5 | narrowed | accepted | `cloud_scan:332-344`, `backuptool:1891` | F-11: the device id also lands in the scan's files and in archive names; the machine-id fallback is 128 bits |
| R-6 | narrowed | accepted, narrowed (`c15`) | `cloud_log_scrub:62`, `:94`, `:193` | F-22: the allowlist drift, once per device, on lines written before the first scrub |
| R-7 | narrowed | accepted | as A-7 | § The deletions, already corrected |
| R-8 | confirmed | accepted | -- | F-02 |
| R-9 | new | **accepted, unproven by fixture** | `cloud_content_restore:750`, `:1046` (argv order) | F-02 sharpened: a filter flag ahead of the excludes |
| R-10 | narrowed | accepted | as A-9 | -- |
| R-11 | refuted | accepted | as A-11, plus `cloud_setup:553`, `:651` | F-23 |
| R-12 | confirmed | accepted | -- | F-01 |
| R-13 | confirmed | accepted | `c08` | the bounds as 02 states them |
| R-14 | narrowed | accepted | `cloud_oauth:2405-2408` | the POST body is read before the gate, bounded by `MAX_BODY` |
| R-15 | narrowed | accepted | as A-14 | F-09 |
| R-16 | narrowed | accepted | `c06` | F-03: the destination; the backup's `RCLONE_NET_OPTS` |
| R-17 | narrowed | accepted in part | `c14`, `c15` | (1) the marker row added (A-20); the `scan.err` redirect is on the statement row `cloud_scan:276` already covers. (2) the scan modes relabelled (A-21). (3) F-06: no directory fsync after the rollback `unlink`. (4) as A-22. |
| R-18 | refuted | **accepted** | `c13_option_key.out` | F-20 (both seats found it independently); 03 § 3.1 |
| R-19 | narrowed | accepted | `c10`, `cloud_oauth:580-583` | F-06 |
| R-20 | narrowed | **accepted** | `c05`, `c15`; `backuptool:1287`, `:655`, `:1342` | F-10's two hardenings |
| R-21 | confirmed | accepted | -- | F-01 at Low, and the fix |
| R-22 | confirmed; Medium | recorded | -- | F-02's severity is the coordinator's |
| R-23 | confirmed; Medium | recorded | -- | F-03's severity is the coordinator's |
| R-24 | narrowed | accepted | as A-29 | F-04 |
| R-25 to R-28 | narrowed | accepted | as A-30 to A-33 | -- |
| R-29 | narrowed | accepted | as A-34 | -- |
| R-30 | narrowed | accepted | as A-35 | F-10 |
| R-31, R-32 | narrowed | accepted | as A-36, A-37 | -- |
| R-33 to R-37 | confirmed | accepted | -- | F-13 to F-17 |
| R-38 | narrowed | accepted | as A-43 | F-18 |
| R-39 | confirmed | accepted | -- | F-19 |
| R-40 | new | accepted | `c13_option_key.out` | F-20 |
| R-41 | new | accepted | as A-50 | F-22 |
| R-42 | new | accepted | as A-46 | F-21 |
| R-43 | new | **accepted** | `c03` | F-21: the probe's substring match on the path |
| R-44 | new | **accepted** | `c15`, `cloud_scan:260`, `:335` | F-21: `CONFIG_ID` before the lock, and the label as a regex |
| R-45 | narrowed: reverse A-49 in part | **accepted** | `c15`, `backuptool:1283-1287` | A-49 re-graded *accepted as an Info hardening* (F-10) |
| R-46 | narrowed: reverse A-23 | **accepted** | `backuptool:1611`, `:1822-1823` | A-23 re-graded *accepted as an Info hardening* (F-10) |
| R-47 | confirmed: Medium | recorded | -- | both seats propose Medium for F-02 and F-03; the coordinator rules |
| R-48 | confirmed | accepted | -- | F-20, fix `^[a-z0-9_]+$` before staging |
| R-49 | narrowed | accepted, narrowed | `c15` | F-22, as R-6 |

**Where the two seats differ, settled from the artifact:**
- **F-20.** Both found it independently (A-45, R-18/R-40). The fixture settles it.
- **A-49 and A-23.** Astra raised them; the lane rejected one and called the other theoretical; Argon reversed both. The artifact supports Argon's narrow form, not Astra's: `wc -l` always prints a number, so the fail-open needs `wc` itself to fail. Both are Info hardenings, not defects with a reach today.
- **R-9.** Argon's filter-order case is a reading of rclone's documented rule. No fixture ran it, so it stays unproven and goes to F-02's guest run as a second case only if the coordinator asks.
- **The seats saw different evidence.** Argon saw the lane's grades of Astra and not Astra's text. Where an item rests on lines the packet only excerpted (`outside the packet` in either reply), the lane settled it from the whole file (`c01` to `c15`).

**Argon's effect:**
- F-20 confirmed a second time;
- three new shapes (R-9, R-43, R-44);
- one new kind in § The secrets' paths;
- two of the lane's grades of Astra reversed, to Info hardenings;
- the scrubber's drift recorded (F-22);
- both seats now propose Medium for F-02 and F-03.

## Finding Verification

| Finding | Re-derivation | Verdict |
| --- | --- | --- |
| F-01 | `cloud_oauth:2196-2206`, `:2308-2344`; `stage-b/fixture-pin.txt` | confirmed by fixture |
| F-02 | `cloud_content_restore:235-279`, `:750`, `:1046`; `cloud_restore:1383`, `:1406-1411`; `stage-b/fixture-content.txt` with the real rclone | confirmed by fixture |
| F-03 | `cloud_content_backup:583-585`, `:710`, `:753`; `cloud_content_restore:1482-1487`; `stage-b/fixture-content.txt` | confirmed by fixture |
| F-04 | `backuptool:551-558`, `:1633-1638`, `:1679`; `stage-b/fixture-archive.txt`; no GNU tar in the tree | refuted by fixture as a bug; kept as a design note |
| F-05 | `cloud_connections.py:161-165`; `cloud_remote:325-335`; `stage-b/fixture-mode.txt` | confirmed; narrowed at stage C (A-1: the `lsd` argv carries no secret) |
| F-06 | `cloud_connections.py:74`, `:157`, `:238`; the lane's grep for a sweep (none) | confirmed |
| F-07 | `cloud_setup:495`, `:537`, `:543`, `:926`, `:937`; `cloud_remote:331` | confirmed; corrected at stage C (A-4: nothing masks rclone's text) |
| F-08 | `cloud_content_restore:837-838`, `:441`, `:886-980` | confirmed |
| F-09 | `cloud_oauth:2206`, `:2271-2290`, `:480-488`; `stage-b/fixture-pin.txt` | confirmed by fixture (the `TypeError`) |
| F-10 | `cloud_content_restore:1405-1407`; `backuptool:1885`; `cloud_setup:69-112` | confirmed; widened at stage C (A-19, A-22) |
| F-11 | `cloud_device_id:143-145`, `:29-31` | confirmed |
| F-12 | `cloud-signin-window.c:532-534`, `:851`; `cloud_oauth:917`, `:990-1000` | confirmed; narrowed at stage C (A-37) |
| F-13 | `cloud_folder_validate:90`, `:252`; the tools' outputs | confirmed |
| F-14 | `stage-b/why-lines.txt`, `stage-b/es-why-sentences.txt` | confirmed |
| F-15 to F-19 | the reads named in each | confirmed; F-18 corrected at stage C (A-43: the scrubber runs at boot) |
| F-20 | `stage-c/rereads/c13_option_key.out`; `cloud_remote:329-334`; `cloud_connections.py:141`, `:161-165` | confirmed by fixture (the seat's A-45) |
| F-21 | `c02`, `c03`, `c04` | confirmed by re-read (A-46 to A-48) |
| F-22 | `c01` | confirmed by re-read (A-50) |
| F-23 | `c09` | confirmed by re-read (A-11) |

**Narrowings made while writing:**
- F-17 first said the rule names `cloud_setup` as a writer; it names no writer of `rclone.conf` at all.
- F-16 first claimed a recount not yet run; it was run.
- F-04 was a candidate bug until the image's `tar` was run against it.
- **At stage C**, the first seat corrected nine claims, each re-read before it was accepted (§ Second opinion).

## Renovation face

### Q1 Modernize

The connection model is the newest shape (F-15). Two asymmetries are proposals for the coordinator:
- `require_manual()` for a new `create` as well as `update`;
- a first connection writing `active-connection`, so the legacy fallback stops being a shape the writer itself leaves.

`cloud_oauth`'s four seams are a split proposal. The four copies of `conf_get` are one helper waiting to be shared.

### Q2 Standards

- **Player text:**
  - `tools/vocabulary-check` against the ES pin: 0 wrong of 163, over `cloud_content_backup`, `cloud_content_restore`, `cloud_setup` and `backuptool`.
  - The other ten files were read by hand against `es-player-text.md`. The departures are rclone's ERROR text on the setup page (F-07) and two why sentences without an interface pair, one of them the *"Not this"* wording (F-14).
  - `cloud_oauth`'s phone page reads in English and French, its warning about the unencrypted LAN in both.
- **Discipline without `set -e`:** the `rc=$?` and `|| return` shapes were read, not assumed. The departures are F-10's three writes.
- **Modes and owners:** § The writers, observed for every Python and busybox writer (`stage-b/fixture-mode.txt`). Everything runs as root; the 0644 files hold no credential but the PIN (F-05).
- **The temp conventions:**
  - `mktemp` checked in `backuptool` (`tmp_file`, `:237-246`);
  - checked with `|| return 5` in `cloud_setup:394`;
  - the `$$` fallbacks in the restore (F-08).

### Q3 Bugs

**(a) Where a secret can travel** (§ The secrets' paths, 28 rows):

- **F-01, a candidate bug.**
  - **The trace:** `cloud_oauth:2330-2344` takes a request's first path segment as its PIN. `_gate` (`:2308-2328`) counts a non-empty mismatch, and `pin_exhausted` (`:2196-2198`) refuses everything at ten.
  - **`Already written:`** nothing; the counter lives in memory.
  - **The VM line:** `tools/t17-pin-fixture.py --expect unfixed|fixed`, on the host now, the guest's serve next.
- **F-20, a candidate bug** (the seat's A-45).
  - **The trace:** `cloud_remote:329-334` splits any `a=b`. `save()` (`cloud_connections.py:161-165`) joins it into rclone's argv, and rclone honours `--config=` and `--log-file=` there.
  - **`Already written:`** nothing a shipped caller wrote.
  - **The VM line:** `tools/t17-option-key-fixture.py` on the host now (outside file written, save refused). The fixed `save()` refuses the key before staging. The guest repeats it under the image's rclone.
- **F-05, F-06, F-07, F-09, F-11, F-12, F-22:** Info and design notes, each with its line in `02`.

**(b) What the deleting path can delete** (§ The deletions):

- **F-02, a candidate bug.**
  - **The trace:** `cloud_content_restore:235-279` splits `RCLONE_NET_OPTS` into the arguments of the deleting `sync` (`:1046`) without an allowlist or a strip.
  - **`Already written:`** nothing deleted until the next apply; no migration.
  - **The VM line:** `tools/t17-content-fixture.py --expect unfixed|fixed --real-rclone <rclone>`: a save deleted unfixed, kept fixed.
  - T16's `cloud_restore` is the same seam, the coordinator's to route.
- **F-03, a candidate bug.**
  - **The trace:** `cloud_content_backup:583-585` and `:710` take any name.
  - **`Already written:`** nothing on the device; an upload already made is the cloud's.
  - **The VM line:** the same fixture, `backup-traversal`.
- **F-04,** refuted as a bug by the image's `tar`; a design note.
- **F-08, F-10, F-21, F-23:** Info. F-10's selection write is proposed for Low by the seat.

### Q4 Package currency

- **rclone:** 1.75.2 on the image (`rclone/package.mk:7`) against the host's 1.60.1-DEV. `tools/cloud-connections-test`'s 26 and `tools/cloud-input-test`'s 9 are host verdicts until the guest repeats them.
- **webkitgtk:** the window's recipe builds against it with the DMABuf renderer off by default (blindspot 48's family, F-19).
- **M7's open issues met:** #1117 (the validator's `rclone` from `PATH`, F-13). #1111, #1113 and #1115 are cited in `03` § 3.5 and met by no finding here.
- **Upstream:** thirteen files absent and `backuptool` rewritten. Nothing upstream-carried to disposition (D-WORKFLOW-209 reaches nothing).

### Q5 Efficiency

The bounds and what the player waits for are F-18's. These scripts run from menus, not on the launch path, so time to play is not touched; the retro cites `docs/vm-qa-log.md`.

### Q6 Dead ends

**Removals: none.**
- `backuptool`'s legacy zip path is reachable while any device holds a zip: a row.
- `cloud_setup`'s console flow is reachable with no argument: a row.
- The lane's recount found no shell function named only once, and three framework-called python methods (F-16).

### Q7 Clarity and structure

**From the directory, no; from the two generated tables, yes.**
- § The writers says which statement writes each file, with its mode, lock and shape.
- § The secrets' paths says where each credential may and may not appear. It is a map, not proof that the inventory is complete: the first seat found the option-shaped key, a log line before validation and a marker it did not hold (A-42, A-45, A-50, A-20).
- `rclone-cloud-sync.md` names no writer of `rclone.conf` (F-17, #909).

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **F-02:** `rclone-cloud-sync.md`'s *"treat any restore-side `--delete-excluded` as a bug"* is written about `RCLONEOPTS`. A rule naming every config value that reaches a deleting statement would have put `RCLONE_NET_OPTS` beside it. A proposal for the coordinator.

### Codification gaps (proposals for the coordinator)

1. **A deleting statement takes its flags from an allowlist, never from a config value whole.** F-02's shape is in two slices' scripts.
2. **Every entry point that names a path under `/storage` checks the name the same way.** F-03 is the one that does not; the restore's regex is the model.
3. **A tool test that asserts a refusal reads its artifacts as "absent means none"** (F-13's content-scope case), so a guard that works is not reported as a failure.

## Quality self-check

- **Blindspot 13:** each scorecard row names its artifact.
- **Blindspot 22:** every fixture has a control that comes out the other way (nine icon requests; the shipped bound; a system name; a `..` member).
- **Blindspot 31:** the selection of writers came from `grep -n` at `8ebaf8daad`, not from the brief's list; two typed claims were corrected before commit (§ Finding Verification).
- **Blindspot 38:** nothing ran on a person's device or cloud. The real rclone ran against a local-backend cloud in scratch.
- **Blindspot 75:** every figure is a command at `8ebaf8daad`, counted unfiltered over 14 paths with `xargs -0`.
- **Rules read this session:** `engineering-practices.md`, `upgrade-and-install.md`, `rclone-cloud-sync.md` (the cited lines), `es-player-text.md`, `player-language.md`, `bugs-are-agent-first.md`, `vm-first.md`, `adversarial-council.md`, `issue-tracking.md`, `decision-register.md`. Decisions: D-CLOUD-023, -141, -142, -149, -175, -178, -179, -181; D-QA-021, -058, -015; D-WORKFLOW-061, -195, -209; D-UI-031, -117.
