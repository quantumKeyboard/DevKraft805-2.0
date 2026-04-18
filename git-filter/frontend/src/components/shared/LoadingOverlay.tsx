import React from 'react';

interface Props {
  status: string;
  detail?: string;
}

const STATUS_STEPS = [
  { key: 'Validating repository', label: 'Validating Repo' },
  { key: 'Fetching file tree', label: 'Fetching Files' },
  { key: 'Fetching commit history', label: 'Commit History' },
  { key: 'Running static analysis', label: 'Static Analysis' },
  { key: 'Analyzing commit patterns', label: 'Churn Analysis' },
  { key: 'Building dependency graph', label: 'Building Graph' },
  { key: 'Generating AI summaries', label: 'AI Summaries' },
  { key: 'Generating onboarding', label: 'Onboarding Path' },
  { key: 'Generating voice guide', label: 'Voice Guide' },
  { key: 'Generating reports', label: 'Reports' },
  { key: 'Analysis complete', label: 'Complete!' },
];

function getCurrentStep(detail: string): number {
  const lower = detail.toLowerCase();
  for (let i = STATUS_STEPS.length - 1; i >= 0; i--) {
    if (lower.includes(STATUS_STEPS[i].key.toLowerCase())) return i;
  }
  return 0;
}

export const LoadingOverlay: React.FC<Props> = ({ status, detail = '' }) => {
  const currentStep = getCurrentStep(detail);
  const progress = Math.round(((currentStep + 1) / STATUS_STEPS.length) * 100);

  return (
    <div className="fixed inset-0 z-50 bg-gray-950/95 backdrop-blur-sm flex flex-col items-center justify-center">
      {/* Animated rings */}
      <div className="relative w-32 h-32 mb-8">
        <div className="absolute inset-0 rounded-full border-2 border-indigo-500/20 animate-ping" />
        <div className="absolute inset-2 rounded-full border-2 border-indigo-500/40 animate-pulse" />
        <div className="absolute inset-4 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-4xl">🔍</span>
        </div>
      </div>

      <h2 className="text-2xl font-bold text-white mb-2">Analyzing Repository</h2>
      <p className="text-gray-400 text-sm mb-8 max-w-sm text-center">
        {detail || 'Preparing analysis pipeline…'}
      </p>

      {/* Progress bar */}
      <div className="w-80 mb-6">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Progress</span>
          <span>{progress}%</span>
        </div>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-1000"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Steps */}
      <div className="grid grid-cols-2 gap-2 w-80 text-xs">
        {STATUS_STEPS.map((step, i) => (
          <div
            key={step.key}
            className={`flex items-center gap-1.5 px-2 py-1 rounded ${
              i < currentStep
                ? 'text-green-400'
                : i === currentStep
                ? 'text-indigo-300 font-semibold'
                : 'text-gray-600'
            }`}
          >
            <span>{i < currentStep ? '✓' : i === currentStep ? '⟳' : '○'}</span>
            <span>{step.label}</span>
          </div>
        ))}
      </div>

      <p className="text-xs text-gray-600 mt-6">
        This may take 2–5 minutes depending on repo size and Ollama speed.
      </p>
    </div>
  );
};
