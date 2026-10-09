# PocketSmart AI

Complete FastAPI + Jinja2 + SQLite + Gemini multimodal budget recommendation assistant.

Implemented from the supplied PocketSmart AI project document:
- Home Interior Planner
- Party Budget Planner
- Jewelry Planner with optional outfit image
- Registration/login/logout
- JWT token endpoint and HTTP-only session cookie
- Session info/data
- Recommendation history
- Structured Gemini recommendations
- Deterministic local fallback when Gemini is not configured
- Mock catalog for Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO-style sources
- Responsive HTML/CSS/JavaScript frontend
- API tests

## Run in VS Code

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Open http://127.0.0.1:8000

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

For Gemini, put your key in `.env`:

GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash

If the key is blank, the app still works in local fallback mode.

## Test

```bash
pytest -q
```

## API

POST /register
POST /login
POST /logout
POST /token
GET /session-info
GET /session-data
POST /generate-home
POST /generate-party
POST /generate-jewelry
GET /recommendations-details/{history_id}
GET /history
GET /health

The source document describes third-party sourcing as mock/simulated in development. This implementation does not scrape marketplaces or claim live prices; it uses a local catalog and search URLs. Real partner APIs can be added later in app/services/catalog.py.

Production hardening should include HTTPS, a production secret, PostgreSQL, rate limiting, stronger session controls, and real partner APIs.
