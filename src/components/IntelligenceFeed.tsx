import { AlertTriangle, CheckCircle2, FileText, ExternalLink } from 'lucide-react';

interface IntelligenceFeedProps {
  onSourceClick: (source: any) => void;
}

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
  }
];

export function IntelligenceFeed({ onSourceClick }: IntelligenceFeedProps) {
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

  return (
    <div className="flex flex-col h-full">
      <div className="mb-4">
        <h2 className="font-medium text-[#2D2D2D] mb-1">Intelligence Feed</h2>
        <p className="text-xs text-gray-500">RAG-sourced drug updates & recalls</p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3">
        {feedItems.map((item) => (
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
                  <div className="text-xs font-medium text-[#3B4D2B]">{item.drug}</div>
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
            <p className="text-sm text-[#2D2D2D] mb-3 leading-relaxed">{item.content}</p>

            {/* Footer */}
            <div className="flex items-center justify-between pt-3 border-t border-current/10">
              <button
                onClick={() => onSourceClick(item)}
                className="flex items-center gap-1 text-xs text-[#606C38] hover:text-[#3B4D2B] font-medium transition-colors"
              >
                <ExternalLink className="w-3 h-3" />
                View Source: {item.source}
              </button>
              
              <span className="text-xs text-gray-500">{item.date}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
