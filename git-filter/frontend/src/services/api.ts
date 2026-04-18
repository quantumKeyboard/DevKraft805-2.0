import axios from 'axios';
import type {
  AnalyzeRequest, AnalyzeResponse, AnalysisStatus,
  GraphResponse, NLQueryRequest, NLQueryResponse,
  OnboardingResponse, StressResponse, TimelineResponse,
} from './types';

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30_000,
});

// ── Analysis ──────────────────────────────────────────────────────────────────

export const analyzeRepo = (payload: AnalyzeRequest) =>
  api.post<AnalyzeResponse>('/analyze', payload).then((r) => r.data);

export const getAnalysisStatus = (repoId: string) =>
  api.get<AnalysisStatus>(`/analyze/status/${repoId}`).then((r) => r.data);

// ── Graph ─────────────────────────────────────────────────────────────────────

export const getGraph = (repoId: string) =>
  api.get<GraphResponse>(`/graph/${repoId}`).then((r) => r.data);

// ── Node Detail ───────────────────────────────────────────────────────────────

export const getNodeDetail = (repoId: string, nodeId: string) =>
  api.get(`/node/${repoId}/${encodeURIComponent(nodeId)}`).then((r) => r.data);

// ── NL Query ──────────────────────────────────────────────────────────────────

export const queryRepo = (payload: NLQueryRequest) =>
  api.post<NLQueryResponse>('/query', payload).then((r) => r.data);

// ── Onboarding ────────────────────────────────────────────────────────────────

export const getOnboarding = (repoId: string) =>
  api.get<OnboardingResponse>(`/onboarding/${repoId}`).then((r) => r.data);

// ── Timeline ──────────────────────────────────────────────────────────────────

export const getTimeline = (repoId: string) =>
  api.get<TimelineResponse>(`/timeline/${repoId}`).then((r) => r.data);

// ── Reports ───────────────────────────────────────────────────────────────────

export const getReportUrl = (repoId: string, type: 'technical' | 'nontechnical') =>
  `${BASE_URL}/reports/${repoId}/${type}`;

// ── Stress Simulator ──────────────────────────────────────────────────────────

export const getStressSimulation = (level: 1 | 2 | 3 | 4) =>
  api.get<StressResponse>(`/stress/${level}`).then((r) => r.data);

// ── Voice ─────────────────────────────────────────────────────────────────────

export const getVoiceScript = (repoId: string) =>
  api.get(`/voice/${repoId}/script`).then((r) => r.data);

export const getVoiceAudioUrl = (repoId: string) =>
  `${BASE_URL}/voice/${repoId}`;

// ── Health ────────────────────────────────────────────────────────────────────

export const checkHealth = () =>
  api.get('/../../health').then((r) => r.data);

export default api;
