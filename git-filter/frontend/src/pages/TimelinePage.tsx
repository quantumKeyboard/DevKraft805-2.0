import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTimeline } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';
import { EvolutionTimeline } from '../components/timeline/EvolutionTimeline';
import type { TimelineMonth } from '../services/types';

export const TimelinePage: React.FC = () => {
  const navigate = useNavigate();
  const { repoId, owner, repo } = useAnalysisStore();
  const [timeline, setTimeline] = useState<TimelineMonth[]>([]);
  const [selectedMonth, setSelectedMonth] = useState<TimelineMonth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!repoId) { navigate('/'); return; }
    getTimeline(repoId)
      .then((data) => { setTimeline(data.timeline); setLoading(false); })
      .catch((err) => { setError(err.message); setLoading(false); });
  }, [repoId, navigate]);

  const handleMonthClick = (month: string) => {
    const entry = timeline.find((t) => t.month === month);
    setSelectedMonth(entry ?? null);
  };

  return (
    <div className="flex-1 overflow-y-auto bg-gray-950 px-6 py-8 max-w-6xl mx-auto w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">📅 Architecture Evolution</h1>
        <p className="text-gray-400">
          Commit activity timeline for <span className="text-indigo-400 font-mono">{owner}/{repo}</span>.
          Click a month to explore its details.
        </p>
      </div>

      {loading && (
        <div className="flex items-center gap-3 text-gray-400">
          <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          Loading timeline…
        </div>
      )}
      {error && <p className="text-red-400 text-sm">{error}</p>}

      {!loading && !error && (
        <>
          <div className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden mb-6">
            <EvolutionTimeline timeline={timeline} onMonthClick={handleMonthClick} />
          </div>

          {/* Month detail */}
          {selectedMonth && (
            <div className="bg-gray-900 border border-indigo-800/30 rounded-2xl p-6">
              <h2 className="text-lg font-bold text-white mb-4">📆 {selectedMonth.month}</h2>
              <div className="grid grid-cols-3 gap-4 mb-4">
                {[
                  { label: 'Total Commits', value: selectedMonth.total_commits },
                  { label: 'Files Changed', value: selectedMonth.files_changed.length },
                  { label: 'Contributors', value: selectedMonth.contributors.length },
                ].map((s) => (
                  <div key={s.label} className="bg-gray-800 rounded-xl p-3 text-center">
                    <p className="text-2xl font-bold text-white">{s.value}</p>
                    <p className="text-xs text-gray-500">{s.label}</p>
                  </div>
                ))}
              </div>

              {selectedMonth.hottest_files.length > 0 && (
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">🔥 Hottest Files</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedMonth.hottest_files.map((f) => (
                      <span key={f} className="text-xs font-mono bg-red-900/20 text-red-400 border border-red-800/30 px-2 py-1 rounded">
                        {f.split('/').pop()}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {selectedMonth.contributors.length > 0 && (
                <div className="mt-3">
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">👤 Contributors</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedMonth.contributors.map((c) => (
                      <span key={c} className="text-xs bg-gray-800 text-gray-300 border border-gray-700 px-2 py-1 rounded">
                        {c}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};
