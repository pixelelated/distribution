# FEX held-source custody: exact Nixpkgs and twenty patches

Original run `20261015T150157Z-c3055ad7` completed command/monitor/runner
0/0/0 and launcher0. Collection took 10.043 seconds and retained the exact
Nixpkgs pin `b6018f87da91d19d0ab4cf979885689b469cdd41` as a canonical NAR:
195,961,000 bytes, SHA256
`b705cf16a16caeb639af6f1987b1e89a0729da050c06043a5834bdf10ff7c452`.
The 85,517 source nodes include 50,250 regular files, 35,264 directories and
three symlinks; executable markers and raw symlink targets were preserved.
This recursive/NAR identity is distinct from any compressed HTTP archive hash.

Twenty exact patch files total 1,959,776 bytes. Their flat hashes and original
paths are bound individually in the retained destination manifest, SHA256
`02f6bcd1d4b3a7f589fda15ca29c5520aeae0ddc5312b77b6302d23b2684a604`.
Destination content totals 197,942,059 bytes including that manifest.
Admission `d199008ea21d4b3a90188dbdc34dd38b` was consumed successfully,
with both owner and source-custody outputs held.

All 30 focused guards passed in original watched run
`20261015T145929Z-eced1be5`, command/monitor/runner0/0/0. Its exact report
SHA256 `7eae3c89a1bee0b196aec53aa8fdc2fe51c9735698656735f202ee8babb9c7cc`
is retained in the owner and coordinator output and matches the live original
report referenced by the prepared plan. Original guard and collection watched
runner/build/monitor records are included. Source seal: `a38da1cf6a0bf86787c108b4c588e16a167b51b00e0b2a4aa5cedfa65dd01a04`.

`originals.tar.gz` also retains the exact source packet, coordinator command
receipts, owner structured receipts and destination manifest. `members.json`
records original paths, SHA256, sizes, modes, owner IDs and nanosecond mtimes;
custody verification compared every archived file and metadata field with its
live original. The NAR and twenty destination patch bodies are excluded.
Original source-only/unrun labels describe preparation; the separate original
run receipts establish the subsequent completed collection.

Accepted libglvnd recursive-source reuse remains bound. Two normalized patch
outputs remain separate inputs, requiring their recorded normalized hashes.
No network, Nix, source code or target code ran during collection. This compact
evidence retention did not repeat collection or rehash the excluded payloads.
Notices, independent retrieval, offhost custody and publication disposition
remain separate; neither a whole compiler closure gate nor complete bundle
or license clearance is asserted.
