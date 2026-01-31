<<<<<<< HEAD
import { useEffect, useState } from 'react';
import { AlertTriangle, CheckCircle2, FileText, ExternalLink, Search, Loader2, RefreshCw } from 'lucide-react';
import { useIntelligenceStore } from '../lib/store';
import { ragApi, IntelFeedItem } from '../lib/api';
=======
import { AlertTriangle, CheckCircle2, FileText, ExternalLink } from 'lucide-react';
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

interface IntelligenceFeedProps {
  onSourceClick: (source: any) => void;
}

<<<<<<< HEAD
// Demo data for offline/development mode
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
    title: 'Safety Communication',
    drug_name: 'Eliquis (apixaban)',
    summary: 'Updated black box warning regarding increased bleeding risk when used concomitantly with antiplatelet agents.',
    source: 'FDA Safety Alerts',
    source_url: 'https://www.fda.gov/drugs/drug-safety-and-availability',
    published_at: '2026-01-25T09:15:00Z',
    severity: 'medium',
    verified: true,
    relevance_score: 0.92
  },
  {
    id: '4',
    type: 'clinical_trial',
    title: 'Clinical Trial Results',
    drug_name: 'Keytruda (pembrolizumab)',
    summary: 'Phase III trial demonstrates significant improvement in progression-free survival for early-stage triple-negative breast cancer.',
    source: 'NEJM Journal',
    source_url: 'https://www.nejm.org',
    published_at: '2026-01-24T16:00:00Z',
    severity: 'info',
    verified: true,
    relevance_score: 0.85
=======
const feedItems = [
  {
    id: 1,
    type: 'recall',
    title: 'FDA Drug Recall Alert',
    drug: 'Metformin HCl 500mg',
    content: 'Voluntary recall due to NDMA contamination detected above acceptable daily intake levels.',
    source: 'FDA MedWatch',
    date: '2026-01-28',
    severity: 'high',
    verified: true
  },
  {
    id: 2,
    type: 'update',
    title: 'New Indication Approved',
    drug: 'Ozempic (semaglutide)',
    content: 'FDA approves expanded use for cardiovascular risk reduction in adults with type 2 diabetes and established cardiovascular disease.',
    source: 'FDA Drug Approvals',
    date: '2026-01-27',
    severity: 'info',
    verified: true
  },
  {
    id: 3,
    type: 'safety',
    title: 'Safety Communication',
    drug: 'Eliquis (apixaban)',
    content: 'Updated black box warning regarding increased bleeding risk when used concomitantly with antiplatelet agents.',
    source: 'FDA Safety Alerts',
    date: '2026-01-25',
    severity: 'medium',
    verified: true
  },
  {
    id: 4,
    type: 'update',
    title: 'Clinical Trial Results',
    drug: 'Keytruda (pembrolizumab)',
    content: 'Phase III trial demonstrates significant improvement in progression-free survival for early-stage triple-negative breast cancer.',
    source: 'NEJM Journal',
    date: '2026-01-24',
    severity: 'info',
    verified: true
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
  }
];

export function IntelligenceFeed({ onSourceClick }: IntelligenceFeedProps) {
<<<<<<< HEAD
  const { feedItems, isLoading, error, setFeedItems, setLoading, setError } = useIntelligenceStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  // Initialize with demo data and attempt API fetch
  useEffect(() => {
    const fetchFeed = async () => {
      setLoading(true);
      try {
        const response = await ragApi.getFeed();
        if (response.items && response.items.length > 0) {
          setFeedItems(response.items);
        } else {
          // Use demo data if API returns empty
          setFeedItems(demoFeedItems);
        }
      } catch (err) {
        // Use demo data on error (development mode)
        console.log('Using demo intelligence feed data');
        setFeedItems(demoFeedItems);
      } finally {
        setLoading(false);
      }
    };

    fetchFeed();
  }, [setFeedItems, setLoading, setError]);

  // Search handler
  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    try {
      const results = await ragApi.search({
        query: searchQuery,
        limit: 10,
        include_sources: ['fda', 'dailymed', 'pubmed']
      });
      
      // Convert search results to feed items format
      const searchItems: IntelFeedItem[] = results.results.map((r, idx) => ({
        id: `search-${idx}`,
        type: 'search_result' as any,
        title: r.title,
        drug_name: r.drug_name || 'N/A',
        summary: r.content,
        source: r.source,
        source_url: r.url || '#',
        published_at: new Date().toISOString(),
        severity: 'info',
        verified: r.confidence > 0.8,
        relevance_score: r.confidence
      }));
      
      setFeedItems(searchItems.length > 0 ? searchItems : demoFeedItems);
    } catch (err) {
      console.log('Search failed, keeping current feed');
    } finally {
      setIsSearching(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    try {
      const response = await ragApi.getFeed();
      setFeedItems(response.items.length > 0 ? response.items : demoFeedItems);
    } catch (err) {
      setFeedItems(demoFeedItems);
    } finally {
      setLoading(false);
    }
  };

  // Format date for display
  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return dateStr;
    }
  };
=======
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'border-[#BC6C25] bg-[#BC6C25]/5';
      case 'medium':
        return 'border-[#D4A574] bg-[#D4A574]/5';
      default:
        return 'border-[#3B4D2B] bg-[#3B4D2B]/5';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-[#BC6C25]" />;
      case 'medium':
        return <AlertTriangle className="w-4 h-4 text-[#D4A574]" />;
      default:
        return <FileText className="w-4 h-4 text-[#606C38]" />;
    }
  };

