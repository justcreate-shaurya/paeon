import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { ClinicalHeader } from './components/ClinicalHeader';
import { SlangTranslator } from './components/SlangTranslator';
import { IntelligenceFeed } from './components/IntelligenceFeed';
import { LiveAssetPreview } from './components/LiveAssetPreview';
import { SourceDrawer } from './components/SourceDrawer';

export default function App() {
  const [regulatoryGuardrails, setRegulatoryGuardrails] = useState(true);
  const [sourceDrawerOpen, setSourceDrawerOpen] = useState(false);
  const [selectedSource, setSelectedSource] = useState<any>(null);

  const handleSourceClick = (source: any) => {
    setSelectedSource(source);
    setSourceDrawerOpen(true);
  };

  return (
    <div className="flex h-screen bg-white">
      {/* Left Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header with Regulatory Toggle */}
        <ClinicalHeader 
          regulatoryGuardrails={regulatoryGuardrails}
          onToggle={setRegulatoryGuardrails}
        />

        {/* Main Workspace - Three Sections */}
        <div className="flex-1 flex gap-6 p-6 overflow-hidden">
          {/* Left: Slang-to-Clinical Translator */}
          <div className="w-[380px] flex flex-col">
            <SlangTranslator regulatoryGuardrails={regulatoryGuardrails} />
          </div>

          {/* Center: Intelligence Feed */}
          <div className="flex-1 flex flex-col min-w-0">
            <IntelligenceFeed onSourceClick={handleSourceClick} />
          </div>

          {/* Right: Live Asset Preview */}
          <div className="w-[340px] flex flex-col">
            <LiveAssetPreview regulatoryGuardrails={regulatoryGuardrails} />
          </div>
        </div>
      </div>

      {/* Source Drawer */}
      <SourceDrawer 
        open={sourceDrawerOpen}
        onClose={() => setSourceDrawerOpen(false)}
        source={selectedSource}
      />
    </div>
  );
}
