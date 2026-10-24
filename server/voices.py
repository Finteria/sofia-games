"""Family voice recordings for Sofia's games, kept on the server so Safari can't wipe them.

Caddy proxies /api/* here. Anyone can listen; recording, deleting and restoring need the
family code (X-Family-Key header). A new take never overwrites the old one: the old one
moves to history/<key>/ and "restore" brings back the newest take from there.

  GET    /api/voices                list of recorded keys: {"cat-ru": {"v": "...", "old": 2}, ...}
  GET    /api/voices/<key>          the current take
  PUT    /api/voices/<key>          save a new take (body = audio)
  DELETE /api/voices/<key>          move the current take to history
  POST   /api/voices/<key>/restore  swap in the newest take from history
  GET    /api/check                 204 if the family code is right

Data dir (VOICES_DIR): current/<key>.<ext>, history/<key>/<time>.<ext>, family-key.txt
"""
import hmac, json, os, re, shutil, time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DATA = Path(os.environ.get("VOICES_DIR", "/data"))
CUR, HIST = DATA / "current", DATA / "history"
FAMILY_KEY = (DATA / "family-key.txt").read_text().strip()
MAX_BYTES = 10 * 1024 * 1024
KEEP_OLD = 30  # older takes kept per key
KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
EXT = {"audio/mp4": "m4a", "audio/x-m4a": "m4a", "audio/aac": "m4a", "audio/mpeg": "mp3", "audio/mp3": "mp3",
       "audio/wav": "wav", "audio/x-wav": "wav", "audio/wave": "wav", "audio/webm": "webm", "audio/ogg": "ogg",
       "audio/flac": "flac"}
TYPE = {ext: t for t, ext in reversed(EXT.items())} | {"bin": "application/octet-stream"}


def current(key):
    return next(CUR.glob(key + ".*"), None)


def history(key):
    d = HIST / key
    return sorted(d.iterdir()) if d.is_dir() else []


def archive(key):
    f = current(key)
    if not f:
        return
    d = HIST / key
    d.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    f.rename(d / f"{stamp}{f.suffix}")
    for old in history(key)[:-KEEP_OLD]:
        old.unlink()


def listing():
    keys = {f.stem for f in CUR.iterdir()} | {d.name for d in HIST.iterdir()}
    out = {}
    for k in sorted(keys):
        f = current(k)
        out[k] = {"v": str(f.stat().st_mtime_ns) if f else None, "old": len(history(k))}
    return out


class Handler(BaseHTTPRequestHandler):
    server_version = "voices"

    def send(self, code, body=b"", ctype="application/json", cache="no-store"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def route(self):
        parts = self.path.split("?")[0].strip("/").split("/")
        if parts[:2] != ["api", "voices"] or len(parts) > 4:
            return None, None
        key = parts[2] if len(parts) > 2 else None
        if key is not None and (len(key) > 60 or not KEY.fullmatch(key)):
            return False, None
        return key, (parts[3] if len(parts) == 4 else None)

    def authorized(self):
        if hmac.compare_digest(self.headers.get("X-Family-Key", "").strip().lower().encode(), FAMILY_KEY.encode()):
            return True
        time.sleep(1)  # makes guessing the code slow
        self.send(403, {"error": "wrong family code"})
        return False

    def do_GET(self):
        if self.path.split("?")[0] == "/api/check":
            return self.authorized() and self.send(204)
        key, action = self.route()
        if key is None and action is None and self.path.split("?")[0].rstrip("/") == "/api/voices":
            return self.send(200, listing())
        f = key and not action and current(key)
        if not f:
            return self.send(404, {"error": "not found"})
        # the URL carries ?v=<version>, so a take can be cached for good
        self.send(200, f.read_bytes(), TYPE.get(f.suffix[1:], TYPE["bin"]), "public, max-age=31536000, immutable")

    do_HEAD = do_GET

    def do_PUT(self):
        key, action = self.route()
        if not key or action:
            return self.send(404, {"error": "not found"})
        if not self.authorized():
            return
        n = int(self.headers.get("Content-Length") or 0)
        if not 0 < n <= MAX_BYTES:
            return self.send(413, {"error": "empty or too big"})
        body = self.rfile.read(n)
        ext = EXT.get(self.headers.get("Content-Type", "").split(";")[0].strip().lower(), "bin")
        tmp = CUR / f".{key}.tmp"
        tmp.write_bytes(body)
        archive(key)
        tmp.rename(CUR / f"{key}.{ext}")
        self.send(200, listing())

    def do_DELETE(self):
        key, action = self.route()
        if not key or action:
            return self.send(404, {"error": "not found"})
        if self.authorized():
            archive(key)
            self.send(200, listing())

    def do_POST(self):
        key, action = self.route()
        if not key or action != "restore":
            return self.send(404, {"error": "not found"})
        if not self.authorized():
            return
        old = history(key)
        if not old:
            return self.send(409, {"error": "no older take"})
        newest = old[-1]
        archive(key)
        newest.rename(CUR / f"{key}{newest.suffix}")
        self.send(200, listing())

    def log_message(self, fmt, *args):
        print(f"{self.headers.get('X-Forwarded-For', self.client_address[0])} {fmt % args}", flush=True)


if __name__ == "__main__":
    CUR.mkdir(parents=True, exist_ok=True)
    HIST.mkdir(parents=True, exist_ok=True)
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
