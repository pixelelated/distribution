# QA16: retained pidfile-removal follow-up failure

An independent qemu-img-compared copy of QA15's actual upgraded disk booted
and passed exact installed payload/virgl checks. It captured five identity
frames, then the first vm-stop implementation incorrectly failed because
QEMU removed its own pidfile after exiting. All four result channels are1;
completion and supplemental guest-PID absence are retained. The local cloud
backend was never started. This attempt remains failed and was not replayed.

QA17 uses a fresh independent copy and the corrected helper with seven host
controls. No product image, frozen source or original upgraded disk changed.
