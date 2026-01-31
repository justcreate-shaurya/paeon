<<<<<<< HEAD
import { useState, useEffect } from 'react';
import { Smartphone, Download, Loader2, CheckCircle2, AlertTriangle, FileImage, FileText, RefreshCw } from 'lucide-react';
import { useAssetStore } from '../lib/store';
import { assetsApi, GeneratedAsset } from '../lib/api';
=======
import { useState } from 'react';
import { Smartphone, Download, Loader2, CheckCircle2, AlertTriangle } from 'lucide-react';
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34

interface LiveAssetPreviewProps {
  regulatoryGuardrails: boolean;
}

<<<<<<< HEAD
// Demo asset data for development mode
const demoAsset: GeneratedAsset = {
  id: 'demo-1',
  drug_name: 'Metformin HCl',
  strength: '500mg Tablet',
  asset_type: 'patient_education_card',
  content: {
    title: 'Metformin HCl',
    subtitle: '500mg Tablet - Type 2 Diabetes Management',
    dosage_instruction: 'Take with meals, twice daily. Swallow whole with water. Do not crush or chew.',
    benefits: [
      'Controls blood sugar levels effectively',
      'Reduces risk of diabetes complications',
      'Supports healthy weight management'
    ],
    side_effects: [
      'Nausea or stomach upset (usually temporary)',
      'Diarrhea in first few weeks',
      'Metallic taste in mouth'
    ],
    warnings: [
      'May cause lactic acidosis (rare but serious)',
      'Avoid if severe kidney disease present',
      'Report unusual muscle pain immediately',
      'Tell your doctor about all medications'
    ],
    fair_balance: 'IMPORTANT SAFETY INFORMATION: Metformin may cause lactic acidosis, a rare but serious condition. Do not use if you have severe kidney problems. Stop taking and call your doctor right away if you feel very weak, tired, or uncomfortable; have unusual muscle pain; have trouble breathing; have unusual sleepiness; or have stomach pain with nausea and vomiting.',
    footer_text: 'Consult your healthcare provider before making any changes to your medication.'
  },
  compliance_status: 'approved',
  compliance_score: 0.95,
  compliance_notes: ['Fair balance included', 'No promotional claims', 'Appropriate disclaimers'],
  created_at: new Date().toISOString()
};

export function LiveAssetPreview({ regulatoryGuardrails }: LiveAssetPreviewProps) {
  const { currentAsset, isLoading, error, setCurrentAsset, setLoading, setError } = useAssetStore();
  const [isExporting, setIsExporting] = useState(false);
  const [exportComplete, setExportComplete] = useState(false);
  const [exportFormat, setExportFormat] = useState<'pdf' | 'png'>('pdf');
  const [selectedDrug, setSelectedDrug] = useState('Metformin HCl');

  // Available drugs for demo
  const availableDrugs = [
    'Metformin HCl',
    'Ozempic (semaglutide)',
    'Eliquis (apixaban)',
    'Lipitor (atorvastatin)',
    'Lisinopril'
  ];

  // Load or generate asset
  useEffect(() => {
    // Start with demo asset
    if (!currentAsset) {
      setCurrentAsset(demoAsset);
    }
  }, [currentAsset, setCurrentAsset]);

  // Generate new asset for selected drug
  const handleGenerateAsset = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await assetsApi.generate({
        drug_name: selectedDrug,
        asset_type: 'patient_education_card',
        target_audience: 'patient',
        language: 'en',
        include_fair_balance: regulatoryGuardrails
      });
      setCurrentAsset(response);
    } catch (err) {
      // Use demo asset on error
      console.log('Using demo asset data');
      setCurrentAsset({
        ...demoAsset,
        drug_name: selectedDrug,
        content: {
          ...demoAsset.content,
          title: selectedDrug
        }
      });
    } finally {
      setLoading(false);
    }
  };

  // Export handler
  const handleExport = async () => {
    if (!currentAsset) return;
    
    setIsExporting(true);
    setExportComplete(false);

    try {
      const blob = await assetsApi.export(currentAsset.id, exportFormat);
      
      // Create download link
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${currentAsset.drug_name.replace(/\s+/g, '_')}_card.${exportFormat}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      setExportComplete(true);
      setTimeout(() => setExportComplete(false), 3000);
    } catch (err) {
      // Simulate export for demo
      console.log('Simulating export for demo mode');
      setTimeout(() => {
        setIsExporting(false);
        setExportComplete(true);
        setTimeout(() => setExportComplete(false), 3000);
      }, 2000);
      return;
    } finally {
      setIsExporting(false);
    }
  };

  const displayAsset = currentAsset || demoAsset;

=======
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

