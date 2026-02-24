import { Panel } from './Panel';
import { fetchCompetitorDiscovery, fetchCompetitorMatrix, type CompetitorDiscoveryItem, type CompetitorMatrixRow } from '@/services/energy-intelligence';

function renderMatrixRows(rows: CompetitorMatrixRow[]): string {
  if (!rows.length) return '<p class="empty">No competitor extraction rows yet.</p>';
  return rows.map((row) => `
    <div class="news-item">
      <div class="news-title">${row.company}</div>
      <div class="news-meta">
        <span>Tech: ${row.technology ?? 'n/a'}</span>
        <span>Volume: ${row.annual_volume ?? 'n/a'}</span>
        <span>Price: ${row.price_signal ?? 'n/a'}</span>
      </div>
      <div class="news-summary">Source PDF: ${row.source_document}</div>
    </div>
  `).join('');
}

function renderDiscoveryRows(rows: CompetitorDiscoveryItem[]): string {
  if (!rows.length) return '<p class="empty">No online proposal discoveries yet.</p>';
  return rows.map((row) => `
    <div class="news-item">
      <a href="${row.url}" target="_blank" rel="noopener noreferrer" class="news-title">${row.title}</a>
      <div class="news-meta"><span>${row.source}</span><span>${row.published_at ?? ''}</span></div>
      <div class="news-summary">${row.summary ?? ''}</div>
    </div>
  `).join('');
}

export class CompetitorAnalysisPanel extends Panel {
  constructor() {
    super({ id: 'competitor-analysis', title: 'Competitor Analysis', showCount: true });
  }

  async refresh(): Promise<void> {
    this.showLoading();
    try {
      const [matrix, discovery] = await Promise.all([
        fetchCompetitorMatrix(),
        fetchCompetitorDiscovery(20),
      ]);

      this.setCount(matrix.length + discovery.length);
      this.setContent(`
        <div class="panel-actions" style="display:flex;justify-content:flex-end;margin-bottom:8px;">
          <button class="btn ai-discovery-refresh">Run AI discovery</button>
        </div>
        <h4>Extracted competitor matrix</h4>
        ${renderMatrixRows(matrix)}
        <h4 style="margin-top:12px;">Online project proposal discoveries</h4>
        ${renderDiscoveryRows(discovery)}
      `);

      const btn = this.getElement().querySelector('.ai-discovery-refresh') as HTMLButtonElement | null;
      btn?.addEventListener('click', () => {
        void this.refresh();
      });
    } catch (error) {
      console.error('[CompetitorAnalysisPanel] refresh failed', error);
      this.showError('Failed to load competitor analysis. Check backend/API configuration.');
    }
  }
}
