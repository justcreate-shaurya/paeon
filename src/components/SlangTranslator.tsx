import { useState } from 'react';
import { Send, CheckCircle, Edit3, ArrowRight } from 'lucide-react';

interface SlangTranslatorProps {
  regulatoryGuardrails: boolean;
}

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

  return (
    <div className="flex flex-col h-full">
      <div className="mb-4">
        <h2 className="font-medium text-[#2D2D2D] mb-1">Slang-to-Clinical</h2>
        <p className="text-xs text-gray-500">Patient language interpreter</p>
      </div>

      {/* Translation History */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {translations.map((translation, idx) => (
          <div
            key={idx}
            className="bg-white border border-[#3B4D2B]/20 rounded-xl p-4 shadow-sm"
          >
            {/* Patient Input */}
            <div className="mb-3">
              <div className="text-xs text-gray-500 mb-1">Patient Input</div>
              <div className="text-sm text-[#2D2D2D] italic">"{translation.input}"</div>
            </div>

            <div className="flex items-center justify-center my-2">
              <ArrowRight className="w-4 h-4 text-[#606C38]" />
            </div>

            {/* Clinical Translation */}
            <div className="mb-3">
              <div className="text-xs text-gray-500 mb-1">AI Translation</div>
              <div className="text-sm font-medium text-[#3B4D2B]">{translation.clinical}</div>
            </div>

            {/* Confidence & Actions */}
            <div className="flex items-center justify-between pt-3 border-t border-gray-100">
              <div className="flex items-center gap-2">
                <div className="text-xs text-gray-500">Confidence:</div>
                <div className="text-xs font-medium text-[#606C38]">{translation.confidence}%</div>
              </div>
              
              <div className="flex gap-2">
                <button className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
                  <CheckCircle className="w-4 h-4 text-[#606C38]" />
                </button>
                <button className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
                  <Edit3 className="w-4 h-4 text-gray-400" />
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
    </div>
  );
}
