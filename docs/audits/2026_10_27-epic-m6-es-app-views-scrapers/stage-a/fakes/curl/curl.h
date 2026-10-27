/* T21 (#668) stage E: a stand-in for <curl/curl.h>, declarations only, so
 * g++ -fsyntax-only can read es-core/src/HttpReq.cpp on a host without
 * libcurl's headers. Every name HttpReq.cpp and HttpReq.h use, with the
 * real API's shapes (curl_easy_getinfo and curl_easy_setopt variadic, as
 * curl declares them). It links nothing and proves nothing about curl;
 * it lets the compiler check the file's own C++. */
#ifndef T21_FAKE_CURL_H
#define T21_FAKE_CURL_H
#include <stddef.h>
typedef void CURL;
typedef void CURLM;
typedef long long curl_off_t;
typedef enum { CURLE_OK = 0, CURLE_OPERATION_TIMEDOUT = 28, CURLE_PEER_FAILED_VERIFICATION = 60 } CURLcode;
typedef enum { CURLM_CALL_MULTI_PERFORM = -1, CURLM_OK = 0 } CURLMcode;
typedef enum { CURLMSG_NONE, CURLMSG_DONE } CURLMSG;
typedef struct CURLMsg { CURLMSG msg; CURL* easy_handle; union { void* whatever; CURLcode result; } data; } CURLMsg;
typedef enum {
  CURLOPT_WRITEFUNCTION = 1, CURLOPT_WRITEDATA, CURLOPT_VERBOSE, CURLOPT_USERAGENT, CURLOPT_URL,
  CURLOPT_TIMEOUT_MS, CURLOPT_SSL_VERIFYPEER, CURLOPT_SSL_VERIFYHOST, CURLOPT_SSLKEY, CURLOPT_SSLCERTTYPE,
  CURLOPT_SSLCERT, CURLOPT_PROXYTYPE, CURLOPT_PROXY, CURLOPT_POSTFIELDSIZE, CURLOPT_POST, CURLOPT_MAXREDIRS,
  CURLOPT_LOW_SPEED_TIME, CURLOPT_LOW_SPEED_LIMIT, CURLOPT_HTTPHEADER, CURLOPT_HEADERFUNCTION, CURLOPT_HEADERDATA,
  CURLOPT_FOLLOWLOCATION, CURLOPT_COPYPOSTFIELDS, CURLOPT_COOKIEJAR, CURLOPT_COOKIEFILE, CURLOPT_CONNECTTIMEOUT_MS,
  CURLOPT_BUFFERSIZE, CURLOPT_REDIR_PROTOCOLS, CURLOPT_REDIR_PROTOCOLS_STR, CURLOPT_CAINFO
} CURLoption;
typedef enum { CURLINFO_RESPONSE_CODE = 0x200002, CURLINFO_CONTENT_LENGTH_DOWNLOAD_T = 0x60000F } CURLINFO;
#define CURLPROTO_HTTP (1 << 0)
#define CURLPROTO_HTTPS (1 << 1)
#define CURLPROXY_HTTP 0
#define CURLVERSION_NOW 10
#define LIBCURL_VERSION_NUM 0x080b00
#define CURL_AT_LEAST_VERSION(x, y, z) (LIBCURL_VERSION_NUM >= (((x) << 16) | ((y) << 8) | (z)))
struct curl_slist { char* data; struct curl_slist* next; };
typedef struct { int age; const char* version; unsigned int version_num; } curl_version_info_data;
#ifdef __cplusplus
extern "C" {
#endif
CURL* curl_easy_init(void);
CURLcode curl_easy_setopt(CURL*, CURLoption, ...);
CURLcode curl_easy_getinfo(CURL*, CURLINFO, ...);
void curl_easy_cleanup(CURL*);
const char* curl_easy_strerror(CURLcode);
CURLM* curl_multi_init(void);
CURLMcode curl_multi_add_handle(CURLM*, CURL*);
CURLMcode curl_multi_remove_handle(CURLM*, CURL*);
CURLMcode curl_multi_perform(CURLM*, int*);
CURLMsg* curl_multi_info_read(CURLM*, int*);
const char* curl_multi_strerror(CURLMcode);
struct curl_slist* curl_slist_append(struct curl_slist*, const char*);
void curl_slist_free_all(struct curl_slist*);
curl_version_info_data* curl_version_info(int);
long curl_getdate(const char*, const long*);
#ifdef __cplusplus
}
#endif
#endif
