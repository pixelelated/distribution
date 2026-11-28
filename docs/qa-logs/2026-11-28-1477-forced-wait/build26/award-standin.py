# A loopback RetroAchievements stand-in for #1477's achievements step: an
# award request (r=awardachievement) is held <delay> seconds, then accepted;
# everything else answers 200 at once. No real account or service.
import json, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
port, delay = int(sys.argv[1]), float(sys.argv[2])
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def answer(self):
        q = parse_qs(urlsplit(self.path).query)
        if self.command == "POST":
            n = int(self.headers.get("Content-Length", "0") or 0)
            q.update(parse_qs(self.rfile.read(n).decode(errors="replace")))
        r = q.get("r", [""])[0]
        if r == "awardachievement":
            sys.stderr.write("standin award held %.0fs at %s\n" % (delay, time.strftime("%H:%M:%S"))); sys.stderr.flush()
            time.sleep(delay)
            body = {"Success": True, "AchievementID": int(q.get("a", ["0"])[0] or 0), "Score": 0}
        else:
            body = {"Success": True}
        data = json.dumps(body).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers()
        if self.command != "HEAD": self.wfile.write(data)
    do_GET = do_POST = do_HEAD = answer
ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
