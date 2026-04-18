import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import type { StressSection } from '../../services/types';

interface Props {
  sections: StressSection[];
}

export const ResourceGraph: React.FC<Props> = ({ sections }) => {
  const data = sections
    .filter((s) => s.cpu_pct > 0 || s.memory_mb > 0)
    .map((s) => ({
      name: s.section,
      CPU: s.cpu_pct,
      'Memory (%)': Math.round((s.memory_mb / 5000) * 100), // normalise to %
    }));

  return (
    <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">Resource Utilization</h3>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <YAxis
            tick={{ fill: '#94a3b8', fontSize: 11 }}
            tickFormatter={(v) => `${v}%`}
            domain={[0, 100]}
          />
          <Tooltip
            contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 8 }}
            labelStyle={{ color: '#e2e8f0' }}
            itemStyle={{ color: '#94a3b8' }}
            formatter={(v: any) => `${v}%`}
          />
          <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
          <Bar dataKey="CPU" fill="#6366f1" radius={[4, 4, 0, 0]} />
          <Bar dataKey="Memory (%)" fill="#22c55e" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
