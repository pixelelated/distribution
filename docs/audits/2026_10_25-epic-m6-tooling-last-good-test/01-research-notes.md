# Research notes: M6.P2 T15, the last-good scripts test (#662)

## Scope

**The read hash:** `8ebaf8daad`. The branch `HEAD` at stage A, `60d7f6a5b2`, does not differ from it on the file: `git diff --stat 8ebaf8daad 60d7f6a5b2 -- tools/last-good-scripts-test` is empty.

**The one path, re-derived with the brief's § 2 block:**

```
{'tree': 'distribution', 'path': 'tools/last-good-scripts-test', 'area': 'tooling-and-guards', 'tier': 'fork-own', 'tier_note': None, 'overlap': False, 'language': 'shell', 'lines': 14238, 'patches': None, 'last_fork_commit': '37d26a203e 2026-10-14', 'last_upstream_commit': None, 'reach': 'n/a', 'reachable_by': [], 'buildable_by': [], 'shadowed_by': None}
```

So: **1 path, 14,238 lines, 1,167,697 bytes** (`git show 8ebaf8daad:tools/last-good-scripts-test | wc -l -c`: `14238 1167697`), fork-own, shell, reach `n/a`.

**Provenance:**
- `git log --oneline 8ebaf8daad -- tools/last-good-scripts-test | wc -l`: **408** fork commits.
- From `52c4249759` (2026-09-10, *tools: last-good-scripts-test -- device-less proof that the writers keep the last good state*) to `37d26a203e` (2026-10-14, *qa: correct waiting-status check and retain M7 follow-ups (#589)*), the inventory's `last_fork_commit`.
- `git log --oneline upstream/next -- tools/last-good-scripts-test | wc -l`: **0**.

**The 34 sections,** from `grep -n -E '^echo "  [a-z]{1,2}\. '` at the hash (the capitalised sub-groups inside `y` and `z`, such as `A.`, `C.`, `CF.`, `D.` and `S315.`, are cases within them, not sections):

| Section | First line | Its echo line, cut |
| --- | --- | --- |
| `a` | `:429` | chksysconfig keeps and restores the last good system.cfg"… |
| `b` | `:518` | backuptool: a kill mid-tar leaves the previous archive; a failed restore puts the snapshot back… |
| `c` | `:607` | set_setting is one rename; sort_settings refuses an empty result"… |
| `d` | `:650` | cloud_sync_helper and the saves scripts keep the config's last good copy; stamps survive a kill… |
| `e` | `:723` | nothing a screen can show carries an exit code, a log path, a tool's name or a flag"… |
| `f` | `:766` | backuptool: rclone.conf never enters an archive, and the scanner knows rclone's key names (#52)… |
| `g` | `:839` | the in-script RCLONE_NET_OPTS fallback is the shipped value (#146)"… |
| `h` | `:854` | the rclone wrapper: an automatic run's stalled call ends at the ceiling, a deliberate run's at … |
| `i` | `:893` | cloud_net_ready settles on a held default route however NetworkManager judges connectivity"… |
| `j` | `:934` | cloud_sync_helper migrates the shipped retry bound once, and leaves a hand-tuned value alone (#… |
| `k` | `:962` | backuptool: what the image ships does not travel, and an older archive's copy of it is not put … |
| `l` | `:1114` | a missing cloud folder reads as not there yet whatever the server's words (#142)"… |
| `m` | `:1251` | the shipped device name becomes this unit's own, once; a player's name is never touched (#50)"… |
| `n` | `:1403` | a deliberate cloud_backup ends a transfer that stops making progress at the stall ceiling, and… |
| `o` | `:1534` | set_setting system.hostname default keeps the line chksysconfig's sentinel reads, empty (D-NET… |
| `p` | `:1565` | raofflineproxy-ctl: enable records hardcore and turns it off, disable puts it back; both harml… |
| `q` | `:1752` | 099-networkservices: a daemon fragment that sets no CONF inherits none from the fragment befor… |
| `r` | `:1860` | the launch log carries no credential value: setsettings' Added setting and Fetch lines, runemu… |
| `s` | `:1949` | rocknix-evidence: every file in the bundle has been through the credential filter, summary.txt… |
| `t` | `:2033` | raofflineproxy-ctl scan, topup and ready against the client the tree describes: the refusals, … |
| `u` | `:2856` | wifictl current, saved, forget and join read NetworkManager, not the setting; forget says when… |
| `v` | `:2991` | the save state manager's arguments reach RetroArch as Batocera's launcher carries them (#196, … |
| `w` | `:3067` | cheevos_armsx2.sh writes one Token line to secrets.ini, however often it runs (#170)"… |
| `x` | `:3113` | the launcher's incremental-save modes, the password's handoff, and the keeper's cut/whole note… |
| `y` | `:7796` | audit #307 / #308, stream B: backuptool, wifictl, the settings writer and lock, factoryreset, … |
| `z` | `:13182` | the audit of the fix round, stream B: the conf read as text, a flag's password redacted, the … |
| `aa` | `:13723` | cloud_migrate_layout --state, --keep and --follow (#353, D-CLOUD-160/161): the layout as fac… |
| `ab` | `:13913` | cloud_scan (#350, D-CLOUD-156): the opening scan's three items, the content scan's one, the … |
| `ac` | `:14121` | the Retroid Pocket Nova's ledcontrol (#332): LED BRIGHTNESS writes the LEDs, rgb with no col… |
| `ad` | `:14142` | a backup does not make a missing earlier-default saves folder (D-CLOUD-172, #363): the offer… |
| `ae` | `:14177` | cloud folder state table and archive writer/reader contracts (#365, #383)"… |
| `af` | `:14191` | content inactivity across provider retries (#401)"… |
| `ag` | `:14221` | settings writers retain private file permissions"… |
| `ah` | `:14229` | melonDS update preserves settings and adds missing hotkeys"… |
