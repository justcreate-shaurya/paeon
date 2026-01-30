import { useState } from 'react';
import { Smartphone, Download, Loader2, CheckCircle2, AlertTriangle } from 'lucide-react';

interface LiveAssetPreviewProps {
  regulatoryGuardrails: boolean;
}

export function LiveAssetPreview({ regulatoryGuardrails }: LiveAssetPreviewProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [exportComplete, setExportComplete] = useState(false);

  const handleExport = () => {
    setIsExporting(true);
    setExportComplete(false);

    // Simulate export process
    setTimeout(() => {
      setIsExporting(false);
      setExportComplete(true);
      setTimeout(() => setExportComplete(false), 3000);
    }, 2000);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="font-medium text-[#2D2D2D] mb-1">Live Asset Preview</h2>
          <p className="text-xs text-gray-500">Patient education card</p>
        </div>
        <Smartphone className="w-4 h-4 text-gray-400" />
      </div>

      {/* Mobile Preview Frame */}
      <div className="flex-1 flex items-center justify-center mb-4">
        <div className="w-full max-w-[280px] bg-gradient-to-br from-gray-50 to-gray-100 rounded-[32px] p-3 shadow-xl">
          <div className="bg-white rounded-[24px] overflow-hidden shadow-inner">
            {/* Phone Notch */}
            <div className="h-6 bg-[#3B4D2B] flex items-center justify-center">
              <div className="w-20 h-3 bg-black/20 rounded-full"></div>
            </div>

            {/* Card Content */}
            <div className="p-4 space-y-3">
              {/* Header */}
              <div className="flex items-start gap-3">
                <div className="w-12 h-12 rounded-xl bg-[#3B4D2B]/10 flex items-center justify-center flex-shrink-0">
                  <span className="text-lg">💊</span>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-[#2D2D2D] text-sm">Metformin HCl</h3>
                  <p className="text-xs text-gray-500">500mg Tablet</p>
                </div>
              </div>

              {/* Usage */}
              <div className="bg-[#3B4D2B]/5 rounded-xl p-3">
                <div className="text-xs font-medium text-[#3B4D2B] mb-1">How to Take</div>
                <p className="text-xs text-[#2D2D2D] leading-relaxed">
                  Take with meals, twice daily. Swallow whole with water.
                </p>
              </div>

              {/* Benefits */}
              <div>
                <div className="text-xs font-medium text-[#2D2D2D] mb-2">Key Benefits</div>
                <ul className="space-y-1">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-3 h-3 text-[#606C38] mt-0.5 flex-shrink-0" />
                    <span className="text-xs text-[#2D2D2D]">Controls blood sugar</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-3 h-3 text-[#606C38] mt-0.5 flex-shrink-0" />
                    <span className="text-xs text-[#2D2D2D]">Reduces diabetes complications</span>
                  </li>
                </ul>
              </div>

              {/* Fair Balance Warning */}
              {regulatoryGuardrails && (
                <div className="bg-[#D4A574]/10 border border-[#D4A574] rounded-xl p-3">
                  <div className="flex items-start gap-2">
                    <AlertTriangle className="w-3 h-3 text-[#BC6C25] mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="text-xs font-medium text-[#BC6C25] mb-1">Important Safety Information</div>
                      <p className="text-xs text-[#2D2D2D] leading-relaxed">
                        May cause lactic acidosis. Avoid if kidney disease present. Report unusual muscle pain immediately.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Footer */}
              <div className="text-[10px] text-gray-400 text-center pt-2 border-t border-gray-100">
                Consult your healthcare provider
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Export Button */}
      <button
        onClick={handleExport}
        disabled={isExporting}
        className={`
          w-full h-11 rounded-xl font-medium text-sm
          transition-all duration-200 shadow-sm
          ${isExporting
            ? 'bg-gray-100 text-gray-400 cursor-wait'
            : exportComplete
            ? 'bg-[#606C38] text-white'
            : 'bg-[#3B4D2B] text-white hover:bg-[#2D3D1F]'
          }
        `}
      >
        {isExporting ? (
          <span className="flex items-center justify-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Formatting & Safety-Checking...</span>
          </span>
        ) : exportComplete ? (
          <span className="flex items-center justify-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            <span>Export Complete!</span>
          </span>
        ) : (
          <span className="flex items-center justify-center gap-2">
            <Download className="w-4 h-4" />
            <span>Export as PDF/PNG</span>
          </span>
        )}
      </button>

      {exportComplete && (
        <div className="text-xs text-center text-gray-500 mt-2">
          Download ready • Compliance verified ✓
        </div>
      )}
    </div>
  );
}
