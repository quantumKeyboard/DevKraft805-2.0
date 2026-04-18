import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAnalysisStore } from '../store/analysisStore';
import { getReportUrl } from '../services/api';

type ReportType = 'technical' | 'nontechnical';

export const ReportsPage: React.FC = () => {
  const navigate = useNavigate();
  const { repoId } = useAnalysisStore();
  const [active, setActive] = useState<ReportType>('technical');

  useEffect(() => {
    if (!repoId) navigate('/');
  }, [repoId, navigate]);

  if (!repoId) return null;

  const techUrl = getReportUrl(repoId, 'technical');
  const nonTechUrl = getReportUrl(repoId, 'nontechnical');
  const currentUrl = active === 'technical' ? techUrl : nonTechUrl;

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-gray-950">
      {/* Tab header */}
      <div className="flex-shrink-0 bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center gap-4">
        <h1 className="text-lg font-bold text-white">📄 Reports</h1>
        <div className="flex gap-1 ml-2 bg-gray-800 rounded-lg p-1">
          {(['technical', 'nontechnical'] as ReportType[]).map((t) => (
            <button
              key={t}
              onClick={() => setActive(t)}
              className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${
                active === t
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              {t === 'technical' ? '🔧 Technical' : '📋 Non-Technical'}
            </button>
          ))}
        </div>

        {/* Download button */}
        <a
          href={currentUrl}
          target="_blank"
          rel="noopener noreferrer"
          download
          className="ml-auto flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300 text-sm rounded-lg transition-colors"
        >
          ⬇ Download HTML
        </a>
      </div>

      {/* Report iframe */}
      <iframe
        key={active}
        src={currentUrl}
        className="flex-1 w-full border-0 bg-white"
        title={`${active} report`}
      />
    </div>
  );
};
