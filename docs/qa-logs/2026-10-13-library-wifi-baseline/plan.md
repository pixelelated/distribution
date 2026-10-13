## Testing-first continuation — October 13

Owner:
> Got it. Can we start working through all of these issues we've discovered and figure out what we need to do to be able to start bringing them to resolution? There's additional testing to do. Let's go ahead and do that first. I'd like to be able to work towards our next release candidate.

Can this be done on the VM? **Yes.** Start a fresh disposable accepted VM20 guest, 8GiB RAM/4vCPU/16GiB sparse disk/640x480, to qualify the synthetic ROM-only versus ROM+gamelist import case (#565) and reproduce initial/delayed/refreshed/empty/error Wi-Fi layout (#577). No owner's saves, account, cloud or handheld is used. Existing accepted image/source and exact VM profile/commands are recorded. Keep unchanged-image reproduction separate from next-candidate qualification.

Current allocation: /workspace/tmp/pix-m7-baseline-tests-20261013, at most8GiB host scratch,8GiB guest RAM, ports10580/5974 checked free. Host has over2.8TB free and50GiB available memory; existing swap occupancy is recorded without changing host swap. Durable watch-build/watch-job owners plus active result consumption supervise each stage; no disconnected alert is claimed. Stop the exact VM and retire its disk/UEFI/access material after compact evidence is accepted.

#570 remains the first product fix to qualify, but #493's final criterion explicitly requires capacity/retention enforcement **before compilation**, including the actual ES candidate. No compiler or full cache copy starts in this baseline stage. Put #493 at that dependency boundary, while the existing-image tests proceed. Diagnostic allocator interposition is already complete and will not be repeated as a substitute for compiling the actual change.
