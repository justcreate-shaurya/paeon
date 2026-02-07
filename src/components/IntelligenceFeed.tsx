import { useEffect, useState } from 'react';
import { CheckCircle2, ExternalLink, Loader2, RefreshCw } from 'lucide-react';
import { useIntelligenceStore } from '../lib/store';
import { ragApi, IntelFeedItem } from '../lib/api';

interface IntelligenceFeedProps {
  onSourceClick: (source: any) => void;
}

const demoFeedItems: IntelFeedItem[] = [
  {
    id: '1',
    type: 'recall',
    title: 'FDA Drug Recall Alert',
    drug_name: 'Metformin HCl 500mg',
    summary: 'Voluntary recall due to NDMA contamination detected above acceptable daily intake levels.',
    source: 'FDA MedWatch',
    source_url: 'https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts',
    published_at: '2026-01-28T10:00:00Z',
    severity: 'high',
    verified: true,
    relevance_score: 0.95
  },
  {
    id: '2',
    type: 'approval',
    title: 'New Indication Approved',
    drug_name: 'Ozempic (semaglutide)',
    summary: 'FDA approves expanded use for cardiovascular risk reduction in adults with type 2 diabetes and established cardiovascular disease.',
    source: 'FDA Drug Approvals',
    source_url: 'https://www.fda.gov/drugs/drug-approvals-and-databases',
    published_at: '2026-01-27T14:30:00Z',
    severity: 'info',
    verified: true,
    relevance_score: 0.88
  },
  {
    id: '3',
    type: 'safety',
    title: 'Safety Communication: Black Box Warning Update',
    drug_name: 'Eliquis (apixaban)',
    summary: 'Updated black box warning regarding increased bleeding risk when used concomitantly with antiplatelet agents. New dosage guidance provided.',
    source: 'FDA Safety Alerts',
    source_url: 'https://www.fda.gov/drugs/drug-safety-and-availability',
    published_at: '2026-01-25T09:15:00Z',
    severity: 'high',
    verified: true,
    relevance_score: 0.92
  },
  {
    id: '4',
    type: 'approval',
    title: 'Phase III Trial Results Published',
    drug_name: 'Keytruda (pembrolizumab)',
    summary: 'Clinical trial demonstrates significant improvement in progression-free survival for early-stage triple-negative breast cancer patients.',
    source: 'NEJM Journal',
    source_url: 'https://www.nejm.org',
    published_at: '2026-01-24T11:20:00Z',
    severity: 'info',
    verified: true,
    relevance_score: 0.85
  },
  {
    id: '5',
    type: 'safety',
    title: 'Monitoring Alert: QT Prolongation Risk',
    drug_name: 'Lipitor (atorvastatin)',
    summary: 'New safety data suggests potential for QT interval prolongation in patients with baseline QTc >480ms. Enhanced monitoring recommended.',
    source: 'Cardiology Today',
    source_url: 'https://www.cardiologytoday.com',
    published_at: '2026-01-22T15:45:00Z',
    severity: 'medium',
    verified: true,
    relevance_score: 0.78
  },
  {
    id: '6',
    type: 'recall',
    title: 'Manufacturing Issue Identified',
    drug_name: 'Lisinopril 10mg',
    summary: 'Precautionary recall due to potential manufacturing defect affecting tablet strength. All affected batches identified and being replaced.',
    source: 'FDA MedWatch',
    source_url: 'https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts',
    published_at: '2026-01-20T08:30:00Z',
    severity: 'medium',
    verified: true,
    relevance_score: 0.81
  }
];

export function IntelligenceFeed({ onSourceClick }: IntelligenceFeedProps) {
  const { feedItems, isLoading, setFeedItems, setLoading } = useIntelligenceStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    const fetchFeed = async () => {
      setLoading(true);
      try {
        const response = await ragApi.getFeed();
        if (response && Array.isArray(response.items) && response.items.length > 0) {
          setFeedItems(response.items);
        } else {
          setFeedItems(demoFeedItems);
        }
      } catch (err) {
        setFeedItems(demoFeedItems);
      } finally {
        setLoading(false);
      }
    };

    fetchFeed();
  }, [setFeedItems, setLoading]);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const results = await ragApi.search({ query: searchQuery, limit: 10 });
      const items: IntelFeedItem[] = (results?.results || []).map((r: any, idx: number) => ({
        id: `search-${idx}`,
        type: 'search_result' as any,
        title: r.title || r.content?.slice(0, 60) || 'Result',
        drug_name: r.drug_name || 'N/A',
        summary: r.content || '',
        source: r.source || 'Unknown',
        source_url: r.url || '#',
        published_at: new Date().toISOString(),
        severity: 'info',
        verified: (r.confidence || 0) > 0.8,
        relevance_score: r.confidence || 0
      }));

      setFeedItems(items.length > 0 ? items : demoFeedItems);
    } catch (err) {
      // keep current feed
    } finally {
      setIsSearching(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    try {
      const response = await ragApi.getFeed();
      setFeedItems(response?.items?.length ? response.items : demoFeedItems);
    } catch (err) {
      setFeedItems(demoFeedItems);
    } finally {
      setLoading(false);
    }
  };

  const display = feedItems && feedItems.length > 0 ? feedItems : demoFeedItems;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-[#2D2D2D]">Intelligence Feed</h3>
        <div className="flex items-center gap-2">
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search feed..."
            className="px-3 py-1 rounded-lg border border-gray-200 text-sm"
          />
          <button onClick={handleSearch} className="px-2 py-1 text-sm rounded bg-[#E65E07] text-white hover:bg-[#B84B06]">
            Search
          </button>
          <button onClick={handleRefresh} className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors" title="Refresh feed">
            <RefreshCw className={`w-4 h-4 text-gray-500 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="animate-spin w-6 h-6 text-[#E65E07]" />
        </div>
      ) : (
        <div className="space-y-2 max-h-[600px] overflow-y-auto pr-2 scroll-smooth">
          {display.map((item) => (
            <div key={item.id} className="p-3 bg-white border rounded-lg shadow-sm flex items-start gap-3">
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-semibold text-[#2D2D2D]">{item.title}</div>
                  <div className="text-xs text-gray-500">{new Date(item.published_at || Date.now()).toLocaleDateString()}</div>
                </div>
                <div className="text-xs text-gray-600 mt-1">{item.summary}</div>
                <div className="mt-2 flex items-center justify-between">
                  <button onClick={() => onSourceClick(item.source)} className="text-xs text-gray-500 hover:text-[#E65E07]">{item.source}</button>
                  <div className="flex items-center gap-2">
                    {item.verified && <CheckCircle2 className="w-4 h-4 text-green-500" />}
                  </div>
                </div>
              </div>
              <div className="flex flex-col items-end gap-2">
                <a href={item.source_url} target="_blank" rel="noreferrer" className="text-gray-400">
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
