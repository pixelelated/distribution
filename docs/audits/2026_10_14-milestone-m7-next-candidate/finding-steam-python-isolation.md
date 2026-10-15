# G-03 — Low — Steam runtime helper inherits Python import context

External refutation R-03, independently confirmed. Frozen Install Steam.sh:780 invokes `python3 -` after `/etc/profile`, whereas root/FEX/client/Proton embedded helpers use `/usr/bin/python3 -I -S -B -`. The runtime body imports only Python standard-library modules (ctypes, fcntl, hashlib, json, lzma, pathlib, re, resource, shutil, signal, stat, subprocess, sys, tarfile); no site dependency is visible or required by its source.

Ordinary stdin Python admits current-directory/module-path and site initialization. A profile-provided Python environment, an alternate PATH interpreter, or a same-named module in the working directory can therefore change runtime-helper startup/import behavior while the sibling helpers remain isolated. This is a reliability/isolation inconsistency, not a claim that shipped images contain malicious code or that arbitrary trusted profile code is sandboxed. Source-wide searches found no shipped STEAM-root or PYTHONPATH/PYTHONHOME profile assignments; that absence does not eliminate stdin's default import context.

Minimal correction: use `/usr/bin/python3 -I -S -B -` for this one self-contained helper, matching its four siblings. Preserve the body, operation order and runtime transaction semantics. Root owns source integration/tracking and any execution.

Bounded acceptance: exact invocation diff plus source/body hash equality; a controlled current-directory/PYTHONPATH shadow or startup sentinel affects the old invocation but is ignored by the isolated candidate, and one existing narrow successful runtime-helper control still reaches the expected result with the installed interpreter. Preserve original statuses and selected state. No full Steam matrix or native ARM launch is required to verify this invocation correction; those remain separate tracked scope.


Tracking: #595; mandatory audit checklist PL-006 in #596. Local d9054efc correction and focused control source reviewed; see source-controls-preallocation-review.md. Execution remains unverified at this checkpoint.


Later resolution: PL-006 is resolved by committed source d9054efc463387df3f0211481c5ae8c793dfadc8 on feature/m7-player-setup and the original installed-interpreter controls02 old-negative/candidate-positive transaction. See source-controls02-readback.md. No next/shipped-image or native ARM claim; frozen finding remains valid.
