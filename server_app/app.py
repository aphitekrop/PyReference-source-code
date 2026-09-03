from flask import Flask, request, jsonify
import sqlite3, hashlib, secrets, os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "app.db")

app = Flask(__name__)

def db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def init():
    c = db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, salt TEXT NOT NULL,
      password_hash TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS tokens(token TEXT PRIMARY KEY, user_id INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS favorites(user_id INTEGER NOT NULL, entry_id TEXT NOT NULL,
      PRIMARY KEY(user_id, entry_id));
    """)
    c.commit(); c.close()

def hash_pw(pw, salt):
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 120000).hex()

def new_token(uid):
    t = secrets.token_urlsafe(32)
    c = db(); c.execute("INSERT INTO tokens(token,user_id) VALUES(?,?)", (t, uid)); c.commit(); c.close()
    return t

@app.after_request
def cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    return r

@app.route("/api/<path:_>", methods=["OPTIONS"])
def opt(_): return "", 204

def user_id():
    a = request.headers.get("Authorization", "")
    if not a.startswith("Bearer "): return None
    c = db(); row = c.execute("SELECT user_id FROM tokens WHERE token=?", (a[7:],)).fetchone(); c.close()
    return row["user_id"] if row else None

@app.route("/api/register", methods=["POST"])
def register():
    d = request.get_json(silent=True) or {}
    name = (d.get("name") or "").strip() or "User"
    email = (d.get("email") or "").strip().lower()
    pw = d.get("password") or ""
    if not email or "@" not in email: return jsonify(error="invalid email"), 400
    if len(pw) < 6: return jsonify(error="password too short"), 400
    salt = secrets.token_hex(16)
    c = db()
    try:
        cur = c.execute("INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
                        (name, email, salt, hash_pw(pw, salt)))
        uid = cur.lastrowid; c.commit()
    except sqlite3.IntegrityError:
        c.close(); return jsonify(error="email already registered"), 409
    c.close()
    return jsonify(token=new_token(uid), user={"name": name, "email": email})

@app.route("/api/login", methods=["POST"])
def login():
    d = request.get_json(silent=True) or {}
    email = (d.get("email") or "").strip().lower(); pw = d.get("password") or ""
    c = db(); row = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone(); c.close()
    if not row: return jsonify(error="user not found"), 404
    if hash_pw(pw, row["salt"]) != row["password_hash"]: return jsonify(error="wrong password"), 403
    return jsonify(token=new_token(row["id"]), user={"name": row["name"], "email": row["email"]})

@app.route("/api/upgrade", methods=["POST"])
def upgrade():
    d = request.get_json(silent=True) or {}
    email = (d.get("email") or "").strip().lower(); pw = d.get("password") or ""
    name = (d.get("name") or "").strip() or "User"
    if not email or len(pw) < 6: return jsonify(error="invalid"), 400
    c = db(); row = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not row:
        salt = secrets.token_hex(16)
        cur = c.execute("INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
                        (name, email, salt, hash_pw(pw, salt)))
        uid = cur.lastrowid; c.commit()
    else:
        if hash_pw(pw, row["salt"]) != row["password_hash"]:
            c.close(); return jsonify(error="wrong password"), 403
        uid = row["id"]
    c.close()
    return jsonify(token=new_token(uid), user={"name": name, "email": email})

@app.route("/api/me")
def me():
    uid = user_id()
    if not uid: return jsonify(error="unauthorized"), 401
    c = db(); row = c.execute("SELECT name,email FROM users WHERE id=?", (uid,)).fetchone(); c.close()
    return jsonify(user=dict(row))

@app.route("/api/favorites", methods=["GET", "PUT"])
def favorites():
    uid = user_id()
    if not uid: return jsonify(error="unauthorized"), 401
    c = db()
    if request.method == "GET":
        rows = c.execute("SELECT entry_id FROM favorites WHERE user_id=?", (uid,)).fetchall()
        c.close(); return jsonify(favorites=[r["entry_id"] for r in rows])
    ids = (request.get_json(silent=True) or {}).get("favorites") or []
    c.execute("DELETE FROM favorites WHERE user_id=?", (uid,))
    for e in ids: c.execute("INSERT OR IGNORE INTO favorites(user_id,entry_id) VALUES(?,?)", (uid, str(e)))
    c.commit(); c.close()
    return jsonify(ok=True)

init()