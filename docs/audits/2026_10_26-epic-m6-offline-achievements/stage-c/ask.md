# Second opinion (Phase 4.6), M6 T19: the offline achievements proxy, in pixelelated's distribution

You are one of two independent reviewers for a read-only renovation audit of 27 paths under a **security and new-functionality lens**. They total 5,369 lines at the distribution commit `8ebaf8daad`.

- **Nine fork-own files:**
  - `raofflineproxy-ctl`, the OS's and the interface's one door to the proxy (bash, 2,455 lines);
  - three python helpers the ctl runs under `timeout`: `raofflineproxy-refresh`, `-cache-images` and `-cache-indexed`;
  - the recipe, the systemd unit, the boot-time daemon file, and two sibling recipes.
- **Eighteen patches** the fork carries against upstream RAOfflineProxy at its pin `c7ebd1b6e7`.

**What it is.** RAOfflineProxy is a Python service between an emulator's rcheevos client and retroachievements.org, on `127.0.0.1:8080`. It answers from a local SQLite store when the link is down, queues awards earned offline and sends them when the link returns, and caches game data and badges.

**What ships.** The product is an immutable handheld OS; a person updates it in place and keeps `/storage`. One player uses one console at a time. Every process on the device, the service and the interface included, runs as root.

**What you get.**

- The first reader is another lab's model. You get its `02-forward-audit.md` (whole: coverage, the listener, the credential's paths, the generated writers table, the patches, the bounds, the runs, the guest cycle, what the next slice inherits, 25 findings, the positives), `03-retrospective.md` and `04-analysis.md`.
- Then context: the order's entry and the brief's questions.
- Then the fork's files whole and line-numbered: the ctl, the three helpers, the unit, the daemon file and the recipe.
- Then the patches the findings turn on, whole: 001, 007, 008, 010, 011, 012, 013 and 015.
- Then **line-numbered excerpts** of the patched upstream modules the analyses cite: `proxy_service.py`, `auth.py`, `network.py`, `storage.py`, `utils.py`, `log_uploader.py` and `usage_report.py`, each cited range with eight lines of context.
- Then the interface's `CloudText.cpp` lines the protocol table cites.
- **When a claim needs lines outside the packet, say `outside the packet` and do not guess.**

**Masking.** Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`; a `***` is the mask, not the code. The packet was scanned for credential shapes before it left, and no hit was a value.

**Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. The ctl's and the helpers' line numbers are `8ebaf8daad`'s. The upstream modules' are the patched pin's.

**What was run.** Nothing can be run for you.

- **On the host:** the patched pin unpacked (18 of 18 at fuzz 0); its integration test, 12 OK; the scripts suite, 1,379 PASS (it runs the real ctl in a sandbox); one fixture reproducing F-17.
- **On a guest:** an image whose ctl and client are a later branch's. So the tree's four scripts ran from `/storage/t19/bin/` against that image's service. `02` § The guest cycle says which side each verdict belongs to.

Answer these first, in this order:

1. **Where a credential travels (Q2; F-01, F-02, F-05, F-25).**
   - Does `handle_offline_login` (`proxy_service.py`, the excerpt around 491-505) really serve the cached sign-in body, `Token` included, to a request that names the account and proves nothing? Under exactly which conditions?
   - Is anything in the request path a check the first reader missed: a header, the peer address, the `Host`?
   - Is the redaction of `t=` and `p=` in the request log and in the upload bundle complete for every credential the service holds?
   - Do the helpers' printed exception texts (`FAIL ... {error}`) ever carry a URL with a credential?
2. **What runs as root on an unauthenticated port (Q1; F-03, F-04).**
   - Is the readiness check's acceptance of a foreign `0.0.0.0:8080` listener right, and is its disagreement with `setsettings.sh:536` (quoted in `03`) what the first reader says?
   - What does the unit's lack of hardening actually expose, given that the device is single-user and root everywhere?
3. **A check whose failure reads as success (Q3, Q6; F-06, F-07, F-08, F-15, F-16, F-17, F-18, F-24).**
   - For each: is the branch the first reader names really reachable, and is its consequence what it says?
   - Is there a `cannot_tell` site that is not reached on a failure it should catch?
   - Is there a pipeline whose first stage's failure is discarded?
4. **A bound that is not enforced (Q4; F-11 to F-15).**
   - Check every row of `02` § The bounds against the code.
   - Is the scan's missing deadline a defect, or the foreground page's design the analyses say it is?
   - Is F-14 right that `http_post` marks no 429 pause where `http_get` does?

Then:

5. **Refute or confirm each finding F-01 to F-25** in `02` § Findings index: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For the six proposed bugs (F-01, F-03, F-06, F-07, F-16, F-17), also judge the severity and the fix a stream would make, and what the code before a fix has already left on devices.
6. **What the first reader missed:**
   - a defect in the whole files, the patches or the excerpts: a credential where it should not be, a write judged by nothing, a lock that fails open, a stamp that can say the wrong thing, a protocol line the interface misreads, or a bound with no enforcement;
   - a patch whose `+` side introduces a defect;
   - a disposition that should be different.

**Output:**

- Numbered items `{PREFIX}-1`, `{PREFIX}-2`, ..., grouped under the six headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.
