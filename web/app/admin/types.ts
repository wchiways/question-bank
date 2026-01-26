// Shared types for admin panel

export interface AIProvider {
  key: string;
  name: string;
  enabled: boolean;
  api_key: string;
  api_url: string;
  model: string;
  max_tokens: number;
  temperature: number;
}

export interface AIConfig {
  default_provider: string;
  timeout: number;
  max_retries: number;
  providers: Record<string, AIProvider>;
}

export interface UsageInfo {
  prompt_tokens?: number;
  completion_tokens?: number;
  total_tokens?: number;
  [key: string]: any; // Allow additional fields
}

export interface TestResult {
  success: boolean;
  provider: string;
  latency?: number;
  model?: string;
  usage?: UsageInfo;
  response?: string;
  error?: string;
}

export interface QuestionItem {
  id: string;
  type: string;
  content: string;
  options?: Array<{
    id: string;
    content: string;
  }>;
  answer: string;
  explanation?: string;
  difficulty?: number;
  category?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
  author?: string;
}

export interface StatsData {
  questions_total: number;
  log_size_bytes: number;
  ai_provider: string;
  debug_mode: boolean;
  users_total?: number;
}

export interface QuestionTypeStat {
  type: string;
  count: number;
  percent: number;
}
