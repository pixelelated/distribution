# Additive final proxy source-chain producer correction (#588, #583)

SOURCE ONLY, UNRUN. This packet replaces only the capture producer for the completed
`d6a87f05c1935516115b2cca1af22151a0209224` engineering image. It preserves the original
producer and its entire sealed packet in `source-originals.tar.gz`. The original
`prepared112.json` is byte-identical. It does not change the product, image,
installed lifecycle, payload checks, or any original result. Payload01 stopped
before this producer ran; its original failure remains the parent's record.

Use `capture-source-chain.py` with its adjacent `prepared112.json` and
`chain-binding.json`. The latter binds the exact reviewed frozen source files
and original install job; it is not a replacement build receipt. The producer
stays `REVIEW_REQUIRED`, with runtime and clean-boot acceptance still outstanding.

The two original producer assumptions corrected are:

- The reviewed 112 files are exactly 45 files under `linux/raofflineproxy/` and
  67 under `linux/tests/`. The runtime tree alone has 45; all of `linux/` has 115.
  Its three unrelated helpers are outside the accepted manifest. Every accepted
  path must match, and no extra Python file is permitted within the two roots.
- The actual job is `DONE 309 10 install raofflineproxy:target`, not a separate
  build job. Keep its original job line and 15,895-byte log, including fresh
  UNPACK, all 18 package patch lines, BUILD, 45 Compiling lines, and INSTALL.

The fail-fast chain was read in the frozen source, with its exact file hashes and
line spans in `chain-binding.json`:

1. `pkgbuilder.py` waits on `pkgbuild`; its real subprocess return code determines
   DONE. `pkgbuild` returns the actual selected install command's success/failure.
2. `scripts/install` runs `scripts/build` as an unguarded command. Both source
   `config/options`, which sources `config/path` and its `set -e`. These scripts
   run in new Bash processes; the caller's `&& result=0 || result=1` does not
   disable the new process's explicit errexit. Nested `tools/watch-build`
   preserves the command by `execvpe`, after checking its existing owner.
3. In `scripts/build`, the `makeinstall_target` `pkg_call` is in the selected
   `then` body, not the condition. `pkg_call` invokes the package function as an
   unguarded command. The recipe invokes `python_compile` unguarded, which invokes
   the real host compileall unguarded before removing source.
4. The fresh successful install, reviewed chain, original compile log, and all
   45 emitted bytecodes support inferred nested build/compileall success. There
   was no independent build or compileall child-wait receipt. Existing consumer
   fields retain zero with explicit inference bases and both standalone-wait
   flags false. The separately observed original task exit is install309 zero.

The source review also found the original producer merely retained the image
verifier receipt. The derivative now checks its PASS/source/ES binding and compares
all 45 final bytecodes and the native library against its recorded hashes, sizes,
and modes. `--verified-root` intentionally points at the completed build's
`image/system`; the independent image verifier established those same product
bytes in the final image. This producer does not claim to re-extract the image.
The 18 patch paths and hashes, three clean-stage originals, recipes/unpack/build
stamps, exact chain sources, prepared manifest, original log, bytecode headers,
and existing native C-input manifest remain inspectable outputs.

Source-only readback found no further deterministic final-output mismatch:
112 prepared hashes match; 45 staged/final bytecodes match the verifier; the
staged/final native hash is
`6c484a2947a5f2a7c187e60dd93de73593d5fa98d57309bfb4b5f07bf390220d`.
The original pre-strip library has a different full hash; all 24 allocated ELF
sections match across pre-strip, staged, and final files. The original strip exit
is unknown because `scripts/build` masks it with `|| :`; the producer preserves
that limitation. No pyc import, marshal decode, compiler, strip, or native runtime
was executed for this packet. `static-review.json` is an AST/file review, not a
producer execution receipt or provenance PASS.

The parent runs the following only inside its next admitted, watched readback
owner, with a fresh output directory. Preserve original stdout, stderr, timeout
status, and original return code. Reuse the existing 120-second producer deadline
and 10-second termination grace; the existing parent's resource/output guard
continues to own the stage. Do not reuse payload01 or alter its sealed inputs.
Host Python 3.11+ is required by the unchanged `hashlib.file_digest` use.

```bash
timeout --kill-after=10s 120s python3 -I -S -B \
  /tmp/pix588-source-chain-correction/capture-source-chain.py \
  --checkout /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01 \
  --build-root /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01/build.pixelelated-GENERIC_X64.x86_64 \
  --build-owner /workspace/tmp/pix-m7-engineering-build-20261014-01 \
  --run /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01/.build-runs/20261014T204343Z-b7a72fc6 \
  --verified-root /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01/build.pixelelated-GENERIC_X64.x86_64/image/system \
  --verification-receipt /workspace/tmp/pix-m7-image-readback-20261014-01/artifacts/result.json \
  --output "$SOURCE_CHAIN_OUTPUT"
```

`SOURCE_CHAIN_OUTPUT` is the next owner's fresh `source-chain` directory. Confirm
this packet's `SHA256SUMS` first. On zero, review original receipts and resulting
`source-receipt.review-required.json`; do not auto-promote its status. A failed
capture retains its partial output and original failure. This packet's worktree
has old worker ancestry: integrate these owned files by content only.
