import { useState, useRef, useEffect, useCallback } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faVideo, faStop, faPlay, faTrash, faDownload,
  faCircle, faClock, faFilm, faMicrophone, faMicrophoneSlash,
  faCamera, faCameraRotate, faShield, faWaveSquare,
  faTag,
} from '@fortawesome/free-solid-svg-icons';

// ── Types ────────────────────────────────────────────────────────────────────

interface SavedRecording {
  id:       string;
  label:    string;
  duration: string;
  time:     string;
  size:     string;
  tags:     string[];
  blobUrl:  string;
  mimeType: string;
}

const BEHAVIOR_TAGS = [
  'gestures', 'symbols', 'eye-tracking', 'voice',
  'text', 'emotional', 'social', 'self-stimulation',
];

const SAMPLE_RECORDINGS: SavedRecording[] = [
  {
    id: '1', label: 'Morning communication session',
    duration: '3:42', time: 'Today, 9:14 AM', size: '28.4 MB',
    tags: ['gestures', 'symbols'], blobUrl: '', mimeType: '',
  },
  {
    id: '2', label: 'Symbol board exploration',
    duration: '2:18', time: 'Today, 11:30 AM', size: '17.9 MB',
    tags: ['symbols'], blobUrl: '', mimeType: '',
  },
  {
    id: '3', label: 'Voice & text session',
    duration: '5:01', time: 'Yesterday, 3:00 PM', size: '38.2 MB',
    tags: ['voice', 'text'], blobUrl: '', mimeType: '',
  },
];

// ── Helpers ──────────────────────────────────────────────────────────────────

function fmtTime(s: number) {
  return `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, '0')}`;
}

