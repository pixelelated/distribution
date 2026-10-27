# Research notes — M6.P2 T26, EmulationStation's main menu, GuiMenu (#673)

## Scope

The brief's § 2 block, run from this worktree at `db7be4b104` (stacked on the P1 branch at `2174265e9c`), with `W` the ES worktree at the pin. Its output, verbatim (`stage-a/membership.txt`):

```text
selects 1 paths 2 lines 11883 {'shipped': 2} {'fork-own': 2}
{'c++': 1, 'c-header': 1}
11747 c++ fork-own es-app/src/guis/GuiMenu.cpp
136 c-header fork-own es-app/src/guis/GuiMenu.h
2 .qa-scratch/t26/paths.txt
wc -l lines 11883
2
5124	436	es-app/src/guis/GuiMenu.cpp
23	1	es-app/src/guis/GuiMenu.h
```

**The definitions parser's line** (`tools/t26-defs.py`, run over the two dumps; `stage-a/runs.txt` § the definitions):

```text
pin 156 definitions {'member': 63, 'static': 92, 'free': 1}; base 60
added 97, removed 1, common 59: changed 12 / unchanged 47 (exact), changed 10 / unchanged 49 (whitespace removed)
removed: GuiMenu::openWifiSettings
```

The brief's figures by the pages digest's body-text rule (15 changed, 44 unchanged) and the statics/free split (91/2) depend on the rule; this parser's rules are in its docstring: definitions at file scope only, braces counted in each conditional's first arm, a definition's whole text compared. `getCountryCodes` is classed static, so 92 statics and 1 free. The ten longest match the brief's list line for line (`stage-a/runs.txt`).

## History

The fork's commits to the two files from the base to the pin, by month (`stage-a/history-callers.txt`): 16 in July, 42 in August, 142 in September and 25 in October -- 225, the figure `git log --oneline bccd715707..<pin> -- GuiMenu.cpp | wc -l` prints (`stage-a/runs.txt`). The first is `3319baa73` (2026-07-24, *GuiMenu: native cloud backup/restore entries, drop rclonectl toggle*), the last `23df404f6` (2026-10-13, *GuiMenu: explain standalone save-state limits (#575)*).

## Callers

From outside the two files, at the pin: 23 lines in 10 files name `GuiMenu` (`stage-a/history-callers.txt`, counted by `cut -d: -f1 | sort | uniq -c`): `GuiGameOptions.cpp` 6, `GuiGamelistOptions.cpp` 4, `HttpServerThread.cpp` 3, `GuiWifi.cpp` 2, `main.cpp` 2, `ViewController.cpp` 2, and one each in `CloudOffer.cpp` (`:54`, `openCloudFolderEditor`), `GuiCollectionSystemsOptions.cpp` (`:368`, `updateGameLists`), `SystemScreenSaver.cpp` (`:681`, `getDecorationsSets`) and `SystemView.cpp`. The stage-B pages table names each page's opener inside this file.

## Context

Read in this session, in the brief's § 3 order:

1. **The rules.** The four ES rules and `engineering-practices.md`, `player-language.md` and `least-surprise.md` were loaded at session start; this worktree's additions to `engineering-practices.md` and `es-code-traps.md` were read at stage A (`00`). The sections the brief names are read at their lines as stage B reaches each page.
2. **The register.** Sixteen of the rows the brief names were read at stage A: D-UI-005, D-UI-015, D-UI-017, D-UI-018, D-UI-020, D-UI-023, D-UI-033, **D-UI-046** (FINISH RESTORE PROCESS), D-UI-118, D-CLOUD-002, **D-CLOUD-170, D-CLOUD-171** (the folder step at the wizard's end) against **D-CLOUD-175, D-CLOUD-178, D-CLOUD-179** (the migration retired, a validator, explicit creation), and the open D-WORKFLOW-080. The rest of the 44 are read with the pages that cite them.
3. **The menu map.** Its headings, `:403-408` -- the relink page's heading reads **FINISH RESTORE SETUP**, D-UI-046's drift confirmed at its line -- and D-UI-039 at `:664-669`.
4. **The blindspots.** 4, 23, 29, 33, 35, 49, 50, 57 and 67, by their headings; 4 and 57 bear on Q1 and Q2.
5. **The tests.** The ten harnesses, run at stage A (all rc 0).
6. **The walks and the frames.** Read at stage B with the window's plan.
7. **The French.** 978 of 980 one-line literals (`tools/t26-french.py`); `es-untranslated` 706 of 706 fork strings.
8. **The audits.** T18's notes routed to #673 (PL-17 and PL-21's composers' half: `BRING DATA BACK` and `DOWNLOADED`, `backuptool backup >/dev/null`, a 9 after a failed part read as COMPLETED, latent). T21's notes routed to #673 (the HOSTNAME row at `:9909`, `:3209`'s literal `linux`, the LED page at `:2989`, `setStorage`'s ignored result at `:3130-3151`, two scripts with no `ScriptId` gate, `writeAllText` at `:11587` as Backlog #1186 -- this slice's to move onto the atomic writer). T20's `02` § What T21 and T26 inherit: the gates `offlineScanOn`, `offlineScanSignedIn`, `offlineScanOnline` and `exists("/usr/bin/raofflineproxy-ctl")`, and the title's source `RetroachievementsMenuitem` (`:190`, `:5760`; `SystemView.cpp:1616`).
9. **The issues**, by title and state: #15 open, #27 closed, #48 closed, #63 open, #65 open, #102 closed, #108 closed, #115 closed, #120 open, #147 closed, #148 closed, #149 closed, #186 closed, #187 closed, #198 closed, #241 closed, #258 closed, #303 open, #307 closed, #512 closed, #535 closed, #536 closed, #537 closed, #540 closed, #1143 open, #1145 open, #1147 open. Their bodies are read at stage B where a question needs them.
10. **Time to play.** Read at stage B, with the retro's line in mind.
