# Quickstart

Get the API running in under a minute.

## 1. Install

From the `api-dev/` folder:

```bash
python3 -m venv venv          # optional but recommended
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Start the server

```bash
uvicorn app.main:app --reload
```

You should see `Uvicorn running on http://127.0.0.1:8000`.

## 3. Open the interactive docs

Visit **http://localhost:8000/docs** in your browser. You can try every
endpoint from there.

## 4. Try it from the terminal

```bash
# Get a token (no auth needed)
curl -X POST http://localhost:8000/token

# Analyze text (needs the bearer token)
curl -X POST http://localhost:8000/analyze-text \
  -H "Authorization: Bearer demo_token" \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI makes building APIs enjoyable!", "analysis_type": "advanced"}'

# Health check (needs the API key)
curl -X GET http://localhost:8000/system/health \
  -H "X-API-KEY: portfolio_showcase_key"
```

## 5. Run the tests

```bash
pytest
```

Expected: `8 passed`.

---

### Demo credentials
| Purpose            | Value                    | Sent as                          |
|--------------------|--------------------------|----------------------------------|
| Bearer token       | `demo_token`             | `Authorization: Bearer <token>`  |
| API key            | `portfolio_showcase_key` | `X-API-KEY: <key>`               |

### Run with Docker (optional)
```bash
docker build -t showcase-api .
docker run -p 8000:8000 showcase-api
```
