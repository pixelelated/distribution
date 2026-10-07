## Maintainer request

> If the user chooses to migrate, must they then migrate their other devices? I assume it is a move and not a copy? We might want to say, if that’s the case, that you’ll need to migrate other devices when they upgrade. Also, can we have the path render as ‘/ROCKNIX’ and ‘/pixelated’ if that styling is supported?

Follow-up to #501. Initial read-only source investigation preceded filing; at that point no product edit or device/cloud operation had occurred. The preceding request asked for comparison without immediate changes. The maintainer subsequently approved implementation and parallel work. The verified source change below does not restart or modify the frozen device builds.

Clarification received in the same conversation:

> I meant ‘/pixelelated’ and was wondering if it supported Markdown-style formatting.

Copy revision from the maintainer:

> Instead of “earlier version”, which implies this is the same OS. We should say that your cloud has a ‘/ROCKNIX’ folder from a previous OS. Move the folder to ‘/pixelelated’? One you do, you’ll need to confirm the migration on other devices that sync with this cloud.

After the existing automatic-follow behavior was explained, the maintainer selected:

> Keep automatic switching; use conditional wording

This settles the copy direction in D-UI-122 without changing migration behavior.

The maintainer then refined the other-device explanation:

> If that’s the case, we should say that, your other devices that sync with this cloud will be updated automatically once they are running pixelelated and connected to the network, or something to that effect.

D-UI-123 refines D-UI-122: describe switching cloud folders automatically, with running pixelelated and network access as prerequisites, rather than implying an automatic operating-system update. Keep a brief remaining-files exception so the text does not promise an automatic switch where the existing merge confirmation applies.

## Current behavior and scope

The installed H700 build43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa pins ES72494bc72e3d64d4dcfeb4e6478052bbdf166c5b. Its initial dialog says YOUR OTHER DEVICES WILL FOLLOW without naming the software prerequisite.

The distribution's cloud_migrate_layout relocate() copies, verifies, updates the pointer, then deletes only the listed old files. This is a move as its final outcome; failure before verification/pointer success leaves the old files. layout_follow() automatically adopts the current saves folder on compatible firmware when the old default saves folder is empty, the new folder exists, and the user has not chosen KEEP. Files written into the old root by another device instead prevent automatic following; migration offers a merge, preserving differing versions (D-CLOUD-160, D-CLOUD-168). Custom paths and populated backup locations have separate preservation rules.

Older ROCKNIX firmware is not changed by moving shared cloud files. Other devices need software that understands the new folder, normally by upgrading to pixelelated. The shared cloud move is not necessarily repeated on each device; a second move is only needed for remaining old-root data. Local saves on other handhelds are not deleted by this cloud migration.

Revised copy direction (D-UI-122, refined by D-UI-123 and D-UI-124), retaining the canonical destination spelling:

```
YOUR CLOUD HAS A ‘/ROCKNIX’ FOLDER FROM A PREVIOUS OS.

MOVE THE FOLDER TO ‘/pixelelated’?

OTHER DEVICES THAT SYNC WITH THIS CLOUD WILL SWITCH TO THE NEW FOLDER AUTOMATICALLY ONCE THEY’RE RUNNING pixelelated AND ONLINE.

IF FILES STILL NEED MOVING, YOU'LL BE ASKED TO CONFIRM.
```

The destination spelling is confirmed as /pixelelated. The original styling question concerned Markdown. The existing GuiMsgBox/TextComponent render path does not parse Markdown: backticks and bold markers would appear literally. Adding inline code/bold styling would require a renderer change, which this question does not commission. The revision above uses supported literal quotation marks. Keep MOVE / KEEP USING /ROCKNIX / NOT NOW and the canonical paths unchanged in behavior. Automatic following remains; confirmation is conditional on the existing migration flow, not newly required for every device.

