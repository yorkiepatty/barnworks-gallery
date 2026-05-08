import { useState, useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faRobot, faBrain, faShieldAlt, faChartLine,
  faSlidersH, faToggleOn, faToggleOff, faSave,
  faNetworkWired, faHeartbeat, faVolumeUp, faPlay, faSpinner,
} from '@fortawesome/free-solid-svg-icons';
import { getVoicePrefs, saveVoicePrefs } from '../services/audio';

// ── AI Config ──────────────────────────────────────────────────────────────────

interface AIConfig {
  empathy_gain: number;
  danger_cutoff: number;
  whisper_cutoff: number;
  soul_forge_enabled: boolean;
  tone_engine_enabled: boolean;
  kernel_fusion_enabled: boolean;
  emotional_salience: number;
  processing_patience: number;
  tonal_stability: number;
  stutter_tolerance: number;
  response_mode: string;
}

const DEFAULT_CONFIG: AIConfig = {
  empathy_gain:          1.5,
  danger_cutoff:         0.75,
  whisper_cutoff:        0.4,
  soul_forge_enabled:    true,
  tone_engine_enabled:   true,
  kernel_fusion_enabled: false,
  emotional_salience:    0.7,
  processing_patience:   0.5,
  tonal_stability:       0.5,
  stutter_tolerance:     0.5,
  response_mode:        'WARM_VALIDATING',
};

const RESPONSE_MODES = [
  'PLAYFUL_VALIDATING', 'WARM_VALIDATING', 'DIRECT_PROBLEM_SOLVING',
  'SERIOUS_SAFETY_CHECK', 'GENTLE_EXPLORATION', 'CELEBRATORY',
];

const EMOTIONS = ['warm', 'calm', 'gentle', 'excited', 'celebratory', 'urgent', 'playful', 'serious', 'sad'];

// ── Voice Config ───────────────────────────────────────────────────────────────

interface VoiceEntry {
  name:     string;
  voice_id: string;
  source:   string;
  cloned:   boolean;
}

// ── Shared sub-components ──────────────────────────────────────────────────────

function SliderRow({ label, id, min, max, step, value, onChange }: {
  label: string; id: string; min: number; max: number; step: number;
  value: number; onChange: (v: number) => void;
}) {
  return (
    <div className="mb-3">
      <label className="form-label-cyber" htmlFor={id}>{label}</label>
      <div className="slider-row">
        <input id={id} type="range" className="cyber-range"
          min={min} max={max} step={step} value={value}
          onChange={e => onChange(parseFloat(e.target.value))} />
        <span className="slider-value">{value.toFixed(2)}</span>
      </div>
    </div>
  );
}

function Toggle({ label, desc, value, onChange }: {
  label: string; desc: string; value: boolean; onChange: (v: boolean) => void;
}) {
  return (
    <div className="d-flex justify-content-between align-items-center mb-3"
      style={{ padding: '0.75rem', background: 'rgba(0,0,0,0.2)', borderRadius: 6, cursor: 'pointer' }}
      onClick={() => onChange(!value)}
    >
      <div>
        <p className="mb-0" style={{ fontSize: '0.88rem', fontWeight: 500 }}>{label}</p>
        <p className="small text-muted mb-0">{desc}</p>
      </div>
      <FontAwesomeIcon icon={value ? faToggleOn : faToggleOff}
        style={{ fontSize: '1.6rem', color: value ? 'var(--success-color)' : 'var(--muted-color)' }} />
    </div>
  );
}

const SYSTEM_STATUS = [
  { name: 'ToneScore™ Engine',           status: 'active',  version: '2.4.1' },
  { name: 'SoulForge Bridge',            status: 'active',  version: '1.0.0' },
  { name: 'Emotion Embedder',            status: 'active',  version: '1.2.0' },
  { name: 'Voice Synthesis Orchestrator',status: 'active',  version: '3.0.1' },
  { name: 'KernelFusion (ULTRA)',        status: 'standby', version: '1.0.0' },
  { name: 'Predictive Intention',        status: 'active',  version: '1.1.0' },
  { name: 'Christman Crypto (PQC)',      status: 'active',  version: '1.0.0' },
];

// ── Page ───────────────────────────────────────────────────────────────────────

function loadSavedConfig(): AIConfig {
  try {
    const raw = localStorage.getItem('alphavox_ai_config');
    return raw ? { ...DEFAULT_CONFIG, ...JSON.parse(raw) } : DEFAULT_CONFIG;
  } catch {
    return DEFAULT_CONFIG;
  }
}

