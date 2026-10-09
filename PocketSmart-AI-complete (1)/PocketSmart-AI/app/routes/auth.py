import sqlite3
from fastapi import APIRouter, HTTPException, Response
import hashlib, hmac, os

def generate_password_hash(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120000)
    return "pbkdf2_sha256$120000$" + salt.hex() + "$" + digest.hex()

def check_password_hash(stored, password):
    try:
        _, rounds, salt_hex, digest_hex = stored.split("$")
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(rounds))
        return hmac.compare_digest(digest.hex(), digest_hex)
    except Exception:
        return False
from app.database import connect
from app.dependencies import create_access_token
from app.models.schemas import RegisterRequest, LoginRequest

router = APIRouter()

@router.post("/register")
def register(p: RegisterRequest):
    conn = connect()
    try:
        cur = conn.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",
                           (p.name.strip(), p.email.lower(), generate_password_hash(p.password)))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(409, "An account with that email already exists.")
    uid = cur.lastrowid
    conn.close()
    return {"message":"Registration successful.","access_token":create_access_token(uid)}

@router.post("/login")
def login(p: LoginRequest, response: Response):
    conn = connect()
    row = conn.execute("SELECT id,name,email,password_hash FROM users WHERE email=?", (p.email.lower(),)).fetchone()
    conn.close()
    if not row or not check_password_hash(row["password_hash"], p.password):
        raise HTTPException(401, "Invalid email or password.")
    token = create_access_token(row["id"])
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=7200)
    return {"message":"Login successful.","access_token":token,"user":{"id":row["id"],"name":row["name"],"email":row["email"]}}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message":"Logged out."}

@router.post("/token")
def token(p: LoginRequest):
    conn=connect()
    row=conn.execute("SELECT id,password_hash FROM users WHERE email=?", (p.email.lower(),)).fetchone()
    conn.close()
    if not row or not check_password_hash(row["password_hash"], p.password):
        raise HTTPException(401, "Invalid email or password.")
    return {"access_token":create_access_token(row["id"]), "token_type":"bearer"}
