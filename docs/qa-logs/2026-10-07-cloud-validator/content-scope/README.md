# Selected cloud library controls — #508/#510

These are host source controls using synthetic isolated filesystems and real
rclone 1.75.1. They are not firmware or VM qualification.

Earlier `pixelelated-content-scope-06/result.json`: 19 PASS against distribution
commit `2cffff3f38`. Its source copies and tool copies are retained with checksums.
Controls cover exact selected ROM/BIOS restoration; refusal of unreadable or
partial listings; selected-root and path traversal boundaries; scan run,
configuration, mode and output binding; and refusal to modify another scan
owner's cache. Synthetic cloud bytes are unchanged after every control.

Earlier runs remain evidence of development. Run03 had 18 PASS before final
minor tightening; run05 had 18 PASS against the final source. Run04 could not
start bubblewrap inside the harness sandbox: its one apparent PASS was vacuous
and is **not accepted evidence**. Run06 requires a successful isolated fixture
startup before any control is graded. The host launch initially failed during
automatic approval review because workspace credits were exhausted; no job
started then. Host execution succeeded after service recovery.

`pixelelated-content-scope-unfixed-01` records three failing controls against
the retained pre-change draft `3268015c`: unselected folders offered, unselected
bytes counted, and an epoch stamp rather than a bound completion result.

Only compact command/result/argv records and final tested sources remain.
Completed fixture filesystems were retired after their receipts were copied
and checksummed. No personal cloud data or credentials were used.

Final `pixelelated-content-scope-07/result.json`: **21 PASS** at
`be7d8104988281314cc4d4400bc318e43fef0cff`. Two additional controls verify
prompt refusal at unreadable relative (`remote:`) and absolute (`remote:/`)
selected roots without changing namespace or reading an ancestor. The preceding
`pixelelated-content-root-unfixed-01` run at `75d44aea8e` reproduced a two-second
timeout at the relative root; the absolute-root control already passed.
The parent walk now shortens each time and preserves the selected namespace.
Both runs retain exact fixture inputs, command records and checksums.

The restore fix is now commit `90df1172a1cdc98865e6efc0422ed3845e5631e9`;
its message-only amend adds issue citations. Its source tree is identical to
`be7d810498`, the identity retained in the run07 receipt.
