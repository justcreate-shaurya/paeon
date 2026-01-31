import { Shield, ShieldAlert } from 'lucide-react';

interface ClinicalHeaderProps {
  regulatoryGuardrails: boolean;
  onToggle: (value: boolean) => void;
}

export function ClinicalHeader({ regulatoryGuardrails, onToggle }: ClinicalHeaderProps) {
  return (
    <header className="h-16 border-b border-gray-200 px-6 flex items-center justify-between bg-white">
      <div>
        <h1 className="font-medium text-[#2D2D2D]">PAEON AI</h1>
        <p className="text-xs text-gray-500">Digital Medical Representative Suite</p>
      </div>

      {/* Regulatory Guardrails Toggle */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          {regulatoryGuardrails ? (
            <Shield className="w-4 h-4 text-[#606C38]" />
          ) : (
            <ShieldAlert className="w-4 h-4 text-[#BC6C25]" />
          )}
          <span className="text-sm text-[#2D2D2D] font-medium">
            Regulatory Guardrails:
          </span>
        </div>
        
        <button
          onClick={() => onToggle(!regulatoryGuardrails)}
          className={`
            relative w-14 h-7 rounded-full transition-colors duration-200
            ${regulatoryGuardrails ? 'bg-[#3B4D2B]' : 'bg-gray-300'}
          `}
        >
          <div
            className={`
              absolute top-1 w-5 h-5 rounded-full bg-white shadow-md
              transition-transform duration-200
              ${regulatoryGuardrails ? 'translate-x-8' : 'translate-x-1'}
            `}
          />
        </button>
        
        <span className={`
          text-sm font-medium px-2 py-1 rounded-md
          ${regulatoryGuardrails 
            ? 'bg-[#3B4D2B]/10 text-[#3B4D2B]' 
            : 'bg-[#BC6C25]/10 text-[#BC6C25]'
          }
        `}>
          {regulatoryGuardrails ? 'ON' : 'OFF'}
        </span>
      </div>
    </header>
  );
}