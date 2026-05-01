import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ── Types ─────────────────────────────────────────────────────────────────────

export interface InputRequest {
  text: string;
  user_id?: string;
  input_type?: 'text' | 'voice' | 'gesture' | 'symbol';
}

export interface InputResponse {
  status: string;
  message: string;
  user_id?: string;
  tone_profile?: ToneProfile;
  empathy_score?: number;
}

export interface TTSRequest {
  text: string;
  voice?: string;
  speed?: number;
  emotion?: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  message: string;
}

export interface ToneProfile {
  emotional_intensity: number;
  humor_score: number;
  distress_score: number;
  sarcasm_score: number;
  needs_validation: boolean;
  wants_action: boolean;
  response_mode: string;
}

export interface ToneAnalyzeRequest {
  text: string;
  user_id?: string;
}

export interface EmotionEmbedRequest {
  emotion: string;
  intensity: number;
  tier?: 'FREE' | 'BASIC' | 'PREMIUM' | 'ELITE' | 'ULTRA';
}

export interface EmotionEmbedding {
  pitch_shift: number;
  tempo_factor: number;
  energy_boost: number;
  vad_vectors: number[];
  emotion: string;
  tier: string;
}

export interface SynthesizeVoiceRequest {
  text: string;
  emotion?: string;
  voice_name?: string;
  generate_lipsync?: boolean;
  tonescore?: ToneProfile;
}

export interface SynthesizeVoiceResponse {
  status: string;
  audio_path?: string;
  quality_score?: number;
  lipsync_data?: unknown;
  message?: string;
}

export interface SpecialistRouteRequest {
  message: string;
  user_tier?: string;
}

export interface SpecialistRouteResponse {
  specialist: string;
  confidence: number;
  response?: string;
  metadata?: Record<string, unknown>;
}

export interface MemoryStats {
  total_interactions: number;
  vocabulary_size: number;
  learning_progress: number;
  soul_forge_weights: Record<string, number>;
}

// ── Core Endpoints ────────────────────────────────────────────────────────────

export const checkHealth = (): Promise<HealthResponse> =>
  api.get<HealthResponse>('/health').then(r => r.data);

export const processInput = (body: InputRequest): Promise<InputResponse> =>
  api.post<InputResponse>('/process-input', body).then(r => r.data);

export const synthesizeTTS = (body: TTSRequest): Promise<{ status: string }> =>
  api.post<{ status: string }>('/tts/synthesize', body).then(r => r.data);

export const listVoices = (): Promise<{ voices: string[] }> =>
  api.get<{ voices: string[] }>('/tts/voices').then(r => r.data);

export const getMemoryStats = (): Promise<MemoryStats> =>
  api.get<MemoryStats>('/memory/stats').then(r => r.data);

// ── ToneScore™ Engine ─────────────────────────────────────────────────────────

export const analyzeTone = (body: ToneAnalyzeRequest): Promise<ToneProfile> =>
  api.post<ToneProfile>('/tone/analyze', body).then(r => r.data);

// ── Emotion Embedder ──────────────────────────────────────────────────────────

export const embedEmotion = (body: EmotionEmbedRequest): Promise<EmotionEmbedding> =>
  api.post<EmotionEmbedding>('/emotion/embed', body).then(r => r.data);

// ── Voice Synthesis Orchestrator ──────────────────────────────────────────────

export const synthesizeVoice = (body: SynthesizeVoiceRequest): Promise<SynthesizeVoiceResponse> =>
  api.post<SynthesizeVoiceResponse>('/synthesize/voice', body).then(r => r.data);

// ── Specialist Orchestrator (CHRISTMAN_MIND routing) ──────────────────────────

export const routeToSpecialist = (body: SpecialistRouteRequest): Promise<SpecialistRouteResponse> =>
  api.post<SpecialistRouteResponse>('/specialist/route', body).then(r => r.data);

// ── SoulForge Bridge ──────────────────────────────────────────────────────────

export const updateSoulForge = (body: {
  observation_data: Record<string, number>;
  actual_cause: string;
  success_rate: number;
  emotional_salience?: number;
}): Promise<Record<string, number>> =>
  api.post<Record<string, number>>('/soulforge/update', body).then(r => r.data);

export const getSoulForgeWeights = (): Promise<Record<string, number>> =>
  api.get<Record<string, number>>('/soulforge/weights').then(r => r.data);

export default api;
