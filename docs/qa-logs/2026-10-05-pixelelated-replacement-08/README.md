# M7.P3 replacement08 build and qualification (#436, #383)

Snapshot 2026-10-05T04:47:56.012150+00:00. Source72121fd03a558725328ea58c092faf1b3324317f,
ESf6f0c134212bc696f2f6a747c8d390a588f2f0ce, input7578b0d91f2f043b492d998c2f8bd4a73467a1524ae692366469153e2eb5c17b.
6547 product files,180 symlinks,200 QA files. The sole product change versus07
is the ES pin; tools/vm-qa adds the actual GPU callback regression.

Build49805/all four rc0 completed04:39:21:642 package tasks,353 ES compilation
steps, image assembly, source and assembled payload checks. Actual04:40:04
runner2481198/watcher2481199/command2481230 absent; observed pinned container
73d31218278e… also exited. Nonroot1000:1000 and canonical mounts were verified.
Copy55433 passed checksum equality and2525725 distinct file inodes; preflight
24955 reclaimed swap while idle. No helper reinstall. Full build log is in the
immutable bundle; the original tail/hash and process receipts are retained here.

Store and independent verify68326=0;14 manifest-bound files. Bundle
`/workspace/artifacts/pixelelated-candidates/sha256/84a794165a6e421cd1aa1dd6d37b97b257c700738c0a53edd282475ecd4780e9`.
Image SHA2567a60c191755cc6203eca4624700249538ecc24182087f8aa20a8ea8afeae59ad;
update SHA256d196d9c2cff496ab8d8a53ac7536e60428b5f18c431090ff44de0f5074864d9b.

Inventory06/tool20676/all rc0:583 mapped components,568 unpacked roots,
525 install stamps,0 source errors. Fourteen known P5 licence-metadata gaps
remain; publication bundle is incomplete. Versus07 the only missing stamp is
initramfs: actual packaged KERNEL, assembled init, Linux build stamp and recipe
are byte-identical. Linux embeds initramfs in pre_make_target; a cached kernel
does not recreate that image-install stamp. Supplemental provenance retains
the embedded recipe for the P5 source bundle; this is not a lost OS component.

QA10/tool98190 started04:40:44 under watch-build5s/5min recursive activity.
Initial clean payload and Back/Back identity walk pass. ES stays PID1636,
start_ticks556; all five actual frames directly reviewed. Defaults and actual
RC2 upgrade remain running. No complete candidate qualification or RC claim.

Prepared owner sources remain under prepared-owners/. QA10/UI09 preserve the
save path and record lifecycle/journal evidence. Existing controls reject the
actual07 crash/restart. First control fixture wrongly supplied a blank line
for no process; corrected to actual empty output and independently rerun.
No executed owner or frozen product was edited.

Next: complete QA10 → boot02 clean/upgraded640/1280 with unchanged0.995 and
negative controls → image09/sweep06/settings08/link08/guest08/runtime09/
proxy07/optins07/memory07/UI09 → predecessor05/subset04/cloud-ui03/signin-ui03/
signin-1g03/ordinaryRA → P4 independent fixes audit → H700 arm then aarch64.
Old failure evidence remains under replacement07. #436 needs upgrade proof;
#433 and #426 still need installed candidate qualification. No inherited passes.

Publication preparation initially stopped before commit on a trailing space in
the raw inventory console log (`cbindgen: `). The original log remains intact;
the second preparation excludes that exact raw log from its manual whitespace
check. Normal commit/push hooks are unchanged.
