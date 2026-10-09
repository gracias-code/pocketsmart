from fastapi.testclient import TestClient
from app.main import app
from app.database import DB_PATH, init_db

if DB_PATH.exists(): DB_PATH.unlink()
init_db()

def test_health():
    with TestClient(app) as c:
        r=c.get("/health")
        assert r.status_code==200

def test_auth_and_home():
    with TestClient(app) as c:
        email="pocketsmart-test@example.com"
        assert c.post("/register",json={"name":"Test User","email":email,"password":"secret123"}).status_code==200
        assert c.post("/login",json={"email":email,"password":"secret123"}).status_code==200
        r=c.post("/generate-home",json={"budget":50000,"style":"Modern","rooms":[{"room_type":"Living Room","quantity":1}],"notes":""})
        assert r.status_code==200
        assert r.json()["history_id"] is not None

def test_protected():
    with TestClient(app) as c:
        assert c.get("/session-info").status_code==401
