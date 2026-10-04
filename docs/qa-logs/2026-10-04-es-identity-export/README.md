# ES identity export — #424

Exact candidate1e6a has OS_NAME=pixelelated in os-release, but the running
EmulationStation child has no OS_NAME. Its actual main menu says ROCKNIX and
the update branch shows NO UPDATE AVAILABLE instead of the manual-update
explanation. The old export profile exports OS_VERSION/OS_BUILD and omits
OS_NAME. ApiSystem::getApplicationName falls back to ROCKNIX when absent.

The source fix adds OS_NAME to the existing export list. The strengthened
rasteratops-identity-check executes this actual profile with a clean shell
environment, starts a child and asserts all three identity values. Original
profile gives1 failure, corrected profile0; all other identity contracts pass.
Installed old/new hashes, exact read-only guest command, status and negative
frames are retained. No live/frozen source or guest file was changed.

A replacement image and actual clean/upgraded process/UI proof are still
required. Source guard success is not an installed fix. Current image cannot
be called an RC. No source pin or compatibility name was changed by this fix.
