# Upstream comparison — October 12 (#534, #558, #559)

This is a read-only comparison, not an upstream integration. D-WORKFLOW-111 still freezes the first-release baseline; #559 owns the later release-based integration strategy and its timing decision.

| Snapshot | Commit | Scope |
| --- | --- | --- |
| Accepted pixelelated firmware | `bc9dfe8141d9561dc1d8502313d00a84c4566ee8` | Installed on RG SP and Nova |
| Frozen ROCKNIX baseline | `9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6` | September 29 |
| Latest full release, 20261001 | `c445081a59518f37d9776e5412dd7b14910696f7` | 11 commits beyond baseline |
| ROCKNIX next, checked October 12 | `d59bdaa28908f7266e40172e088ec40813fd3f46` | 205 commits beyond baseline; 194 beyond release |

[ROCKNIX 20261001](https://github.com/ROCKNIX/distribution/releases/tag/20261001) was published October 1 at 22:56 UTC. Fetching the tracking ref did not merge, rebase, rebuild or change a package pin.

## RG SP LED

The H700 `ledcontrol`, common dispatcher and `led_flash` are byte-identical across all four snapshots. Upstream `powerstate.sh` is unchanged between baseline, release and next; our version includes fork changes. The correctly located `packages/tools/batteryplus`, H700 quirks, RG SP device tree and its inherited LED patch have no upstream delta in this interval. New RK3326 clone LED changes target different hardware. The comparison's absent `sysutils/batteryplus` row is an initially incorrect lookup, not evidence about the real package; the real path was checked separately.

No applicable new H700 LED fix was found. The installed red preference and LED values under [#534](../2026-10-12-rgsp-led/README.md) remain the supported explanation. No setting was changed. Common settings/flock, memory, kernel and suspend changes on upstream next still require overlay review; newer does not establish relevance to this observation.

## Nova bootloader

Our accepted ABL package is 1.1.9. [Upstream v1.2](https://github.com/ROCKNIX/abl/releases/tag/v1.2) changes logo/version, SoC labels and incompatible-SoC messaging. Its release notes do not describe a shutdown or intermittent Linux-load fix. The referenced LinuxLoader commit is `e9d37131c0c2273076468156fb0f87aa6834202b`; the prior reference is `4588733123554b1f7bf935b04e494e4284894546`. Available release notes are not an implementation-source diff; #528's ABL source-access gap remains.

The SM8550 path history adds `gpt` to the Linux kernel command line (`03401927293e7ad83f81245d3cb7e8be3b555036`), updates kernel configuration, skips the RAID6 benchmark, and calibrates other models' panel timings. The Nova device tree and existing USB boot-hang patch are unchanged across this interval. Kernel command-line handling occurs after ABL loads Linux, so the `gpt` change is not evidence of a fix for the reported pre-Linux error. No tested corrective change is identified here.

[Upstream charging documentation](https://rocknix.org/configure/fake-suspend/#charging) says many supported devices start again if shut down while a charger is connected. This is a possible explanation for the restart only; it does not explain the bootloader load error or establish the cable state during this incident. Current charging state cannot prove past charging state. Initial GitHub/documentation searches found no exact Nova report; this is a bounded search, not proof that none exists.

## Future work

#559 proposes release checkpoints, explicit targeted-fix triage, an overlay/conflict inventory and clean/retained VM plus required physical qualification before integration. A reviewed merge preserving published history is a proposal; no strategy or freeze exception is adopted here. #560 separately evaluates fast shutdown: accepted ES skips gamelist writes via `IgnoreGamelist`, then follows normal teardown and the power-off command. Actual time saved and exact metadata-loss scope remain to be measured.
