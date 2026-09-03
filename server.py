#!/usr/bin/env python3
import hashlib
import json
import secrets
import sqlite3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "app.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          salt TEXT NOT NULL,
          password_hash TEXT NOT NULL,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tokens(
          token TEXT PRIMARY KEY,
          user_id INTEGER NOT NULL,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS favorites(
          user_id INTEGER NOT NULL,
          entry_id TEXT NOT NULL,
          PRIMARY KEY(user_id, entry_id)
        );
        """
    )
    conn.commit()
    conn.close()


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()


def create_token(user_id):
    token = secrets.token_urlsafe(32)
    conn = get_db()
    conn.execute("INSERT INTO tokens(token, user_id) VALUES(?,?)", (token, user_id))
    conn.commit()
    conn.close()
    return token


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".json": "application/json; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
    }

    def _json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:
            return {}

    def _user_id(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        token = auth[7:].strip()
        conn = get_db()
        row = conn.execute("SELECT user_id FROM tokens WHERE token=?", (token,)).fetchone()
        conn.close()
        return row["user_id"] if row else None

    def do_GET(self):
        if self.path == "/api/me":
            uid = self._user_id()
            if not uid:
                return self._json({"error": "unauthorized"}, 401)
            conn = get_db()
            row = conn.execute("SELECT name,email FROM users WHERE id=?", (uid,)).fetchone()
            conn.close()
            return self._json({"user": dict(row)})

        if self.path == "/api/favorites":
            uid = self._user_id()
            if not uid:
                return self._json({"error": "unauthorized"}, 401)
            conn = get_db()
            rows = conn.execute("SELECT entry_id FROM favorites WHERE user_id=?", (uid,)).fetchall()
            conn.close()
            return self._json({"favorites": [r["entry_id"] for r in rows]})

        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/register":
            data = self._body()
            name = (data.get("name") or "").strip() or "User"
            email = (data.get("email") or "").strip().lower()
            password = data.get("password") or ""

            if not email or "@" not in email:
                return self._json({"error": "invalid email"}, 400)
            if len(password) < 6:
                return self._json({"error": "password too short"}, 400)

            salt = secrets.token_hex(16)
            ph = hash_password(password, salt)

            conn = get_db()
            try:
                cur = conn.execute(
                    "INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
                    (name, email, salt, ph),
                )
                uid = cur.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                conn.close()
if self.path == "/api/upgrade":
    data = self._body()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip() or "User"

    if not email or "@" not in email:
        return self._json({"error": "invalid email"}, 400)
    if len(password) < 6:
        return self._json({"error": "password too short"}, 400)

    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

    if not row:
        salt = secrets.token_hex(16)
        ph = hash_password(password, salt)
        cur = conn.execute(
            "INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
            (name, email, salt, ph),
        )
        uid = cur.lastrowid
        conn.commit()
    else:
        if hash_password(password, row["salt"]) != row["password_hash"]:
            conn.close()
if self.path == "/api/upgrade":
    data = self._body()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip() or "User"

    if not email or "@" not in email:
        return self._json({"error": "invalid email"}, 400)
    if len(password) < 6:
        return self._json({"error": "password too short"}, 400)

    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

    if not row:
        salt = secrets.token_hex(16)
        ph = hash_password(password, salt)
        cur = conn.execute(
            "INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
            (name, email, salt, ph),
        )
        uid = cur.lastrowid
        conn.commit()
    else:
        if hash_password(password, row["salt"]) != row["password_hash"]:
            conn.close()
            return self._json({"error": "wrong password"}, 403)
        uid = row["id"]

    conn.close()
    token = create_token(uid)
    return self._json({"token": token, "user": {"name": name, "email": email}})
        uid = row["id"]

    conn.close()
    token = create_token(uid)
    return self._json({"token": token, "user": {"name": name, "email": email}})
            conn.close()

            token = create_token(uid)
if self.path == "/api/upgrade":
    data = self._body()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip() or "User"

    if not email or "@" not in email:
        return self._json({"error": "invalid email"}, 400)
    if len(password) < 6:
        return self._json({"error": "password too short"}, 400)

    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

    if not row:
        salt = secrets.token_hex(16)
        ph = hash_password(password, salt)
        cur = conn.execute(
            "INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
            (name, email, salt, ph),
        )
        uid = cur.lastrowid
        conn.commit()
    else:
        if hash_password(password, row["salt"]) != row["password_hash"]:
            conn.close()
            return self._json({"error": "wrong password"}, 403)
        uid = row["id"]

    conn.close()
    token = create_token(uid)
    return self._json({"token": token, "user": {"name": name, "email": email}})

        if self.path == "/api/login":
            data = self._body()
            email = (data.get("email") or "").strip().lower()
            password = data.get("password") or ""

            conn = get_db()
            row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            conn.close()

            if not row:
                return self._json({"error": "user not found"}, 404)
            if hash_password(password, row["salt"]) != row["password_hash"]:
                return self._json({"error": "wrong password"}, 403)

            token = create_token(row["id"])
            return self._json({"token": token, "user": {"name": row["name"], "email": row["email"]}})

        return self._json({"error": "not found"}, 404)

    def do_PUT(self):
        if self.path == "/api/favorites":
            uid = self._user_id()
            if not uid:
                return self._json({"error": "unauthorized"}, 401)

            data = self._body()
            ids = data.get("favorites") or []

            conn = get_db()
            conn.execute("DELETE FROM favorites WHERE user_id=?", (uid,))
            for eid in ids:
                conn.execute(
                    "INSERT OR IGNORE INTO favorites(user_id,entry_id) VALUES(?,?)",
                    (uid, str(eid)),
                )
            conn.commit()
            conn.close()
            return self._json({"ok": True})

        return self._json({"error": "not found"}, 404)


def main():
    init_db()
    port = 8000
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)

    print("PyReference server (static + API):")
    print("  http://localhost:8000")
    print("Нажми Ctrl+C для остановки.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()