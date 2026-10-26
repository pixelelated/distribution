# T19's F-01 probe: a login2 naming the account, with no password and no token.
# Prints the status, the X-RA-Offline header, the body's key names and whether
# a Token key is present -- never a value, never the account name.
import json, re, urllib.request, urllib.parse
cfg = open("/storage/.config/system/configs/system.cfg", encoding="utf-8", errors="replace").read()
m = re.search(r"^global\.retroachievements\.username=(.*)$", cfg, re.M)
user = (m.group(1).strip() if m else "")
print("account name read from system.cfg:", "yes" if user else "no")
url = "http://127.0.0.1:8080/dorequest.php?" + urllib.parse.urlencode({"r": "login2", "u": user})
try:
    with urllib.request.urlopen(url, timeout=30) as r:
        status, offline, body = r.status, r.headers.get("X-RA-Offline"), r.read()
except urllib.error.HTTPError as e:
    status, offline, body = e.code, e.headers.get("X-RA-Offline"), e.read()
data = None
try:
    data = json.loads(body)
    keys = sorted(data.keys()) if isinstance(data, dict) else ["<JSON, not an object>"]
except Exception:
    keys = ["<not JSON: %d bytes>" % len(body)]
print("status", status, "| X-RA-Offline", offline, "| body keys", keys, "| Token key present:", "yes" if "Token" in keys else "no", "| Token non-empty:", "yes" if isinstance(data, dict) and data.get("Token") else "no")
