import { create } from 'zustand';

interface QueryStore {
  query: string;
  resultIds: string[];
  explanation: string;
  primaryMatch: string | null;
  keywords: string[];
  isLoading: boolean;

  setQuery: (q: string) => void;
  setResults: (ids: string[], explanation: string, primaryMatch: string | null, keywords: string[]) => void;
  setLoading: (val: boolean) => void;
  clearResults: () => void;
}

export const useQueryStore = create<QueryStore>((set) => ({
  query: '',
  resultIds: [],
  explanation: '',
  primaryMatch: null,
  keywords: [],
  isLoading: false,

  setQuery: (q) => set({ query: q }),
  setResults: (ids, explanation, primaryMatch, keywords) =>
    set({ resultIds: ids, explanation, primaryMatch, keywords, isLoading: false }),
  setLoading: (val) => set({ isLoading: val }),
  clearResults: () =>
    set({ resultIds: [], explanation: '', primaryMatch: null, keywords: [], query: '' }),
}));
