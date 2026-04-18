import React from 'react';
import type { StressSection } from '../../services/types';

interface Props {
  sections: StressSection[];
}

export const StressTable: React.FC<Props> = ({ sections }) => (
  <div className="bg-gray-900 rounded-xl border border-gray-700 overflow-hidden">
    <table className="w-full text-sm">
      <thead>
        <tr className="bg-gray-800 text-gray-400 text-xs uppercase tracking-wider">
          <th className="text-left px-4 py-3">Section</th>
          <th className="text-right px-4 py-3">CPU %</th>
          <th className="text-right px-4 py-3">Memory</th>
          <th className="text-right px-4 py-3">Response</th>
          <th className="text-right px-4 py-3">Failure Prob.</th>
          <th className="text-center px-4 py-3">Status</th>
        </tr>
      </thead>
      <tbody>
        {sections.map((s) => (
          <tr key={s.section} className="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
            <td className="px-4 py-3 font-semibold text-white">{s.section}</td>
            <td className="px-4 py-3 text-right">
              <span className={s.cpu_pct >= 80 ? 'text-red-400 font-bold' : s.cpu_pct >= 50 ? 'text-yellow-400' : 'text-gray-300'}>
                {s.cpu_pct}%
              </span>
            </td>
            <td className="px-4 py-3 text-right text-gray-300">
              {s.memory_mb >= 1000 ? `${(s.memory_mb / 1000).toFixed(1)} GB` : `${s.memory_mb} MB`}
            </td>
            <td className="px-4 py-3 text-right text-gray-300">
              {s.response_time_ms >= 1000 ? `${(s.response_time_ms / 1000).toFixed(1)}s` : `${s.response_time_ms}ms`}
            </td>
            <td className="px-4 py-3 text-right">
              <span className={
                s.is_critical ? 'text-red-400 font-bold' :
                s.is_warning ? 'text-orange-400 font-semibold' :
                'text-gray-300'
              }>
                {s.failure_probability_pct}%
              </span>
            </td>
            <td className="px-4 py-3 text-center">
              {s.is_critical ? (
                <span className="bg-red-500/20 text-red-400 border border-red-500/30 text-xs px-2 py-0.5 rounded-full">Critical</span>
              ) : s.is_warning ? (
                <span className="bg-orange-500/20 text-orange-400 border border-orange-500/30 text-xs px-2 py-0.5 rounded-full">Warning</span>
              ) : (
                <span className="bg-green-500/20 text-green-400 border border-green-500/30 text-xs px-2 py-0.5 rounded-full">OK</span>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