function fmtBytes(bytes: number) {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function BehaviorCapture() {
  // ── Camera / stream state ──────────────────────────────────────────────────
  const [cameraOn,      setCameraOn]      = useState(false);
  const [cameraError,   setCameraError]   = useState<string | null>(null);
  const [resolution,    setResolution]    = useState('—');
  const [micActive,     setMicActive]     = useState(false);

  // ── Recording state ────────────────────────────────────────────────────────
  const [recording,     setRecording]     = useState(false);
  const [elapsed,       setElapsed]       = useState(0);
  const [recordings,    setRecordings]    = useState<SavedRecording[]>(SAMPLE_RECORDINGS);
  const [sessionLabel,  setSessionLabel]  = useState('');
  const [selectedTags,  setSelectedTags]  = useState<string[]>([]);

  // ── Audio level meter ──────────────────────────────────────────────────────
  const [micLevel,      setMicLevel]      = useState<number[]>(new Array(12).fill(0));

  // ── Refs ───────────────────────────────────────────────────────────────────
  const videoRef      = useRef<HTMLVideoElement>(null);
  const streamRef     = useRef<MediaStream | null>(null);
  const recorderRef   = useRef<MediaRecorder | null>(null);
  const chunksRef     = useRef<Blob[]>([]);
  const intervalRef   = useRef<ReturnType<typeof setInterval> | null>(null);
  const analyserRef   = useRef<AnalyserNode | null>(null);
  const audioCtxRef   = useRef<AudioContext | null>(null);
  const animFrameRef  = useRef<number>(0);

  // ── Audio level animation ──────────────────────────────────────────────────
  const animateMicLevel = useCallback(() => {
    if (!analyserRef.current) return;
    const data = new Uint8Array(analyserRef.current.frequencyBinCount);
    analyserRef.current.getByteFrequencyData(data);
    const bars = Array.from({ length: 12 }, (_, i) => {
      const start = Math.floor((i / 12) * data.length);
      const end   = Math.floor(((i + 1) / 12) * data.length);
      const slice = data.slice(start, end);
      const avg   = slice.reduce((a, b) => a + b, 0) / slice.length;
      return Math.min(100, (avg / 255) * 130);
    });
    setMicLevel(bars);
    animFrameRef.current = requestAnimationFrame(animateMicLevel);
  }, []);

  // ── Start camera ──────────────────────────────────────────────────────────
  const startCamera = useCallback(async () => {
    setCameraError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
        audio: true,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play().catch(() => {});
      }
      // Resolution readout
      const vTrack = stream.getVideoTracks()[0];
      if (vTrack) {
        const s = vTrack.getSettings();
        setResolution(`${s.width ?? '?'}×${s.height ?? '?'}`);
      }
      // Audio analyser for level meter
      const ctx      = new AudioContext();
      const source   = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      audioCtxRef.current  = ctx;
      analyserRef.current  = analyser;
      animFrameRef.current = requestAnimationFrame(animateMicLevel);

      setCameraOn(true);
      setMicActive(true);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setCameraError(
        msg.includes('Permission')
          ? 'Camera access denied. Please allow camera permissions in your browser.'
          : `Could not access camera: ${msg}`
      );
    }
  }, [animateMicLevel]);

  // ── Stop camera ───────────────────────────────────────────────────────────
  const stopCamera = useCallback(() => {
    cancelAnimationFrame(animFrameRef.current);
    streamRef.current?.getTracks().forEach(t => t.stop());
    streamRef.current = null;
    audioCtxRef.current?.close();
    audioCtxRef.current = null;
    analyserRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    setCameraOn(false);
    setMicActive(false);
    setMicLevel(new Array(12).fill(0));
    setResolution('—');
  }, []);

  // ── Start recording ────────────────────────────────────────────────────────
  const startRecording = useCallback(() => {
    if (!streamRef.current) return;
    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9')
      ? 'video/webm;codecs=vp9'
      : MediaRecorder.isTypeSupported('video/webm')
      ? 'video/webm'
      : 'video/mp4';
    const recorder = new MediaRecorder(streamRef.current, { mimeType });
    chunksRef.current = [];
    recorder.ondataavailable = e => { if (e.data.size > 0) chunksRef.current.push(e.data); };
    recorder.start(500);
    recorderRef.current = recorder;
    setRecording(true);
    setElapsed(0);
    intervalRef.current = setInterval(() => setElapsed(e => e + 1), 1000);
  }, []);

  // ── Stop recording ─────────────────────────────────────────────────────────
  const stopRecording = useCallback(() => {
    if (!recorderRef.current) return;
    recorderRef.current.onstop = () => {
      const mimeType = recorderRef.current?.mimeType ?? 'video/webm';
      const blob     = new Blob(chunksRef.current, { type: mimeType });
      const blobUrl  = URL.createObjectURL(blob);
      const newRec: SavedRecording = {
        id:       Date.now().toString(),
        label:    sessionLabel || 'Untitled session',
        duration: fmtTime(elapsed),
        time:     `Today, ${new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`,
        size:     fmtBytes(blob.size),
        tags:     selectedTags,
        blobUrl,
        mimeType,
      };
      setRecordings(r => [newRec, ...r]);
      setSessionLabel('');
      setSelectedTags([]);
      setElapsed(0);
    };
    recorderRef.current.stop();
    if (intervalRef.current) clearInterval(intervalRef.current);
    setRecording(false);
  }, [elapsed, sessionLabel, selectedTags]);

  // ── Delete recording ───────────────────────────────────────────────────────
  const deleteRecording = useCallback((id: string) => {
    setRecordings(r => {
      const rec = r.find(x => x.id === id);
      if (rec?.blobUrl) URL.revokeObjectURL(rec.blobUrl);
      return r.filter(x => x.id !== id);
    });
  }, []);

  // ── Cleanup on unmount ─────────────────────────────────────────────────────
  useEffect(() => () => {
    stopCamera();
    if (intervalRef.current) clearInterval(intervalRef.current);
  }, [stopCamera]);

  const toggleTag = (tag: string) =>
    setSelectedTags(p => p.includes(tag) ? p.filter(t => t !== tag) : [...p, tag]);

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <div className="container" style={{ paddingTop: '1.5rem' }}>

      {/* ── Page header ─────────────────────────────────────────────── */}
      <div className="mb-4 d-flex justify-content-between align-items-end flex-wrap gap-2">
        <div>
          <h1 className="display-5 mb-1 cyber-glow-text" style={{ fontSize: '1.75rem', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            <FontAwesomeIcon icon={faVideo} className="me-2" style={{ color: 'var(--primary-color)' }} />
            Behavior Capture
          </h1>
          <p className="lead" style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.85rem', color: 'var(--muted-color)', letterSpacing: '0.08em' }}>
            CLINICAL SESSION RECORDING · MULTIMODAL ANALYSIS
          </p>
        </div>

        {/* System status bar */}
        <div style={{
          display: 'flex', gap: 0,
          background: 'rgba(10,20,40,0.85)',
          border: '1px solid rgba(0,180,216,0.25)',
          padding: '0.45rem 0',
        }}>
          {[
            { label: 'CAMERA', value: cameraOn ? 'ACTIVE' : 'STANDBY', ok: cameraOn },
            { label: 'MIC',    value: micActive ? 'ACTIVE' : 'STANDBY', ok: micActive },
            { label: 'RES',    value: resolution, ok: resolution !== '—' },
            { label: 'CODEC',  value: cameraOn ? 'VP9/WEBM' : '—', ok: cameraOn },
            { label: 'REC',    value: recording ? fmtTime(elapsed) : 'IDLE', ok: recording },
          ].map(({ label, value, ok }, i, arr) => (
            <div key={label} style={{
              display: 'flex', alignItems: 'center', padding: '0 1rem',
              borderRight: i < arr.length - 1 ? '1px solid rgba(0,180,216,0.2)' : 'none',
            }}>
              <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.65rem', color: 'var(--muted-color)', marginRight: '0.4rem', letterSpacing: '0.1em' }}>{label}</span>
              <span style={{
                fontFamily: 'Share Tech Mono, monospace', fontSize: '0.78rem',
                color: ok ? (recording && label === 'REC' ? 'var(--danger-color)' : 'var(--primary-color)') : 'var(--muted-color)',
              }}>{value}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="row" style={{ gap: '1rem', flexWrap: 'wrap' }}>

        {/* ── Left column: camera + controls ──────────────────────── */}
        <div style={{ flex: '1 1 520px', minWidth: 0 }}>

          {/* Camera feed */}
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <div className="d-flex align-items-center gap-2">
                <span style={{
                  width: 10, height: 10, borderRadius: '50%',
                  background: cameraOn ? 'var(--primary-color)' : 'var(--border-color)',
                  boxShadow: cameraOn ? '0 0 8px var(--primary-color)' : 'none',
                  display: 'inline-block',
                  animation: cameraOn ? 'blink 2s infinite' : 'none',
                }} />
                <span>VISION FEED</span>
              </div>
              <div className="d-flex align-items-center gap-2">
                {recording && (
                  <span style={{
                    fontFamily: 'Share Tech Mono, monospace', fontSize: '0.8rem',
                    color: 'var(--danger-color)', display: 'flex', alignItems: 'center', gap: '0.4rem',
                  }}>
                    <FontAwesomeIcon icon={faCircle} style={{ fontSize: '0.6rem', animation: 'blink 1s infinite' }} />
                    REC {fmtTime(elapsed)}
                  </span>
                )}
                <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.7rem', color: 'var(--muted-color)' }}>
                  {cameraOn ? '30 FPS' : '— FPS'}
                </span>
              </div>
            </div>

            <div className="card-body-cyber" style={{ padding: '0.75rem' }}>
              {/* Video container with corner brackets */}
              <div style={{
                position: 'relative', background: '#000',
                minHeight: 300, overflow: 'hidden',
                marginBottom: '0.75rem',
              }}>
                {/* Actual video element */}
                <video
                  ref={videoRef}
                  autoPlay
                  muted
                  playsInline
                  style={{
                    width: '100%', display: 'block',
                    minHeight: 300, objectFit: 'cover',
                    opacity: cameraOn ? 1 : 0,
                  }}
                />

                {/* Scanlines overlay */}
                <div style={{
                  position: 'absolute', inset: 0, pointerEvents: 'none',
                  backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,247,255,0.03) 0px, rgba(0,247,255,0.03) 1px, transparent 1px, transparent 2px)',
                  zIndex: 2,
                }} />

                {/* Neural grid overlay */}
                {recording && (
                  <div style={{
                    position: 'absolute', inset: 0, pointerEvents: 'none',
                    backgroundImage: 'linear-gradient(rgba(0,247,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,247,255,0.05) 1px, transparent 1px)',
                    backgroundSize: '30px 30px', zIndex: 2,
                  }} />
                )}

                {/* Scanning line */}
                {recording && (
                  <div style={{
                    position: 'absolute', left: 0, width: '100%', height: 2,
                    background: 'linear-gradient(to right, transparent, rgba(0,247,255,0.9), transparent)',
                    boxShadow: '0 0 10px rgba(0,247,255,0.8)',
                    zIndex: 3, pointerEvents: 'none',
                    animation: 'scanVertical 3s linear infinite',
                  }} />
                )}

                {/* Recording border pulse */}
                {recording && (
                  <div style={{
                    position: 'absolute', inset: 0,
                    border: '2px solid rgba(239,35,60,0.6)',
                    animation: 'blink 1.5s infinite',
                    zIndex: 3, pointerEvents: 'none',
                  }} />
                )}

                {/* Corner brackets — always visible */}
                {(['tl','tr','bl','br'] as const).map(pos => (
                  <div key={pos} style={{
                    position: 'absolute', width: 20, height: 20, zIndex: 4,
                    ...(pos === 'tl' ? { top: 8, left: 8, borderTop: '2px solid #00f7ff', borderLeft: '2px solid #00f7ff' } : {}),
                    ...(pos === 'tr' ? { top: 8, right: 8, borderTop: '2px solid #00f7ff', borderRight: '2px solid #00f7ff' } : {}),
                    ...(pos === 'bl' ? { bottom: 8, left: 8, borderBottom: '2px solid #00f7ff', borderLeft: '2px solid #00f7ff' } : {}),
                    ...(pos === 'br' ? { bottom: 8, right: 8, borderBottom: '2px solid #00f7ff', borderRight: '2px solid #00f7ff' } : {}),
                  }} />
                ))}

                {/* Standby / error overlay */}
                {!cameraOn && (
                  <div style={{
                    position: 'absolute', inset: 0, display: 'flex',
                    flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                    background: 'rgba(0,0,0,0.92)', gap: '0.75rem', zIndex: 5,
                  }}>
                    {cameraError ? (
                      <>
                        <FontAwesomeIcon icon={faMicrophoneSlash} style={{ fontSize: '2.5rem', color: 'var(--danger-color)' }} />
                        <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.8rem', color: 'var(--danger-color)', textAlign: 'center', padding: '0 1rem' }}>
                          {cameraError}
                        </span>
                      </>
                    ) : (
                      <>
                        <FontAwesomeIcon icon={faCamera} style={{ fontSize: '2.5rem', color: 'var(--border-color)' }} />
                        <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.82rem', color: 'var(--muted-color)', letterSpacing: '0.1em' }}>
                          CAMERA STANDBY
                        </span>
                        <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.72rem', color: 'var(--muted-color)', opacity: 0.6 }}>
                          PRESS ACTIVATE TO BEGIN
                        </span>
                      </>
                    )}
                  </div>
                )}

                {/* Top-left live label */}
                {cameraOn && (
                  <div style={{
                    position: 'absolute', top: 10, left: 30,
                    fontFamily: 'Share Tech Mono, monospace', fontSize: '0.68rem',
                    color: 'rgba(0,247,255,0.7)', zIndex: 4, letterSpacing: '0.1em',
                  }}>
                    {resolution} · 30FPS
                  </div>
                )}
              </div>

              {/* Audio level meter */}
              <div style={{ marginBottom: '0.75rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
                  <FontAwesomeIcon icon={faMicrophone} style={{ fontSize: '0.8rem', color: micActive ? 'var(--primary-color)' : 'var(--border-color)' }} />
                  <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.7rem', color: 'var(--muted-color)', letterSpacing: '0.08em' }}>
                    AUDIO LEVEL
                  </span>
                </div>
                <div style={{ display: 'flex', gap: 3, alignItems: 'flex-end', height: 36, background: 'rgba(0,0,0,0.4)', padding: '4px 8px', border: '1px solid rgba(0,180,216,0.15)' }}>
                  {micLevel.map((lvl, i) => (
                    <div key={i} style={{
                      flex: 1, minWidth: 4,
                      height: `${Math.max(4, lvl)}%`,
                      background: lvl > 70
                        ? 'var(--danger-color)'
                        : lvl > 40
                        ? 'var(--warning-color)'
                        : 'var(--primary-color)',
                      transition: 'height 0.08s ease',
                      opacity: micActive ? 1 : 0.25,
                    }} />
                  ))}
                </div>
              </div>

              {/* Camera toggle button */}
              <div className="d-flex gap-2">
                {!cameraOn ? (
                  <button className="neural-btn btn-success-cyber" onClick={startCamera}>
                    <FontAwesomeIcon icon={faCamera} /> Activate Camera
                  </button>
                ) : (
                  <button className="cyber-btn btn-warning-cyber" onClick={stopCamera} disabled={recording}>
                    <FontAwesomeIcon icon={faCameraRotate} /> Deactivate
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Session controls */}
          <div className="system-card">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faWaveSquare} className="me-2" />Session Controls</span>
            </div>
            <div className="card-body-cyber">
              {/* Session label */}
              <div className="mb-3">
                <label className="form-label-cyber">SESSION LABEL</label>
                <input
                  className="cyber-input"
                  placeholder="e.g. Morning gesture session"
                  value={sessionLabel}
                  onChange={e => setSessionLabel(e.target.value)}
                  disabled={recording}
                  style={{ fontFamily: 'Share Tech Mono, monospace' }}
                />
              </div>

              {/* Behavior tags */}
              <div className="mb-4">
                <label className="form-label-cyber">
                  <FontAwesomeIcon icon={faTag} className="me-2" />BEHAVIOR TAGS
                </label>
                <div className="d-flex flex-wrap gap-2">
                  {BEHAVIOR_TAGS.map(tag => (
                    <button
                      key={tag}
                      type="button"
                      className={selectedTags.includes(tag) ? 'cyber-btn tag-btn-selected' : 'cyber-btn'}
                      style={{ padding: '0.2rem 0.65rem', fontSize: '0.75rem', fontFamily: 'Share Tech Mono, monospace', letterSpacing: '0.06em' }}
                      onClick={() => toggleTag(tag)}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>

              {/* Record button */}
              <div className="d-flex align-items-center gap-3">
                {!recording ? (
                  <button
                    className="neural-btn"
                    onClick={startRecording}
                    disabled={!cameraOn}
                    style={{ background: cameraOn ? 'rgba(239,35,60,0.15)' : undefined, borderColor: cameraOn ? 'var(--danger-color)' : undefined }}
                    title={!cameraOn ? 'Activate camera first' : undefined}
                  >
                    <FontAwesomeIcon icon={faCircle} style={{ color: 'var(--danger-color)' }} />
                    Start Recording
                  </button>
                ) : (
                  <button className="neural-btn" onClick={stopRecording}>
                    <FontAwesomeIcon icon={faStop} />
                    Stop & Save
                  </button>
                )}
                {!cameraOn && (
                  <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.72rem', color: 'var(--muted-color)' }}>
                    Activate camera to enable recording
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* ── Right column: saved recordings ──────────────────────── */}
        <div style={{ flex: '0 0 340px', minWidth: 280 }}>
          <div className="system-card">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faFilm} className="me-2" />SAVED RECORDINGS</span>
              <span className="badge-cyber">{recordings.length}</span>
            </div>
            <div className="card-body-cyber">
              {recordings.length === 0 ? (
                <div className="text-center" style={{ padding: '2.5rem 1rem', color: 'var(--muted-color)' }}>
                  <FontAwesomeIcon icon={faFilm} style={{ fontSize: '2rem', marginBottom: '0.5rem', opacity: 0.4 }} />
                  <p className="small" style={{ fontFamily: 'Share Tech Mono, monospace', letterSpacing: '0.1em' }}>NO RECORDINGS</p>
                </div>
              ) : (
                <div className="d-flex flex-column gap-3">
                  {recordings.map(rec => (
                    <div key={rec.id} style={{
                      background: 'rgba(10,20,40,0.6)',
                      border: '1px solid rgba(0,180,216,0.18)',
                      padding: '0.85rem',
                      position: 'relative',
                    }}>
                      {/* Corner accents */}
                      {(['tl','br'] as const).map(pos => (
                        <div key={pos} style={{
                          position: 'absolute', width: 8, height: 8,
                          ...(pos === 'tl' ? { top: 3, left: 3, borderTop: '1px solid var(--primary-color)', borderLeft: '1px solid var(--primary-color)' } : {}),
                          ...(pos === 'br' ? { bottom: 3, right: 3, borderBottom: '1px solid var(--primary-color)', borderRight: '1px solid var(--primary-color)' } : {}),
                        }} />
                      ))}

                      <div className="d-flex justify-content-between align-items-start mb-2">
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <p className="mb-1" style={{
                            fontSize: '0.85rem', fontWeight: 600,
                            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                          }}>
                            {rec.label}
                          </p>
                          <div className="d-flex gap-2 small text-muted" style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.72rem' }}>
                            <span><FontAwesomeIcon icon={faClock} className="me-1" />{rec.duration}</span>
                            <span>{rec.size}</span>
                          </div>
                          <p className="small text-muted mb-1 mt-1" style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.68rem' }}>
                            {rec.time}
                          </p>
                        </div>
                      </div>

                      {rec.tags.length > 0 && (
                        <div className="d-flex flex-wrap gap-1 mb-2">
                          {rec.tags.map(t => (
                            <span key={t} className="badge-cyber" style={{ fontSize: '0.65rem', padding: '0.12rem 0.4rem', fontFamily: 'Share Tech Mono, monospace' }}>{t}</span>
                          ))}
                        </div>
                      )}

                      <div className="d-flex gap-2">
                        {rec.blobUrl ? (
                          <a href={rec.blobUrl} target="_blank" rel="noreferrer">
                            <button className="cyber-btn" style={{ padding: '0.2rem 0.6rem', fontSize: '0.72rem' }}>
                              <FontAwesomeIcon icon={faPlay} /> Play
                            </button>
                          </a>
                        ) : (
                          <button className="cyber-btn" style={{ padding: '0.2rem 0.6rem', fontSize: '0.72rem' }} disabled>
                            <FontAwesomeIcon icon={faPlay} /> Play
                          </button>
                        )}
                        {rec.blobUrl && (
                          <a href={rec.blobUrl} download={`${rec.label}.webm`}>
                            <button className="cyber-btn" style={{ padding: '0.2rem 0.6rem', fontSize: '0.72rem' }}>
                              <FontAwesomeIcon icon={faDownload} />
                            </button>
                          </a>
                        )}
                        <button
                          className="cyber-btn btn-danger-cyber"
                          style={{ padding: '0.2rem 0.6rem', fontSize: '0.72rem' }}
                          onClick={() => deleteRecording(rec.id)}
                        >
                          <FontAwesomeIcon icon={faTrash} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Privacy note */}
            <div style={{ padding: '0.75rem 1rem', borderTop: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FontAwesomeIcon icon={faShield} style={{ color: 'var(--primary-color)', fontSize: '0.75rem' }} />
              <span style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.68rem', color: 'var(--muted-color)', letterSpacing: '0.06em' }}>
                RECORDINGS STORED LOCALLY · HIPAA-COMPLIANT PIPELINE
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Scanning line keyframe (inline, scoped) */}
      <style>{`
        @keyframes scanVertical {
          0%   { top: 0%; }
          100% { top: 100%; }
        }
      `}</style>
    </div>
  );
}
