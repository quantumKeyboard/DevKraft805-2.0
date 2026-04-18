import React, { useCallback, useEffect, useMemo } from 'react';
import {
  Background,
  Controls,
  MiniMap,
  ReactFlow as RF,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
  type NodeMouseHandler,
  BackgroundVariant,
  Panel,
} from '@xyflow/react';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const ReactFlow = RF as any;
import '@xyflow/react/dist/style.css';
import * as d3 from 'd3';
import type { GraphNode as ApiNode, GraphEdge as ApiEdge } from '../../services/types';
import { useGraphStore } from '../../store/graphStore';

// Section → color mapping
const SECTION_COLORS: Record<string, string> = {
  UI: '#3b82f6',
  Backend: '#22c55e',
  Utils: '#94a3b8',
  Config: '#eab308',
  Tests: '#a855f7',
  External: '#f97316',
};

function sectionColor(section: string) {
  return SECTION_COLORS[section] ?? '#6366f1';
}

function buildFlowNodes(
  apiNodes: ApiNode[],
  highlightIds: Set<string>,
  hasQuery: boolean,
): Node[] {
  // Run D3 force simulation for layout
  const simNodes = apiNodes.map((n) => ({ ...n }));
  const sim = d3
    .forceSimulation(simNodes as any)
    .force('charge', d3.forceManyBody().strength(-400))
    .force('center', d3.forceCenter(0, 0))
    .force('collision', d3.forceCollide(60))
    .stop();

  // Run simulation ahead of time
  for (let i = 0; i < 200; i++) sim.tick();

  return (simNodes as any[]).map((n) => {
    const apiNode = apiNodes.find((a) => a.id === n.id)!;
    const isHighlighted = highlightIds.has(n.id);
    const isDimmed = hasQuery && !isHighlighted;
    const nodeSize = 20 + (apiNode.impact_score / 100) * 30;
    const color = sectionColor(apiNode.section);

    return {
      id: n.id as string,
      position: { x: (n as any).x ?? 0, y: (n as any).y ?? 0 },
      type: 'default',
      data: { label: apiNode.label, apiNode },
      style: {
        background: isDimmed ? '#1e293b' : color,
        border: apiNode.is_high_impact
          ? `3px solid #f97316`
          : apiNode.is_orphan
          ? `2px dashed #94a3b8`
          : `2px solid transparent`,
        borderRadius: '50%',
        width: nodeSize,
        height: nodeSize,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#fff',
        fontSize: '9px',
        fontWeight: '600',
        opacity: isDimmed ? 0.25 : 1,
        boxShadow: isHighlighted
          ? '0 0 16px 4px #f59e0b'
          : apiNode.is_high_impact
          ? '0 0 12px 2px rgba(249,115,22,0.6)'
          : '0 2px 8px rgba(0,0,0,0.3)',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
      },
    };
  });
}

function buildFlowEdges(apiEdges: ApiEdge[]): Edge[] {
  return apiEdges.map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
    type: 'smoothstep',
    animated: e.type === 'co_changes',
    style: {
      stroke: e.type === 'co_changes' ? '#f59e0b' : '#4b5563',
      strokeWidth: e.type === 'co_changes' ? 2 : 1,
      opacity: 0.7,
    },
    markerEnd: {
      type: 'arrowclosed' as any,
      color: e.type === 'co_changes' ? '#f59e0b' : '#4b5563',
    },
  }));
}

interface Props {
  onNodeClick: (node: ApiNode) => void;
}

export const ArchitectureGraph: React.FC<Props> = ({ onNodeClick }) => {
  const { visibleNodes, visibleEdges, filters } = useGraphStore();
  const highlightSet = useMemo(
    () => new Set(filters.nlQueryHighlightIds),
    [filters.nlQueryHighlightIds],
  );
  const hasQuery = filters.nlQueryHighlightIds.length > 0;

  const flowNodes = useMemo(
    () => buildFlowNodes(visibleNodes, highlightSet, hasQuery),
    [visibleNodes, highlightSet, hasQuery],
  );
  const flowEdges = useMemo(() => buildFlowEdges(visibleEdges), [visibleEdges]);

  const [nodes, setNodes, onNodesChange] = useNodesState(flowNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(flowEdges);

  useEffect(() => {
    setNodes(flowNodes);
    setEdges(flowEdges);
  }, [flowNodes, flowEdges, setNodes, setEdges]);

  const handleNodeClick: NodeMouseHandler = useCallback(
    (_event, node) => {
      const apiNode = node.data?.apiNode as ApiNode;
      if (apiNode) onNodeClick(apiNode);
    },
    [onNodeClick],
  );

  return (
    <div className="w-full h-full bg-gray-950 rounded-xl overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.1}
        maxZoom={3}
        attributionPosition="bottom-left"
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={20}
          size={1}
          color="#1e293b"
        />
        <Controls className="!bg-gray-800 !border-gray-700" />
        <MiniMap
          nodeColor={(n) => sectionColor((n.data?.apiNode as ApiNode)?.section ?? '')}
          className="!bg-gray-900 !border-gray-700"
        />
        <Panel position="top-right">
          <div className="flex flex-col gap-1 bg-gray-900/90 rounded-lg p-2 text-xs border border-gray-700">
            {Object.entries(SECTION_COLORS).map(([section, color]) => (
              <div key={section} className="flex items-center gap-1.5">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ background: color }}
                />
                <span className="text-gray-300">{section}</span>
              </div>
            ))}
            <div className="border-t border-gray-700 mt-1 pt-1 flex items-center gap-1.5">
              <div className="w-3 h-3 rounded-full border-2 border-orange-500" />
              <span className="text-gray-300">High Impact</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-3 h-3 rounded-full border-2 border-dashed border-gray-400" />
              <span className="text-gray-300">Orphan</span>
            </div>
          </div>
        </Panel>
      </ReactFlow>
    </div>
  );
};
