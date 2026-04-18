import { create } from 'zustand';
import type { GraphNode, GraphEdge, GraphStats, GraphFilters, Section } from '../services/types';

const ALL_SECTIONS: Section[] = ['UI', 'Backend', 'Utils', 'Config', 'Tests', 'External'];

interface GraphStore {
  // Raw data from API
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: GraphStats | null;

  // Selection
  selectedNodeId: string | null;

  // Filters
  filters: GraphFilters;

  // Computed (derived from filters)
  visibleNodes: GraphNode[];
  visibleEdges: GraphEdge[];

  // Actions
  setGraph: (nodes: GraphNode[], edges: GraphEdge[], stats: GraphStats) => void;
  selectNode: (nodeId: string | null) => void;
  setActiveSections: (sections: Section[]) => void;
  setSelectedDeveloper: (dev: string | null) => void;
  setShowOrphansOnly: (val: boolean) => void;
  setShowHotZonesOnly: (val: boolean) => void;
  setNlQueryHighlights: (ids: string[]) => void;
  resetFilters: () => void;
}

const defaultFilters: GraphFilters = {
  activeSections: [...ALL_SECTIONS],
  selectedDeveloper: null,
  showOrphansOnly: false,
  showHotZonesOnly: false,
  nlQueryHighlightIds: [],
};

function applyFilters(
  nodes: GraphNode[],
  edges: GraphEdge[],
  filters: GraphFilters,
): { visibleNodes: GraphNode[]; visibleEdges: GraphEdge[] } {
  const visible = nodes.filter((n) => {
    if (!filters.activeSections.includes(n.section)) return false;
    if (filters.selectedDeveloper && !n.contributors.includes(filters.selectedDeveloper))
      return false;
    if (filters.showOrphansOnly && !n.is_orphan) return false;
    if (filters.showHotZonesOnly && !n.is_hot_zone) return false;
    return true;
  });

  const visibleIds = new Set(visible.map((n) => n.id));
  const visibleEdges = edges.filter(
    (e) => visibleIds.has(e.source) && visibleIds.has(e.target),
  );

  return { visibleNodes: visible, visibleEdges };
}

export const useGraphStore = create<GraphStore>((set, get) => ({
  nodes: [],
  edges: [],
  stats: null,
  selectedNodeId: null,
  filters: defaultFilters,
  visibleNodes: [],
  visibleEdges: [],

  setGraph: (nodes, edges, stats) => {
    const { filters } = get();
    const { visibleNodes, visibleEdges } = applyFilters(nodes, edges, filters);
    set({ nodes, edges, stats, visibleNodes, visibleEdges });
  },

  selectNode: (nodeId) => set({ selectedNodeId: nodeId }),

  setActiveSections: (sections) => {
    const { nodes, edges } = get();
    const filters = { ...get().filters, activeSections: sections };
    const { visibleNodes, visibleEdges } = applyFilters(nodes, edges, filters);
    set({ filters, visibleNodes, visibleEdges });
  },

  setSelectedDeveloper: (dev) => {
    const { nodes, edges } = get();
    const filters = { ...get().filters, selectedDeveloper: dev };
    const { visibleNodes, visibleEdges } = applyFilters(nodes, edges, filters);
    set({ filters, visibleNodes, visibleEdges });
  },

  setShowOrphansOnly: (val) => {
    const { nodes, edges } = get();
    const filters = { ...get().filters, showOrphansOnly: val };
    const { visibleNodes, visibleEdges } = applyFilters(nodes, edges, filters);
    set({ filters, visibleNodes, visibleEdges });
  },

  setShowHotZonesOnly: (val) => {
    const { nodes, edges } = get();
    const filters = { ...get().filters, showHotZonesOnly: val };
    const { visibleNodes, visibleEdges } = applyFilters(nodes, edges, filters);
    set({ filters, visibleNodes, visibleEdges });
  },

  setNlQueryHighlights: (ids) => {
    set((state) => ({
      filters: { ...state.filters, nlQueryHighlightIds: ids },
    }));
  },

  resetFilters: () => {
    const { nodes, edges } = get();
    const filters = { ...defaultFilters };
    const { visibleNodes, visibleEdges } = applyFilters(nodes, edges, filters);
    set({ filters, visibleNodes, visibleEdges, selectedNodeId: null });
  },
}));
