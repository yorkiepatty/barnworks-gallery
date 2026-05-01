import { useEffect, useRef, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCheckCircle, faTimesCircle, faHandPointUp, faHandPaper,
  faThumbsUp, faThumbsDown, faPlay, faPause, faThLarge,
  faGraduationCap, faComments, faBrain, faHeartbeat,
  faSyncAlt, faChartLine, faSmile, faVolumeUp, faCommentDots,
  faKeyboard, faPaperPlane, faMicrophone, faMicrophoneSlash,
  faInfoCircle, faUniversalAccess, faCamera,
} from '@fortawesome/free-solid-svg-icons';
import { checkHealth, processInput } from '../services/api';
import { speakText, buildGreeting } from '../services/audio';
import OnboardingTour from '../components/OnboardingTour';

interface Message { role: 'user' | 'alpha'; text: string; }

const GESTURES = [
  { id: 'nod',         icon: faCheckCircle,  label: 'Nod (Yes)' },
  { id: 'shake',       icon: faTimesCircle,  label: 'Shake (No)' },
  { id: 'point_up',   icon: faHandPointUp,  label: 'Need Help' },
  { id: 'wave',        icon: faHandPaper,    label: 'Wave (Hello)' },
  { id: 'thumbs_up',  icon: faThumbsUp,     label: 'Like' },
  { id: 'thumbs_down',icon: faThumbsDown,   label: 'Dislike' },
  { id: 'open_palm',  icon: faHandPaper,    label: 'Stop' },
];

const GESTURE_PHRASES: Record<string, string> = {
  nod: 'Yes', shake: 'No', point_up: 'I need help',
  wave: 'Hello', thumbs_up: 'I like this',
  thumbs_down: 'I dislike this', open_palm: 'Stop',
};

// ── Hands-Free Voice Phrase Map ────────────────────────────────────────────
// These are the words a paralyzed or non-touching user can speak aloud.
// AlphaVox hears them → speaks the full phrase on their behalf.
// No touch. No tap. Just their voice.
const VOICE_PHRASE_MAP: Record<string, string> = {
  // Basic needs
  'bathroom':   'I need to use the bathroom',
  'toilet':     'I need to use the bathroom',
  'hungry':     'I am hungry',
  'food':       'I am hungry',
  'eat':        'I am hungry',
  'water':      'I need water',
  'drink':      'I need water',
  'thirsty':    'I need water',
  'tired':      'I am tired',
  'sleep':      'I am tired',
  'rest':       'I need to rest',
  'pain':       'I am in pain',
  'hurt':       'I am hurting',
  'help':       'I need help',
  'hot':        'I am too hot',
  'cold':       'I am too cold',
  'medicine':   'I need my medicine',
  // Communication
  'yes':        'Yes',
  'no':         'No',
  'hello':      'Hello',
  'hi':         'Hello',
  'bye':        'Goodbye',
  'goodbye':    'Goodbye',
  'stop':       'Stop',
  'more':       'I want more',
  'done':       'I am done',
  'finished':   'I am done',
  'wait':       'Please wait',
  // Emotions
  'happy':      'I am happy',
  'sad':        'I am sad',
  'scared':     'I am scared',
  'frustrated': 'I am frustrated',
  'excited':    'I am excited',
  'angry':      'I am upset',
  'love':       'I love you',
  // Activities
  'music':      'I want to listen to music',
  'outside':    'I want to go outside',
  'home':       'I want to go home',
  'phone':      'I need my phone',
  'tv':         'I want to watch TV',
};


