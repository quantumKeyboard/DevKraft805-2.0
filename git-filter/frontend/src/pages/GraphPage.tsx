import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArchitectureGraph } from '../components/graph/ArchitectureGraph';
import { NodeDetailPanel } from '../components/graph/NodeDetailPanel';
import { FilterPanel } from '../components/graph/FilterPanel';
import { NLQueryBar } from '../components/query/NLQueryBar';
import { VoiceGuidePlayer } from '../components/voice/VoiceGuidePlayer';
import { useAnalysisStore } from '../store/analysisStore';
import { useGraphStore } from '../store/graphStore';
import { getVoiceScript, getVoiceAudioUrl } from '../services/api';
import type { GraphNode } from '../services/types';

export const GraphPage: React.FC = () => {
  const navigate = useNavigate();
  const { repoId, owner, repo } = useAnalysisStore();
  const { nodes, visibleNodes, stats, selectNode, selectedNodeId } = useGraphStore();

  const [voiceSections, setVoiceSections] = useState<any[]>([]);
  const [voiceAudioUrl, setVoiceAudioUrl] = useState('');

  // Redirect if no repo loaded
  useEffect(() => {
    if (!repoId) navigate('/');
  }, [repoId, navigate]);

  // Load voice script
  useEffect(() => {
    if (!repoId) return;
    getVoiceScript(repoId)
      .then((data: any) => {
        setVoiceSections(data.sections ?? []);
        setVoiceAudioUrl(getVoiceAudioUrl(repoId));
      })
      .catch(() => {});
  }, [repoId]);

  const selectedNode = nodes.find((n) => n.id === selectedNodeId) ?? null;

  const handleNodeClick = useCallback((node: GraphNode) => {
    selectNode(node.id);
  }, [selectNode]);

  const handleClosePanel = useCallback(() => {
    selectNode(null);
  }, [selectNode]);

  if (!repoId) return null;

  return (
    <div className="flex-1 flex overflow-hidden">
      {/* Left: Filter Panel */}
      <div className="w-60 flex-shrink-0">
        <FilterPanel />
      </div>

      {/* Center: Graph canvas */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar: NL query + stats */}
        <div className="bg-gray-950 border-b border-gray-800 px-4 py-2 flex items-center gap-4">
          <div className="flex-1">
            <NLQueryBar />
          </div>
          <div className="hidden lg:flex items-center gap-4 text-xs text-gray-500 flex-shrink-0">
            <span>{visibleNodes.length} / {nodes.length} nodes</span>
            {stats && (
              <>
                <span className="text-orange-400">⚡ {stats.high_impact_count}</span>
                <span className="text-red-400">🔥 {stats.hot_zone_count}</span>
                <span className="text-gray-500">🔌 {stats.orphan_count}</span>
              </>
            )}
          </div>
        </div>

        {/* Graph canvas */}
        <div className="flex-1">
          <ArchitectureGraph onNodeClick={handleNodeClick} />
        </div>
      </div>

      {/* Right: Node Detail Panel (conditional) */}
      {selectedNode && (
        <div className="w-80 flex-shrink-0">
          <NodeDetailPanel
            node={selectedNode}
            repoOwner={owner}
            repoName={repo}
            onClose={handleClosePanel}
          />
        </div>
      )}

      {/* Voice Guide Player (floating) */}
      {voiceSections.length > 0 && (
        <VoiceGuidePlayer sections={voiceSections} audioUrl={voiceAudioUrl} />
      )}
    </div>
  );
};
