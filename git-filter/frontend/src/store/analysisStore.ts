import { create } from 'zustand';

interface AnalysisStore {
  repoUrl: string;
  repoId: string | null;
  owner: string;
  repo: string;
  status: 'idle' | 'queued' | 'running' | 'complete' | 'error';
  statusDetail: string;
  errorMessage: string;

  setRepoUrl: (url: string) => void;
  setRepoId: (id: string) => void;
  setOwnerRepo: (owner: string, repo: string) => void;
  setStatus: (status: AnalysisStore['status'], detail?: string) => void;
  setError: (msg: string) => void;
  reset: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  repoUrl: '',
  repoId: null,
  owner: '',
  repo: '',
  status: 'idle',
  statusDetail: '',
  errorMessage: '',

  setRepoUrl: (url) => set({ repoUrl: url }),
  setRepoId: (id) => set({ repoId: id }),
  setOwnerRepo: (owner, repo) => set({ owner, repo }),
  setStatus: (status, detail = '') => set({ status, statusDetail: detail }),
  setError: (msg) => set({ status: 'error', errorMessage: msg }),
  reset: () =>
    set({
      repoUrl: '',
      repoId: null,
      owner: '',
      repo: '',
      status: 'idle',
      statusDetail: '',
      errorMessage: '',
    }),
}));
