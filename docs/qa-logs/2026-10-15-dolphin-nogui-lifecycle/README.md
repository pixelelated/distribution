# Dolphin NoGUI achievements lifecycle — source repair, uncompiled

#584: default NoGUI did not initialize AchievementManager. Root read the exact
frozen startup, manager Init/Shutdown, ScopeGuard and normal/early exit paths.
Patch018 adds guarded initialization and scope cleanup, before native window
teardown. Existing Qt/Android ownership and user settings/schema stay unchanged.
Source applies at zero fuzz to the exact pin+existing patches and current upstream.
Root verified source sealb2eb32d3 before integrating into the editable coordinator.
The frozen fac608ff image is unchanged. Compilation and actual installed request
proof remain due. Do not call this source fix qualified or close#584 yet.

Current Dolphin stable2609a and master still omit this NoGUI lifecycle; ROCKNIX
next pins the same6094 source and remains affected. Retain the existing stable
ROCKNIX foundation pin while making this narrow fix; no claim of latest Dolphin.
The code belongs upstream in dolphin-emu/dolphin, with a focused ROCKNIX backport.
Its bug tracker duplicate search remains incomplete. Queue under#585; submissions
wait for the qualified initial build. Source queries/results are in the archive.

#583's completed format/scanner/native/proxy evidence is independent of this
frontend lifecycle; see the exact original-artifact map and proposed combined
#574 note. No screenshots change because the settings/navigation are unchanged;
the actual normal game-launch flow and runtime evidence remain pending#584/#575.
