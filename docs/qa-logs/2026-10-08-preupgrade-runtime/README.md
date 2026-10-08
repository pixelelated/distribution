# #519 pre-upgrade transaction and restart rehearsal

The installed old-source transaction and guarded restart qualify on a
disposable GENERIC_X64 guest. **Service masks alone do not survive this
distribution's boot policy.** The corrected operational plan uses temporary
systemd `ConditionPathExists` drop-ins plus a private maintenance marker.
Those conditions blocked the real frontend after a power interruption even
with both automatic-sync settings still enabled. Explicit recovery then
aligned the configuration, removed the temporary conditions and marker, and
restored the original frontend state.

This is synthetic operational evidence, not owner-device acceptance or a new
product feature. No personal credentials, cloud contents or saves were used.
The RG35XX SP was only read separately; no alignment, update or reboot ran on
it. #519 still blocks its next update until the concrete private execution
packet, named authorization and current-state acceptance are complete.

## Source and execution

- Retained replacement16 image SHA256
  `74e57ad8957b1c719c18db098d5713577a952af8802524658d0ada7dee1b6b12`;
  distribution `ee014909137e03706e0b3020b8396be589aaa705`, ES
  `72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`.
- The private plan's 34 distribution inputs match installed-handheld source
  `43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa`. Eight core installed guest files
  were independently hashed. Three additional boot consumers were subsequently
  bound to both source refs and the installed guest after the power failure.
- The guest used a fresh 16 GiB disk, 640×480 virgl display, invented saves,
  recovery copies and a real rclone alias to its own local filesystem. External
  IPv4/IPv6 destinations were blackholed before each proof. No remote account
  was configured. Loopback SSH used a disposable key excluded from this packet.
- Observer bind mounts recorded helper arguments and executed byte-identical
  originals, including real rclone. They are disclosed in `observers.json`;
  this is not a claim of an entirely uninstrumented image qualification.
  After reboot the original installed helpers were checked before observation
  was reattached. The real EmulationStation binary and systemd ran throughout.

## Accepted evidence and retained failures

| Owner | Original result | What it proves |
|---|---:|---|
| runtime-01 | 0 | Fresh matching guest and installed-source hashes |
| proof-01 | 0 | 19 controls: cached ES settings, eight transaction interruption/rollback boundaries, lease/recovery/drift refusal, exact preservation, real guarded restart |
| proof-02 | 0 | Six follow-ups: installed write refusal, real ENOSPC, detached worker lease, actual cloud fallback consumer, durable checkpoint |
| power-01 | **1, unchanged** | Invalid mask-only assumption; boot sorted settings and unmasked/restarted essway |
| power-02 | **1, unchanged** | Corrected gate survived the power cut; post-boot verifier could not read an unsynchronized QA source upload |
| power-03 | 0 | Continuation of power-02's actual boot, with restored/hash-verified QA source; conditional isolation, full transaction and restored frontend pass |

Each owner retains command source, hashes, original inner/outer/wrapper/build
results, terminal watcher status and a later actual-host process-exit receipt.
Submission and terminal watcher `alive=yes` snapshots are not exit proof.
Power-03 neither repeats nor relabels power-02's result. Its evidence binds the
same boot/checkpoint; no new power event is claimed.

`proof-01/evidence/results.json`, `proof-02/evidence/results.json` and
`power-03/evidence/result.json` hold the accepted assertions. The first source
packet's 13 helper controls remain separate and were not rerun.

## Findings that change the operational plan

1. An ES start hook changed the on-disk sync setting to 0 after SystemConf
   loaded 1. Actual startup still invoked `cloud_net_ready`. Editing the file
   alone does not revoke cached automation; stop and guarded restart are needed.
2. `111-sway-init` explicitly unmasks essway during kiosk boot. A persistent
   systemd mask is not a persistent maintenance barrier here. The corrected
   negative path condition remained false across boot while auto1 was present;
   the real frontend never started. Normal completion removes only the owned,
   hash-matched drop-ins and marker before restoring original service states.
3. `001-setup` sorts settings and refreshes the last-good record at boot. The
   touchscreen-keyboard service can also introduce its default. The failed
   first power oracle retains those exact deltas. The corrected control starts
   from the observed boot state and checks the full assignment multiset,
   effective values and modes. **A device reboot still invalidates its private
   byte/boot binding; this is not a general exception for unexplained drift.**
4. A synthetic systemd unit with the installed emustation `KillMode=process`
   policy left its detached worker holding the actual transfer lease after
   stop. The resulting refusal preserved configs. This is an explicitly
   synthetic worker control, not a fabricated ES runtime.
5. The installed cloud fallback restored the aligned `.bak` before refusing a
   missing remote. Only that control temporarily emptied the invented alias
   config, then restored it; no transfer was possible. The operational plan
   does not rewrite credentials.
6. Synchronize every guest fixture **after its last write**, before power-cut
   injection. The missed source upload in power-02 was a harness failure, not
   evidence that the maintenance condition failed.

The eight injected phase failures are deliberate boundary exceptions, not an
exhaustive simulation of flash-write timing. The real power event occurred at
the durable pre-alignment barrier; rollback restored exact synthetic config,
record and mode snapshots. No claim covers arbitrary hardware corruption.

## Retention and remaining work

The guest exited and its disk, firmware-variable copy and QA key were removed
after acceptance; `retirement.json` records 2,333,687,808 allocated disk bytes
released and both ports free. Only compact evidence and the retained source
firmware remain. Full synthetic tar records stay in the small host owners;
this packet omits full stock configuration and duplicate source from them.

Finish the private execution packet using the corrected condition barrier,
fresh source/config/boot/payload binding, exact residue dispositions and
failure recovery. Then obtain named device authorization. The helper scripts
here deliberately refuse ordinary device use and are not the deployment tool.
No RC, publication, personal-data integrity refresh or physical boot claim is
made by this rehearsal. Canonical ES flows are unchanged; the exercised flow
is old-source startup, interruption recovery and return to the idle frontend.
