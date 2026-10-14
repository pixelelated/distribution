# Pinned Dolphin HostUrl source excerpts

Read only; no compiler or upstream tests executed. Each whole-file SHA256 and git blob is bound in bindings.json.

## dolphin/Source/Core/Core/Config/AchievementSettings.cpp

```text
1: // Copyright 2023 Dolphin Emulator Project
2: // SPDX-License-Identifier: GPL-2.0-or-later
3:
4: #ifdef USE_RETRO_ACHIEVEMENTS
5: #include "Core/Config/AchievementSettings.h"
6:
7: #include <string>
8:
9: namespace Config
10: {
11: // Configuration Information
12: const Info<bool> RA_ENABLED{{System::Achievements, "Achievements", "Enabled"}, false};
13: const Info<std::string> RA_HOST_URL{{System::Achievements, "Achievements", "HostUrl"}, ""};
14: const Info<std::string> RA_USERNAME{{System::Achievements, "Achievements", "Username"}, ""};
15: const Info<std::string> RA_API_TOKEN{{System::Achievements, "Achievements", "ApiToken"}, ""};
16: const Info<bool> RA_HARDCORE_ENABLED{{System::Achievements, "Achievements", "HardcoreEnabled"},
17:                                      true};
18: const Info<bool> RA_UNOFFICIAL_ENABLED{{System::Achievements, "Achievements", "UnofficialEnabled"},
19:                                        false};

```

## dolphin/Source/Core/Core/AchievementManager.cpp

```text
1: // Copyright 2023 Dolphin Emulator Project
2: // SPDX-License-Identifier: GPL-2.0-or-later
3:
4: #ifdef USE_RETRO_ACHIEVEMENTS
5:
6: #include "Core/AchievementManager.h"
7:
8: #include <memory>

64: void AchievementManager::Init(void* hwnd)
65: {
66:   LoadDefaultBadges();
67:   if (!m_client && Config::Get(Config::RA_ENABLED))
68:   {
69:     {
70:       std::lock_guard lg{m_lock};
71:       m_client = rc_client_create(MemoryPeeker, Request);
72:     }
73:     std::string host_url = Config::Get(Config::RA_HOST_URL);
74:     if (!host_url.empty())
75:       rc_client_set_host(m_client, host_url.c_str());
76:     rc_client_set_event_handler(m_client, EventHandler);
77:     rc_client_enable_logging(m_client, RC_CLIENT_LOG_LEVEL_VERBOSE,
78:                              [](const char* message, const rc_client_t* client) {
79:                                INFO_LOG_FMT(ACHIEVEMENTS, "{}", message);
80:                              });
81:     m_config_changed_callback_id = Config::AddConfigChangedCallback([this] { SetHardcoreMode(); });
82:     SetHardcoreMode();
83:     m_queue.Reset("AchievementManagerQueue");
84:     m_image_queue.Reset("AchievementManagerImageQueue");

1301:   ERROR_LOG_FMT(ACHIEVEMENTS, "RetroAchievements server error: {} {}",
1302:                 client_event->server_error->api, client_event->server_error->error_message);
1303: }
1304:
1305: void AchievementManager::Request(const rc_api_request_t* request,
1306:                                  rc_client_server_callback_t callback, void* callback_data,
1307:                                  rc_client_t* client)
1308: {
1309:   std::string url = request->url;
1310:   std::string post_data = request->post_data;
1311:   AchievementManager::GetInstance().m_queue.Push(
1312:       [url = std::move(url), post_data = std::move(post_data), callback, callback_data] {
1313:         Common::HttpRequest http_request;
1314:         Common::HttpRequest::Response http_response;
1315:         if (!post_data.empty())
1316:         {
1317:           http_response = http_request.Post(url, post_data, USER_AGENT_HEADER,
1318:                                             Common::HttpRequest::AllowedReturnCodes::All);
1319:         }
1320:         else
1321:         {
1322:           http_response = http_request.Get(url, USER_AGENT_HEADER,
1323:                                            Common::HttpRequest::AllowedReturnCodes::All);
1324:         }
1325:
1326:         rc_api_server_response_t server_response;
1327:         if (http_response.has_value() && http_response->size() > 0)
1328:         {
1329:           server_response.body = reinterpret_cast<const char*>(http_response->data());
1330:           server_response.body_length = http_response->size();
1331:           server_response.http_status_code = http_request.GetLastResponseCode();
1332:         }
1333:         else
1334:         {
1335:           static constexpr char error_message[] = "Failed HTTP request.";
1336:           server_response.body = error_message;
1337:           server_response.body_length = sizeof(error_message);
1338:           server_response.http_status_code = RC_API_SERVER_RESPONSE_RETRYABLE_CLIENT_ERROR;
1339:         }
1340:
1341:         callback(&server_response, callback_data);
1342:       });
1343: }
1344:
1345: u32 AchievementManager::MemoryPeeker(u32 address, u8* buffer, u32 num_bytes, rc_client_t* client)
1346: {
1347:   if (buffer == nullptr)
1348:     return 0u;
1349:   auto& system = Core::System::GetInstance();
1350:   Core::CPUThreadGuard thread_guard(system);
1351:   for (u32 num_read = 0; num_read < num_bytes; num_read++)
1352:   {
1353:     auto value = system.GetMMU().HostTryRead<u8>(thread_guard, address + num_read,
1354:                                                  PowerPC::RequestedAddressSpace::Physical);
1355:     if (!value.has_value())
1356:       return num_read;
1357:     buffer[num_read] = value.value().value;
1358:   }
1359:   return num_bytes;

```

