# Energy Intelligence Backend (FastAPI)

This backend is the production-oriented Python layer for RNG/Biomethane and Industrial Gases market intelligence.

## Install Python dependencies
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r python_backend/requirements.txt
python -m spacy download en_core_web_sm
```

## Required environment variables
```bash
export APP_ENV=development
export LOG_LEVEL=INFO
export LMOP_CSV_PATH=/absolute/path/to/epa_lmop.csv
export WWTP_CSV_PATH=/absolute/path/to/wwtp.csv
export CATTLE_CSV_PATH=/absolute/path/to/cattle_dairy.csv
export NEWS_API_URL=https://newsapi.org/v2/everything
export NEWS_API_KEY=replace_with_real_api_key
export COMPETITOR_PDF_DIR=/absolute/path/to/industry_pdfs
export REQUEST_TIMEOUT_S=20
export BREAKER_FAIL_MAX=4
export BREAKER_RESET_TIMEOUT_S=60
```

## Run backend
```bash
uvicorn python_backend.app.main:app --host 0.0.0.0 --port 8081
```

## Frontend npm dependencies
No additional npm package is required for the initial bridge because frontend integration uses native `fetch`. Existing project install remains:
```bash
npm install
```

## Endpoints
- `GET /health`
- `POST /api/energy/v1/facilities/reload`
- `GET /api/energy/v1/news/matches?limit=100`
- `GET /api/energy/v1/competitor/matrix`
- `GET /api/energy/v1/competitor/discovery?limit=20`

## News API compatibility
The backend continues to use a single remote news provider URL/key (`NEWS_API_URL`, `NEWS_API_KEY`) in the same operational style as existing worldmonitor fetch-based integrations: one configurable upstream endpoint, server-side filtering/querying, and frontend consumption via typed fetch services.
