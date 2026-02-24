import { getRemoteApiBaseUrl, isDesktopRuntime } from '@/services/runtime';

export interface EnergyNewsMatch {
  article_title: string;
  article_url: string;
  article_source: string;
  facility_id: string;
  facility_name: string;
  state?: string;
  confidence: number;
  readiness_stage: 'origination' | 'development' | 'execution' | 'monitoring';
}

export interface CompetitorMatrixRow {
  company: string;
  product_line?: string;
  annual_volume?: string;
  price_signal?: string;
  technology?: string;
  source_document: string;
}

export interface CompetitorDiscoveryItem {
  title: string;
  url: string;
  source: string;
  summary?: string;
  published_at?: string;
}

function apiBase(): string {
  return isDesktopRuntime() ? getRemoteApiBaseUrl() : '';
}

export async function fetchEnergyNewsMatches(limit = 100): Promise<EnergyNewsMatch[]> {
  const response = await fetch(`${apiBase()}/api/energy/v1/news/matches?limit=${limit}`);
  if (!response.ok) throw new Error(`Failed fetching energy news matches: ${response.status}`);
  return await response.json() as EnergyNewsMatch[];
}

export async function fetchCompetitorMatrix(): Promise<CompetitorMatrixRow[]> {
  const response = await fetch(`${apiBase()}/api/energy/v1/competitor/matrix`);
  if (!response.ok) throw new Error(`Failed fetching competitor matrix: ${response.status}`);
  return await response.json() as CompetitorMatrixRow[];
}

export async function fetchCompetitorDiscovery(limit = 20): Promise<CompetitorDiscoveryItem[]> {
  const response = await fetch(`${apiBase()}/api/energy/v1/competitor/discovery?limit=${limit}`);
  if (!response.ok) throw new Error(`Failed fetching competitor discovery: ${response.status}`);
  return await response.json() as CompetitorDiscoveryItem[];
}
