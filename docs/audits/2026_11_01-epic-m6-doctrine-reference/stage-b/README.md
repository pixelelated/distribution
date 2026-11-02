# T39 (#686) stage B: the reading notes

Moved in at the stage-B completion (issuecomment-6565986529) from the lane's
scratch `/workspace/tmp/m6-t39/stage-b/`, as written on 2026-11-01 06:49-06:53 UTC.
These are lists and hashes. **Nothing from the export is copied.**

| File | What it is |
| --- | --- |
| `allpaths.txt` | every repository path at the tip, the base the 254's links and paths were resolved against (0 dead over 511 relative links) |
| `dead-links.txt` | the dead relative links found against the worktree: empty |
| `binary.txt`, `binaries-dispatch.tsv` | the 31 binaries, with size and sha256 at the tip (`02` § Binaries) |
| `art-text.txt`, `art-dispatch.tsv` | the 18 art text files, with size and sha256 at the tip (`02` § Art bytes) |
| `register-ids.txt` | the register's 716 IDs at the tip |
| `cited-ids.txt` | the 442 distinct IDs the 223 text rows cite: 0 unresolved |

**Kept out on purpose:** `reader-digest.txt` (685 lines, sha256
`e484f752554f42cb83dea42f4d1c935a50ed171f1b84259b95077cc4c7b274a4`). It holds the
reader's pass input, which is the head of each document read, so it is text of the 254.
It stays at `/workspace/tmp/m6-t39/stage-b/` and is retired with the export at
stage H. What the reader made of each group is `01-research-notes.md` § The
reader's pass.
