import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeRepo, getAnalysisStatus, getGraph } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';
import { useGraphStore } from '../store/graphStore';
import { LoadingOverlay } from '../components/shared/LoadingOverlay';

const EXAMPLE_REPOS = [
  'https://github.com/tiangolo/fastapi',
  'https://github.com/pallets/flask',
  'https://github.com/django/django',
  'https://github.com/expressjs/express',
];

export const LandingPage: React.FC = () => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [loadDetail, setLoadDetail] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const { setRepoUrl, setRepoId, setOwnerRepo, setStatus } = useAnalysisStore();
  const { setGraph } = useGraphStore();

  const handleAnalyze = async (repoUrl: string) => {
    if (!repoUrl.trim()) return;
    setError('');
    setIsLoading(true);
    setLoadDetail('Submitting repository for analysis…');

    try {
      const { repo_id } = await analyzeRepo({ repo_url: repoUrl.trim() });
      setRepoUrl(repoUrl.trim());
      setRepoId(repo_id);

      // Poll for completion
      let attempts = 0;
      const maxAttempts = 360; // 6 minutes max
      while (attempts < maxAttempts) {
        await new Promise((r) => setTimeout(r, 5000));
        const status = await getAnalysisStatus(repo_id);
        setLoadDetail(status.status_detail || 'Processing…');

        if (status.status === 'complete') {
          const graphData = await getGraph(repo_id);
          setOwnerRepo(graphData.owner ?? '', graphData.repo ?? '');
          setGraph(graphData.nodes, graphData.edges, graphData.stats);
          setStatus('complete');
          setIsLoading(false);
          navigate('/graph');
          return;
        }

        if (status.status === 'error') {
          throw new Error(status.error_message || 'Analysis failed.');
        }

        attempts++;
      }
      throw new Error('Analysis timed out. Please try again.');
    } catch (err: any) {
      setIsLoading(false);
      setError(err.message ?? 'An unexpected error occurred.');
    }
  };

  return (
    <>
      {isLoading && <LoadingOverlay status="running" detail={loadDetail} />}
      <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center px-4">
        {/* Background gradient blobs */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -left-40 w-96 h-96 bg-indigo-900/30 rounded-full blur-3xl" />
          <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-purple-900/30 rounded-full blur-3xl" />
        </div>

        <div className="relative z-10 w-full max-w-xl">
          {/* Logo */}
          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-1 text-5xl font-black mb-4">
              <span className="text-indigo-400">git</span>
              <span className="text-white">-filter</span>
            </div>
            <p className="text-gray-400 text-lg leading-relaxed">
              Instantly understand any GitHub codebase.<br />
              <span className="text-gray-500 text-base">
                Interactive dependency graph · AI summaries · Onboarding path · Voice guide
              </span>
            </p>
          </div>

          {/* Input */}
          <div className="bg-gray-900/80 backdrop-blur border border-gray-800 rounded-2xl p-6 shadow-2xl">
            <label className="block text-sm font-medium text-gray-400 mb-2">
              GitHub Repository URL
            </label>
            <div className="flex gap-2">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAnalyze(url)}
                placeholder="https://github.com/owner/repo"
                className="flex-1 bg-gray-800 border border-gray-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 placeholder-gray-600 transition-colors"
              />
              <button
                onClick={() => handleAnalyze(url)}
                disabled={!url.trim() || isLoading}
                className="px-5 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-semibold rounded-xl transition-all hover:scale-105 active:scale-95 text-sm flex-shrink-0"
              >
                Analyze →
              </button>
            </div>

            {error && (
              <div className="mt-3 px-3 py-2 bg-red-900/30 border border-red-700/50 rounded-lg text-sm text-red-400">
                {error}
              </div>
            )}

            {/* Example repos */}
            <div className="mt-4">
              <p className="text-xs text-gray-600 mb-2">Try an example:</p>
              <div className="flex flex-wrap gap-1.5">
                {EXAMPLE_REPOS.map((repo) => (
                  <button
                    key={repo}
                    onClick={() => { setUrl(repo); handleAnalyze(repo); }}
                    className="text-xs text-indigo-400 hover:text-indigo-300 bg-indigo-900/20 hover:bg-indigo-900/40 border border-indigo-800/30 px-2.5 py-1 rounded-full transition-colors"
                  >
                    {repo.split('/').slice(-2).join('/')}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Feature highlights */}
          <div className="grid grid-cols-2 gap-3 mt-6">
            {[
              { icon: '🕸', label: 'Dependency Graph', desc: 'Interactive force-directed graph with filters' },
              { icon: '🤖', label: 'AI Summaries', desc: 'Ollama-powered file explanations' },
              { icon: '🗺', label: 'Onboarding Path', desc: 'LLM-ranked reading order for new devs' },
              { icon: '🎙', label: 'Voice Guide', desc: 'Audio walkthrough of the architecture' },
              { icon: '📅', label: 'Commit Timeline', desc: 'Architectural evolution over time' },
              { icon: '⚡', label: 'Stress Simulator', desc: 'Visualize component behaviour under load' },
            ].map((f) => (
              <div key={f.label} className="bg-gray-900/50 border border-gray-800 rounded-xl p-3">
                <div className="text-xl mb-1">{f.icon}</div>
                <p className="text-xs font-semibold text-gray-300">{f.label}</p>
                <p className="text-xs text-gray-600">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
};