## dolphin/Externals/rcheevos/CMakeLists.txt

```text
1: add_library(rcheevos
2:   rcheevos/include/rc_api_editor.h
3:   rcheevos/include/rc_api_info.h
4:   rcheevos/include/rc_api_request.h
5:   rcheevos/include/rc_api_runtime.h
6:   rcheevos/include/rc_api_user.h
7:   rcheevos/include/rc_client.h
8:   rcheevos/include/rc_client_raintegration.h
9:   rcheevos/include/rc_consoles.h
10:   rcheevos/include/rc_error.h
11:   rcheevos/include/rc_export.h
12:   rcheevos/include/rc_hash.h
13:   rcheevos/include/rcheevos.h
14:   rcheevos/include/rc_runtime.h
15:   rcheevos/include/rc_runtime_types.h
16:   rcheevos/include/rc_util.h
17:   rcheevos/src/rapi/rc_api_common.c
18:   rcheevos/src/rapi/rc_api_common.h
19:   rcheevos/src/rapi/rc_api_editor.c
20:   rcheevos/src/rapi/rc_api_info.c
21:   rcheevos/src/rapi/rc_api_runtime.c
22:   rcheevos/src/rapi/rc_api_user.c
23:   rcheevos/src/rcheevos/alloc.c
24:   rcheevos/src/rcheevos/condition.c
25:   rcheevos/src/rcheevos/condset.c
26:   rcheevos/src/rcheevos/consoleinfo.c
27:   rcheevos/src/rcheevos/format.c
28:   rcheevos/src/rcheevos/lboard.c
29:   rcheevos/src/rcheevos/memref.c
30:   rcheevos/src/rcheevos/operand.c
31:   rcheevos/src/rcheevos/rc_internal.h
32:   rcheevos/src/rcheevos/rc_validate.c
33:   rcheevos/src/rcheevos/rc_validate.h
34:   rcheevos/src/rcheevos/richpresence.c
35:   rcheevos/src/rcheevos/runtime.c
36:   rcheevos/src/rcheevos/runtime_progress.c
37:   rcheevos/src/rcheevos/trigger.c
38:   rcheevos/src/rcheevos/value.c
39:   rcheevos/src/rhash/aes.c
40:   rcheevos/src/rhash/aes.h
41:   rcheevos/src/rhash/cdreader.c
42:   rcheevos/src/rhash/hash.c
43:   rcheevos/src/rhash/hash_disc.c
44:   rcheevos/src/rhash/md5.c
45:   rcheevos/src/rhash/md5.h
46:   rcheevos/src/rhash/rc_hash_internal.h
47:   rcheevos/src/rc_client.c
48:   rcheevos/src/rc_client_external.c
49:   rcheevos/src/rc_client_external.h
50:   rcheevos/src/rc_client_external_versions.h
51:   rcheevos/src/rc_client_internal.h
52:   rcheevos/src/rc_client_raintegration.c
53:   rcheevos/src/rc_client_raintegration_internal.h
54:   rcheevos/src/rc_compat.c
55:   rcheevos/src/rc_compat.h
56:   rcheevos/src/rc_util.c
57:   rcheevos/src/rc_version.c
58:   rcheevos/src/rc_version.h
59: )
60: dolphin_disable_warnings(rcheevos)
61:
62: target_include_directories(rcheevos PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/rcheevos/include")
63: target_include_directories(rcheevos INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}")
64: target_compile_definitions(rcheevos PRIVATE "RC_DISABLE_LUA=1" "RCHEEVOS_URL_SSL")
65: target_compile_definitions(rcheevos PRIVATE "RC_CLIENT_SUPPORTS_HASH")
66: target_compile_definitions(rcheevos PRIVATE "RC_CLIENT_SUPPORTS_EXTERNAL")
67: target_compile_definitions(rcheevos PRIVATE "RC_HASH_NO_ENCRYPTED")
68: target_compile_definitions(rcheevos PRIVATE "RC_HASH_NO_ROM")
69: target_compile_definitions(rcheevos PRIVATE "RC_HASH_NO_ZIP")
70: if(CMAKE_SYSTEM_NAME MATCHES "Windows")
71:   target_compile_definitions(rcheevos PRIVATE "RC_CLIENT_SUPPORTS_RAINTEGRATION")
72:   target_compile_definitions(rcheevos PRIVATE "_CRT_SECURE_NO_WARNINGS")
73: endif()

```

