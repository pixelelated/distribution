# Draft only — exact ABL v1.2 source locator

Suggested recipient: @spycat88, verified author of the upstream OpenABL transition, as a routing contact; no claim that this person owns all legacy implementation rights.
Suggested channel: the existing [ROCKNIX OpenABL transition commit discussion](https://github.com/ROCKNIX/distribution/commit/71d8932b3374d2a9e04fbc200b5779394a57dae2). Its exact comments API URL is retained in the original commit response. This is a verified dated route, not a successful posting or a current permission test. ROCKNIX/distribution issues are disabled; do not open a new issue there.

Suggested subject: Source locator for legacy ABL v1.2 / LinuxLoader e9d37131

---

Hi @spycat88 — we are completing source and notice custody for an existing pixelelated SM8550 engineering image that contains ROCKNIX ABL v1.2. Could you point us to the public source or the appropriate source maintainer for the exact legacy build?

The [v1.2 release](https://github.com/ROCKNIX/abl/releases/tag/v1.2) identifies LinuxLoader commit `e9d37131c0c2273076468156fb0f87aa6834202b` (2026-10-01 19:31 UTC). The selected archive SHA256 is `64034fb076ea0bb858beaa2f29dbef635e97d29f3e3d32c13bce61bd4af4cff7`; its `abl_signed-SM8550.elf` is 258,048 bytes, SHA256 `8c27a70961476b327071ada2fd9b9c55dd2dcdc913eff3d33f2576133d7e398c`.

We have retained the public ABL packaging repository and release workflow. Its LinuxLoader checkout uses a deploy key; our public lookup of the named legacy commit did not return the source. We need a source snapshot for that revision, its selected submodules/dependencies and build scripts, and their applicable licence/copyright notices. An existing exact source archive or repository reference would be sufficient to start the custody readback; we are not asking for a new binary or reproducible-build guarantee.

We have also found OpenABL v1.0's published source and its distinct SM8550 revision `78b81b585f0f82882e9272cead99e1d395622de5`. We are keeping that potential migration separate and are not treating its source as the source of the legacy ABL payload. If another maintainer is the right contact for the legacy revision, a pointer would help.

Thank you.
