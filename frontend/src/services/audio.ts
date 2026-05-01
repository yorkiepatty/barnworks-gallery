/**
 * AlphaVox Audio Service
 *
 * Handles voice synthesis playback with a priority chain:
 *   1. Backend /api/tts/synthesize  → ElevenLabs (highest quality, emotionally expressive)
 *   2. Browser SpeechSynthesis API  → fallback when backend is offline
 *
 * Voice quality matters enormously for AlphaVox users.
 * ElevenLabs gives us human-level naturalness — not robotic TTS.
 */

// ── User voice preference (persisted) ────────────────────────────────────────

export interface VoicePrefs {
  voiceName:  string;   // ElevenLabs voice name e.g. "Rachel"
  voiceId?:   string;   // Custom/cloned voice ID (overrides voiceName)
  speed:      number;   // 0.5 – 2.0
  emotion?:   string;   // "warm" | "calm" | "excited" etc.
  stability?: number;
  similarityBoost?: number;
}

export function getVoicePrefs(): VoicePrefs {
  const saved = localStorage.getItem('alphavox_voice_prefs');
  if (saved) {
    try { return JSON.parse(saved); } catch { /* fall through */ }
  }
  return { voiceName: 'Bella', speed: 1.0, emotion: 'warm' };
}

export function saveVoicePrefs(prefs: Partial<VoicePrefs>): void {
  const current = getVoicePrefs();
  localStorage.setItem('alphavox_voice_prefs', JSON.stringify({ ...current, ...prefs }));
}

// ── Active audio instance (allows cancelling mid-playback) ───────────────────

let activeAudio: HTMLAudioElement | null = null;

export function stopSpeaking(): void {
  if (activeAudio) {
    activeAudio.pause();
    activeAudio.src = '';
    activeAudio = null;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
}

// ── Core: speak text ──────────────────────────────────────────────────────────

export interface SpeakOptions {
  emotion?:   string;
  voiceName?: string;
  voiceId?:   string;
  speed?:     number;
  // ToneScore™ integration
  stability?:       number;
  similarityBoost?: number;
  style?:           number;
}

/**
 * Speak text using the best available TTS provider.
 * Returns a promise that resolves when playback completes.
 */
/**
 * Speak text via ElevenLabs only.
 * If the backend is unavailable, we stay silent — no robotic fallback, ever.
 */
export async function speakText(text: string, options: SpeakOptions = {}): Promise<void> {
  if (!text?.trim()) return;

  stopSpeaking();

  const prefs = getVoicePrefs();
  const merged: SpeakOptions = {
    emotion:         options.emotion         ?? prefs.emotion ?? 'warm',
    voiceName:       options.voiceName       ?? prefs.voiceName ?? 'Bella',
    voiceId:         options.voiceId         ?? prefs.voiceId,
    speed:           options.speed           ?? prefs.speed ?? 1.0,
    stability:       options.stability       ?? prefs.stability,
    similarityBoost: options.similarityBoost ?? prefs.similarityBoost,
    style:           options.style,
  };

  // ElevenLabs only — silence if unavailable
  await _tryBackendTTS(text, merged);
}

async function _tryBackendTTS(text: string, opts: SpeakOptions): Promise<boolean> {
  try {
    const body: Record<string, unknown> = {
      text,
      voice:    opts.voiceName,
      speed:    opts.speed ?? 1.0,
      emotion:  opts.emotion,
    };
    if (opts.voiceId)         body.voice_id         = opts.voiceId;
    if (opts.stability)       body.stability        = opts.stability;
    if (opts.similarityBoost) body.similarity_boost = opts.similarityBoost;
    if (opts.style)           body.style            = opts.style;

    const response = await fetch('/api/tts/synthesize', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(body),
      signal:  AbortSignal.timeout(10000),
    });

    if (!response.ok) return false;

    const blob  = await response.blob();
    const url   = URL.createObjectURL(blob);
    const audio = new Audio(url);
    activeAudio = audio;
    audio.playbackRate = opts.speed ?? 1.0;

    return new Promise<boolean>((resolve) => {
      audio.onended  = () => { URL.revokeObjectURL(url); activeAudio = null; resolve(true); };
      audio.onerror  = () => { URL.revokeObjectURL(url); activeAudio = null; resolve(false); };
      audio.play().catch(() => { URL.revokeObjectURL(url); activeAudio = null; resolve(false); });
    });
  } catch {
    return false;
  }
}

// ── Greeting helpers ──────────────────────────────────────────────────────────

export function buildGreeting(name: string, isNew: boolean): string {
  if (isNew) {
    return `Hello ${name}, and welcome. I'm AlphaVox — I'm here to help you communicate. We'll learn together, at your pace. There's no rush. Let's begin.`;
  }
  const hour = new Date().getHours();
  const time  = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
  const phrases = [
    `${time}, ${name}. It's good to have you back.`,
    `${time}, ${name}. I've been looking forward to talking with you.`,
    `${time}, ${name}. Ready when you are.`,
    `${time}, ${name}. I'm here.`,
  ];
  return phrases[Math.floor(Math.random() * phrases.length)];
}
