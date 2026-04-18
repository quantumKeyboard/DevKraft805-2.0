import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getStressSimulation } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';
import { StressSlider } from '../components/stress/StressSlider';
import { ResourceGraph } from '../components/stress/ResourceGraph';
import { StressTable } from '../components/stress/StressTable';
import type { StressResponse } from '../services/types';

export const StressSimulatorPage: React.FC = () => {
  const navigate = useNavigate();
  const { repoId } = useAnalysisStore();
  const [level, setLevel] = useState<1 | 2 | 3 | 4>(1);
  const [data, setData] = useState<StressResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!repoId) navigate('/');
  }, [repoId, navigate]);

  useEffect(() => {
    setLoading(true);
    getStressSimulation(level)
      .then((r) => { setData(r); setLoading(false); })
      .catch(() => setLoading(false));
  }, [level]);

  const criticalSections = data?.sections.filter((s) => s.is_critical) ?? [];
  const warningSections = data?.sections.filter((s) => s.is_warning && !s.is_critical) ?? [];

  return (
    <div className="flex-1 overflow-y-auto bg-gray-950 px-6 py-8 max-w-5xl mx-auto w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">⚡ Stress Simulator</h1>
        <p className="text-gray-400">
          Visualize how codebase components behave under different load scenarios.
          <span className="ml-2 text-xs text-gray-600">(Hardcoded simulation · real computation is a future feature)</span>
        </p>
      </div>

      {/* Level selector */}
      <div className="mb-6">
        <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Stress Level</p>
        <StressSlider selected={level} onChange={setLevel} />
        {data && (
          <p className="mt-3 text-sm text-gray-400">
            <span className="font-semibold text-white">{data.label}</span> · {data.description}
          </p>
        )}
      </div>

      {/* Warning banners */}
      {criticalSections.length > 0 && (
        <div className="mb-4 px-4 py-3 bg-red-900/30 border border-red-700/50 rounded-xl text-sm text-red-400">
          🚨 <strong>Critical failure risk:</strong> {criticalSections.map((s) => s.section).join(', ')} exceed 50% failure probability.
        </div>
      )}
      {warningSections.length > 0 && (
        <div className="mb-4 px-4 py-3 bg-orange-900/20 border border-orange-700/40 rounded-xl text-sm text-orange-400">
          ⚠️ <strong>Warning:</strong> {warningSections.map((s) => s.section).join(', ')} are under significant stress.
        </div>
      )}

      {loading ? (
        <div className="flex items-center gap-3 text-gray-400 py-8">
          <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          Loading simulation…
        </div>
      ) : data ? (
        <div className="space-y-6">
          <ResourceGraph sections={data.sections} />
          <StressTable sections={data.sections} />
        </div>
      ) : null}
    </div>
  );
};
