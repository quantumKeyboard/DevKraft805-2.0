import React from 'react';
import type { OnboardingStep } from '../../services/types';
import { SectionBadge } from '../shared/SectionBadge';

interface Props {
  steps: OnboardingStep[];
  owner: string;
  repo: string;
}

const PHASE_LABELS: Record<number, string> = {
  0: '🏁 Foundation',
  1: '🧠 Core Logic',
  2: '🔧 Services',
  3: '⚙️ Configuration',
};

export const OnboardingStepList: React.FC<Props> = ({ steps, owner, repo }) => {
  if (!steps.length) return (
    <div className="text-center py-16 text-gray-500">
      <p className="text-4xl mb-3">🗺</p>
      <p>No onboarding path available.</p>
    </div>
  );

  // Group into 4 phases (roughly equal quarters)
  const phaseSize = Math.ceil(steps.length / 4);

  return (
    <div className="space-y-6">
      {[0, 1, 2, 3].map((phase) => {
        const phaseSteps = steps.slice(phase * phaseSize, (phase + 1) * phaseSize);
        if (!phaseSteps.length) return null;
        return (
          <div key={phase}>
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
              {PHASE_LABELS[phase]}
              <span className="bg-gray-800 text-gray-500 text-xs px-2 py-0.5 rounded-full">{phaseSteps.length} files</span>
            </h3>
            <div className="space-y-2">
              {phaseSteps.map((step, localIdx) => {
                const globalIdx = phase * phaseSize + localIdx;
                const ghUrl = owner && repo
                  ? `https://github.com/${owner}/${repo}/blob/HEAD/${step.file_path}`
                  : '#';

                return (
                  <div
                    key={step.file_path}
                    className="flex gap-4 items-start bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-indigo-800/50 transition-colors group"
                  >
                    {/* Step number */}
                    <div className="w-9 h-9 bg-indigo-600/20 border border-indigo-500/30 rounded-full flex items-center justify-center flex-shrink-0 text-indigo-300 font-bold text-sm">
                      {globalIdx + 1}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className="font-mono text-sm text-white font-semibold truncate">
                          {step.file_path.split('/').pop()}
                        </span>
                        <SectionBadge section={step.section} />
                      </div>
                      <p className="text-xs text-gray-500 font-mono truncate mb-1">{step.file_path}</p>
                      {step.reason && (
                        <p className="text-xs text-indigo-300 italic mb-1">💡 {step.reason}</p>
                      )}
                      {step.ai_summary_excerpt && (
                        <p className="text-xs text-gray-400">{step.ai_summary_excerpt}</p>
                      )}
                    </div>

                    {/* Action */}
                    <a
                      href={ghUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-shrink-0 text-xs text-gray-600 group-hover:text-indigo-400 transition-colors mt-1"
                    >
                      View →
                    </a>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};
