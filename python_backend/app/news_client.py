from __future__ import annotations

import httpx

from .matching import Article


def fetch_news(news_api_url: str, api_key: str, timeout_s: float) -> list[Article]:
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {
        'q': '(biomethane OR renewable natural gas OR wastewater methane OR hydrogen purification OR helium plant)',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 100,
    }
    with httpx.Client(timeout=timeout_s) as client:
        res = client.get(news_api_url, headers=headers, params=params)
        res.raise_for_status()
        payload = res.json()

    items = payload.get('articles', [])
    return [
        Article(
            title=item.get('title', ''),
            url=item.get('url', ''),
            source=(item.get('source') or {}).get('name', 'unknown'),
            content=item.get('content') or item.get('description') or '',
        )
        for item in items
        if item.get('title') and item.get('url')
    ]
