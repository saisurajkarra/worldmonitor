# Phase 0 Refactor Audit: WorldMonitor -> B2B Market Intelligence Platform

This audit identifies files in the requested trees that should be **deleted** or **fundamentally rewritten** to support the new RNG/Biomethane + Industrial Gases product direction.

## Scope inspected
- `src/services/**`
- `server/worldmonitor/**`
- `proto/worldmonitor/**`
- `src/components/**`

## Delete candidates (domain modules to remove entirely)

### Server handlers (`server/worldmonitor/**`)
Delete entire domain folders:
- `server/worldmonitor/wildfire/**`
- `server/worldmonitor/maritime/**`
- `server/worldmonitor/displacement/**`
- `server/worldmonitor/aviation/**`
- `server/worldmonitor/infrastructure/**`
- `server/worldmonitor/military/**`
- `server/worldmonitor/conflict/**`
- `server/worldmonitor/intelligence/**`
- `server/worldmonitor/unrest/**`
- `server/worldmonitor/prediction/**`
- `server/worldmonitor/cyber/**`
- `server/worldmonitor/seismology/**`
- `server/worldmonitor/climate/**`
- `server/worldmonitor/economic/**`

### Protobuf API surfaces (`proto/worldmonitor/**`)
Delete domain proto trees:
- `proto/worldmonitor/wildfire/**`
- `proto/worldmonitor/maritime/**`
- `proto/worldmonitor/displacement/**`
- `proto/worldmonitor/aviation/**`
- `proto/worldmonitor/infrastructure/**`
- `proto/worldmonitor/military/**`
- `proto/worldmonitor/conflict/**`
- `proto/worldmonitor/intelligence/**`
- `proto/worldmonitor/unrest/**`
- `proto/worldmonitor/prediction/**`
- `proto/worldmonitor/cyber/**`
- `proto/worldmonitor/seismology/**`
- `proto/worldmonitor/climate/**`
- `proto/worldmonitor/economic/**`

### Frontend services (`src/services/**`)
Delete service files/folders tied to removed domains and military/cyber/climate-era worldview (examples include):
- folders: `src/services/{wildfires,maritime,displacement,aviation,infrastructure,military,conflict,intelligence,unrest,prediction,economic,cyber,climate}/**`
- files: `src/services/{military-flights,usni-fleet,gdelt-intel,cached-risk-scores,cached-theater-posture,population-exposure,cable-health,tech-hub-index,tech-activity,hotspot-escalation,correlation}.ts`

### Frontend components (`src/components/**`)
Delete components tied to removed modules (examples include):
- `src/components/{StrategicPosturePanel,StrategicRiskPanel,SatelliteFiresPanel,DisplacementPanel,UcdpEventsPanel,PizzIntIndicator,PopulationExposurePanel,ClimateAnomalyPanel,EconomicPanel,MacroSignalsPanel,TechHubsPanel,GeoHubsPanel,TechReadinessPanel,GdeltIntelPanel,StatusPanel,ServiceStatusPanel}.ts`

## Rewrite candidates (keep path, replace implementation)

### Backend boundary and data APIs
- `server/worldmonitor/news/v1/**` (repurpose into real news ingestion + linking pipeline)
- `server/worldmonitor/market/v1/**` (repurpose into competitor/pricing intelligence APIs)
- `server/worldmonitor/research/v1/**` (repurpose into deep-research document pipeline)

### Proto contracts
- `proto/worldmonitor/news/v1/**` (facility linking + readiness stage inference)
- `proto/worldmonitor/market/v1/**` (competitor matrix/price-volume-tech specs)
- `proto/worldmonitor/research/v1/**` (document extraction outputs)
- `proto/worldmonitor/core/v1/**` (retain common geo/time IDs but extend for entity resolution confidence and model provenance)

### Frontend service layer
- `src/services/live-news.ts`
- `src/services/story-data.ts`
- `src/services/entity-extraction.ts`
- `src/services/entity-index.ts`
- `src/services/runtime-config.ts`
- `src/services/storage.ts`

### Frontend UI shell
- `src/components/MapContainer.ts`
- `src/components/Map.ts`
- `src/components/DeckGLMap.ts`
- `src/components/MonitorPanel.ts`
- `src/components/WorldMonitorTab.ts`
- `src/components/InsightsPanel.ts`
- `src/components/LiveNewsPanel.ts`
- `src/components/NewsPanel.ts`
- `src/components/MarketPanel.ts`
- `src/components/index.ts`

## First 5 critical files needed to define the ML/Frontend bridge
1. `proto/worldmonitor/news/v1/service.proto`
2. `proto/worldmonitor/news/v1/news_item.proto`
3. `server/worldmonitor/news/v1/handler.ts`
4. `src/services/live-news.ts`
5. `src/components/WorldMonitorTab.ts`

