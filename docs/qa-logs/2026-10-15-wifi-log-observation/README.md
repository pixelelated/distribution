# Wi-Fi scan observation correction — #577

Original owner02 ended at00:25:31 with exit1: the scan-completion log observation
never arrived. The actual installed wifictl list child returned0 with all three
expected networks. Five backend starts have five original completion records.
The fixture set system.loglevel instead of ES LogLevel; the default warning
threshold suppresses the awaited information line. Source correction sets and
reads back LogLevel=information before normal ES startup. No product/backend
change or assertion relaxation. Exact original settings restoration and normal
VM cleanup passed; admission6b69d53f was consumed as failed-investigated.

The corrected source archive is unrun as a qualification claim here; a separate
owner03 is actively supervised. Its later original result must be recorded
separately. The original failure remains unchanged.
