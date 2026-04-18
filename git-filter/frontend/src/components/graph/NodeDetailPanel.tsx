import React from 'react';
import type { GraphNode } from '../../services/types';
import { SectionBadge } from '../shared/SectionBadge';
import { ImpactScoreBar } from '../shared/ImpactScoreBar';

interface Props {
  node: GraphNode;
  repoOwner: string;
  repoName: string;
  onClose: () => void;
}

export const NodeDetailPanel: React.FC<Props> = ({ node, repoOwner, repoName, onClose }) => {
  const githubUrl = repoOwner && repoName
    ? `https://github.com/${repoOwner}/${repoName}/blob/HEAD/${node.path}`
    : '#';

  return (
    <div className="h-full overflow-y-auto bg-gray-900 border-l border-gray-700 flex flex-col">
      {/* Header */}
      <div className="flex items-start justify-between p-4 border-b border-gray-700">
        <div className="min-w-0">
          <p className="text-xs text-gray-500 font-mono truncate">{node.path}</p>
          <h3 className="text-white font-bold text-lg truncate mt-0.5">{node.label}</h3>
          <div className="flex items-center gap-2 mt-1">
            <SectionBadge section={node.section} />
            <span className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded">
              {node.language}
            </span>
          </div>
        </div>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-white ml-2 flex-shrink-0 text-xl leading-none"
        >
          ×
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Impact Score */}
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Impact Score</p>
          <ImpactScoreBar score={node.impact_score} />
          <div className="flex gap-3 mt-2">
            {node.is_high_impact && (
              <span className="text-xs bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded-full border border-orange-500/30">
                ⚡ High Impact
              </span>
            )}
            {node.is_hot_zone && (
              <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full border border-red-500/30">
                🔥 Hot Zone
              </span>
            )}
            {node.is_orphan && (
              <span className="text-xs bg-gray-500/20 text-gray-400 px-2 py-0.5 rounded-full border border-gray-500/30">
                🔌 Orphan
              </span>
            )}
          </div>
        </div>

        {/* AI Summary */}
        {node.ai_summary && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">AI Summary</p>
            <p className="text-sm text-gray-300 leading-relaxed bg-gray-800/50 rounded-lg p-3 border border-gray-700/50">
              {node.ai_summary}
            </p>
          </div>
        )}

        {/* Functions & Classes */}
        {(node.functions.length > 0 || node.classes.length > 0) && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Defines</p>
            <div className="flex flex-wrap gap-1.5">
              {[...node.classes.slice(0, 6).map((c) => ({ name: c, type: 'class' })),
                ...node.functions.slice(0, 8).map((f) => ({ name: f, type: 'fn' }))].map((d) => (
                <span
                  key={d.name}
                  className={`text-xs px-2 py-0.5 rounded font-mono ${
                    d.type === 'class'
                      ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                      : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                  }`}
                >
                  {d.type === 'class' ? '🏛 ' : 'ƒ '}{d.name}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Dependencies */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
              Depends On ({node.depends_on.length})
            </p>
            <div className="space-y-1 max-h-36 overflow-y-auto">
              {node.depends_on.slice(0, 12).map((dep) => (
                <p key={dep} className="text-xs font-mono text-indigo-400 truncate">{dep.split('/').pop()}</p>
              ))}
              {node.depends_on.length === 0 && (
                <p className="text-xs text-gray-600 italic">None</p>
              )}
            </div>
          </div>
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
              Depended on By ({node.depended_on_by.length})
            </p>
            <div className="space-y-1 max-h-36 overflow-y-auto">
              {node.depended_on_by.slice(0, 12).map((dep) => (
                <p key={dep} className="text-xs font-mono text-green-400 truncate">{dep.split('/').pop()}</p>
              ))}
              {node.depended_on_by.length === 0 && (
                <p className="text-xs text-gray-600 italic">None</p>
              )}
            </div>
          </div>
        </div>

        {/* Metrics */}
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Metrics</p>
          <div className="grid grid-cols-2 gap-2">
            {[
              { label: 'Churn Score', value: node.churn_score.toFixed(1), unit: '/100' },
              { label: 'Hot Zone Score', value: node.hot_zone_score.toFixed(1), unit: '/100' },
              { label: 'Bug Commit Ratio', value: (node.bug_commit_ratio * 100).toFixed(1), unit: '%' },
              { label: 'Contributors', value: String(node.contributor_count), unit: '' },
            ].map((m) => (
              <div key={m.label} className="bg-gray-800 rounded-lg p-2 border border-gray-700/50">
                <p className="text-xs text-gray-500">{m.label}</p>
                <p className="text-lg font-bold text-white">{m.value}<span className="text-xs text-gray-500">{m.unit}</span></p>
              </div>
            ))}
          </div>
        </div>

        {/* Contributors */}
        {node.contributors.length > 0 && (
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Contributors</p>
            <div className="flex flex-wrap gap-1.5">
              {node.contributors.slice(0, 10).map((c) => (
                <span key={c} className="text-xs bg-gray-800 text-gray-300 px-2 py-0.5 rounded border border-gray-700">
                  👤 {c}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Last Modified */}
        {node.last_modified && (
          <p className="text-xs text-gray-600">
            Last modified: <span className="text-gray-400">{node.last_modified.slice(0, 10)}</span>
          </p>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700">
        <a
          href={githubUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="block w-full text-center text-sm py-2 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors"
        >
          Open on GitHub →
        </a>
      </div>
    </div>
  );
};
