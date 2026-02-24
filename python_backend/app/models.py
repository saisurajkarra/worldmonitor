from pydantic import BaseModel, Field


class Facility(BaseModel):
    facility_id: str
    source: str
    facility_name: str
    city: str | None = None
    state: str | None = None
    country: str = 'US'
    latitude: float | None = None
    longitude: float | None = None
    feedstock: str | None = None


class NewsMatch(BaseModel):
    article_title: str
    article_url: str
    article_source: str
    facility_id: str
    facility_name: str
    state: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    readiness_stage: str


class CompetitorSignal(BaseModel):
    company: str
    product_line: str | None = None
    annual_volume: str | None = None
    price_signal: str | None = None
    technology: str | None = None
    source_document: str


class IngestStats(BaseModel):
    facilities_loaded: int
    sources: dict[str, int]
