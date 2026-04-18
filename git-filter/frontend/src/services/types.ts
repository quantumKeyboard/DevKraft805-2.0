// Frontend TypeScript types — matches the backend API response shapes exactly

export type Section = "UI" | "Backend" | "Utils" | "Config" | "Tests" | "External";
export type Language = "python" | "javascript" | "typescript" | "java" | "unknown";

export interface GraphNode {
  id: string;
  label: string;
  path: string;
  language: Language;
  section: Section;
  impact_score: number;
  is_high_impact: boolean;
  is_orphan: boolean;
  is_hot_zone: boolean;
  churn_score: number;
  bug_commit_ratio: number;
  hot_zone_score: number;
  functions: string[];
  classes: string[];
  contributors: string[];
  contributor_count: number;
  last_modified: string;
  ai_summary: string;
  depends_on: string[];
  depended_on_by: string[];
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: "imports" | "co_changes";
  weight: number;
}

export interface GraphStats {
  total_nodes: number;
  total_edges: number;
  high_impact_count: number;
  orphan_count: number;
  hot_zone_count: number;
  sections: Record<string, number>;
  languages: Record<string, number>;
  avg_in_degree: number;
  avg_out_degree: number;
  isolated_components: number;
}

export interface GraphResponse {
  repo_id: string;
  status: string;
  status_detail?: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: GraphStats;
  repo_url?: string;
  owner?: string;
  repo?: string;
}

export interface AnalyzeRequest {
  repo_url: string;
}

export interface AnalyzeResponse {
  repo_id: string;
  status: string;
  message: string;
}

export interface AnalysisStatus {
  repo_id: string;
  status: "queued" | "running" | "complete" | "error";
  status_detail: string;
  error_message: string;
  started_at: string;
  completed_at: string;
}

export interface OnboardingStep {
  file_path: string;
  section: Section;
  reason: string;
  ai_summary_excerpt: string;
}

export interface OnboardingResponse {
  repo_id: string;
  onboarding_path: OnboardingStep[];
}

export interface NLQueryRequest {
  repo_id: string;
  query: string;
}

export interface NLQueryResponse {
  matching_node_ids: string[];
  explanation: string;
  primary_match: string | null;
  keywords: string[];
}

export interface StressSection {
  section: Section;
  cpu_pct: number;
  memory_mb: number;
  response_time_ms: number;
  failure_probability_pct: number;
  is_critical: boolean;
  is_warning: boolean;
}

export interface StressResponse {
  level: number;
  name: string;
  label: string;
  description: string;
  multiplier: string;
  sections: StressSection[];
}

export interface TimelineMonth {
  month: string;
  files_changed: string[];
  hottest_files: string[];
  contributors: string[];
  total_commits: number;
}

export interface TimelineResponse {
  repo_id: string;
  timeline: TimelineMonth[];
}

export interface VoiceSection {
  section_title: string;
  script_text: string;
}

export interface GraphFilters {
  activeSections: Section[];
  selectedDeveloper: string | null;
  showOrphansOnly: boolean;
  showHotZonesOnly: boolean;
  nlQueryHighlightIds: string[];
}
