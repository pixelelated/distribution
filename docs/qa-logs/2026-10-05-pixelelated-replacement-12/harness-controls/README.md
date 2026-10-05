# Host controls for the VM harness corrections

The first six vm-stop controls passed but did not model QEMU removing its own
pidfile. QA16 exposed that case. The corrected helper passes all seven,
including delayed exit/port reuse, self-removed pidfile, timeout and wrong
process/disk refusal. Local sockets were denied in the first sandbox attempt;
these retained controls ran on the actual host. No guest/image was modified.

Five manager-system parser controls cover a correct selection and refusal of
wrong, missing, hidden and empty systems. Installed ES selection and actual
manager frames are verified separately by QA17. Refs #454,#455.

Three CLI refusal controls reject unknown/path-like walk names and the
internal default-pre directive before any backend starts. This final parser
guard follows QA17; its four valid selected walks use the unchanged path.