export default function AIControl() {
  const [config, setConfig]   = useState<AIConfig>(loadSavedConfig);
  const [aiSaved, setAiSaved] = useState(false);

  // Voice state — seeded from audio.ts prefs
  const initialVoicePrefs = getVoicePrefs();
  const [voices, setVoices]           = useState<VoiceEntry[]>([]);
  const [voicesLoading, setVoicesLoading] = useState(true);
  const [selectedVoice, setSelectedVoice] = useState(initialVoicePrefs.voiceName ?? 'Joanna');
  const [speed, setSpeed]             = useState(initialVoicePrefs.speed ?? 1.0);
  const [emotion, setEmotion]         = useState(initialVoicePrefs.emotion ?? 'warm');
  const [voiceSaved, setVoiceSaved]   = useState(false);
  const [previewing, setPreviewing]   = useState(false);
  const previewAudio = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    fetch('/api/tts/voices')
      .then(r => r.json())
      .then((data: { voices: VoiceEntry[]; default: string }) => setVoices(data.voices ?? []))
      .catch(() => setVoices([]))
      .finally(() => setVoicesLoading(false));
  }, []);

  const update = (key: keyof AIConfig, value: AIConfig[keyof AIConfig]) => {
    setConfig(c => ({ ...c, [key]: value }));
    setAiSaved(false);
  };

  const handleSaveAI = () => {
    localStorage.setItem('alphavox_ai_config', JSON.stringify(config));
    setAiSaved(true);
    setTimeout(() => setAiSaved(false), 2500);
  };

  const handleSaveVoice = () => {
    saveVoicePrefs({ voiceName: selectedVoice, speed, emotion });
    setVoiceSaved(true);
    setTimeout(() => setVoiceSaved(false), 2500);
  };

  const handlePreview = async () => {
    if (previewing) return;
    setPreviewing(true);
    try {
      const res = await fetch('/api/tts/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text:    `Hi, I'm ${selectedVoice}. This is what I sound like.`,
          voice:   selectedVoice,
          speed,
          emotion,
        }),
      });
      if (!res.ok) throw new Error('TTS failed');
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      if (previewAudio.current) { previewAudio.current.pause(); URL.revokeObjectURL(previewAudio.current.src); }
      const audio = new Audio(url);
      previewAudio.current = audio;
      audio.playbackRate = speed;
      audio.onended = () => { URL.revokeObjectURL(url); setPreviewing(false); };
      audio.onerror = () => { URL.revokeObjectURL(url); setPreviewing(false); };
      audio.play();
    } catch {
      setPreviewing(false);
    }
  };

  return (
    <div className="container" style={{ paddingTop: '1.5rem' }}>
      <div className="mb-4">
        <h1 className="display-5 mb-1 cyber-title" style={{ fontSize: '1.75rem' }}>
          <FontAwesomeIcon icon={faRobot} className="me-2" />AI Control Center
        </h1>
        <p className="lead">Configure the AlphaVox neural systems and empathy parameters</p>
      </div>

      <div className="row">
        {/* ── Left column ── */}
        <div style={{ flex: '1 1 520px', minWidth: 0 }}>

          {/* Voice Engine */}
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faVolumeUp} className="me-2" />Voice Engine — AWS Polly</span>
            </div>
            <div className="card-body-cyber">

              {/* Voice selector */}
              <div className="mb-3">
                <label className="form-label-cyber">Active Voice</label>
                {voicesLoading ? (
                  <p className="small text-muted"><FontAwesomeIcon icon={faSpinner} spin className="me-1" />Loading voices…</p>
                ) : (
                  <select className="cyber-select" value={selectedVoice}
                    onChange={e => setSelectedVoice(e.target.value)}>
                    {voices.map(v => (
                      <option key={v.voice_id} value={v.name}>
                        {v.name}{v.cloned ? ' ★ (cloned)' : ''}
                      </option>
                    ))}
                  </select>
                )}
              </div>

              {/* Emotion */}
              <div className="mb-3">
                <label className="form-label-cyber">Emotional Tone</label>
                <select className="cyber-select" value={emotion} onChange={e => setEmotion(e.target.value)}>
                  {EMOTIONS.map(em => <option key={em} value={em}>{em.charAt(0).toUpperCase() + em.slice(1)}</option>)}
                </select>
              </div>

              {/* Sliders */}
              <SliderRow label="Speed" id="vs" min={0.5} max={2.0} step={0.05} value={speed} onChange={setSpeed} />

              <div className="cyber-alert mb-3">
                <p className="small mb-0">
                  Emotion drives ToneScore™ — Polly adjusts pitch, rate, and volume automatically.
                </p>
              </div>

              {/* Preview + Save */}
              <div className="d-flex gap-2 align-items-center">
                <button className="neural-btn" onClick={handlePreview} disabled={previewing}>
                  <FontAwesomeIcon icon={previewing ? faSpinner : faPlay} spin={previewing} className="me-1" />
                  {previewing ? 'Playing…' : 'Preview Voice'}
                </button>
                {voiceSaved && <span className="badge-success" style={{ padding: '0.4rem 0.8rem', borderRadius: 6 }}>✓ Saved!</span>}
                <button className="neural-btn lg ms-auto" onClick={handleSaveVoice}>
                  <FontAwesomeIcon icon={faSave} /> Save Voice
                </button>
              </div>
            </div>
          </div>

          {/* SoulForge / Empathy */}
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faHeartbeat} className="me-2" />SoulForge™ Empathy Engine</span>
            </div>
            <div className="card-body-cyber">
              <SliderRow label="Empathy Gain" id="eg" min={0.5} max={3.0} step={0.1}
                value={config.empathy_gain} onChange={v => update('empathy_gain', v)} />
              <SliderRow label="Danger Cutoff (Crisis threshold)" id="dc" min={0.3} max={1.0} step={0.05}
                value={config.danger_cutoff} onChange={v => update('danger_cutoff', v)} />
              <SliderRow label="Whisper Cutoff (Gentle mode threshold)" id="wc" min={0.1} max={0.8} step={0.05}
                value={config.whisper_cutoff} onChange={v => update('whisper_cutoff', v)} />
              <SliderRow label="Emotional Salience (LTP Multiplier)" id="es" min={0.0} max={1.0} step={0.05}
                value={config.emotional_salience} onChange={v => update('emotional_salience', v)} />
              <div className="cyber-alert mt-3">
                <p className="small mb-0">
                  LTP Multiplier: <strong style={{ color: 'var(--primary-color)' }}>
                    x{(1.0 + config.emotional_salience * 0.2).toFixed(2)}
                  </strong>
                  &nbsp;— Higher salience creates deeper learning events.
                </p>
              </div>
            </div>
          </div>

          {/* Carbon Memory / Factor Weights */}
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faBrain} className="me-2" />Carbon Memory — Factor Weights</span>
            </div>
            <div className="card-body-cyber">
              <SliderRow label="Processing Patience" id="pp" min={0.05} max={1.2} step={0.05}
                value={config.processing_patience} onChange={v => update('processing_patience', v)} />
              <SliderRow label="Tonal Stability" id="ts" min={0.05} max={1.2} step={0.05}
                value={config.tonal_stability} onChange={v => update('tonal_stability', v)} />
              <SliderRow label="Stutter Tolerance" id="st" min={0.05} max={1.2} step={0.05}
                value={config.stutter_tolerance} onChange={v => update('stutter_tolerance', v)} />
            </div>
          </div>

          {/* ToneScore / Response Mode */}
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faSlidersH} className="me-2" />ToneScore™ — Response Mode</span>
            </div>
            <div className="card-body-cyber">
              <label className="form-label-cyber">Active Response Mode</label>
              <select className="cyber-select mb-4" value={config.response_mode}
                onChange={e => update('response_mode', e.target.value)}>
                {RESPONSE_MODES.map(m => <option key={m} value={m}>{m.replace(/_/g,' ')}</option>)}
              </select>
              <div className="cyber-alert">
                <p className="small mb-0">
                  <strong>Current:</strong> {config.response_mode.replace(/_/g,' ')}
                  &nbsp;— AlphaVox will adapt its tone to match this mode.
                </p>
              </div>
            </div>
          </div>

          {/* Module toggles */}
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faNetworkWired} className="me-2" />Module Activation</span>
            </div>
            <div className="card-body-cyber">
              <Toggle label="SoulForge Bridge" desc="LTP-inspired adaptive learning"
                value={config.soul_forge_enabled} onChange={v => update('soul_forge_enabled', v)} />
              <Toggle label="ToneScore™ Engine" desc="Quantified empathy + mood analysis"
                value={config.tone_engine_enabled} onChange={v => update('tone_engine_enabled', v)} />
              <Toggle label="KernelFusion (ULTRA)" desc="Neuro-symbolic fusion — ULTRA tier required"
                value={config.kernel_fusion_enabled} onChange={v => update('kernel_fusion_enabled', v)} />
            </div>
          </div>

          <div className="d-flex justify-content-end gap-2">
            {aiSaved && <span className="badge-success" style={{ padding: '0.4rem 0.8rem', borderRadius: 6 }}>✓ Saved!</span>}
            <button className="neural-btn lg" onClick={handleSaveAI}>
              <FontAwesomeIcon icon={faSave} /> Save Configuration
            </button>
          </div>
        </div>

        {/* ── Right column ── */}
        <div style={{ flex: '0 0 300px', minWidth: 240 }}>
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <FontAwesomeIcon icon={faChartLine} className="me-2" />System Status
            </div>
            <div className="card-body-cyber">
              {SYSTEM_STATUS.map(s => (
                <div key={s.name} className="d-flex justify-content-between align-items-center mb-3"
                  style={{ paddingBottom: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <div>
                    <p className="mb-0" style={{ fontSize: '0.82rem', fontWeight: 500 }}>{s.name}</p>
                    <p className="small text-muted mb-0">v{s.version}</p>
                  </div>
                  <span className={s.status === 'active' ? 'badge-success badge-cyber' : 'badge-warning badge-cyber'}>
                    {s.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="system-card">
            <div className="card-header-cyber">
              <FontAwesomeIcon icon={faShieldAlt} className="me-2" />Security
            </div>
            <div className="card-body-cyber">
              <div className="mb-2">
                <p className="small text-muted mb-1">Encryption</p>
                <span className="badge-success badge-cyber">ML-KEM-768 + XChaCha20</span>
              </div>
              <div className="mb-2">
                <p className="small text-muted mb-1">Processing Mode</p>
                <span className="badge-cyber">On-Device (HIPAA)</span>
              </div>
              <div>
                <p className="small text-muted mb-1">Threat Model</p>
                <span className="badge-cyber">Harvest-Now-Decrypt-Later Protected</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
