# Proxy lifecycle review — #570

Owner, verbatim:
> Should RA offline proxy be running at the point where someone's launching a browser? Does it need to be active at all times like this?

The browser has no RAOfflineProxy dependency. Current system integration deliberately
starts the proxy when offline achievements is enabled, before the frontend, with a
30-second listener readiness check. The unit remains active across browser use.
The setting is the boot marker's authority; temporary resource management must not
toggle the player's preference or call the destructive configuration-revert path.

Exact packaged upstream pin c7ebd1b6e777f3751ff0ecdf8aba54045844e00d plus the fork's
patches: proxy_service.py creates the listener, connectivity monitor, periodic
refresh, cache queue worker, folder watcher and consent-gated usage reporter.
Connectivity is checked every15s and reconnect flushes pending awards; an online
startup also flushes. Cache/folder workers poll each60s when applicable, with a
one-hour periodic refresh. These are worker capabilities, not evidence every job
was active during our browser tests. GameActivityTracker's idle gate follows proxy
activity, not browser/whole-system pressure. It may therefore allow background
preparation while the user is in the browser.

Pending awards are stored in the database. Graceful termination signals stop_event,
shuts down the listener/workers and closes storage. This is a designed shutdown
path, not proof it is safe at every interrupted award/cache-write point or within
our unit's15s stop timeout. Restart can immediately send queued awards upstream.
No stop/restart experiment was performed on the owner's proxy or account.

RetroArch setsettings.sh and PPSSPP cheevos_ppsspp.sh check whether the proxy is
listening; if not, they route direct and log it. They do NOT start it on demand.
A naive stop-and-forget could lose offline achievement availability for the next
game. ES summary/pending readers already read SQLite directly, so those particular
queries do not require the long-lived daemon. Other frontend store-only/image
requests still need a dependency inventory. Freezing the process does not reclaim
its resident RAM; an optimization needs cache release or an orderly unload/restart.

A narrower candidate is a browser-owned temporary stop with guaranteed restoration,
a readiness gate before gameplay, and no interference with active award/preparation
work. A broader on-demand service needs explicit reconnect/queue/maintenance triggers.
Neither is selected or implemented. First profile the ~76–105MiB resident cost in
an isolated VM: main.py imports menu/CLI modules even for run-service, but the
attribution of memory to those imports is unmeasured. Any useful upstreamable
improvement should preserve the existing offline functionality and queue behavior.

Can this be done on the VM? Yes: synthetic queued awards, no real account calls,
normal browser launch/close/crash, next-game listener readiness, refresh/cache work,
DB recovery and process memory can all be tested in disposable guests. Physical
H700 memory is corroboration only. The next #570 VM accounting includes this
lifecycle investigation before choosing an optimization. No service toggle or
production launch behavior changed in this review.

Upstream check2026-10-13: official repository README confirms reconnect uploads.
API head3958abcecd4762128cdb1d4c24cbf179ea4c0f44 has four commits after our pin:
version bump, stats label, muOS boot logging, free-port fallback. Those titles do
not establish a memory/lifecycle fix. Public search found no confirmed applicable
fix; GitHub issue-search API failed, so no exhaustive issue-search claim is made.
Sources: https://github.com/misantronic/RAOfflineProxy and exact pinned
linux/raofflineproxy/{main,service,proxy_service,storage}.py; fork unit/controller,
boot daemon and emulator launch scripts. Preserve pin freshness review before the
next candidate; free-port fallback especially needs our fixed8080 listener contract
checked rather than being imported blindly.
