/**
 * AlphaVox Audio Service
 *
 * Priority chain for speaking:
 *   1. Backend /api/tts/speak  → Amazon Polly (best quality) → gTTS fallback
 *   2. Browser SpeechSynthesis → fallback when backend is offline or audio fails
 *
 * Voice is everything for AlphaVox users — this MUST always produce sound.
 */

// ── User voice preference (persisted) ────────────────────────────────────────

export interface VoicePrefs {
  voiceName:  string;
  voiceId?:   string;
  speed:      number;
  emotion?:   string;
  stability?: number;
  similarityBoost?: number;
}

export function getVoicePrefs(): VoicePrefs {
  const saved = localStorage.getItem('alphavox_voice_prefs');
  if (saved) {
    try { return JSON.parse(saved); } catch { /* fall through */ }
  }
  return { voiceName: 'Matthew', speed: 1.0, emotion: 'warm' };
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
  stability?:       number;
  similarityBoost?: number;
  style?:           number;
}

/**
 * Speak text using the best available TTS provider.
 * Always produces sound — backend first, browser SpeechSynthesis as fallback.
 */
export async function speakText(text: string, options: SpeakOptions = {}): Promise<void> {
  if (!text?.trim()) return;

  stopSpeaking();

  const prefs = getVoicePrefs();
  const merged: SpeakOptions = {
    emotion:         options.emotion         ?? prefs.emotion ?? 'warm',
    voiceName:       options.voiceName       ?? prefs.voiceName ?? 'Matthew',
    voiceId:         options.voiceId         ?? prefs.voiceId,
    speed:           options.speed           ?? prefs.speed ?? 1.0,
    stability:       options.stability       ?? prefs.stability,
    similarityBoost: options.similarityBoost ?? prefs.similarityBoost,
    style:           options.style,
  };

  // Try backend audio first
  const ok = await _tryBackendTTS(text, merged);

  // Always fall back to browser SpeechSynthesis if backend audio didn't play
  if (!ok) {
    _speakWithBrowser(text, merged.speed ?? 1.0);
  }
}

// ── Browser SpeechSynthesis helper ───────────────────────────────────────────

function _speakWithBrowser(text: string, rate = 1.0): void {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  const utt = new SpeechSynthesisUtterance(text);
  utt.rate  = rate;
  utt.pitch = 1.0;
  window.speechSynthesis.speak(utt);
}

// ── Backend TTS via fetch → Audio blob ───────────────────────────────────────

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

    const response = await fetch('/api/tts/speak', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(body),
      signal:  AbortSignal.timeout(10000),
    });

    if (!response.ok) return false;

    const blob  = await response.blob();
    if (!blob.size) return false;

    const url   = URL.createObjectURL(blob);
    const audio = new Audio(url);
    activeAudio = audio;
    audio.playbackRate = opts.speed ?? 1.0;

    return new Promise<boolean>((resolve) => {
      audio.onended  = () => { URL.revokeObjectURL(url); activeAudio = null; resolve(true); };
      audio.onerror  = () => { URL.revokeObjectURL(url); activeAudio = null; resolve(false); };
      // NOTE: do NOT revoke the URL in play().catch() — that causes a race condition
      // where onerror fires after the URL is already revoked (ERR_FILE_NOT_FOUND).
      // onerror handles cleanup.
      audio.play().catch(() => { activeAudio = null; resolve(false); });
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
