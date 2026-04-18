import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAnalysisStore } from '../../store/analysisStore';

const NAV_LINKS = [
  { to: '/graph', label: 'Graph', icon: '🕸' },
  { to: '/onboarding', label: 'Onboarding', icon: '🗺' },
  { to: '/timeline', label: 'Timeline', icon: '📅' },
  { to: '/reports', label: 'Reports', icon: '📄' },
  { to: '/stress', label: 'Stress Sim', icon: '⚡' },
];

export const Navbar: React.FC = () => {
  const { pathname } = useLocation();
  const { repoId, owner, repo } = useAnalysisStore();

  return (
    <nav className="h-14 bg-gray-950 border-b border-gray-800 flex items-center px-4 gap-6 flex-shrink-0">
      {/* Logo */}
      <Link to="/" className="flex items-center gap-2 text-white font-bold text-lg hover:opacity-80 transition-opacity">
        <span className="text-indigo-400">git</span>
        <span className="text-white">-filter</span>
      </Link>

      {/* Repo name */}
      {repoId && owner && repo && (
        <span className="hidden md:flex items-center gap-1.5 text-xs bg-gray-800 text-gray-400 px-3 py-1 rounded-full border border-gray-700">
          <span className="text-gray-500">📦</span>
          {owner}/{repo}
        </span>
      )}

      {/* Nav Links */}
      {repoId && (
        <div className="flex items-center gap-1 ml-auto">
          {NAV_LINKS.map(({ to, label, icon }) => {
            const active = pathname.startsWith(to);
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition-all ${
                  active
                    ? 'bg-indigo-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
              >
                <span>{icon}</span>
                <span className="hidden sm:inline">{label}</span>
              </Link>
            );
          })}
        </div>
      )}

      {!repoId && (
        <div className="ml-auto">
          <Link
            to="/"
            className="text-sm text-indigo-400 hover:text-indigo-300 transition-colors"
          >
            ← Analyze a Repo
          </Link>
        </div>
      )}
    </nav>
  );
};
