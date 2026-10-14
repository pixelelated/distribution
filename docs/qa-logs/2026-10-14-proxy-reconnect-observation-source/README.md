# Observed offline baseline before reconnect

Attempt04 passed stop/start/manual and automatic restart with original exit
status retained. It failed normal reconnect assertion: state became online but
no background flush. Initial ConnectivityMonitor force-probe may still be in
progress when fixture peer opens, so was_online may initialize true. Product
startup transition race is still an open item; this packet does not dismiss it.

Observe actual refresh_reachability call/return (no override) and wait up to6s
for the fourth incarnation's background false return before opening peer. All
real15s/60s timers,240s work, unit, prepared Python and native bytes unchanged.
Keep peer calls even on failure. This only qualifies steady offline→online;
a separately controlled startup-window proof remains required.
