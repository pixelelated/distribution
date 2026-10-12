# Owner testing feedback — October 12

Four future tasks preserve the owner's exact feedback and agent-verifiable criteria:

| Issue | Observation / current evidence | Future verification |
| --- | --- | --- |
| #565 | Nova already had the owner's RetroAchievements sign-in. Exact accepted SYSTEM defaults have empty player credentials; the update preserved prior parsed settings. | Original provenance if recoverable; clean/retained VM account separation and final public-firmware credential gate. |
| #566 | Ordinary players should not need ScreenScraper developer credentials. Runtime entry was intentional under D-QA-005/006; compiled credentials already take precedence. | Obtain/verify the supported pixelelated developer identity and distribution terms, then release provisioning and updated account flows. No shared credential embedded. |
| #567 | Game-list refresh starts offline achievement preparation without advance explanation. Accepted GuiMenu.cpp:5756/8459 shows UPDATE GAMELISTS and REALLY UPDATE GAMELISTS? only. | Conditional clear copy with English/French small/large VM frames, preserving behavior. |
| #568 | Nova's game309of309 took much longer than earlier games. Source has work after game processing. | Distinguish slow final game, retries and finalization using phase timings; add a truthful finishing state only where warranted. |

These are outside M7's current source/build sequence. #528's existing publication
credential obligations remain; no confirmed personal-credential leak was found.
No device command, cloud operation or new actual RetroAchievements request ran.

## Exact firmware triage

The existing accepted Nova update tar was read locally, extracting only its SYSTEM
to private scratch. SHA256 matches accepted c97f57f1c9926dc294a0c08236e0d3229f0a654a9e0f2b2ac29be2087445bf89.
`unsquashfs -cat` read four default config files and the shipped ES binary. Config
parsing recorded field names and presence booleans only; no values or personal
config hashes. Known compiled developer URL-pair patterns were checked in memory.
The ES binary matches accepted e71a3f8dec7035ac03def95fcadcd639b49444ba11f4124539512b4bf58ee056.
Existing private #557 pre/post receipts were compared for aggregate settings equality.
The1.59GB SYSTEM scratch was deleted immediately after inspection.

`firmware-triage.json` retains the exact checks. This is a selected-surface inspection,
not a universal secret scan or fresh boot proof. Original sign-in author is unknown.
The manual inspection script remains private under
`/workspace/tmp/pixelelated-owner-feedback-20261012/inspect-firmware.py`.

The current `tools/fork-publish-release` prepares an offline release plan and names
artifact credential inspection as a remaining gate. Older rule prose describing its
retired uploader is historical behavior, not proof of the current gate's execution.
#565 must bind the real publication path to an executable verified check.

## Progress-phase lead

Accepted raofflineproxy-ctl's run_jobs processes DONE but retains its last game
index while waiting for helper termination. Badge work can follow game processing.
The scan then may run an image pass (default300-second bound), and top-up has a
recently-played pass. run_image_pass logs its phase but emits no distinct UI phase.
This is a reason to test NofN/finishing behavior, not a diagnosis of the reported run.
No new performance or UI proof is claimed. Canonical flow and source-bound frames
must accompany any eventual text/behavior change (D-WORKFLOW-155/156).
