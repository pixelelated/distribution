# Owner03 closure input rebind — UNRUN

Derived from immutable `94ca020acc65f9038f3a44a2f894be40868b1e1a`; that packet
is unchanged. This copy uses corrected builder commit
`2608923ba0ab80752e555adb393d7a029baeaf8c` and its exact revised input JSON
`b151b9218c6d91ef7148a14a7f0468c02c9ef299bce69c7cc7f556e9b6ce15ce`.

The additional source check binds both recorded scratch adjustments and actual
patched Lua files before readelf. Their hashes are rechecked at completion.
Original target receipt/generated inventory binding remains dynamic. ELF parsing,
recursive dependency/version-provider checks, pinned SDK loader mapping, raw
readelf receipts, copy bounds and output layout are unchanged. Common support,
loader resolver and loader-binding.json are byte-identical to 94ca020.

Use only through this parent packet's fresh admitted bridge. It mounts the
corrected plan/work/build receipts and invokes this copy at `/closure/closure.py`.
The parent README gives exact commands and remaining acceptance. Static checks
do not qualify actual readelf execution, VM loading/help or CHD conversion.
