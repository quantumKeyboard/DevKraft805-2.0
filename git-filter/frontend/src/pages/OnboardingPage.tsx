import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getOnboarding } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';
import { OnboardingStepList } from '../components/onboarding/OnboardingStepList';
import type { OnboardingStep } from '../services/types';

export const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const { repoId, owner, repo } = useAnalysisStore();
  const [steps, setSteps] = useState<OnboardingStep[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!repoId) { navigate('/'); return; }
    getOnboarding(repoId)
      .then((data) => { setSteps(data.onboarding_path); setLoading(false); })
      .catch((err) => { setError(err.message); setLoading(false); });
  }, [repoId, navigate]);

  return (
    <div className="flex-1 overflow-y-auto bg-gray-950 px-6 py-8 max-w-4xl mx-auto w-full">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">🗺 Onboarding Path</h1>
        <p className="text-gray-400">
          AI-recommended reading order for <span className="text-indigo-400 font-mono">{owner}/{repo}</span>.
          Start from the top and work your way down.
        </p>
        {steps.length > 0 && (
          <div className="mt-3 flex items-center gap-3">
            <span className="text-sm text-gray-500">{steps.length} files</span>
            <span className="text-xs bg-indigo-900/30 text-indigo-400 border border-indigo-800/30 px-3 py-1 rounded-full">
              4 phases
            </span>
          </div>
        )}
      </div>

      {loading && (
        <div className="flex items-center gap-3 text-gray-400">
          <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          Loading onboarding path…
        </div>
      )}
      {error && <p className="text-red-400 text-sm">{error}</p>}
      {!loading && !error && (
        <OnboardingStepList steps={steps} owner={owner} repo={repo} />
      )}
    </div>
  );
};
