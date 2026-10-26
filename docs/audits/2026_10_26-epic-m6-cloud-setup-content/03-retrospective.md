# Retrospective audit — M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

*The fourteen as a system: what they are built on, what they keep to, where they meet the rest. Findings are `02`'s, by number.*

## 3.1 Architectural coherence

- **One writer, one lock, one set of refusals.** `cloud_connections.py` is the only file that writes `rclone.conf` or `active-connection`. It does so atomically, under the transfer lock, and verifies a new connection in a private copy before installing it. Every path to `rclone.conf` goes through `save` or `remove`: `cloud_remote create` and `update`, `cloud_oauth`'s sign-in, and the interface's pages through `cloud_remote`. `select()` is a third writer of `active-connection` (`:218-224`). `atomic()` takes no lock itself; its callers hold it. This is the newest and cleanest shape in the slice (F-15).
  - **Stage C:** the boundary fails open on the keys. An option-shaped key reaches rclone as a flag, and `--config=` writes the new connection elsewhere (F-20, the seat's A-45). Its publishes are each atomic, and the set is not one transaction under a kill (A-18).
- **Three scripts read `cloud_sync.conf` with one reader.** `cloud_setup`, the two content scripts and `cloud_scan` carry the same `conf_get` awk, so the tiers read one value the same way (D-CLOUD-149). It is copied four times rather than shared: a fix to one copy is a fix to four.
- **The only deleting path is guarded by its order of refusals** (§ The deletions). The plan is spent first, then context and mode, an empty plan, an empty root, and the per-system verb and count are checked, with `--max-delete` as the cap. What the order does not cover is the flags another file contributes (F-02).
- **`backuptool` is a transaction with a model archive write** (§ The archive): staged, counted, scanned, listed back, renamed. Its restore takes a copy and a mark before the first write and reverts on failure.
- **`cloud_oauth` is the largest file the fork wrote** (2,830 lines, seven classes), and its seams are visible: broker, phone page, device input, state. A split is a proposal, not a defect (F-15).

## 3.2 Project conformance

- **`engineering-practices.md` § Guards must fail closed.**
  - Mostly kept: `cloud_scan`'s `stop_on`, `cloud_folder_validate`'s `Unreadable`, `backuptool`'s counts, and the refusal that the match's exclusion arrays are loaded (`cloud_content_restore:866-870`).
  - Guards that fail open:
    - the match takes whatever flags `RCLONE_NET_OPTS` holds (F-02), and so do the backup's and the restore's copies;
    - `cloud_content_backup` takes any name (F-03);
    - `save()` takes any key (F-20);
    - the scan's temp, the setup probe and the scan's writes (F-21), found at stage C.
- **`engineering-practices.md` § Verify the artifact, not the report.** `backuptool`'s archive is the model. `--set-systems` and `backuptool`'s rotation report success from an exit status, or from nothing (F-10).
- **`upgrade-and-install.md`.** Each candidate bug's `Already written:` is in `02`. None leaves state to migrate: the PIN counter is in memory; a conf value acts only on the next run; an upload already made is the cloud's. F-06's leftover staging directories are the one already-written state a fix would want to sweep.
- **`player-language.md` and `es-player-text.md`.**
  - Two `>>> why` sentences are not in the interface's table, and one of them is the rule's *"Not this"* wording (F-14).
  - rclone's own ERROR text reaches the setup page (F-07): *a tool's words never reach a player*.
  - `tools/vocabulary-check`: 0 wrong of 163.
- **`rclone-cloud-sync.md`:** `--delete-excluded` *"stripped unconditionally"* is kept for `RCLONEOPTS` and not for `RCLONE_NET_OPTS` (F-02). The rule does not say which script writes `rclone.conf` (F-17, #909).
- **D-CLOUD-142** (no command in `cloud_sync.conf` ever runs) is kept: every reader is text. `backuptool.conf` is sourced, by design: it is the player's own list, and a restore can already write any file under `/storage` (F-04's design note).
- **D-QA-021:** every config-shaped read in this audit went through the filter; the packet goes through the mask and the three-way scan.

## 3.3 Spec fidelity

The brief's figures were re-derived at stage A, and every one held but four, recorded as deltas in `01` and `02`:
- 15 `.$$` lines;
- the staging prefix sweep;
- the directory-wide exit-constant run;
- the vocabulary check, which ran.

At stage B two of the five tools could not give a clean verdict, and the symlink proof was answered on the host by the image's own `tar`. The brief's *"Q6: three python defs referenced once"* held, and so did *"0 shell functions defined and never named"*.

## 3.4 Platform conformance

- **On the host:** the product's own code, with the image's busybox applets where the scripts run under busybox, and M6's donor rclone 1.75.2 where a real rclone was needed.
- **Substitutes, named:** a recording stub rclone, path rewrites into a scratch root, the host's GNU `grep`, `sort`, `gzip` and `timeout` (absent from the donor's busybox), and the host's python 3.
- **The guest** repeats each proof on the installed files under the image's python and rclone, in the window asked for on #664.
- **What only a device shows:** nothing here. The phone page from the host is `CANNOT` under user-mode networking, a harness gap rather than a device fact.

