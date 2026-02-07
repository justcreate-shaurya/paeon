import { useState } from 'react';
import { Download, Loader2, Smartphone, FileDown } from 'lucide-react';
import { useAssetStore } from '../lib/store';

interface LiveAssetPreviewProps {
  regulatoryGuardrails?: boolean;
}

// Generate an SVG patient education card
const generatePatientCard = (drugName: string, drugs: string[] = [], diagnosis: string = ''): string => {
  const colors = {
    'Metformin': { bg: '#FFF5E6', accent: '#E65E07' },
    'Ozempic': { bg: '#E6F3FF', accent: '#0066CC' },
    'Eliquis': { bg: '#F0E6FF', accent: '#7722CC' },
    'Keytruda': { bg: '#E6F9F0', accent: '#008060' }
  };
  
  const primaryDrug = drugs.length > 0 ? drugs[0] : drugName;
  const theme = (colors as any)[primaryDrug] || { bg: '#FFF5E6', accent: '#E65E07' };
  
  // Generate varied content based on diagnosis
  const dosageMap: Record<string, string> = {
    'Type 2 Diabetes': 'Take 500-1000mg twice daily with meals',
    'Hypertension': 'Take 5-10mg daily, preferably in morning',
    'Bleeding Disorder': 'Take exactly as prescribed, usually twice daily',
    'Cancer': 'Take as part of infusion regimen every 3 weeks',
    'High Cholesterol': 'Take 10-80mg once daily in evening'
  };
  
  const sideEffectsMap: Record<string, string[]> = {
    'Type 2 Diabetes': ['Nausea (usually temporary)', 'Stomach upset', 'Diarrhea', 'Metallic taste'],
    'Hypertension': ['Dizziness', 'Fatigue', 'Cough', 'Headache'],
    'Bleeding Disorder': ['Easy bruising', 'Nosebleeds', 'Gum bleeding'],
    'Cancer': ['Fatigue', 'Fever', 'Skin reactions', 'Immune system effects'],
    'High Cholesterol': ['Muscle pain', 'Elevated liver enzymes', 'Memory issues']
  };
  
  const warningsMap: Record<string, string[]> = {
    'Type 2 Diabetes': ['May cause lactic acidosis (rare)', 'Check kidney function regularly', 'Report unusual muscle pain'],
    'Hypertension': ['Do not stop suddenly', 'Check blood pressure regularly', 'Avoid potassium supplements'],
    'Bleeding Disorder': ['High bleeding risk', 'Inform all providers', 'Report any unusual bleeding'],
    'Cancer': ['Severe immune reactions possible', 'Monitor for infections', 'Fertility may be affected'],
    'High Cholesterol': ['Liver function monitoring required', 'Muscle pain may indicate damage', 'Avoid grapefruit']
  };
  
  const dosage = dosageMap[diagnosis] || 'Take as directed by healthcare provider';
  const sideEffects = sideEffectsMap[diagnosis] || ['Nausea', 'Stomach upset', 'Diarrhea'];
  const warnings = warningsMap[diagnosis] || ['Consult healthcare provider', 'Report unusual symptoms'];
  
  const drugList = drugs.length > 0 ? drugs.slice(0, 2) : [drugName];
  const drugNames = drugList.join(' + ');
  
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 650">
      <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:${theme.bg};stop-opacity:1" />
          <stop offset="100%" style="stop-color:#FFFFFF;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="400" height="650" fill="url(#grad)"/>
      
      <!-- Header -->
      <rect x="0" y="0" width="400" height="90" fill="${theme.accent}"/>
      <text x="20" y="35" font-size="22" font-weight="bold" fill="white">${drugNames}</text>
      <text x="20" y="58" font-size="13" fill="rgba(255,255,255,0.9)">${diagnosis || 'Patient Education Guide'}</text>
      <text x="20" y="75" font-size="11" fill="rgba(255,255,255,0.7)">Generated: ${new Date().toLocaleDateString()}</text>
      
      <!-- Icon -->
      <circle cx="360" cy="45" r="28" fill="rgba(255,255,255,0.2)"/>
      <text x="354" y="58" font-size="32">💊</text>
      
      <!-- How to Take -->
      <text x="20" y="125" font-size="13" font-weight="bold" fill="#2D2D2D">How to Take</text>
      <text x="20" y="150" font-size="10" fill="#555">${dosage}</text>
      
      <!-- Side Effects -->
      <text x="20" y="185" font-size="13" font-weight="bold" fill="#2D2D2D">Common Side Effects</text>
      ${sideEffects.slice(0, 3).map((effect, i) => `<text x="20" y="${205 + i * 18}" font-size="10" fill="#555">• ${effect}</text>`).join('')}
      
      <!-- Warnings -->
      <rect x="15" y="265" width="370" height="90" fill="${theme.accent}" opacity="0.12" rx="8"/>
      <text x="25" y="285" font-size="12" font-weight="bold" fill="${theme.accent}">⚠ Important Safety Information</text>
      ${warnings.slice(0, 3).map((warning, i) => `<text x="25" y="${305 + i * 18}" font-size="9" fill="#2D2D2D">• ${warning}</text>`).join('')}
      
      <!-- Footer -->
      <rect x="0" y="580" width="400" height="70" fill="${theme.accent}" opacity="0.1"/>
      <text x="20" y="605" font-size="10" font-weight="bold" fill="#2D2D2D">📋 Next Steps</text>
      <text x="20" y="625" font-size="8" fill="#555">1. Schedule follow-up appointment  2. Keep medication list updated</text>
      <text x="20" y="640" font-size="8" fill="#555">3. Report any side effects to your doctor immediately</text>
    </svg>
  `;
  return 'data:image/svg+xml,' + encodeURIComponent(svg);
};

export function LiveAssetPreview({ regulatoryGuardrails }: LiveAssetPreviewProps) {
  const { exportPdf, exportPng } = useAssetStore();
  const [selectedDrugs, setSelectedDrugs] = useState<string[]>(['Metformin']);
  const [diagnosis, setDiagnosis] = useState('Type 2 Diabetes');
  const [currentAsset, setCurrentAsset] = useState(() => 
    generatePatientCard('Metformin', ['Metformin'], 'Type 2 Diabetes')
  );
  const [isLoading, setIsLoading] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportComplete, setExportComplete] = useState(false);

  const availableDrugs = ['Metformin', 'Ozempic', 'Eliquis', 'Keytruda'];
  const availableDiagnoses = ['Type 2 Diabetes', 'Hypertension', 'Bleeding Disorder', 'Cancer', 'High Cholesterol'];

  const handleAddDrug = (drug: string) => {
    if (!selectedDrugs.includes(drug)) {
      setSelectedDrugs([...selectedDrugs, drug]);
    }
  };

  const handleRemoveDrug = (drug: string) => {
    setSelectedDrugs(selectedDrugs.filter(d => d !== drug));
  };

  const handleGenerateAsset = async () => {
    setIsLoading(true);
    try {
      // Generate new card with current selections
      const newCard = generatePatientCard(
        selectedDrugs[0] || 'Medication',
        selectedDrugs,
        diagnosis
      );
      setCurrentAsset(newCard);
    } catch (err) {
      console.error('Failed to generate asset:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportPdf = async () => {
    setIsExporting(true);
    setExportComplete(false);
    try {
      await exportPdf();
      setTimeout(() => {
        setExportComplete(true);
        setTimeout(() => setExportComplete(false), 3000);
      }, 1000);
    } catch (err) {
      console.error('Export failed:', err);
    } finally {
      setIsExporting(false);
    }
  };

  const handleExportPng = async () => {
    setIsExporting(true);
    setExportComplete(false);
    try {
      await exportPng();
      setTimeout(() => {
        setExportComplete(true);
        setTimeout(() => setExportComplete(false), 3000);
      }, 1000);
    } catch (err) {
      console.error('Export failed:', err);
    } finally {
      setIsExporting(false);
    }
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

      {/* Diagnosis Selector */}
      <div className="mb-3">
        <label className="block text-xs font-medium text-gray-600 mb-1">Patient Diagnosis</label>
        <select
          value={diagnosis}
          onChange={(e) => setDiagnosis(e.target.value)}
          className="w-full px-3 py-2 text-sm rounded-xl border border-gray-200 focus:border-[#E65E07] focus:outline-none bg-white"
        >
          {availableDiagnoses.map(dx => (
            <option key={dx} value={dx}>{dx}</option>
          ))}
        </select>
      </div>

      {/* Drug Selector & Tags */}
      <div className="mb-3">
        <label className="block text-xs font-medium text-gray-600 mb-2">Medications ({selectedDrugs.length})</label>
        <div className="flex gap-2 mb-2">
          <select
            defaultValue=""
            onChange={(e) => {
              if (e.target.value) {
                handleAddDrug(e.target.value);
                (e.target as HTMLSelectElement).value = '';
              }
            }}
            className="flex-1 px-3 py-2 text-sm rounded-xl border border-gray-200 focus:border-[#E65E07] focus:outline-none bg-white"
          >
            <option value="">Add medication...</option>
            {availableDrugs.map(drug => (
              <option key={drug} value={drug} disabled={selectedDrugs.includes(drug)}>
                {drug}
              </option>
            ))}
          </select>
          <button
            onClick={handleGenerateAsset}
            disabled={isLoading}
            className="px-3 py-2 rounded-xl bg-[#E65E07]/10 text-[#E65E07] hover:bg-[#E65E07]/20 transition-colors disabled:opacity-50 flex items-center gap-1"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Generate'}
          </button>
        </div>
        
        {/* Selected Drugs Tags */}
        <div className="flex flex-wrap gap-2">
          {selectedDrugs.map(drug => (
            <div key={drug} className="px-2 py-1 bg-[#E65E07]/10 text-[#E65E07] text-xs rounded-full flex items-center gap-1">
              {drug}
              <button
                onClick={() => handleRemoveDrug(drug)}
                className="text-[#E65E07] hover:text-[#B84B06]"
                title="Remove"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Preview */}
      <div className="flex-1 rounded-xl border border-gray-200 bg-gray-50 p-4 mb-4 flex items-center justify-center overflow-auto">
        {currentAsset ? (
          <img
            src={currentAsset}
            alt={`${selectedDrugs.join(' + ')} - ${diagnosis}`}
            className="max-w-full max-h-full object-contain rounded-lg"
          />
        ) : (
          <div className="text-center text-gray-400">
            <Smartphone className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p className="text-xs">No asset generated yet</p>
          </div>
        )}
      </div>

      {/* Export Controls */}
      <div className="space-y-2">
        {exportComplete && (
          <div className="p-2 bg-green-50 border border-green-200 rounded-lg text-xs text-green-700 text-center">
            ✓ Export complete
          </div>
        )}
        <div className="flex gap-2">
          <button
            onClick={handleExportPdf}
            disabled={isExporting || !currentAsset}
            className="flex-1 px-3 py-2 rounded-xl bg-[#E65E07] text-white text-sm font-medium hover:bg-[#B84B06] transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1"
          >
            {isExporting ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileDown className="w-4 h-4" />}
            Export PDF
          </button>
          <button
            onClick={handleExportPng}
            disabled={isExporting || !currentAsset}
            className="flex-1 px-3 py-2 rounded-xl border border-[#E65E07] text-[#E65E07] text-sm font-medium hover:bg-[#E65E07]/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1"
          >
            <Download className="w-4 h-4" />
            PNG
          </button>
        </div>
      </div>

      {regulatoryGuardrails && (
        <p className="text-[10px] text-gray-400 mt-2 text-center">
          For HCP use only. Not patient-approved until reviewed.
        </p>
      )}
    </div>
  );
}
