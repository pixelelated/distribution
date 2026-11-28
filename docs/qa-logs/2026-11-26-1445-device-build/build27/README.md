# Build 27: H700 from the round's final head 6169621a4b (route 16)

- **Run:** `m7-round-h700-20261128/.build-runs/20261128T040114Z-1a8e3f25`, warm, owner `m7-round-h700-20261128-02-owner`. It ran 04:01:14 to 06:23:35 UTC with build.rc 0 and [666/666] packages.
- **Before it:** the cold run `20261128T024822Z-ef0b547e` stopped at 03:49 with build.rc 2 at package 366: duckstation-sa's source had been withdrawn upstream (#1509). The source was restored from the 2026-11-25 image by its pin and 13 half-built packages were cleaned. The 03:59 relaunch was refused because its owner folder was already used (#1510; the `attempt-0359-*` files).
- **Accepted:** `ACCEPTANCE-27.json`, admission `0b493debbc214055a3def8a9d10f8a5e` consumed. The evidence is `image-reads-27.txt`:
  - the DDR3 and DDR4 images and the update tar check out against their checksums;
  - BUILD_ID is the head, with no `.dirty`;
  - the ES binary carries the sign-in-again and wait sentences, and the French catalog carries the #1501 line;
  - `raofflineproxy-ctl` equals the round's source;
  - `/usr/bin/duckstation-sa` hashes to the pin `f92319a0…` (#1509 c2).
- **Not a device qualification.** Nothing has been staged on a handheld.
