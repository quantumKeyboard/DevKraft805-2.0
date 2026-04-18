import React, { useState, useRef } from 'react';
import { useAnalysisStore } from '../../store/analysisStore';
import { useQueryStore } from '../../store/queryStore';
import { useGraphStore } from '../../store/graphStore';
import { queryRepo } from '../../services/api';

export const NLQueryBar: React.FC = () => {
  const [input, setInput] = useState('');
  const { repoId } = useAnalysisStore();
  const { isLoading, resultIds, explanation, setLoading, setResults, clearResults, query } = useQueryStore();
  const { setNlQueryHighlights } = useGraphStore();
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !repoId) return;
    setLoading(true);
    try {
      const result = await queryRepo({ repo_id: repoId, query: input.trim() });
      setResults(result.matching_node_ids, result.explanation, result.primary_match, result.keywords);
      setNlQueryHighlights(result.matching_node_ids);
    } catch (err) {
      setResults([], 'Query failed. Please try again.', null, []);
    }
  };

  const handleClear = () => {
    setInput('');
    clearResults();
    setNlQueryHighlights([]);
    inputRef.current?.focus();
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <div className="relative flex-1">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm">🔍</span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything… e.g. where is authentication handled?"
            className="w-full bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded-lg pl-9 pr-4 py-2 focus:outline-none focus:border-indigo-500 placeholder-gray-600 transition-colors"
          />
        </div>
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white text-sm font-medium rounded-lg transition-colors flex-shrink-0"
        >
          {isLoading ? '...' : 'Search'}
        </button>
        {resultIds.length > 0 && (
          <button
            type="button"
            onClick={handleClear}
            className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-gray-300 text-sm rounded-lg transition-colors flex-shrink-0"
          >
            Clear
          </button>
        )}
      </form>

      {/* Results summary */}
      {resultIds.length > 0 && (
        <div className="mt-2 px-1">
          <p className="text-xs text-indigo-400 font-medium">
            {resultIds.length} matching file{resultIds.length !== 1 ? 's' : ''} found
          </p>
          {explanation && (
            <p className="text-xs text-gray-400 mt-0.5 italic">{explanation}</p>
          )}
        </div>
      )}
    </div>
  );
};
