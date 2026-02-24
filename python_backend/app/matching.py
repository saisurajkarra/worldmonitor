from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import spacy
from rapidfuzz import fuzz

from .models import Facility, NewsMatch


@dataclass
class Article:
    title: str
    url: str
    source: str
    content: str


class FacilityMatcher:
    def __init__(self) -> None:
        self.nlp = spacy.load('en_core_web_sm')

    def match(self, articles: Iterable[Article], facilities: list[Facility]) -> list[NewsMatch]:
        matches: list[NewsMatch] = []
        for article in articles:
            doc = self.nlp(f"{article.title}. {article.content}")
            locations = {ent.text.lower() for ent in doc.ents if ent.label_ in {'GPE', 'LOC'}}
            for facility in facilities:
                score = fuzz.token_set_ratio(article.title.lower(), facility.facility_name.lower()) / 100.0
                if facility.state and facility.state.lower() in locations:
                    score = min(1.0, score + 0.25)
                if score >= 0.68:
                    matches.append(
                        NewsMatch(
                            article_title=article.title,
                            article_url=article.url,
                            article_source=article.source,
                            facility_id=facility.facility_id,
                            facility_name=facility.facility_name,
                            state=facility.state or None,
                            confidence=round(score, 3),
                            readiness_stage=self._infer_readiness(article.title, article.content),
                        )
                    )
        return matches

    @staticmethod
    def _infer_readiness(title: str, content: str) -> str:
        text = f"{title} {content}".lower()
        if any(k in text for k in ('awarded', 'epc contract', 'fina investment decision', 'construction start')):
            return 'execution'
        if any(k in text for k in ('permitting', 'environmental review', 'front-end engineering', 'feasibility')):
            return 'development'
        if any(k in text for k in ('mou', 'letter of intent', 'preliminary talks')):
            return 'origination'
        return 'monitoring'
