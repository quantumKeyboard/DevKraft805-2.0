import React from 'react';
import type { Section } from '../../services/types';
import { useGraphStore } from '../../store/graphStore';

const ALL_SECTIONS: Section[] = ['UI', 'Backend', 'Utils', 'Config', 'Tests', 'External'];

const SECTION_COLORS: Record<Section, string> = {
  UI: '#3b82f6',
  Backend: '#22c55e',
  Utils: '#94a3b8',
  Config: '#eab308',
  Tests: '#a855f7',
  External: '#f97316',
};

export const FilterPanel: React.FC = () => {
  const {
    filters,
    nodes,
    setActiveSections,
    setSelectedDeveloper,
    setShowOrphansOnly,
    setShowHotZonesOnly,
    resetFilters,
    stats,
  } = useGraphStore();

  // Collect unique contributors from all nodes
  const allContributors = React.useMemo(() => {
    const set = new Set<string>();
    nodes.forEach((n) => n.contributors.forEach((c) => set.add(c)));
    return ['', ...Array.from(set).sort()];
  }, [nodes]);

  const toggleSection = (section: Section) => {
    if (filters.activeSections.includes(section)) {
      setActiveSections(filters.activeSections.filter((s) => s !== section));
    } else {
      setActiveSections([...filters.activeSections, section]);
    }
  };

  return (
    <div className="h-full bg-gray-900 border-r border-gray-700 p-4 overflow-y-auto flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Filters</h2>
        <button
          onClick={resetFilters}
          className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
        >
          Reset
        </button>
      </div>

      {/* Stats summary */}
      {stats && (
        <div className="grid grid-cols-2 gap-2">
          {[
            { label: 'Files', value: stats.total_nodes },
            { label: 'Deps', value: stats.total_edges },
            { label: 'High Impact', value: stats.high_impact_count },
            { label: 'Hot Zones', value: stats.hot_zone_count },
          ].map((s) => (
            <div key={s.label} className="bg-gray-800 rounded-lg p-2 border border-gray-700/50 text-center">
              <p className="text-lg font-bold text-white">{s.value}</p>
              <p className="text-xs text-gray-500">{s.label}</p>
            </div>
          ))}
        </div>
      )}

      {/* Section Filter */}
      <div>
        <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Sections</p>
        <div className="flex flex-col gap-1.5">
          {ALL_SECTIONS.map((section) => {
            const count = stats?.sections?.[section] ?? 0;
            const isActive = filters.activeSections.includes(section);
            return (
              <button
                key={section}
                onClick={() => toggleSection(section)}
                className={`flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm transition-all ${
                  isActive
                    ? 'bg-gray-800 text-white border border-gray-600'
                    : 'bg-transparent text-gray-600 border border-transparent'
                }`}
              >
                <div
                  className="w-3 h-3 rounded-full flex-shrink-0"
                  style={{ background: isActive ? SECTION_COLORS[section] : '#374151' }}
                />
                <span className="flex-1 text-left">{section}</span>
                {count > 0 && (
                  <span className="text-xs text-gray-500">{count}</span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Developer Filter */}
      <div>
        <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Developer</p>
        <select
          value={filters.selectedDeveloper ?? ''}
          onChange={(e) => setSelectedDeveloper(e.target.value || null)}
          className="w-full bg-gray-800 border border-gray-700 text-gray-300 text-sm rounded-lg px-3 py-2 focus:outline-none focus:border-indigo-500"
        >
          {allContributors.map((c) => (
            <option key={c} value={c}>{c || 'All Developers'}</option>
          ))}
        </select>
      </div>

      {/* Boolean Toggles */}
      <div className="flex flex-col gap-2">
        {[
          {
            label: '🔌 Orphans Only',
            value: filters.showOrphansOnly,
            toggle: () => setShowOrphansOnly(!filters.showOrphansOnly),
            count: stats?.orphan_count,
          },
          {
            label: '🔥 Hot Zones Only',
            value: filters.showHotZonesOnly,
            toggle: () => setShowHotZonesOnly(!filters.showHotZonesOnly),
            count: stats?.hot_zone_count,
          },
        ].map((t) => (
          <button
            key={t.label}
            onClick={t.toggle}
            className={`flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-all border ${
              t.value
                ? 'bg-indigo-600/20 border-indigo-500/50 text-indigo-300'
                : 'bg-gray-800 border-gray-700 text-gray-400 hover:border-gray-600'
            }`}
          >
            <span>{t.label}</span>
            <div className="flex items-center gap-2">
              {t.count !== undefined && (
                <span className="text-xs text-gray-500">{t.count}</span>
              )}
              <div className={`w-8 h-4 rounded-full transition-colors ${t.value ? 'bg-indigo-500' : 'bg-gray-600'}`}>
                <div className={`w-3 h-3 rounded-full bg-white mt-0.5 transition-transform ${t.value ? 'translate-x-4 ml-0.5' : 'ml-0.5'}`} />
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};
