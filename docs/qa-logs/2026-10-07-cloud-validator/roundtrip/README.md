# Ordinary VM cloud round trips — #508/#510

Final distribution `6f89bc7cec` and ES `baeea2a8c9` source overlays on the retained
candidate VM passed **108 checks each on local WebDAV and SFTP**. Both suites
returned `PASSED`; inner, runner, wrapper and launcher results are all zero.
Recorded job PIDs are absent (or exited zombies), independently read after
completion. Raw logs, exact tool copies and installed-script hashes are retained.

The first launcher was refused by the worktree monitor lock with rc2 before
starting a backend or guest test. Independent VM QA then ran from a private
runtime directory using verified copies of the same watcher helpers. The host
regression suite retained its own worktree lock and watcher.

The suite covers ordinary save and settings archives, ROM/BIOS backup/restore,
selected systems, independent cloud pointers, explicit/idempotent folder
creation, missing/unreadable handling, recency and transfer-lock behavior.
The guest's synthetic original remote and three paths were restored; readback
is retained. No handheld or personal cloud was contacted. This is source-overlay
proof, not an assembled firmware or public ROCKNIX upgrade rehearsal.
