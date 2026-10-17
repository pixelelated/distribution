# Supported native input direction

GTK4 makes GdkEvent opaque. Its public4.24.1 header exposes key getters, not the
constructor used by GTK3; `gdk_key_event_new` belongs to a private header.
GtkEventControllerKey.forward forwards the current native event; it cannot
turn an OSK letter selection into an unrelated letter; it is also deprecated
in GTK4.24. The replacement GtkEditable interceptor does not turn WebKitWebView
into GtkEditable or create arbitrary native WebKit key events. A DOM value assignment,
JavaScript KeyboardEvent, private GDK ABI or toolkit-signal emission does not
preserve the provider's native-input semantics.

Use the existing product uinput keyboard as the candidate producer. The new
mechanism is a local inherited AF_UNIX/SOCK_SEQPACKET channel; no listening port,
filesystem socket, provider script bridge or input logging. The fixture sends
one network-order32-bit GDK key value. Only ASCII32–126, Backspace, Tab and
Return are accepted; the reply is one Boolean byte. The current implementation
accepts one outstanding request and fails after2s. That proves a bounded API
experiment, not a production text queue. Ack means the kernel writes completed,
not that the field received the key: the page's trusted-event counters and
reviewed frame are the independent witness.

The necessary product change is **separate control and text namespaces**.
Today cloud_oauth maps a pad's A to Return and B to Backspace; while the OSK is
visible the window consumes those as select/hide. Reinjecting OSK Enter or
Backspace through uinput would recurse or hide the OSK. In the candidate design,
pad controls use reserved F13–F24 values (or the same private control channel),
whereas actual text/edit keys always reach WebKit. The fixture uses F13–F17 as
explicit synthetic controls. Production mappings and UI must be ported together;
changing just the window would break the existing broker.

Do not identify the physical producer using only GdkDevice.name. Wayland exposes
seat-level keyboard events; multiple libinput keyboards can feed the same seat.
A marker key around injected text is also unsafe under concurrent phone input.
Instead the broker must own one bounded serialized native-key queue for phone,
OSK and page-navigation output, with admission/order recorded before emission,
non-interleaved modifier/press/release reports, session generation/cancellation,
held-key release on failure, and a clear busy/error result. Pad commands stay
out of that text stream, and Select+Start keeps its broker-side exit path.
No such complete broker patch or queue is claimed in this packet.

The fixture reuses the exact RemoteKeyboard class rather than inventing a second
US-layout implementation. It supports all printable ASCII through that mapping;
its UI exposes five representative controls. The normal physical/phone native
keyboard can type directly into the fixture. The real phone HTTP/session route
and parallel ordering still need a full port control before functional acceptance.
The fixture does not log key values, passwords or field content.

Related views are constructed with related-view and settings only. They inherit
the parent's ephemeral network session; supplying a competing explicit session
alongside related-view is invalid. The fixture asserts pointer/ephemeral state,
permits one gesture-created about:blank popup, restores parent focus on close,
and removes the popup widget. It is intentionally synthetic-only: the full
product's navigation/localhost allowlist and callback-file protections must be
retained unchanged, exercised independently and never inferred from this probe.

Public references: [GTK4 input changes](https://docs.gtk.org/gtk4/migrating-3to4.html),
[forwarding existing input](https://docs.gtk.org/gtk4/method.EventControllerKey.forward.html),
[Linux uinput](https://docs.kernel.org/input/uinput.html),
[Wayland keyboard seat protocol](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_keyboard),
[exact WebKit6 migration](https://github.com/WebKit/WebKit/blob/webkitgtk-2.54.1/Source/WebKit/gtk/migrating-to-webkitgtk-6.0.md).
These are a supported design route and concrete source blocker, not evidence of
successful compiled keyboard delivery.
