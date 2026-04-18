import React from 'react';

const LEVELS = [
  { id: 1, name: 'LOW', label: 'Normal', color: 'bg-green-500', text: 'text-green-400', border: 'border-green-500/50' },
  { id: 2, name: 'MEDIUM', label: 'Elevated', color: 'bg-yellow-500', text: 'text-yellow-400', border: 'border-yellow-500/50' },
  { id: 3, name: 'HIGH', label: 'Stressed', color: 'bg-orange-500', text: 'text-orange-400', border: 'border-orange-500/50' },
  { id: 4, name: 'PEAK', label: 'Critical', color: 'bg-red-500', text: 'text-red-400', border: 'border-red-500/50' },
];

interface Props {
  selected: number;
  onChange: (level: 1 | 2 | 3 | 4) => void;
}

export const StressSlider: React.FC<Props> = ({ selected, onChange }) => (
  <div className="flex gap-3">
    {LEVELS.map((lvl) => {
      const active = selected === lvl.id;
      return (
        <button
          key={lvl.id}
          onClick={() => onChange(lvl.id as 1 | 2 | 3 | 4)}
          className={`flex-1 py-3 px-4 rounded-xl border-2 transition-all font-semibold text-sm ${
            active
              ? `${lvl.color} border-transparent text-white shadow-lg scale-105`
              : `bg-gray-800 ${lvl.border} ${lvl.text} hover:scale-102`
          }`}
        >
          <div className="text-lg mb-0.5">
            {lvl.id === 1 ? '🟢' : lvl.id === 2 ? '🟡' : lvl.id === 3 ? '🟠' : '🔴'}
          </div>
          <div>{lvl.name}</div>
          <div className="text-xs opacity-75">{lvl.label}</div>
        </button>
      );
    })}
  </div>
);
