Read-only process dependency check for issue #494

Scope: replacement09, replacement10, replacement12 and replacement14 only.
The helper reads /proc cwd, executable, process-root, command arguments,
open-file references and mapped-file references. Output contains only matched
tree names, process IDs, unreadable fields and counts, not raw command lines
or arbitrary mapped paths. It changes no processes, permissions, devices,
builds, swap or data. It installs nothing and removes nothing.

Run from this directory after reviewing the helper:

sha256sum -c SHA256SUMS && sudo /usr/bin/python3 -I ./readonly-process-dependencies.py > root-process-readback.json

Exit 0 means no matches/unreadable processes at that observation. Exit 1
retains the JSON and means further review is required. A prior check on five
different trees cannot establish these four trees are unused. This does not
authorize deleting any tree; a concrete deletion proposal remains separate.
