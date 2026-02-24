from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from .models import CompetitorSignal

COMPANY_PAT = re.compile(r'\b(?:Inc\.|LLC|Ltd\.|Corporation|Corp\.)\b', re.IGNORECASE)
VOLUME_PAT = re.compile(r'(\d[\d,\.]*\s*(?:MMscfd|tonnes|tons|kg|kg/day|Nm3/h|MTPA))', re.IGNORECASE)
PRICE_PAT = re.compile(r'(\$\s?\d[\d,\.]*\s*(?:/\s?(?:kg|MMBtu|ton|Nm3|Mcf)))', re.IGNORECASE)
TECH_PAT = re.compile(r'\b(PSA|membrane separation|cryogenic|SMR|electrolyzer|amine scrubbing)\b', re.IGNORECASE)


def extract_competitor_signals(pdf_dir: str) -> list[CompetitorSignal]:
    signals: list[CompetitorSignal] = []
    for pdf_path in Path(pdf_dir).glob('*.pdf'):
        text = ''
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            text += '\n' + (page.extract_text() or '')

        company = _extract_company_name(text) or pdf_path.stem
        volume = _first(VOLUME_PAT, text)
        price = _first(PRICE_PAT, text)
        tech = _first(TECH_PAT, text)

        signals.append(
            CompetitorSignal(
                company=company,
                product_line=None,
                annual_volume=volume,
                price_signal=price,
                technology=tech,
                source_document=pdf_path.name,
            )
        )
    return signals


def _first(pattern: re.Pattern[str], text: str) -> str | None:
    m = pattern.search(text)
    return m.group(1) if m else None


def _extract_company_name(text: str) -> str | None:
    for line in text.splitlines()[:50]:
        if COMPANY_PAT.search(line):
            return line.strip()[:200]
    return None
