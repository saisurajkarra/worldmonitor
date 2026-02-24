from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pybreaker import CircuitBreaker, CircuitBreakerError

from .competitor_matrix import extract_competitor_signals
from .config import settings
from .data_ingest import load_facilities
from .matching import FacilityMatcher
from .news_client import fetch_news
from .telemetry import configure_logging, get_logger

configure_logging(settings.log_level)
log = get_logger('energy-intel-api')

app = FastAPI(title='Energy Market Intelligence API', version='0.2.0')
matcher = FacilityMatcher()
breaker = CircuitBreaker(fail_max=settings.breaker_fail_max, reset_timeout=settings.breaker_reset_timeout_s)
facilities = []


@app.on_event('startup')
def startup() -> None:
    global facilities
    facilities, stats = load_facilities(settings.lmop_csv_path, settings.wwtp_csv_path, settings.cattle_csv_path)
    log.info('facilities_loaded', total=stats.facilities_loaded, sources=stats.sources)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok', 'env': settings.app_env}


@app.post('/api/energy/v1/facilities/reload')
def reload_facilities() -> dict:
    global facilities
    facilities, stats = load_facilities(settings.lmop_csv_path, settings.wwtp_csv_path, settings.cattle_csv_path)
    return {'status': 'reloaded', 'stats': stats.model_dump()}


@app.get('/api/energy/v1/news/matches')
def get_news_matches(limit: int = 100) -> list[dict]:
    if not facilities:
        raise HTTPException(status_code=503, detail='Facility index not loaded')

    try:
        articles = breaker.call(fetch_news, settings.news_api_url, settings.news_api_key, settings.request_timeout_s)
    except CircuitBreakerError as exc:
        log.warning('news_upstream_circuit_open')
        raise HTTPException(status_code=503, detail='News provider circuit open') from exc
    except Exception as exc:  # noqa: BLE001
        log.error('news_fetch_failed', error=str(exc))
        raise HTTPException(status_code=502, detail='News provider request failed') from exc

    matches = matcher.match(articles, facilities)
    matches = sorted(matches, key=lambda m: m.confidence, reverse=True)[:limit]
    return [m.model_dump() for m in matches]


@app.get('/api/energy/v1/competitor/matrix')
def competitor_matrix() -> list[dict]:
    try:
        signals = breaker.call(extract_competitor_signals, settings.competitor_pdf_dir)
        return [s.model_dump() for s in signals]
    except CircuitBreakerError as exc:
        raise HTTPException(status_code=503, detail='Document processing circuit open') from exc
    except Exception as exc:  # noqa: BLE001
        log.error('competitor_matrix_failed', error=str(exc))
        raise HTTPException(status_code=500, detail='Competitor extraction failed') from exc


@app.get('/api/energy/v1/competitor/discovery')
def competitor_discovery(limit: int = 20) -> list[dict]:
    query = '((RFP OR RFQ OR proposal OR EPC OR FEED OR procurement) AND (biogas OR biomethane OR RNG OR hydrogen OR helium membrane))'
    try:
        articles = breaker.call(fetch_news, settings.news_api_url, settings.news_api_key, settings.request_timeout_s, query, min(100, max(limit, 20)))
    except CircuitBreakerError as exc:
        raise HTTPException(status_code=503, detail='Discovery circuit open') from exc
    except Exception as exc:  # noqa: BLE001
        log.error('competitor_discovery_failed', error=str(exc))
        raise HTTPException(status_code=502, detail='Competitor discovery failed') from exc

    return [
        {
            'title': a.title,
            'url': a.url,
            'source': a.source,
            'summary': a.content[:350],
            'published_at': None,
        }
        for a in articles[:limit]
    ]
