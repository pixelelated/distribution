# Failed in-place preparation (#441)

Actual inline chunk5aa277 returned1 before its first source write: sealed
boot03 qualify-boot.py was mode0400. Original source/seal backup was created;
no original source changed. The following launch should have been gated on
that result but was not. Boot03/tool60221/allfourrc1 correctly rejected its
old QA11 dependency before any guest; actual06:37:58 all processes absent.
Original source hashes were reverified while creating16 fresh successorowners.
Preparation tool53e3c8 returned0 with139 sealed members and consistentQA13/
successor dependencies. A separate preparation readback6d00cd passed before
boot04/tool90675 launch. Original owners remain untouched; no chmod bypass.