Renderer evidence: pinned GuiMsgBox.cpp:104 passes the full string to TextComponent; TextComponent.cpp:110 stores it unchanged and :342-414 passes the wrapped string directly to Font::buildTextCache, with no Markdown parser. fc-query of the accepted H700 theme's Roboto-Bold.ttf shows ASCII20-7e and Unicode2017-201e, covering straight/curly single quotation marks and backticks. This establishes glyph availability, not visual fit of a revised dialog.

Already written: the current installed firmware displays the unqualified promise and unquoted paths. A copy correction must not migrate files, alter stored pointers, or rename the canonical cloud destination.

Can this be done on the VM? Yes. Source inspection answers the migration question; host font inspection can check glyph coverage. Any implemented prompt change needs English/French frames at640x480 with all buttons visible. No physical-device or personal-cloud action is needed.

## Acceptance criteria

- [x] Source trace distinguishes the move, upgrade prerequisite, automatic following, and residual-file merge: cloud_migrate_layout relocate(), layout_follow(), and merge_into().
- [x] Renderer/font evidence answers the clarified styling question: Markdown is unsupported in this dialog; literal quotation marks have font coverage.
- [x] Capture PREVIOUS OS / MOVE THE FOLDER, automatic switching once running pixelelated and online, and the residual-file confirmation exception (D-UI-122, D-UI-123).
- [x] Revised English/French source uses PREVIOUS OS / MOVE THE FOLDER and explains automatic cloud-folder switching once running pixelelated and online, with the residual-file confirmation exception; /pixelelated, existing behavior, and all choices stay unchanged. Syntax/localization checks pass. Sweep the old prompt in GuiMenu.cpp and the French catalog; no Markdown parser is introduced.
- [x] VM frames at640x480 show complete English/French prompts and buttons without clipping; changed-image qualification is scoped separately from already accepted candidate16 evidence.

The source change is now verified and published as described below. The installed H700 build has not changed; distribution pin integration and a future image are tracked separately.

Latest wording correction (D-UI-124), recorded verbatim:

> instead of `THEY’LL ASK YOU TO CONFIRM.` it should be `YOU'LL BE ASKED TO CONFIRM.`

## Verified source and scoped VM proof — 2026-10-07

Published ES commit [5d2fcb9b71f363cfa4813d5356f02c48ab58e139](https://github.com/pixelelated/emulationstation/commit/5d2fcb9b71f363cfa4813d5356f02c48ab58e139) changes only the English prompt and matching French catalog entry. Both `feature/m7-migration-copy` and `test/qa-integration` point to that commit after a clean fast-forward and normal-hook push; remote hashes were read back. The exact approved final English sentence is preserved.

PASS: `tools/es-syntax-check`, vocabulary, `msgfmt --check --check-format`, the existing build-style xgettext command, `git diff --check`, and register citations. C++ Unicode escapes retain the supported quotation marks while allowing the existing xgettext invocation to extract the matching French msgid. Migration logic, runtime paths, automatic following, button labels/order, and confirmation conditions are unchanged.

Actual EN/FR frames at **640x480 and 1280x800** were directly inspected. All prompt text and three choices are visible; no scrolling is needed. The French button row's slight overhang outside its dialog background remains inside the screen and was separately reproduced with the original source; this copy change does not introduce it. Accepted frame hashes and both reviewers' scope are captured in the compact evidence packet `docs/qa-logs/2026-10-07-migration-copy/acceptance.json` (local; distribution evidence publication follows).

The narrow proof used one owner-local recompiled object and relink, retained candidate16 build inputs read-only, and one disposable guest with a local QA alias. No migration was selected. All guest/compiler/watch processes exited; the named guest disk, keys, and runtime binaries were removed after proof capture, reclaiming 2,556,751,872 allocated bytes. Failed harness attempts are retained in the compact logs and excluded from visual acceptance.

The distribution pin and accepted candidate16/H700 artifacts remain unchanged by this source lane. Leave this issue open for the parent lane's distribution integration/build handoff.
