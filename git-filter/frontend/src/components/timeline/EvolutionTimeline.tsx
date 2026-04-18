import React from 'react';
import type { TimelineMonth } from '../../services/types';

interface Props {
  timeline: TimelineMonth[];
  onMonthClick?: (month: string) => void;
}

export const EvolutionTimeline: React.FC<Props> = ({ timeline, onMonthClick }) => {
  if (!timeline.length) {
    return (
      <div className="text-center py-16 text-gray-500">
        <p className="text-4xl mb-3">📅</p>
        <p>No timeline data available.</p>
      </div>
    );
  }

  const maxCommits = Math.max(...timeline.map((t) => t.total_commits), 1);

  return (
    <div className="overflow-x-auto pb-4">
      {/* Scrollable horizontal timeline */}
      <div className="flex items-end gap-3 min-w-max px-4 py-6">
        {timeline.map((month, i) => {
          const heightPct = (month.total_commits / maxCommits) * 100;
          const barH = Math.max(heightPct * 1.2, 20);

          return (
            <div
              key={month.month}
              className="flex flex-col items-center gap-2 cursor-pointer group"
              onClick={() => onMonthClick?.(month.month)}
            >
              {/* Commit count label */}
              <span className="text-xs text-gray-500 group-hover:text-indigo-400 transition-colors">
                {month.total_commits}
              </span>

              {/* Bar */}
              <div
                className="w-10 bg-indigo-600 group-hover:bg-indigo-400 rounded-t-lg transition-all duration-300 relative"
                style={{ height: `${barH}px` }}
              >
                {/* Contributors indicator */}
                {month.contributors.length > 0 && (
                  <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-xs text-gray-600">
                    👤{month.contributors.length}
                  </div>
                )}
              </div>

              {/* Month label */}
              <div className="flex flex-col items-center">
                <span className="text-xs font-semibold text-gray-300">
                  {month.month.slice(5)} {/* MM */}
                </span>
                {(i === 0 || month.month.slice(0, 4) !== timeline[i - 1]?.month.slice(0, 4)) && (
                  <span className="text-xs text-gray-600">{month.month.slice(0, 4)}</span>
                )}
              </div>

              {/* Tooltip card on hover */}
              <div className="hidden group-hover:block absolute z-10 bottom-full mb-2 bg-gray-800 border border-gray-700 rounded-lg p-2 w-48 shadow-xl">
                <p className="text-xs font-bold text-white mb-1">{month.month}</p>
                <p className="text-xs text-gray-400">Commits: {month.total_commits}</p>
                <p className="text-xs text-gray-400">Files: {month.files_changed.length}</p>
                {month.hottest_files[0] && (
                  <p className="text-xs text-orange-400 mt-1 truncate">🔥 {month.hottest_files[0].split('/').pop()}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="flex items-center gap-4 px-4 text-xs text-gray-500">
        <div className="flex items-center gap-1.5"><div className="w-3 h-3 bg-indigo-600 rounded" /><span>Commit Activity</span></div>
        <span>👤 = contributors that month</span>
        <span>🔥 = hottest file</span>
      </div>
    </div>
  );
};
