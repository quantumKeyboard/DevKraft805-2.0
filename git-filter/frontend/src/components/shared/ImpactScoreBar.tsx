import React from 'react';

interface Props {
  score: number; // 0–100
  showLabel?: boolean;
}

export const ImpactScoreBar: React.FC<Props> = ({ score, showLabel = true }) => {
  const clipped = Math.max(0, Math.min(100, score));
  const color =
    clipped > 80 ? '#ef4444' :
    clipped > 60 ? '#f97316' :
    clipped > 40 ? '#eab308' :
    clipped > 20 ? '#22c55e' :
    '#94a3b8';

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-1">
        {showLabel && <span className="text-xs text-gray-500">Impact Score</span>}
        <span className="text-xs font-bold ml-auto" style={{ color }}>{clipped.toFixed(0)}</span>
      </div>
      <div className="w-full h-2 bg-gray-800 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${clipped}%`, background: color }}
        />
      </div>
    </div>
  );
};
