from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Cookie, Header, HTTPException
from app.config import get_settings
from app.database import connect

def create_access_token(user_id: int):
    s = get_settings()
    exp = datetime.now(timezone.utc) + timedelta(minutes=s.access_token_minutes)
    return jwt.encode({"sub": str(user_id), "exp": exp}, s.secret_key, algorithm="HS256")

def current_user(access_token: Optional[str] = Cookie(default=None), authorization: Optional[str] = Header(default=None)):
    token = access_token
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:]
    if not token:
        raise HTTPException(401, "Login required.")
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=["HS256"])
        uid = int(payload["sub"])
    except Exception:
        raise HTTPException(401, "Invalid or expired session.")
    conn = connect()
    row = conn.execute("SELECT id,name,email,created_at FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(401, "User no longer exists.")
    return dict(row)