<<<<<<< HEAD
  const displayItems = feedItems.length > 0 ? feedItems : demoFeedItems;

  return (
    <div className="flex flex-col h-full">
      <div className="mb-4">
        <div className="flex items-center justify-between mb-1">
          <h2 className="font-medium text-[#2D2D2D]">Intelligence Feed</h2>
          <button
            onClick={handleRefresh}
            disabled={isLoading}
            className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50"
            title="Refresh feed"
          >
            <RefreshCw className={`w-4 h-4 text-gray-500 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
        <p className="text-xs text-gray-500">RAG-sourced drug updates & recalls</p>
      </div>

      {/* Search Bar */}
      <div className="relative mb-4">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Search drug intelligence..."
          className="w-full pl-9 pr-4 py-2 text-sm rounded-xl border border-gray-200 focus:border-[#3B4D2B] focus:outline-none"
        />
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        {isSearching && (
          <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#606C38] animate-spin" />
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-3 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
          {error}
        </div>
      )}

      {/* Loading State */}
      {isLoading && feedItems.length === 0 && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="w-8 h-8 text-[#606C38] animate-spin mx-auto mb-2" />
            <p className="text-sm text-gray-500">Loading intelligence feed...</p>
          </div>
        </div>
      )}

      {/* Feed Items */}
      <div className="flex-1 overflow-y-auto space-y-3">
        {displayItems.map((item) => (
=======
  return (
    <div className="flex flex-col h-full">
      <div className="mb-4">
        <h2 className="font-medium text-[#2D2D2D] mb-1">Intelligence Feed</h2>
        <p className="text-xs text-gray-500">RAG-sourced drug updates & recalls</p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3">
        {feedItems.map((item) => (
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
          <div
            key={item.id}
            className={`rounded-xl border-2 p-4 shadow-sm transition-all hover:shadow-md ${getSeverityColor(item.severity)}`}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-start gap-2 flex-1">
                <div className="mt-0.5">{getSeverityIcon(item.severity)}</div>
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-[#2D2D2D] mb-1">{item.title}</h3>
<<<<<<< HEAD
                  <div className="text-xs font-medium text-[#3B4D2B]">{item.drug_name}</div>
=======
                  <div className="text-xs font-medium text-[#3B4D2B]">{item.drug}</div>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
                </div>
              </div>
              
              {item.verified && (
                <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-[#606C38]/10 text-[#606C38]">
                  <CheckCircle2 className="w-3 h-3" />
                  <span className="text-xs font-medium">Verified</span>
                </div>
              )}
            </div>

            {/* Content */}
<<<<<<< HEAD
            <p className="text-sm text-[#2D2D2D] mb-3 leading-relaxed">{item.summary}</p>

            {/* Relevance Score */}
            {item.relevance_score && (
              <div className="flex items-center gap-2 mb-3">
                <div className="text-xs text-gray-500">Relevance:</div>
                <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-[#606C38] rounded-full"
                    style={{ width: `${item.relevance_score * 100}%` }}
                  />
                </div>
                <div className="text-xs text-[#606C38] font-medium">
                  {Math.round(item.relevance_score * 100)}%
                </div>
              </div>
            )}
=======
            <p className="text-sm text-[#2D2D2D] mb-3 leading-relaxed">{item.content}</p>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

            {/* Footer */}
            <div className="flex items-center justify-between pt-3 border-t border-current/10">
              <button
<<<<<<< HEAD
                onClick={() => onSourceClick({
                  ...item,
                  url: item.source_url,
                  content: item.summary
                })}
=======
                onClick={() => onSourceClick(item)}
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
                className="flex items-center gap-1 text-xs text-[#606C38] hover:text-[#3B4D2B] font-medium transition-colors"
              >
                <ExternalLink className="w-3 h-3" />
                View Source: {item.source}
              </button>
              
<<<<<<< HEAD
              <span className="text-xs text-gray-500">{formatDate(item.published_at)}</span>
=======
              <span className="text-xs text-gray-500">{item.date}</span>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