## rcheevos/src/rc_client.c

```text
1: #include "rc_client_internal.h"
2:
3: #include "rc_api_info.h"
4: #include "rc_api_runtime.h"
5: #include "rc_api_user.h"

6802: void rc_client_set_host(rc_client_t* client, const char* hostname)
6803: {
6804:   if (!client)
6805:     return;
6806:
6807:   if (client->state.host.host && hostname && strcmp(hostname, client->state.host.host) == 0)
6808:     return;
6809:
6810:   /* clear out any previously specified host information */
6811:   memset(&client->state.host, 0, sizeof(client->state.host));
6812:
6813:   if (hostname && (!hostname[0] || strcmp(hostname, rc_api_default_host()) == 0)) {
6814:     RC_CLIENT_LOG_VERBOSE_FORMATTED(client, "Using host: %s", rc_api_default_host());
6815:     hostname = rc_api_default_host();
6816:   }
6817:   else {
6818:     RC_CLIENT_LOG_VERBOSE_FORMATTED(client, "Using host: %s", hostname);
6819:     client->state.host.host = rc_buffer_strcpy(&client->state.buffer, hostname);
6820:   }
6821:
6822: #ifdef RC_CLIENT_SUPPORTS_EXTERNAL
6823:   if (client->state.external_client && client->state.external_client->set_host)
6824:     client->state.external_client->set_host(hostname);
6825: #endif
6826: }
6827:
6828: size_t rc_client_get_user_agent_clause(rc_client_t* client, char buffer[], size_t buffer_size)

```

## rcheevos/src/rapi/rc_api_common.c

```text
1: #include "rc_api_common.h"
2: #include "rc_api_request.h"
3: #include "rc_api_runtime.h"
4:
5: #include "../rc_compat.h"

1193: void rc_api_url_build_dorequest_url(rc_api_request_t* request, const rc_api_host_t* host) {
1194:   #define DOREQUEST_ENDPOINT "/dorequest.php"
1195:   rc_buffer_init(&request->buffer);
1196:
1197:   if (!host || !host->host) {
1198:     request->url = RETROACHIEVEMENTS_HOST DOREQUEST_ENDPOINT;
1199:   }
1200:   else {
1201:     const size_t endpoint_len = sizeof(DOREQUEST_ENDPOINT);
1202:     const size_t host_len = strlen(host->host);
1203:     const size_t protocol_len = (strstr(host->host, "://")) ? 0 : 7;
1204:     const size_t url_len = protocol_len + host_len + endpoint_len;
1205:     uint8_t* url = rc_buffer_reserve(&request->buffer, url_len);
1206:
1207:     if (protocol_len)
1208:       memcpy(url, "http://", protocol_len);
1209:
1210:     memcpy(url + protocol_len, host->host, host_len);
1211:     memcpy(url + protocol_len + host_len, DOREQUEST_ENDPOINT, endpoint_len);
1212:     rc_buffer_consume(&request->buffer, url, url + url_len);
1213:
1214:     request->url = (char*)url;
1215:   }
1216:   #undef DOREQUEST_ENDPOINT
1217: }
1218:

```

## rcheevos/test/rapi/test_rc_api_common.c

```text
1: #include "../rapi/rc_api_common.h"
2:
3: #include "rc_api_runtime.h" /* for rc_fetch_image */
4:
5: #include "../rc_compat.h"

592: static void test_url_build_dorequest_url_custom_host_no_protocol() {
593:   rc_api_request_t request;
594:   rc_api_fetch_image_request_t api_params;
595:   rc_api_host_t host;
596:
597:   memset(&host, 0, sizeof(host));
598:   host.host = "my.host";
599:
600:   rc_api_url_build_dorequest_url(&request, &host);
601:   ASSERT_STR_EQUALS(request.url, "http://my.host/dorequest.php");
602:   rc_api_destroy_request(&request);
603:
604:   api_params.image_type = RC_IMAGE_TYPE_ACHIEVEMENT;
605:   api_params.image_name = "12345";
606:   rc_api_init_fetch_image_request_hosted(&request, &api_params, &host);
607:   ASSERT_STR_EQUALS(request.url, "http://my.host/Badge/12345.png");
608:   rc_api_destroy_request(&request);
609: }
610:

```
