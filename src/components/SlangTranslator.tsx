import { useState } from 'react';
import { Send, CheckCircle, Edit3, ArrowRight, Globe, Loader2 } from 'lucide-react';
import { useTranslationStore } from '../lib/store';

interface SlangTranslatorProps {
  regulatoryGuardrails: boolean;
}

export function SlangTranslator({ regulatoryGuardrails }: SlangTranslatorProps) {
  const [input, setInput] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  
  const { 
    translations, 
    isLoading, 
    error, 
    translate, 
    approveFeedback,
    editTranslation 
  } = useTranslationStore();

  const [demoTranslations] = useState<any[]>([
    {
      id: 'demo-1',
      raw_input: "I feel like my chest is tight and fluttery",
      original_language: "English",
      clinical_interpretation: "Palpitations with Chest Tightness",
      confidence: 0.94,
      standard_codes: [
        { system: 'SNOMED-CT', code: '80313002', display: 'Palpitations' },
        { system: 'ICD-10', code: 'R00.2', display: 'Palpitations' }
      ],
      rationale: "Patient describes cardiac sensation with chest constriction"
    },
    {
      id: 'demo-2',
      raw_input: "My head be pounding real bad",
      original_language: "English (Vernacular)",
      clinical_interpretation: "Severe Headache / Migraine",
      confidence: 0.87,
      standard_codes: [
        { system: 'SNOMED-CT', code: '25064002', display: 'Headache' },
        { system: 'ICD-10', code: 'R51.9', display: 'Unspecified Headache' }
      ],
      rationale: "Patient reports intense cranial pain"
    },
    {
      id: 'demo-3',
      raw_input: "I can't catch my breath, bro",
      original_language: "English (Slang)",
      clinical_interpretation: "Dyspnea / Shortness of Breath",
      confidence: 0.91,
      standard_codes: [
        { system: 'SNOMED-CT', code: '13398005', display: 'Dyspnea' },
        { system: 'ICD-10', code: 'R06.02', display: 'Shortness of breath' }
      ],
      rationale: "Patient experiencing respiratory difficulty"
    },
    {
      id: 'demo-4',
      raw_input: "My belly's been acting up all week",
      original_language: "English (Colloquial)",
      clinical_interpretation: "Gastrointestinal Distress / Abdominal Discomfort",
      confidence: 0.85,
      standard_codes: [
        { system: 'SNOMED-CT', code: '21522001', display: 'Abdominal pain' },
        { system: 'ICD-10', code: 'R10.9', display: 'Unspecified abdominal pain' }
      ],
      rationale: "Patient reports persistent GI symptoms"
    }
  ]);

  const handleSubmit = async () => {
    if (!input.trim() || isLoading) return;
    
    try {
      await translate(input);
      setInput('');
    } catch (err) {
      console.error('Translation failed:', err);
    }
  };

  const handleApprove = (id: string) => {
    approveFeedback(id);
  };

  const handleEdit = (id: string, currentValue: string) => {
    setEditingId(id);
    setEditValue(currentValue);
  };

  const handleSaveEdit = (id: string) => {
    if (editValue.trim()) {
      editTranslation(id, editValue);
    }
    setEditingId(null);
    setEditValue('');
  };

  const allTranslations = translations.length > 0 ? translations : demoTranslations;

  return (
    <div className="flex flex-col h-full">
      <div className="mb-4">
        <h2 className="font-medium text-[#2D2D2D] mb-1">Slang-to-Clinical</h2>
        <p className="text-xs text-gray-500">Patient language interpreter • 20+ languages</p>
      </div>

      {error && (
        <div className="mb-3 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
          {error}
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {allTranslations.map((translation: any, idx: number) => (
          <div
            key={translation.id || idx}
            className="bg-white border border-[#E65E07]/20 rounded-xl p-4 shadow-sm"
          >
            <div className="mb-3">
              <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
                <Globe className="w-3 h-3" />
                <span>Patient Input ({translation.original_language})</span>
              </div>
              <div className="text-sm text-[#2D2D2D] italic">"{translation.raw_input}"</div>
            </div>

            <div className="flex items-center justify-center my-2">
              <ArrowRight className="w-4 h-4 text-[#E65E07]" />
            </div>

            <div className="mb-3">
              <div className="text-xs text-gray-500 mb-1">AI Translation</div>
              {editingId === translation.id ? (
                <input
                  type="text"
                  value={editValue}
                  onChange={(e) => setEditValue(e.target.value)}
                  onBlur={() => handleSaveEdit(translation.id)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSaveEdit(translation.id)}
                  className="w-full px-2 py-1 text-sm font-medium text-[#E65E07] border border-[#E65E07] rounded focus:outline-none"
                  autoFocus
                />
              ) : (
                <div className="text-sm font-medium text-[#E65E07]">
                  {translation.clinical_interpretation}
                </div>
              )}
              
              {translation.standard_codes && translation.standard_codes.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {translation.standard_codes.map((code: any, codeIdx: number) => (
                    <span 
                      key={codeIdx}
                      className="px-2 py-0.5 bg-[#E65E07]/10 text-[#E65E07] text-xs rounded-full"
                    >
                      {code.system}: {code.code}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-gray-100">
              <div className="flex items-center gap-2">
                <div className="text-xs text-gray-500">Confidence:</div>
                <div className={`text-xs font-medium ${
                  (translation.confidence * 100) >= 85 ? 'text-[#E65E07]' : 
                  (translation.confidence * 100) >= 70 ? 'text-[#D4A574]' : 'text-[#BC6C25]'
                }`}>
                  {Math.round(translation.confidence * 100)}%
                </div>
              </div>
              
              <div className="flex gap-2">
                <button 
                  onClick={() => handleApprove(translation.id)}
                  className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Approve translation"
                >
                  <CheckCircle className={`w-4 h-4 ${
                    (translation as any).approved ? 'text-[#E65E07]' : 'text-gray-400'
                  }`} />
                </button>
                <button 
                  onClick={() => handleEdit(translation.id, translation.clinical_interpretation)}
                  className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Edit translation"
                >
                  <Edit3 className={`w-4 h-4 ${
                    (translation as any).edited ? 'text-[#E65E07]' : 'text-gray-400'
                  }`} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit();
            }
          }}
          placeholder="Enter patient description in any language..."
          className="w-full h-24 px-4 py-3 pr-12 rounded-xl border border-gray-200 focus:border-[#E65E07] focus:outline-none resize-none text-sm"
          disabled={isLoading}
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading || !input.trim()}
          className="absolute bottom-3 right-3 w-8 h-8 rounded-lg bg-[#E65E07] text-white flex items-center justify-center hover:bg-[#B84B06] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </div>
      
      {regulatoryGuardrails && (
        <p className="text-[10px] text-gray-400 mt-2 text-center">
          For HCP use only. Not a diagnostic tool.
        </p>
      )}
    </div>
  );
}
