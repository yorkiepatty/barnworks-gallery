import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faHandPaper, faEye, faVolumeUp, faThLarge,
  faPowerOff, faUser, faSignLanguage, faBrain,
  faComments, faFingerprint, faCloud, faDesktop, faSync,
} from '@fortawesome/free-solid-svg-icons';

const FEATURE_ICONS = [
  { icon: faHandPaper, label: 'Gestures' },
  { icon: faEye,       label: 'Eye Tracking' },
  { icon: faVolumeUp,  label: 'Vocalizations' },
  { icon: faThLarge,   label: 'Symbol Boards' },
];

const ARCH_CARDS = [
  { icon: faSignLanguage, title: 'Input Processing',    desc: 'Multi-modal input through touch, eye-tracking, and gesture recognition.' },
  { icon: faBrain,        title: 'Intent Understanding', desc: 'Contextual memory engine that interprets user intent and maintains conversation context.' },
  { icon: faComments,     title: 'Expression Output',   desc: 'Emotionally-aware speech synthesis that adjusts tone and expression to match intent.' },
  { icon: faFingerprint,  title: 'User Modeling',       desc: 'Personalization layer that adapts to individual communication styles and preferences.' },
  { icon: faCloud,        title: 'Cloud Integration',   desc: 'Secure data synchronization across devices with user control over privacy and sharing.' },
  { icon: faDesktop,      title: 'Accessible Interface',desc: 'AAC-style grid interface with customizable symbols and adaptive input methods.' },
  { icon: faSync,         title: 'Self-Learning AI',    desc: 'Continuous adaptation through analysis of interaction patterns and user feedback.' },
];

export default function Home() {
  const [name, setName] = useState('');
  const navigate = useNavigate();

  // If already logged in, redirect
  useEffect(() => {
    const user = localStorage.getItem('alphavox_user');
    if (user) navigate('/dashboard', { replace: true });
  }, [navigate]);

  const handleStart = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    localStorage.setItem('alphavox_user', JSON.stringify({ name: name.trim(), created: new Date().toISOString() }));
    navigate('/dashboard');
  };

  return (
    <div style={{ position: 'relative' }}>
      <div className="cyber-grid-overlay" />

      <div className="container" style={{ position: 'relative', zIndex: 1, paddingTop: '2rem', paddingBottom: '3rem' }}>
        {/* ── Welcome Card ── */}
        <div style={{ maxWidth: 860, margin: '0 auto' }}>
          <div className="system-card p-5" style={{ padding: '2.5rem' }}>
            <div className="processor-bar mb-4" />

            <div className="text-center mb-5">
              <h1 className="cyber-glow-text mb-3">AlphaVox</h1>
              <p className="cyber-text mb-4" style={{ color: 'var(--primary-color)', fontSize: '1rem', letterSpacing: '0.06em' }}>
                Multi-modal · Neurodiverse-inclusive · Speech-generating AI
              </p>
              <p className="lead mb-5">
                AlphaVox empowers expression, enhances social connection, and promotes dignity through technology
                that listens, learns, and adapts.
              </p>

              {/* Feature Icons */}
              <div style={{ display: 'flex', justifyContent: 'center', gap: '2.5rem', flexWrap: 'wrap', marginBottom: '2.5rem' }}>
                {FEATURE_ICONS.map(({ icon, label }) => (
                  <div key={label} className="text-center">
                    <div className="communication-icon">
                      <FontAwesomeIcon icon={icon} style={{ fontSize: '2.5rem', color: 'var(--primary-color)' }} />
                      <div className="pulse-ring" />
                    </div>
                    <p className="cyber-text mt-2" style={{ fontSize: '0.82rem', color: 'var(--accent-color)' }}>{label}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Init Form */}
            <div className="system-card" style={{ padding: '1.75rem', maxWidth: 480, margin: '0 auto' }}>
              <div className="processor-bar mb-3" />
              <h3 className="cyber-title text-center mb-4" style={{ fontSize: '1rem' }}>
                Initialize Communication System
              </h3>
              <form onSubmit={handleStart}>
                <div className="mb-4">
                  <label className="form-label-cyber">User Identification</label>
                  <div className="input-group-cyber">
                    <span className="input-icon"><FontAwesomeIcon icon={faUser} /></span>
                    <input
                      type="text"
                      className="cyber-input"
                      placeholder="Enter your name"
                      value={name}
                      onChange={e => setName(e.target.value)}
                      autoFocus
                      required
                    />
                  </div>
                </div>
                <button type="submit" className="neural-btn lg w-100" style={{ justifyContent: 'center' }}>
                  <FontAwesomeIcon icon={faPowerOff} />
                  Initialize System
                </button>
              </form>
            </div>
          </div>

          {/* ── Architecture Cards ── */}
          <div style={{ marginTop: '2.5rem' }}>
            <h2 className="cyber-title text-center mb-4" style={{ fontSize: '1.25rem' }}>Core System Architecture</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1rem' }}>
              {ARCH_CARDS.map(({ icon, title, desc }) => (
                <div key={title} className="cyber-card" style={{ padding: '1.25rem', textAlign: 'center' }}>
                  <FontAwesomeIcon icon={icon} style={{ fontSize: '1.75rem', color: 'var(--primary-color)', marginBottom: '0.75rem' }} />
                  <h5 className="cyber-text mb-2" style={{ fontSize: '0.82rem' }}>{title}</h5>
                  <p className="small text-muted">{desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
