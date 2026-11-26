# #1427: COPY TO FREE SLOT from an autosave that is the game's only state

Proof packet for [#1427](https://github.com/pixelelated/distribution/issues/1427), 2026-11-26.

**The defect.** At the shipped ES pin `16dbac5211`, `SaveStateRepository::getNextFreeSlot` returned the first slot only when the game had no states at all. An AUTO SAVE is slot -1, so a game whose only state was its autosave fell through to the search for a numbered slot, found none, and returned -99. The manager's north press then stopped silently.

**The fix is not new in this round.** The round's ES (`d87891f24`) and the candidate `0a3e979e50`'s ES (`409704f3b`, tree `0d852e5d1106`) both carry it, with the same function body. It returns the first slot when no state has a slot of 0 or more. The same ES carries #1242's worker, lock gate and `SAVE STATE COPIED.` feedback around the copy.

## Criterion 1: the allocator, from exact bytes

`allocator-test.py` cuts `getNextFreeSlot` out of two ES revisions with `git show` and compiles each body unchanged against stub collaborators:

- `isEnabled()`;
- the FileData → SystemData → repository chain;
- `getSaveStates()`, which returns the case's slots, where -1 is the AUTO SAVE.

It then runs the same 14 cases on both.

```
python3 -I allocator-test.py --es <ES checkout> --baseline 16dbac5211 --candidate d87891f24 --out run-1420Z
```

| Mode | Revision | Body sha256 | File sha256 | As expected |
| --- | --- | --- | --- | --- |
| baseline | `16dbac5211` | `82ea2b73959d0805…` | `34bda9a72d037af7…` | 10 of 14 |
| candidate | `d87891f24e` | `dd008d37871ae2dc…` | `9fe8414b6d123e5c…` | 14 of 14 |

- **The baseline's four mismatches** are the autosave-only cases: no config, and `firstslot` 0, 1 and 7. Each returned -99 where 0, 0, 1 and 7 were wanted.
- **The ten unchanged cases** are disabled, empty (four configs), slot 0, slots 0 1 2, gap 0 2, autosave and slot 3, and high bound 99999.
- **The record** is in `run-1420Z/`: `RESULT.json`, and per mode the extracted body, the harness, `compile.txt` and `stdout.txt`.
- **The binaries** were removed after the run; the script now does that itself.

This repeats the November 8 component result (four autosave-only mismatches, 14 of 14 on the candidate) against the bytes that ship. That test's own source was not found outside M6's records.

## Criteria 2 to 4: the installed run

**The guest:** a fresh `tools/vm-pair` guest from build 12's image, `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261126T140833Z.ga069abd23615-from-ROCKNIX` (`BUILD_ID` `a069abd236…`, ES `d87891f24`), at 640x480, English.

**The run:** `free-slot-proof.sh` into `guest-1502Z/`, from 15:02 to 15:07 UTC. Its own record is `RESULT.txt`: 16 checks, every one PASS, then PASSED.

**Can this be done on the VM? Yes.**
- **The game:** a 32 KiB Game Boy ROM built at run time (`tools/ra-auto-slot-test`'s SlotProbe; this run's copy hashed `618f68095f216943…` and was not kept), so the core makes a real state.
- **The control set:** another game's saves, seeded first: `Ctrl.state.auto`, `Ctrl.state2`, their thumbnails, and an `.srm`.

**The steps.** Every step hashes the saves tree and the capture records.

| Step | What happens | Result |
| --- | --- | --- |
| 1 | Launch through the interface's API. RetroArch's clean exit writes the AUTO SAVE. | `SlotProbe.state.auto` `da549ef4…` and its thumbnail `4f016368…`. The manager shows START NEW GAME and AUTO SAVE only. |
| 2 | The transfer lock held (`flock /var/run/cloud_sync.lock`), north on AUTO SAVE. | A SYNC IS ALREADY RUNNING. / WAIT FOR IT TO FINISH, THEN TRY AGAIN. No `SlotProbe.state` is made and the AUTO SAVE is unchanged. |
| 3 | The lock free, north on AUTO SAVE. | The toast SAVE STATE COPIED. appears, with a SLOT 0 tile and the cursor on it. `SlotProbe.state` has the AUTO SAVE's bytes (`da549ef4…`), and its thumbnail has the AUTO SAVE thumbnail's. The AUTO SAVE and every control file are unchanged. `cloud_capture --adopt` recorded "SlotProbe.state is a copy of savestates/gb/SlotProbe.state.auto: the same version, recorded at the new path" (`3-cloud_sync-log.txt`, `3-records.diff`). |
| 4 | Reboot, then reopen the manager. | The SLOT 0 tile is there and the copy's bytes are unchanged. |
| 5 | A second launch, then a controlled exit. | RetroArch loaded `SlotProbe.state.auto`, and the exit replaced it (`edc5d2bf…`; the tile moves to 10:06). The copy and the control files are unchanged. |
| 6 | LAUNCH on SLOT 0. | RetroArch logged `Loading state "/storage/roms/savestates/gb/SlotProbe.state"`. After that session's exit, the copy and the control files are unchanged. |

**The exit is RetroArch's clean exit on SIGTERM**, which is what the exit hotkey sends. Only the press is a substitute: the exit path is real (the exit auto save, `runemu.sh`'s return, the interface's end of game). The real Quit confirmation was seen on 2026-11-22, on the retained-storage candidate (#1427's comment of that day): the numbered copy was kept, and it loaded the earlier state.

**What the composition holds.** It is #1242's, composed in the round's ES and not changed here:
- **The press:** `GuiSaveState::input` refuses while a sync runs or another process holds the transfer lock (`savesTreeBusy`), and asks `getNextFreeSlot`.
- **The worker:** `SaveStateBookkeeper::makeCopy` takes the transfer lock, refuses a slot that is no longer free, and copies with `Utils::AtomicFile::copy` (temp then rename) under a size check, removing a partial copy on failure.
- **The record:** `runCopy` publishes the outcome and then runs `cloud_capture --adopt` for the copy's provenance (#206, D-CLOUD-134).
- **The page:** `update()` reads the ticket, refreshes, puts the cursor on the new tile and says SAVE STATE COPIED.
- **The build:** build 12 built, and standard `vm-qa` run 9 passed on it (#1465).

**Fresh and retained storage.**
- **Fresh:** this guest, whose seeded control saves came through every step byte for byte.
- **Retained across a reboot:** step 4.
- **Retained across an update:** #555's PC run, check 2a of 2026-11-25. Updating in place from the November 5 build kept a Slot 0 state and its thumbnail byte for byte.

`evidence-index.json` maps the eight reviewed frames to the flow (`docs/es-menu-map.md` § Save state manager).