export default function Dashboard() {
  const rawUser = localStorage.getItem('alphavox_user');
  const user = rawUser ? JSON.parse(rawUser) : { name: 'Friend' };

  // Has this user ever seen the dashboard before?
  const tourKey    = `alphavox_tour_done_${user.name}`;
  const visitedKey = `alphavox_visited_${user.name}`;
  const isNew      = !localStorage.getItem(visitedKey);

  const [apiStatus, setApiStatus]   = useState<'checking'|'online'|'offline'>('checking');
  const [messages, setMessages]     = useState<Message[]>([]);
  const [inputText, setInputText]   = useState('');
  const [loading, setLoading]       = useState(false);
  const [aiActive, setAiActive]     = useState(false);
  const [cameraError, setCameraError] = useState('');
  const [waveBars, setWaveBars]     = useState(false);
  const [showTour, setShowTour]     = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  // ── Hands-Free Mode ─────────────────────────────────────────────
  const [handsFree, setHandsFree]   = useState(false);
  const [lastVoiceWord, setLastVoiceWord] = useState('');
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recognitionRef = useRef<any>(null);
  const chatRef  = useRef<HTMLDivElement>(null);

  // ── Health check ──────────────────────────────────────────────
  useEffect(() => {
    checkHealth().then(() => setApiStatus('online')).catch(() => setApiStatus('offline'));
  }, []);

  // ── Camera ────────────────────────────────────────────────────
  useEffect(() => {
    if (aiActive) {
      setCameraError('');
      navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(stream => {
          streamRef.current = stream;
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.play().catch(() => {});
          }
        })
        .catch(() => {
          setCameraError('Camera permission denied or unavailable');
          setAiActive(false);
        });
    } else {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
        streamRef.current = null;
      }
      if (videoRef.current) videoRef.current.srcObject = null;
    }
    return () => {
      streamRef.current?.getTracks().forEach(t => t.stop());
    };
  }, [aiActive]);

  // ── Hands-Free Mode: continuous speech recognition ─────────────
  // Designed for paralyzed users who cannot touch the screen.
  // They speak a keyword → AlphaVox speaks the full phrase.
  // No touch. No tap. Their voice is the only interface.
  useEffect(() => {
    const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRec) return;

    if (!handsFree) {
      recognitionRef.current?.stop();
      recognitionRef.current = null;
      return;
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const rec: any = new SpeechRec();
    rec.continuous      = true;
    rec.interimResults  = false;
    rec.lang            = 'en-US';
    rec.maxAlternatives = 3;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    rec.onresult = async (event: any) => {
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (!event.results[i].isFinal) continue;
        // Check all alternatives for a match
        for (let a = 0; a < event.results[i].length; a++) {
          const spoken  = event.results[i][a].transcript.toLowerCase().trim();
          // Match single-word or multi-word phrases
          const matched = Object.entries(VOICE_PHRASE_MAP).find(([key]) =>
            spoken === key || spoken.includes(key)
          );
          if (matched) {
            const [keyword, fullPhrase] = matched;
            setLastVoiceWord(keyword);
            setMessages(m => [...m,
              { role: 'user',  text: `🎙 "${spoken}"` },
              { role: 'alpha', text: fullPhrase },
            ]);
            await speakText(fullPhrase, { emotion: 'warm' });
            setTimeout(() => setLastVoiceWord(''), 3000);
            break;
          }
        }
      }
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    rec.onerror = (e: any) => {
      // 'no-speech' is normal — just restart
      if (e.error !== 'no-speech') {
        console.warn('Voice recognition error:', e.error);
      }
    };

    rec.onend = () => {
      // Auto-restart so it stays active continuously
      if (handsFree && recognitionRef.current) {
        try { rec.start(); } catch { /* already started */ }
      }
    };

    recognitionRef.current = rec;
    try { rec.start(); } catch { /* permission issue */ }

    return () => {
      rec.onend = null;
      rec.stop();
      recognitionRef.current = null;
    };
  }, [handsFree]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Greeting on first mount ───────────────────────────────────
  // Browsers block audio autoplay on fresh page load until the user has interacted.
  // trySpeak (timer): shows message + attempts audio — does NOT mark spoken or
  //   remove the listener, so the interaction path can still fire later.
  // doSpeak (gesture): marks spoken + removes listener, then plays with gesture ctx.
  useEffect(() => {
    const greeting = buildGreeting(user.name, isNew);
    let spoken = false;
    let msgShown = false;

    const showMsg = () => {
      if (msgShown) return;
      msgShown = true;
      setMessages([{ role: 'alpha', text: greeting }]);
      localStorage.setItem(visitedKey, 'true');
    };

    // Timer path: silent attempt — leaves listener active for gesture fallback
    const trySpeak = () => {
      showMsg();
      speakText(greeting, { emotion: 'warm' });
    };

    // Gesture path: guaranteed to work — marks spoken so it only fires once
    const doSpeak = () => {
      if (spoken) return;
      spoken = true;
      document.removeEventListener('pointerdown', doSpeak);
      document.removeEventListener('keydown', doSpeak);
      showMsg();
      speakText(greeting, { emotion: 'warm' });
      if (isNew && !localStorage.getItem(tourKey)) {
        setTimeout(() => setShowTour(true), 2400);
      }
    };

    const timer = setTimeout(trySpeak, 600);
    document.addEventListener('pointerdown', doSpeak, { once: true });
    document.addEventListener('keydown', doSpeak, { once: true });

    return () => {
      clearTimeout(timer);
      document.removeEventListener('pointerdown', doSpeak);
      document.removeEventListener('keydown', doSpeak);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Auto-scroll chat ──────────────────────────────────────────
  useEffect(() => {
    if (chatRef.current) chatRef.current.scrollTop = chatRef.current.scrollHeight;
  }, [messages]);

  // ── Send a message ────────────────────────────────────────────
  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || loading) return;
    const msg = text.trim();
    setMessages(m => [...m, { role: 'user', text: msg }]);
    setInputText('');
    setLoading(true);
    setWaveBars(true);
    try {
      const result = await processInput({
        text: msg,
        user_id: user.name.toLowerCase().replace(/\s+/g, '_'),
      });
      const reply = result.message ?? 'I heard you.';
      setMessages(m => [...m, { role: 'alpha', text: reply }]);
      await speakText(reply);
    } catch {
      const err = '(Connection issue — please check the backend is running)';
      setMessages(m => [...m, { role: 'alpha', text: err }]);
    } finally {
      setLoading(false);
      setWaveBars(false);
    }
  }, [loading, user.name]);

  const handleGesture = (gesture: string) => {
    sendMessage(GESTURE_PHRASES[gesture] ?? gesture);
  };

  const closeTour = () => {
    setShowTour(false);
    localStorage.setItem(tourKey, 'true');
  };

  const statusClass = apiStatus;

  return (
    <div className="container" style={{ paddingTop: '1.5rem' }}>
      {/* Onboarding tour */}
      {showTour && <OnboardingTour onClose={closeTour} />}

      {/* Greeting + status row */}
      <div className="mb-4 d-flex align-items-center justify-content-between flex-wrap gap-2">
        <div>
          <h1 className="display-5 mb-1">Welcome, {user.name}!</h1>
          <p className="lead">
            AlphaVox is here — your autonomous communication companion
          </p>
        </div>
        <div className="d-flex align-items-center gap-2 flex-wrap">
          {/* Hands-Free Mode toggle */}
          <button
            className={handsFree ? 'neural-btn' : 'cyber-btn'}
            onClick={() => setHandsFree(hf => !hf)}
            title="Hands-Free Mode — for users who cannot touch the screen"
            style={handsFree ? {
              background: 'rgba(0,180,216,0.15)',
              borderColor: 'var(--primary-color)',
              color: 'var(--primary-color)',
              animation: 'blink 2s infinite',
            } : {}}
          >
            <FontAwesomeIcon icon={handsFree ? faMicrophone : faUniversalAccess} className="me-1" />
            {handsFree ? 'Voice Active' : 'Hands-Free'}
          </button>

          <button
            className="cyber-btn"
            onClick={() => setShowTour(true)}
            title="Take the tour"
          >
            <FontAwesomeIcon icon={faInfoCircle} /> Tour
          </button>
          <span className={`api-pill ${statusClass}`}>
            <span className={`status-dot ${statusClass === 'online' ? 'speaking' : statusClass === 'checking' ? 'listening' : 'error'}`} />
            {apiStatus === 'online' ? 'Connected' : apiStatus === 'checking' ? 'Connecting…' : 'Offline'}
          </span>
        </div>
      </div>

      {/* Hands-Free active banner */}
      {handsFree && (
        <div style={{
          background: 'rgba(0,180,216,0.08)',
          border: '1px solid rgba(0,180,216,0.4)',
          padding: '0.9rem 1.25rem',
          marginBottom: '1rem',
          display: 'flex', alignItems: 'center', gap: '1rem',
          animation: 'blink 2.5s infinite',
        }}>
          <FontAwesomeIcon icon={faMicrophone} style={{ fontSize: '1.4rem', color: 'var(--primary-color)', flexShrink: 0 }} />
          <div>
            <p style={{ margin: 0, fontFamily: 'Share Tech Mono, monospace', color: 'var(--primary-color)', fontSize: '0.9rem', letterSpacing: '0.08em' }}>
              HANDS-FREE MODE ACTIVE — LISTENING
            </p>
            <p style={{ margin: 0, fontSize: '0.78rem', color: 'var(--muted-color)', marginTop: '0.2rem' }}>
              Just say a word: <strong style={{ color: 'var(--text-color)' }}>bathroom · hungry · help · water · pain · yes · no · tired · home…</strong>
            </p>
            {lastVoiceWord && (
              <p style={{ margin: 0, marginTop: '0.3rem', fontFamily: 'Share Tech Mono, monospace', color: 'var(--success-color)', fontSize: '0.8rem' }}>
                ✓ Heard: "{lastVoiceWord}"
              </p>
            )}
          </div>
          <button className="cyber-btn" style={{ marginLeft: 'auto', flexShrink: 0 }} onClick={() => setHandsFree(false)}>
            <FontAwesomeIcon icon={faMicrophoneSlash} /> Stop
          </button>
        </div>
      )}

      {/* Mission statement */}
      <div className="cyber-alert mb-4 d-flex gap-3 align-items-start">
        <FontAwesomeIcon icon={faHeartbeat} style={{ fontSize: '1.2rem', flexShrink: 0, marginTop: 2, color: 'var(--primary-color)' }} />
        <p style={{ margin: 0 }}>
          AlphaVox is built to empower expression, enhance social connection, and promote dignity
          through a being that listens, learns, and adapts to your unique communication style.
        </p>
      </div>

      {/* Main two-column layout */}
      <div className="row mb-4">
        {/* Vision Feed */}
        <div className="col-half">
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <span>Vision Feed</span>
              <span className={`video-feed-badge ${aiActive ? 'ai-status-active' : 'ai-status-inactive'}`}>
                {aiActive ? 'ACTIVE' : 'STANDBY'}
              </span>
            </div>
            <div className="card-body-cyber">
              <div className="video-feed-container" style={{ position: 'relative', background: '#000', borderRadius: 8, overflow: 'hidden', minHeight: 200 }}>
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  style={{
                    width: '100%', height: '100%', objectFit: 'cover',
                    display: aiActive ? 'block' : 'none',
                    transform: 'scaleX(-1)', // mirror so it feels natural
                  }}
                />
                {!aiActive && (
                  <div className="video-feed-placeholder">
                    <FontAwesomeIcon icon={faCamera} style={{ fontSize: '2rem', color: 'var(--border-color)' }} />
                    <span>Click Activate Vision to start camera</span>
                    {cameraError && <span style={{ color: 'var(--danger-color)', fontSize: '0.8rem' }}>{cameraError}</span>}
                  </div>
                )}
                {aiActive && (
                  <span style={{
                    position: 'absolute', top: 8, left: 10,
                    background: 'rgba(0,0,0,0.55)', padding: '2px 8px', borderRadius: 4,
                    color: 'var(--primary-color)', fontSize: '0.72rem', fontFamily: 'Share Tech Mono, monospace',
                    letterSpacing: '0.05em',
                  }}>● LIVE</span>
                )}
              </div>
              <div className="d-flex justify-content-between align-items-center mt-3">
                <div>
                  {!aiActive ? (
                    <button className="cyber-btn btn-success-cyber" onClick={() => setAiActive(true)}>
                      <FontAwesomeIcon icon={faPlay} /> Activate Vision
                    </button>
                  ) : (
                    <button className="cyber-btn btn-warning-cyber" onClick={() => setAiActive(false)}>
                      <FontAwesomeIcon icon={faPause} /> Pause Vision
                    </button>
                  )}
                </div>
                <Link to="/symbols" className="cyber-btn">
                  <FontAwesomeIcon icon={faThLarge} /> Symbol Board
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Communication panel */}
        <div className="col-half">
          <div className="system-card mb-4">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faComments} className="me-2" />Communication</span>
            </div>
            <div className="card-body-cyber">
              {/* Chat feed */}
              <div className="chat-feed mb-3" ref={chatRef}>
                {messages.map((m, i) => (
                  <div key={i}>
                    <div className={`chat-label ${m.role === 'user' ? 'text-right' : ''}`}>
                      {m.role === 'user' ? user.name : 'AlphaVox'}
                    </div>
                    <div className={`chat-bubble ${m.role}`}>{m.text}</div>
                  </div>
                ))}
                {loading && (
                  <div>
                    <div className="chat-label">AlphaVox</div>
                    <div className="chat-bubble alpha" style={{ fontStyle: 'italic', opacity: 0.7 }}>
                      listening…
                    </div>
                  </div>
                )}
              </div>

              {/* Voice visualization */}
              <div className="d-flex align-items-center justify-content-between mb-3">
                <button className="neural-btn" onClick={() => setWaveBars(b => !b)}>
                  <FontAwesomeIcon icon={faMicrophone} />
                  {waveBars ? 'Stop Recording' : 'Start Speaking'}
                </button>
                <div className="d-flex align-items-center">
                  <span className={`status-dot ${waveBars ? 'listening' : loading ? 'speaking' : ''}`} />
                  <span className="small text-muted">
                    {waveBars ? 'Listening…' : loading ? 'Speaking…' : 'Ready'}
                  </span>
                </div>
              </div>

              <div className="wave-container mb-3" style={{ justifyContent: 'flex-start' }}>
                {Array.from({ length: 15 }).map((_, i) => (
                  <div key={i} className={`wave-bar ${waveBars || loading ? 'active' : ''}`} />
                ))}
              </div>

              {/* Text input */}
              <form
                onSubmit={e => { e.preventDefault(); sendMessage(inputText); }}
                className="d-flex gap-2"
              >
                <div className="input-group-cyber" style={{ flex: 1 }}>
                  <span className="input-icon"><FontAwesomeIcon icon={faKeyboard} /></span>
                  <input
                    type="text"
                    className="cyber-input"
                    placeholder="Type a message…"
                    value={inputText}
                    onChange={e => setInputText(e.target.value)}
                    onKeyDown={e => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage(inputText);
                      }
                    }}
                  />
                </div>
                <button
                  type="submit"
                  className="neural-btn"
                  disabled={loading || !inputText.trim()}
                >
                  <FontAwesomeIcon icon={faPaperPlane} />
                </button>
              </form>
            </div>
          </div>

          {/* Quick Gestures */}
          <div className="system-card">
            <div className="card-header-cyber">
              <FontAwesomeIcon icon={faHandPaper} className="me-2" />Quick Gestures
            </div>
            <div className="card-body-cyber">
              <div className="gesture-grid">
                {GESTURES.map(({ id, icon, label }) => (
                  <button
                    key={id}
                    className="gesture-button"
                    onClick={() => handleGesture(id)}
                    aria-label={label}
                  >
                    <FontAwesomeIcon icon={icon} />
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* AlphaVox Neural System */}
      <div className="system-card mb-4">
        <div className="card-header-cyber">AlphaVox Core Systems</div>
        <div className="card-body-cyber">
          <div className="row mb-3">
            <div className="col-third">
              <div className="cyber-card p-4 text-center h-100">
                <FontAwesomeIcon icon={faGraduationCap} style={{ fontSize: '1.75rem', color: 'var(--primary-color)', marginBottom: '0.75rem' }} />
                <h5 className="cyber-text mb-2" style={{ fontSize: '0.85rem' }}>Learning Hub</h5>
                <p className="small text-muted mb-3">
                  Personalized vocabulary growth, topic exploration, and adaptive learning.
                </p>
                <Link to="/learning" className="cyber-btn">
                  <FontAwesomeIcon icon={faGraduationCap} /> Enter
                </Link>
              </div>
            </div>
            <div className="col-third">
              <div className="cyber-card p-4 text-center h-100">
                <FontAwesomeIcon icon={faComments} style={{ fontSize: '1.75rem', color: 'var(--success-color)', marginBottom: '0.75rem' }} />
                <h5 className="cyber-text mb-2" style={{ fontSize: '0.85rem' }}>Adaptive Conversation</h5>
                <p className="small text-muted mb-3">
                  Communication that adjusts complexity to meet the user exactly where they are.
                </p>
                <button className="cyber-btn btn-success-cyber">
                  <FontAwesomeIcon icon={faComments} /> Start Talking
                </button>
              </div>
            </div>
            <div className="col-third">
              <div className="cyber-card p-4 text-center h-100">
                <FontAwesomeIcon icon={faThLarge} style={{ fontSize: '1.75rem', color: 'var(--accent-color)', marginBottom: '0.75rem' }} />
                <h5 className="cyber-text mb-2" style={{ fontSize: '0.85rem' }}>Symbol Communication</h5>
                <p className="small text-muted mb-3">
                  Customizable symbol boards with expressive, emotionally-aware voice output.
                </p>
                <Link to="/symbols" className="cyber-btn">
                  <FontAwesomeIcon icon={faThLarge} /> Open Board
                </Link>
              </div>
            </div>
          </div>

          <div className="row">
            <div className="col-half">
              <div className="cyber-card p-4">
                <h5 className="cyber-text mb-3" style={{ fontSize: '0.85rem', color: 'var(--warning-color)' }}>
                  <FontAwesomeIcon icon={faBrain} className="me-2" />SoulForge™ — Adaptive Memory
                </h5>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {[
                    { icon: faSyncAlt,  text: 'Biological-inspired long-term potentiation (LTP)' },
                    { icon: faChartLine,text: 'Continuously adapts from every interaction' },
                    { icon: faHeartbeat,text: 'Learns what works emotionally for this person' },
                  ].map(({ icon, text }) => (
                    <li key={text} className="small d-flex align-items-center gap-2">
                      <FontAwesomeIcon icon={icon} style={{ color: 'var(--primary-color)', flexShrink: 0 }} />
                      {text}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="col-half">
              <div className="cyber-card p-4">
                <h5 className="cyber-text mb-3" style={{ fontSize: '0.85rem', color: 'var(--danger-color)' }}>
                  <FontAwesomeIcon icon={faHeartbeat} className="me-2" />ToneScore™ — Emotion-Aware Voice
                </h5>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {[
                    { icon: faSmile,       text: 'Matches tone to the emotional moment' },
                    { icon: faVolumeUp,    text: 'Softer when upset, warm when celebrating' },
                    { icon: faCommentDots, text: 'Responses that honor where the user is' },
                  ].map(({ icon, text }) => (
                    <li key={text} className="small d-flex align-items-center gap-2">
                      <FontAwesomeIcon icon={icon} style={{ color: 'var(--warning-color)', flexShrink: 0 }} />
                      {text}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
