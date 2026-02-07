/**
 * Paeon AI - API Client
 * 
 * Type-safe API client for backend communication.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('paeon_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('paeon_token');
      // Optionally redirect to login
    }
    return Promise.reject(error);
  }
);

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface StandardCode {
  system: string;
  code: string;
  display?: string;
}

export interface TranslationRequest {
  text: string;
  context?: string;
  session_id?: string;
}

export interface TranslationResponse {
  id: string;
  original_language: string;
  raw_input: string;
  normalized_english: string;
  clinical_interpretation: string;
  standard_codes: StandardCode[];
  confidence: number;
  rationale: string;
  processing_time_ms: number;
  created_at: string;
}

export interface IntelligenceItem {
  id: string;
  type: 'recall' | 'safety_alert' | 'new_indication' | 'label_update' | 'approval' | 'safety' | 'clinical_trial' | 'search_result';
  severity: 'high' | 'medium' | 'low' | 'info';
  title: string;
  drug_name: string;
  summary: string;
  source_name: string;
  source_url?: string;
  published_date: string;
  is_verified: boolean;
  verification_badge?: string;
  relevance_score?: number;
}

// Alias for component compatibility
export interface IntelFeedItem {
  id: string;
  type: string;
  title: string;
  drug_name: string;
  summary: string;
  source: string;
  source_url: string;
  published_at: string;
  severity: 'high' | 'medium' | 'info';
  verified: boolean;
  relevance_score?: number;
}

export interface IntelligenceFeedResponse {
  items: IntelFeedItem[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

export interface SearchRequest {
  query: string;
  limit?: number;
  include_sources?: string[];
}

export interface SearchResult {
  title: string;
  content: string;
  source: string;
  url?: string;
  drug_name?: string;
  confidence: number;
}

export interface SearchResponse {
  results: SearchResult[];
  query: string;
  total: number;
}

export interface AssetGenerationRequest {
  drug_name: string;
  dosage?: string;
  indication?: string;
  asset_type?: string;
  target_audience?: 'patient' | 'hcp';
  language?: string;
  include_black_box?: boolean;
  include_fair_balance?: boolean;
}

export interface AssetContent {
  title: string;
  subtitle?: string;
  dosage_instruction: string;
  benefits: string[];
  side_effects?: string[];
  warnings?: string[];
  fair_balance: string;
  footer_text?: string;
}

export interface GeneratedAsset {
  id: string;
  drug_name: string;
  strength?: string;
  dosage?: string;
  asset_type: string;
  title?: string;
  content: AssetContent;
  how_to_take?: string;
  key_benefits?: string[];
  safety_information?: string;
  contraindications?: string[];
  black_box_warning?: string;
  disclaimer?: string;
  compliance_status?: 'approved' | 'pending' | 'rejected';
  compliance_score?: number;
  compliance_notes?: string[];
  fair_balance_score?: number;
  compliance_verified?: boolean;
  created_at: string;
}

export interface SourceVerification {
  source_name: string;
  source_url: string;
  is_verified: boolean;
  verification_method: string;
  verification_date: string;
  document_excerpt: string;
  authority: string;
  related_documents: { title: string; url: string }[];
}

export interface SupportedLanguage {
  code: string;
  name: string;
  native_name: string;
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  version: string;
  timestamp: string;
  components: Record<string, { status: string; latency_ms: number }>;
}

// ============================================================================
// API FUNCTIONS
// ============================================================================

/**
 * Slang-to-Clinical Translation API
 */
export const slangApi = {
  /**
   * Translate patient language to clinical terms
   */
  async translate(request: TranslationRequest): Promise<TranslationResponse> {
    const response = await apiClient.post<TranslationResponse>('/slang/translate', request);
    return response.data;
  },

  /**
   * Quick translation for demo purposes
   */
  async quickTranslate(text: string): Promise<{
    input: string;
    language: string;
    clinical: string;
    confidence: number;
    codes: StandardCode[];
  }> {
    const response = await apiClient.post('/slang/quick-translate', { text });
    return response.data;
  },

  /**
   * Get supported languages
   */
  async getLanguages(): Promise<SupportedLanguage[]> {
    const response = await apiClient.get<SupportedLanguage[]>('/slang/languages');
    return response.data;
  },

  /**
   * Submit feedback on a translation
   */
  async submitFeedback(
    translationId: string,
    approved: boolean,
    correction?: string
  ): Promise<void> {
    await apiClient.post(`/slang/translations/${translationId}/feedback`, {
      approved,
      correction,
    });
  },
};

