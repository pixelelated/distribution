# #1474: the offline switch says why a change did not take

Proof packet for [#1474](https://github.com/pixelelated/distribution/issues/1474), 2026-11-26. The canonical reference is `docs/es-menu-map.md` § RetroAchievements (our rows). The frame index is `evidence-index.json` (schema 1).

**Source:**
- EmulationStation `2f6c01fd7` (local branch `m7/rc-round-es-20261125`);
- the round `bfff87f94c` (local, build 9);
- the image `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261126T095201Z.gbfff87f94c1b-from-ROCKNIX`.

**Guest:** a QA guest from that image at 640x480 (`VM_RES=640x480 tools/vm-pair up`), English.

**The run:** `tools/vm-walks/offline-toggle-outcomes` at round `d74be32a88`. It ran 10:06 to 10:13 UTC; `RESULT.txt` is its own record.

Can this be done on the VM? Yes. Each outcome is made on the guest with `tools/raofflineproxy-lifecycle-test`'s constructions, in `tools/vm-walks/fixtures/offline-toggle-guest.sh`. Each case starts from a rebooted guest with the proxy on. Before the condition is armed, the proxy's admission is confirmed free (`<case>-idle.txt`).

| Case | Armed | Lifecycle answer | State after | Frames |
| --- | --- | --- | --- | --- |
| busy | an images pass holding the proxy's admission | `BUSY`, terminal, `busy` | on, service active | `busy-2-answer.png`: OFFLINE ACHIEVEMENTS ARE STILL ON. GAMES ARE STILL GETTING READY FOR OFFLINE PLAY. TRY AGAIN WHEN THAT FINISHES. `busy-3-after-ok.png`: switch ON, Current setting: on. |
| refused | a drop-in on the lifecycle owner unit | `REFUSED`, terminal, `refused` | on, active | `refused-2-answer.png`: OFFLINE ACHIEVEMENTS ARE STILL ON. THE CHANGE COULDN'T START. TRY AGAIN. `refused-3-after-ok.png`: switch ON. |
| restored | a directory at `system.cfg.tmp`, so both settings writes fail (#1467) | `RESTORED`, terminal, `restored` | on, active | `restored-2-answer.png`: OFFLINE ACHIEVEMENTS ARE STILL ON. THE CHANGE COULDN'T BE SAVED. TRY AGAIN. `restored-3-after-ok.png`: switch ON. |
| took (control) | nothing | `DISABLED`, terminal, `disabled` | off, inactive | `took-2-answer.png`: no dialog, switch OFF, Current setting: off. |

`<case>-1-page.png` is the page before the press, the same in every case.

**Not framed here:**
- ROLLED_BACK, after an enable, and the refused-at-submit case attached to another operation. Both are covered by `OfflineAchievementsText::toggleDeclined`'s doctest cases, not by a guest frame.
- The French sentences. Their catalog entries are in the image's `emulationstation2.mo`, read with `msgunfmt` at build 9's acceptance, but no French frame was taken.

**The first full run** at 1280x800 (`/workspace/tmp/rocknix-session/1474-walk-0958Z-3/`) framed busy, refused and took the same way.
- Its restored case answered `busy`: something held the proxy's admission at the press that the case had not armed. The frame showed the busy sentence, which is the page reporting what the backend actually said.
- That run had no idle check, so the holder is unknown. The driver now waits for idle admission and writes down who held it. This run found it idle at 0 s in every case.