## 3.5 Cross-system interaction audit

### Interaction: T16's sync core x this slice's content scripts (`RCLONE_NET_OPTS`)

- **The shared state:** one config line, read by both slices' scripts and split the same way (`cloud_restore:1406-1411`, `cloud_backup:1367-1371`, `cloud_content_restore:276-279`, `cloud_content_backup:230-232`).
- **The interaction.** T16's scripts strip `--delete-excluded` from `RCLONEOPTS` and not from `RCLONE_NET_OPTS`; this slice's strip neither. On the content side it reaches the only deleting statement (F-02) and every other content transfer. On T16's side it reaches `cloud_restore`'s `sync` restores, the rule's catastrophic case. This is named here and is T16's to read.
- **Stage C (A-8):** the value carries any rclone flag, not one, so the shared fix is one allowlist with checked values, used by both slices.

### Interaction: the interface x the `>>> why` lines

- **The shared state:** `CloudText::whySentences()` at the ES pin, 38 sentences, and `localizedWhy`'s fall-through to the sentence itself.
- **The interaction:** two sentences the scripts print have no pair (F-14). A French screen shows them in English if it shows them at all, and that is the ES slice's read.

### Interaction: the interface's connection pages x `cloud_remote`

- **The shared state:** `cloud_remote`'s argv, carrying every `key=value` the player typed, and its exit and stderr sentences.
- **The interaction:** the pages reach the one writer through `cloud_remote create` and `update`, so the secrets ride on two processes' argv (F-05). The interface logs `cloud_remote create: ` through `maskSecrets` at the pin (`GuiMenu.cpp:7414`); what that mask catches is the ES slice's.

### Interaction: `backuptool` x `chksysconfig` and `post-update` (T1)

- **The shared state:** the restore mark `/storage/.config/.restore-in-progress`, read by `chksysconfig verify` at the next boot to put the copy back and remove what the restore created, and the `.restore-finish-pending` and `.cloud-journey-pending` markers the interface reads.
- **The interaction:** the mark is written whole and read back before the first write (`backuptool:1608-1620`), and removed only once the tree is whole or reverted. The reader is T1's.

### Interaction: `cloud_scan` x `rasteratops-settings-archive` (T16)

- **The shared state:** `select_settings_archives` and `SETTINGS_ARCHIVE_LISTING`, sourced at `cloud_scan:326-329`.
- **The interaction:** the scan's settings row is the archive helper's answer. The call site is read here; the helper is T16's.

### Interaction: M7's open work on these files

- **#1111** connection folders and active selection; **#1113** the phone disconnect notice; **#1115** accessibility against the validator's limits; **#1117** the validator bound to the package's rclone (F-13).
- They are cited by number and never read from M7's worktrees. Every finding here stands against `8ebaf8daad`'s bytes.
