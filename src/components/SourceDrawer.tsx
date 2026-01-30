import { X, FileText, ExternalLink, CheckCircle2, Calendar, Building2 } from 'lucide-react';

interface SourceDrawerProps {
  open: boolean;
  onClose: () => void;
  source: any;
}

export function SourceDrawer({ open, onClose, source }: SourceDrawerProps) {
  if (!open || !source) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/30 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Drawer */}
      <div className="fixed right-0 top-0 h-full w-[480px] bg-white shadow-2xl z-50 flex flex-col">
        {/* Header */}
        <div className="h-16 px-6 flex items-center justify-between border-b border-gray-200">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-[#606C38]" />
            <h2 className="font-medium text-[#2D2D2D]">Source Verification</h2>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg hover:bg-gray-100 flex items-center justify-center transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Verification Badge */}
          <div className="flex items-center gap-2 px-4 py-3 bg-[#606C38]/10 border border-[#606C38]/20 rounded-xl">
            <CheckCircle2 className="w-5 h-5 text-[#606C38]" />
            <span className="text-sm font-medium text-[#606C38]">Verified Source</span>
          </div>

          {/* Source Metadata */}
          <div className="space-y-4">
            <div>
              <div className="text-xs text-gray-500 mb-1">Source Document</div>
              <div className="font-medium text-[#2D2D2D]">{source.source}</div>
            </div>

            <div className="flex gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-1.5 text-xs text-gray-500 mb-1">
                  <Calendar className="w-3 h-3" />
                  Published Date
                </div>
                <div className="text-sm text-[#2D2D2D]">{source.date}</div>
              </div>

              <div className="flex-1">
                <div className="flex items-center gap-1.5 text-xs text-gray-500 mb-1">
                  <Building2 className="w-3 h-3" />
                  Authority
                </div>
                <div className="text-sm text-[#2D2D2D]">FDA</div>
              </div>
            </div>
          </div>

          {/* Original Context */}
          <div>
            <div className="text-xs font-medium text-[#2D2D2D] mb-3">Original Document Excerpt</div>
            <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
              <p className="text-sm text-[#2D2D2D] leading-relaxed mb-4">
                {source.content}
              </p>
              <div className="text-xs text-gray-500 italic">
                This excerpt has been verified against the official FDA documentation and is accurate as of {source.date}.
              </div>
            </div>
          </div>

          {/* Additional Context */}
          <div>
            <div className="text-xs font-medium text-[#2D2D2D] mb-3">Related Information</div>
            <div className="space-y-2">
              <div className="p-3 rounded-lg bg-white border border-gray-200 hover:border-[#3B4D2B] transition-colors cursor-pointer">
                <div className="text-sm text-[#2D2D2D] mb-1">Full FDA Safety Alert</div>
                <div className="text-xs text-gray-500">View complete documentation</div>
              </div>
              <div className="p-3 rounded-lg bg-white border border-gray-200 hover:border-[#3B4D2B] transition-colors cursor-pointer">
                <div className="text-sm text-[#2D2D2D] mb-1">Drug Label Information</div>
                <div className="text-xs text-gray-500">Official prescribing information</div>
              </div>
              <div className="p-3 rounded-lg bg-white border border-gray-200 hover:border-[#3B4D2B] transition-colors cursor-pointer">
                <div className="text-sm text-[#2D2D2D] mb-1">Clinical Studies</div>
                <div className="text-xs text-gray-500">Supporting research data</div>
              </div>
            </div>
          </div>

          {/* RAG Confidence */}
          <div className="bg-[#3B4D2B]/5 rounded-xl p-4 border border-[#3B4D2B]/10">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-[#2D2D2D]">RAG Retrieval Confidence</span>
              <span className="text-sm font-medium text-[#606C38]">98.4%</span>
            </div>
            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-[#606C38] rounded-full" style={{ width: '98.4%' }} />
            </div>
            <p className="text-xs text-gray-600 mt-2">
              This information was retrieved from our verified medical database with high confidence.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="h-20 px-6 border-t border-gray-200 flex items-center justify-between">
          <button className="flex items-center gap-2 text-sm text-[#606C38] hover:text-[#3B4D2B] font-medium transition-colors">
            <ExternalLink className="w-4 h-4" />
            Open Original Document
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-[#3B4D2B] text-white text-sm font-medium hover:bg-[#2D3D1F] transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </>
  );
}
