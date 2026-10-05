# Persistent VNC observer controls

Issue #449. VM-first: yes; the protocol controls first use a local loopback
RFB server, followed by the full installed sign-in test on a disposable VM.

The original full Pixman signin-ui12 reached all27 checks and captured six
intended surfaces, then failed on observer TimeoutError. Four channels retain
rc1; actual ab6ec0 verified cleanup18:36:05. Its330 complete observer frames
end18:35:30. The old helper did not retain the failing read phase, so the
specific timeout is not retrospectively classified as harmless idle.

The helper had no distinction between waiting for an update and receiving an
incomplete message. RFB permits an indefinite interval before an update;
see [RFC6143 §7.6.1](https://www.rfc-editor.org/rfc/rfc6143.html#section-7.6.1).
It also counted rectangle area rather than unique pixel coverage.

The corrected helper keeps the first frame and partial messages bounded. A
quiet boundary after a complete frame is explicitly recorded and may end on
the caller's stop event. EOF, partial-message timeouts, unsupported encodings,
invalid rectangles and missing coverage remain errors. Errors record their
phase. Clipboard messages are discarded without retaining their contents;
the observer sends no input or resize. It remains a connection/frame observer,
not a verdict that the displayed page is current. Separate semantic captures
and exact pixel rejection remain required.

Run `python3 docs/qa-logs/2026-10-05-vnc-observer/test_observer.py`.
Actual e7c507/5c01ac returned0; `controls.log` retains all nine results:
idle stop, fragmented valid frame, missing first frame, truncated header,
truncated pixels, overlapping incomplete coverage, invalid rectangle,
unsupported encoding and EOF after a complete frame.

Fresh full signin-ui13 copies these exact helper bytes into its sealed owner.
Its page/phone/provider assertions, stable-screen helper, finishing reference
and Pixman selection are byte-identical to12. The original failed owner is
immutable; its six frames were directly reviewed and retain their failed-run
context. No product change or authenticated-provider claim follows.