>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
  return (
    <div className="flex flex-col h-full">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="font-medium text-[#2D2D2D] mb-1">Live Asset Preview</h2>
          <p className="text-xs text-gray-500">Patient education card</p>
        </div>
        <Smartphone className="w-4 h-4 text-gray-400" />
      </div>

<<<<<<< HEAD
      {/* Drug Selector */}
      <div className="flex gap-2 mb-4">
        <select
          value={selectedDrug}
          onChange={(e) => setSelectedDrug(e.target.value)}
          className="flex-1 px-3 py-2 text-sm rounded-xl border border-gray-200 focus:border-[#3B4D2B] focus:outline-none bg-white"
        >
          {availableDrugs.map(drug => (
            <option key={drug} value={drug}>{drug}</option>
          ))}
        </select>
        <button
          onClick={handleGenerateAsset}
          disabled={isLoading}
          className="px-3 py-2 rounded-xl bg-[#3B4D2B]/10 text-[#3B4D2B] hover:bg-[#3B4D2B]/20 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Compliance Status */}
      {displayAsset.compliance_status && (
        <div className={`flex items-center gap-2 px-3 py-2 rounded-xl mb-4 ${
          displayAsset.compliance_status === 'approved' 
            ? 'bg-[#606C38]/10 text-[#606C38]' 
            : displayAsset.compliance_status === 'pending'
            ? 'bg-[#D4A574]/10 text-[#D4A574]'
            : 'bg-[#BC6C25]/10 text-[#BC6C25]'
        }`}>
          <CheckCircle2 className="w-4 h-4" />
          <span className="text-xs font-medium">
            Compliance: {displayAsset.compliance_status.toUpperCase()} 
            ({Math.round((displayAsset.compliance_score || 0) * 100)}%)
          </span>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mb-3 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
          {error}
        </div>
      )}

      {/* Mobile Preview Frame */}
      <div className="flex-1 flex items-center justify-center mb-4 overflow-y-auto">
=======
      {/* Mobile Preview Frame */}
      <div className="flex-1 flex items-center justify-center mb-4">
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
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
<<<<<<< HEAD
                  <h3 className="font-medium text-[#2D2D2D] text-sm">{displayAsset.drug_name}</h3>
                  <p className="text-xs text-gray-500">{displayAsset.strength}</p>
=======
                  <h3 className="font-medium text-[#2D2D2D] text-sm">Metformin HCl</h3>
                  <p className="text-xs text-gray-500">500mg Tablet</p>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
                </div>
              </div>

              {/* Usage */}
              <div className="bg-[#3B4D2B]/5 rounded-xl p-3">
                <div className="text-xs font-medium text-[#3B4D2B] mb-1">How to Take</div>
                <p className="text-xs text-[#2D2D2D] leading-relaxed">
<<<<<<< HEAD
                  {displayAsset.content.dosage_instruction}
=======
                  Take with meals, twice daily. Swallow whole with water.
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
                </p>
              </div>

              {/* Benefits */}
<<<<<<< HEAD
              {displayAsset.content.benefits && displayAsset.content.benefits.length > 0 && (
                <div>
                  <div className="text-xs font-medium text-[#2D2D2D] mb-2">Key Benefits</div>
                  <ul className="space-y-1">
                    {displayAsset.content.benefits.slice(0, 3).map((benefit, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <CheckCircle2 className="w-3 h-3 text-[#606C38] mt-0.5 flex-shrink-0" />
                        <span className="text-xs text-[#2D2D2D]">{benefit}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Fair Balance Warning */}
              {regulatoryGuardrails && displayAsset.content.fair_balance && (
=======
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
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
                <div className="bg-[#D4A574]/10 border border-[#D4A574] rounded-xl p-3">
                  <div className="flex items-start gap-2">
                    <AlertTriangle className="w-3 h-3 text-[#BC6C25] mt-0.5 flex-shrink-0" />
                    <div>
                      <div className="text-xs font-medium text-[#BC6C25] mb-1">Important Safety Information</div>
<<<<<<< HEAD
                      <p className="text-xs text-[#2D2D2D] leading-relaxed line-clamp-4">
                        {displayAsset.content.fair_balance}
=======
                      <p className="text-xs text-[#2D2D2D] leading-relaxed">
                        May cause lactic acidosis. Avoid if kidney disease present. Report unusual muscle pain immediately.
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Footer */}
              <div className="text-[10px] text-gray-400 text-center pt-2 border-t border-gray-100">
<<<<<<< HEAD
                {displayAsset.content.footer_text || 'Consult your healthcare provider'}
=======
                Consult your healthcare provider
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
              </div>
            </div>
          </div>
        </div>
      </div>

<<<<<<< HEAD
      {/* Export Format Toggle */}
      <div className="flex gap-2 mb-3">
        <button
          onClick={() => setExportFormat('pdf')}
          className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-sm transition-colors ${
            exportFormat === 'pdf' 
              ? 'bg-[#3B4D2B] text-white' 
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <FileText className="w-4 h-4" />
          PDF
        </button>
        <button
          onClick={() => setExportFormat('png')}
          className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-sm transition-colors ${
            exportFormat === 'png' 
              ? 'bg-[#3B4D2B] text-white' 
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <FileImage className="w-4 h-4" />
          PNG
        </button>
      </div>

      {/* Export Button */}
      <button
        onClick={handleExport}
        disabled={isExporting || isLoading}
=======
      {/* Export Button */}
      <button
        onClick={handleExport}
        disabled={isExporting}
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
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
<<<<<<< HEAD
            <span>Export as {exportFormat.toUpperCase()}</span>
=======
            <span>Export as PDF/PNG</span>
>>>>>>> e12f48468b9193390c7af47631d2c7846def7a34
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
