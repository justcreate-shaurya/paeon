/**
 * Paeon AI - Global State Store
 * 
 * Zustand store for application state management.
 */

import { create } from 'zustand';
import { 
  TranslationResponse, 
  IntelFeedItem, 
  GeneratedAsset,
  slangApi,
  ragApi,
  assetsApi,
} from './api';

// ============================================================================
// TRANSLATION STORE
// ============================================================================

interface TranslationState {
  translations: TranslationResponse[];
  isLoading: boolean;
  error: string | null;
  regulatoryGuardrails: boolean;
  
  // Computed
  allTranslations: TranslationResponse[];
  latestTranslation: TranslationResponse | null;
  
  // Actions
  translate: (text: string, context?: string) => Promise<TranslationResponse>;
  clearTranslations: () => void;
  approveFeedback: (id: string) => void;
  editTranslation: (id: string, correction: string) => void;
  setRegulatoryGuardrails: (enabled: boolean) => void;
}

export const useTranslationStore = create<TranslationState>((set, get) => ({
  translations: [],
  isLoading: false,
  error: null,
  regulatoryGuardrails: true,
  
  // Computed getters
  get allTranslations() {
    return get().translations;
  },
  
  get latestTranslation() {
    const translations = get().translations;
    return translations.length > 0 ? translations[0] : null;
  },

  translate: async (text: string, context?: string) => {
    set({ isLoading: true, error: null });
    try {
      const result = await slangApi.translate({ text, context });
      set((state) => ({
        translations: [result, ...state.translations],
        isLoading: false,
      }));
      return result;
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Translation failed';
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  clearTranslations: () => set({ translations: [], error: null }),

  approveFeedback: (id: string) => {
    // In production, this would call the API
    set((state) => ({
      translations: state.translations.map((t) =>
        t.id === id ? { ...t, approved: true } as any : t
      ),
    }));
  },

  editTranslation: (id: string, correction: string) => {
    set((state) => ({
      translations: state.translations.map((t) =>
        t.id === id ? { ...t, clinical_interpretation: correction, edited: true } as any : t
      ),
    }));
  },
  
  setRegulatoryGuardrails: (enabled: boolean) => set({ regulatoryGuardrails: enabled }),
}));

// ============================================================================
// INTELLIGENCE FEED STORE
// ============================================================================

interface IntelligenceState {
  feedItems: IntelFeedItem[];
  isLoading: boolean;
  error: string | null;
  page: number;
  hasMore: boolean;
  selectedItem: IntelFeedItem | null;
  filters: {
    types: string[];
    severity: string[];
  };

  // Actions
  setFeedItems: (items: IntelFeedItem[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  fetchFeed: (reset?: boolean) => Promise<void>;
  loadMore: () => Promise<void>;
  selectItem: (item: IntelFeedItem | null) => void;
  setFilters: (filters: { types?: string[]; severity?: string[] }) => void;
  search: (query: string) => Promise<void>;
}

export const useIntelligenceStore = create<IntelligenceState>((set, get) => ({
  feedItems: [],
  isLoading: false,
  error: null,
  page: 1,
  hasMore: true,
  selectedItem: null,
  filters: {
    types: [],
    severity: [],
  },
  
  setFeedItems: (items) => set({ feedItems: items }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),

  fetchFeed: async (reset = false) => {
    const { filters } = get();
    set({ isLoading: true, error: null });
    
    if (reset) {
      set({ page: 1, feedItems: [] });
    }

    try {
      const result = await ragApi.getFeed({
        page: reset ? 1 : get().page,
        page_size: 20,
        types: filters.types.length > 0 ? filters.types : undefined,
        severity: filters.severity.length > 0 ? filters.severity : undefined,
      });

      set((state) => ({
        feedItems: reset ? result.items : [...state.feedItems, ...result.items],
        hasMore: result.has_more,
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: 'Failed to fetch intelligence feed', isLoading: false });
    }
  },

  loadMore: async () => {
    const { hasMore, page, isLoading } = get();
    if (!hasMore || isLoading) return;

    set({ page: page + 1 });
    await get().fetchFeed();
  },

  selectItem: (item) => set({ selectedItem: item }),

  setFilters: (newFilters) => {
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    }));
    get().fetchFeed(true);
  },

  search: async (query: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await ragApi.search({ query, limit: 20 });
      // Convert search results to feed items format
      const feedItems: IntelFeedItem[] = response.results.map((r, idx) => ({
        id: `search-${idx}`,
        type: 'search_result',
        title: r.title,
        drug_name: r.drug_name || 'N/A',
        summary: r.content,
        source: r.source,
        source_url: r.url || '#',
        published_at: new Date().toISOString(),
        severity: 'info' as const,
        verified: r.confidence > 0.8,
        relevance_score: r.confidence
      }));
      set({ feedItems, isLoading: false, hasMore: false });
    } catch (error: any) {
      set({ error: 'Search failed', isLoading: false });
    }
  },
}));

// ============================================================================
// ASSET STORE
// ============================================================================

interface AssetState {
  currentAsset: GeneratedAsset | null;
  isLoading: boolean;
  isExporting: boolean;
  error: string | null;
  selectedDrug: string | null;
  availableDrugs: { name: string; brand_names: string[]; drug_class: string }[];

  // Actions
  setCurrentAsset: (asset: GeneratedAsset | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  generateAsset: (drugName: string, dosage?: string) => Promise<GeneratedAsset>;
  exportPdf: () => Promise<void>;
  exportPng: () => Promise<void>;
  setSelectedDrug: (drug: string | null) => void;
  fetchAvailableDrugs: () => Promise<void>;
  clearAsset: () => void;
}

export const useAssetStore = create<AssetState>((set, get) => ({
  currentAsset: null,
  isLoading: false,
  isExporting: false,
  error: null,
  selectedDrug: null,
  availableDrugs: [],
  
  setCurrentAsset: (asset) => set({ currentAsset: asset }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),

  generateAsset: async (drugName: string, dosage?: string) => {
    set({ isLoading: true, error: null });
    try {
      const asset = await assetsApi.generate({
        drug_name: drugName,
        dosage,
        include_black_box: true,
      });
      set({ currentAsset: asset, isLoading: false });
      return asset;
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Asset generation failed';
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  exportPdf: async () => {
    const { currentAsset } = get();
    if (!currentAsset) return;

    set({ isExporting: true });
    try {
      const blob = await assetsApi.export(currentAsset.id, 'pdf');
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `patient_card_${currentAsset.drug_name}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('PDF export failed:', error);
    } finally {
      set({ isExporting: false });
    }
  },

  exportPng: async () => {
    const { currentAsset } = get();
    if (!currentAsset) return;

    set({ isExporting: true });
    try {
      const blob = await assetsApi.export(currentAsset.id, 'png');
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `patient_card_${currentAsset.drug_name}.png`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('PNG export failed:', error);
    } finally {
      set({ isExporting: false });
    }
  },

  setSelectedDrug: (drug: string | null) => set({ selectedDrug: drug }),

  fetchAvailableDrugs: async () => {
    try {
      // In production, fetch from API
      // For now, use static list
      set({ 
        availableDrugs: [
          { name: 'Metformin HCl', brand_names: ['Glucophage'], drug_class: 'Biguanide' },
          { name: 'Semaglutide', brand_names: ['Ozempic', 'Wegovy'], drug_class: 'GLP-1 Agonist' },
          { name: 'Apixaban', brand_names: ['Eliquis'], drug_class: 'Anticoagulant' },
        ]
      });
    } catch (error) {
      console.error('Failed to fetch drugs:', error);
    }
  },

  clearAsset: () => set({ currentAsset: null, error: null }),
}));

// ============================================================================
// UI STORE
// ============================================================================

interface UIState {
  regulatoryGuardrails: boolean;
  sourceDrawerOpen: boolean;
  selectedSource: IntelFeedItem | null;
  sidebarTab: 'history' | 'drug-intelligence' | 'asset-generator';
  isDemoMode: boolean;

  // Actions
  toggleGuardrails: () => void;
  openSourceDrawer: (source: IntelFeedItem) => void;
  closeSourceDrawer: () => void;
  setSidebarTab: (tab: 'history' | 'drug-intelligence' | 'asset-generator') => void;
  setDemoMode: (enabled: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  regulatoryGuardrails: true,
  sourceDrawerOpen: false,
  selectedSource: null,
  sidebarTab: 'drug-intelligence',
  isDemoMode: true, // Start in demo mode

  toggleGuardrails: () =>
    set((state: UIState) => ({ regulatoryGuardrails: !state.regulatoryGuardrails })),

  openSourceDrawer: (source: IntelFeedItem) =>
    set({ sourceDrawerOpen: true, selectedSource: source }),

  closeSourceDrawer: () =>
    set({ sourceDrawerOpen: false, selectedSource: null }),

  setSidebarTab: (tab: 'history' | 'drug-intelligence' | 'asset-generator') => set({ sidebarTab: tab }),

  setDemoMode: (enabled: boolean) => set({ isDemoMode: enabled }),
}));
