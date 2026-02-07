import { History, Brain, FileText, Pill } from 'lucide-react';
import { useState } from 'react';

export function Sidebar() {
  const [activeTab, setActiveTab] = useState('drug-intelligence');

  const navItems = [
    { id: 'history', label: 'History', icon: History },
    { id: 'drug-intelligence', label: 'Drug Intelligence', icon: Brain },
    { id: 'asset-generator', label: 'Asset Generator', icon: FileText },
  ];

  return (
    <div className="w-20 bg-[#E65E07] flex flex-col items-center py-6 gap-6">
      {/* Logo */}
      <div className="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center mb-4">
        <Pill className="w-6 h-6 text-white" />
      </div>

      {/* Navigation Items */}
      <nav className="flex flex-col gap-4 flex-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`
                w-14 h-14 rounded-xl flex items-center justify-center
                transition-all duration-200
                ${isActive 
                  ? 'bg-white text-[#E65E07] shadow-lg' 
                  : 'text-white/70 hover:text-white hover:bg-white/10'
                }
              `}
              title={item.label}
            >
              <Icon className="w-5 h-5" />
            </button>
          );
        })}
      </nav>

      {/* User Avatar */}
      <div className="w-10 h-10 rounded-full bg-[#B84B06] flex items-center justify-center text-white text-sm font-medium">
        DR
      </div>
    </div>
  );
}
