import { useState } from 'react';
<<<<<<< HEAD
import { Send, CheckCircle, Edit3, ArrowRight, Globe, Loader2 } from 'lucide-react';
import { useTranslationStore } from '../lib/store';
=======
import { Send, CheckCircle, Edit3, ArrowRight } from 'lucide-react';
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

interface SlangTranslatorProps {
  regulatoryGuardrails: boolean;
}

<<<<<<< HEAD
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

  // Demo translations for initial state
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
    }
  ]);

  const handleSubmit = async () => {
    if (!input.trim() || isLoading) return;
    
    try {
      await translate(input);
      setInput('');
    } catch (err) {
      // Error is handled in store
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

  // Combine real translations with demo data
  const allTranslations = translations.length > 0 ? translations : demoTranslations;

=======
interface Translation {
  input: string;
  clinical: string;
  confidence: number;
}

export function SlangTranslator({ regulatoryGuardrails }: SlangTranslatorProps) {
  const [input, setInput] = useState('');
  const [translations, setTranslations] = useState<Translation[]>([
    {
      input: "I feel like my chest is tight and fluttery",
      clinical: "Potential Tachycardia / Chest Constriction",
      confidence: 94
    }
  ]);

  const handleSubmit = () => {
    if (!input.trim()) return;
    
    // Mock translation
    const mockTranslations = [
      "Suspected Cardiac Arrhythmia",
      "Possible Anxiety-Induced Palpitations",
      "Dyspnea with Tachycardia Symptoms"
    ];
    
    setTranslations([
      {
        input: input,
        clinical: mockTranslations[Math.floor(Math.random() * mockTranslations.length)],
        confidence: Math.floor(Math.random() * 20) + 80
      },
      ...translations
    ]);
    setInput('');
  };

>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
  return (
    <div className="flex flex-col h-full">
      <div className="mb-4">
        <h2 className="font-medium text-[#2D2D2D] mb-1">Slang-to-Clinical</h2>
<<<<<<< HEAD
        <p className="text-xs text-gray-500">Patient language interpreter • 20+ languages</p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-3 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
          {error}
        </div>
      )}

      {/* Translation History */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {allTranslations.map((translation: any, idx: number) => (
          <div
            key={translation.id || idx}
=======
        <p className="text-xs text-gray-500">Patient language interpreter</p>
      </div>

      {/* Translation History */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {translations.map((translation, idx) => (
          <div
            key={idx}
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
            className="bg-white border border-[#3B4D2B]/20 rounded-xl p-4 shadow-sm"
          >
            {/* Patient Input */}
            <div className="mb-3">
<<<<<<< HEAD
              <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
                <Globe className="w-3 h-3" />
                <span>Patient Input ({translation.original_language})</span>
              </div>
              <div className="text-sm text-[#2D2D2D] italic">"{translation.raw_input}"</div>
=======
              <div className="text-xs text-gray-500 mb-1">Patient Input</div>
              <div className="text-sm text-[#2D2D2D] italic">"{translation.input}"</div>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
            </div>

            <div className="flex items-center justify-center my-2">
              <ArrowRight className="w-4 h-4 text-[#606C38]" />
            </div>

            {/* Clinical Translation */}
            <div className="mb-3">
              <div className="text-xs text-gray-500 mb-1">AI Translation</div>
<<<<<<< HEAD
              {editingId === translation.id ? (
                <input
                  type="text"
                  value={editValue}
                  onChange={(e) => setEditValue(e.target.value)}
                  onBlur={() => handleSaveEdit(translation.id)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSaveEdit(translation.id)}
                  className="w-full px-2 py-1 text-sm font-medium text-[#3B4D2B] border border-[#606C38] rounded focus:outline-none"
                  autoFocus
                />
              ) : (
                <div className="text-sm font-medium text-[#3B4D2B]">
                  {translation.clinical_interpretation}
                </div>
              )}
              
              {/* Standard Codes */}
              {translation.standard_codes && translation.standard_codes.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {translation.standard_codes.map((code: any, codeIdx: number) => (
                    <span 
                      key={codeIdx}
                      className="px-2 py-0.5 bg-[#606C38]/10 text-[#606C38] text-xs rounded-full"
                    >
                      {code.system}: {code.code}
                    </span>
                  ))}
                </div>
              )}
=======
              <div className="text-sm font-medium text-[#3B4D2B]">{translation.clinical}</div>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
            </div>

            {/* Confidence & Actions */}
            <div className="flex items-center justify-between pt-3 border-t border-gray-100">
              <div className="flex items-center gap-2">
                <div className="text-xs text-gray-500">Confidence:</div>
<<<<<<< HEAD
                <div className={`text-xs font-medium ${
                  (translation.confidence * 100) >= 85 ? 'text-[#606C38]' : 
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
                    (translation as any).approved ? 'text-[#606C38]' : 'text-gray-400'
                  }`} />
                </button>
                <button 
                  onClick={() => handleEdit(translation.id, translation.clinical_interpretation)}
                  className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Edit translation"
                >
                  <Edit3 className={`w-4 h-4 ${
                    (translation as any).edited ? 'text-[#606C38]' : 'text-gray-400'
                  }`} />
=======
                <div className="text-xs font-medium text-[#606C38]">{translation.confidence}%</div>
              </div>
              
              <div className="flex gap-2">
                <button className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
                  <CheckCircle className="w-4 h-4 text-[#606C38]" />
                </button>
                <button className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
                  <Edit3 className="w-4 h-4 text-gray-400" />
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
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
<<<<<<< HEAD
          placeholder="Enter patient description in any language..."
          className="w-full h-24 px-4 py-3 pr-12 rounded-xl border border-gray-200 focus:border-[#3B4D2B] focus:outline-none resize-none text-sm"
          disabled={isLoading}
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading || !input.trim()}
          className="absolute bottom-3 right-3 w-8 h-8 rounded-lg bg-[#3B4D2B] text-white flex items-center justify-center hover:bg-[#2D3D1F] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </div>
      
      {/* Disclaimer */}
      {regulatoryGuardrails && (
        <p className="text-[10px] text-gray-400 mt-2 text-center">
          For HCP use only. Not a diagnostic tool.
        </p>
      )}
=======
          placeholder="Enter patient description..."
          className="w-full h-24 px-4 py-3 pr-12 rounded-xl border border-gray-200 focus:border-[#3B4D2B] focus:outline-none resize-none text-sm"
        />
        <button
          onClick={handleSubmit}
          className="absolute bottom-3 right-3 w-8 h-8 rounded-lg bg-[#3B4D2B] text-white flex items-center justify-center hover:bg-[#2D3D1F] transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
    </div>
  );
}
