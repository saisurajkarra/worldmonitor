from __future__ import annotations

import pandas as pd
from .models import Facility, IngestStats


def _normalize(df: pd.DataFrame, source: str) -> pd.DataFrame:
    cols = {c.lower().strip(): c for c in df.columns}
    def pick(*names: str) -> str | None:
        for n in names:
            if n in cols:
                return cols[n]
        return None

    mapped = pd.DataFrame()
    mapped['facility_id'] = df[pick('id', 'facility_id', 'site_id')].astype(str)
    mapped['facility_name'] = df[pick('facility_name', 'name', 'site_name')].astype(str)
    mapped['city'] = df[pick('city')] if pick('city') else pd.Series([None]*len(df))
    mapped['state'] = df[pick('state', 'state_abbrev')] if pick('state', 'state_abbrev') else pd.Series([None]*len(df))
    mapped['latitude'] = pd.to_numeric(df[pick('lat', 'latitude')], errors='coerce') if pick('lat', 'latitude') else pd.Series([None]*len(df))
    mapped['longitude'] = pd.to_numeric(df[pick('lon', 'lng', 'longitude')], errors='coerce') if pick('lon', 'lng', 'longitude') else pd.Series([None]*len(df))
    mapped['feedstock'] = df[pick('feedstock', 'waste_type')] if pick('feedstock', 'waste_type') else pd.Series([None]*len(df))
    mapped['source'] = source
    mapped['country'] = 'US'
    return mapped


def load_facilities(lmop_csv_path: str, wwtp_csv_path: str, cattle_csv_path: str) -> tuple[list[Facility], IngestStats]:
    lmop = _normalize(pd.read_csv(lmop_csv_path), 'lmop')
    wwtp = _normalize(pd.read_csv(wwtp_csv_path), 'wwtp')
    cattle = _normalize(pd.read_csv(cattle_csv_path), 'cattle')

    all_df = pd.concat([lmop, wwtp, cattle], ignore_index=True)
    all_df = all_df[all_df['facility_name'].astype(str).str.len() > 1].drop_duplicates(subset=['facility_id'])

    facilities = [Facility(**row) for row in all_df.to_dict(orient='records')]
    stats = IngestStats(
        facilities_loaded=len(facilities),
        sources={
            'lmop': int(len(lmop)),
            'wwtp': int(len(wwtp)),
            'cattle': int(len(cattle)),
        },
    )
    return facilities, stats