/**
 * RAG Intelligence API
 */
export const ragApi = {
  /**
   * Get intelligence feed
   */
  async getFeed(params?: {
    page?: number;
    page_size?: number;
    types?: string[];
    severity?: string[];
  }): Promise<IntelligenceFeedResponse> {
    const response = await apiClient.get<IntelligenceFeedResponse>('/rag/intel-feed', {
      params,
    });
    return response.data;
  },

  /**
   * Search intelligence
   */
  async search(request: SearchRequest): Promise<SearchResponse> {
    const response = await apiClient.post<any>('/rag/search', request);
    const data = response.data;

    // Backend may return either a list of intelligence items or a wrapped SearchResponse.
    // Normalize both shapes into the frontend `SearchResponse` type.
    if (Array.isArray(data)) {
      const results = data.map((item: any) => ({
        title: item.title,
        content: item.summary ?? item.content ?? '',
        source: item.source_name ?? item.source ?? '',
        url: item.source_url ?? item.url ?? undefined,
        drug_name: item.drug_name ?? undefined,
        confidence: (item.relevance_score ?? item.confidence ?? 0) as number,
      }));

      return {
        results,
        query: request.query,
        total: results.length,
      };
    }

    return data as SearchResponse;
  },

  /**
   * Verify a source
   */
  async verifySource(sourceId: string, sourceName: string): Promise<SourceVerification> {
    const response = await apiClient.get<SourceVerification>(`/rag/verify-source/${sourceId}`, {
      params: { source_name: sourceName },
    });
    return response.data;
  },

  /**
   * Get drug information
   */
  async getDrugInfo(drugName: string): Promise<{
    drug_name: string;
    label: Record<string, any> | null;
    recent_intelligence: IntelligenceItem[];
  }> {
    const response = await apiClient.get(`/rag/drug/${encodeURIComponent(drugName)}`);
    return response.data;
  },
};

/**
 * Asset Generation API
 */
export const assetsApi = {
  /**
   * Generate patient education asset
   */
  async generate(request: AssetGenerationRequest): Promise<GeneratedAsset> {
    const response = await apiClient.post<GeneratedAsset>('/assets/generate', request);
    return response.data;
  },

  /**
   * Get a generated asset
   */
  async get(assetId: string): Promise<GeneratedAsset> {
    const response = await apiClient.get<GeneratedAsset>(`/assets/${assetId}`);
    return response.data;
  },

  /**
   * Export asset as PDF or PNG
   */
  async export(assetId: string, format: 'pdf' | 'png'): Promise<Blob> {
    const response = await apiClient.post(
      `/assets/export/${format}`,
      { asset_id: assetId },
      { responseType: 'blob' }
    );
    return response.data;
  },

  /**
   * Quick generate for demo
   */
  async quickGenerate(drugName: string, dosage?: string): Promise<{
    id: string;
    drug_name: string;
    dosage?: string;
    how_to_take: string;
    benefits: string[];
    safety: string;
    black_box?: string;
    disclaimer: string;
    fair_balance_score: number;
    compliance_verified: boolean;
  }> {
    const response = await apiClient.post('/assets/quick-generate', null, {
      params: { drug_name: drugName, dosage },
    });
    return response.data;
  },

  /**
   * Get available drugs
   */
  async getAvailableDrugs(): Promise<{
    name: string;
    brand_names: string[];
    drug_class: string;
  }[]> {
    const response = await apiClient.get('/assets/drugs/available');
    return response.data;
  },
};

/**
 * System API
 */
export const systemApi = {
  /**
   * Health check
   */
  async health(): Promise<HealthStatus> {
    const response = await apiClient.get<HealthStatus>('/health');
    return response.data;
  },

  /**
   * Get compliance status
   */
  async compliance(): Promise<{
    pii_protection: boolean;
    fair_balance: boolean;
    source_verification: boolean;
    audit_logging: boolean;
    all_compliant: boolean;
  }> {
    const response = await apiClient.get('/compliance');
    return response.data;
  },
};

export default apiClient;
