import { useState } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave, faArrowLeft, faSync } from '@fortawesome/free-solid-svg-icons';

interface Prefs {
  gesture_sensitivity: number;
  eye_tracking_sensitivity: number;
  sound_sensitivity: number;
  response_speed: number;
  voice_type: string;
  symbol_system: string;
  preferred_emotion_display: boolean;
  multimodal_processing: boolean;
}

const DEFAULT_PREFS: Prefs = {
  gesture_sensitivity: 0.8,
  eye_tracking_sensitivity: 0.8,
  sound_sensitivity: 0.7,
  response_speed: 1.0,
  voice_type: 'default',
  symbol_system: 'default',
  preferred_emotion_display: true,
  multimodal_processing: true,
};

const RECENT_ACTIVITY = [
  { time: '5 min ago',  action: 'Used gesture: thumbs_up',  detail: 'Intent: like (Confidence: 92.3%)' },
  { time: '12 min ago', action: 'Used symbol: food',        detail: 'Intent: hungry (Confidence: 89.7%)' },
  { time: '25 min ago', action: 'Text input',               detail: '"I need help with this"' },
];

function SliderRow({ label, id, min, max, step, value, onChange }: {
  label: string; id: string; min: number; max: number; step: number;
  value: number; onChange: (v: number) => void;
}) {
  return (
    <div className="mb-3">
      <label className="form-label-cyber" htmlFor={id}>{label}</label>
      <div className="slider-row">
        <input
          id={id} type="range" className="cyber-range"
          min={min} max={max} step={step} value={value}
          onChange={e => onChange(parseFloat(e.target.value))}
        />
        <span className="slider-value">{value.toFixed(1)}</span>
      </div>
    </div>
  );
}

export default function Profile() {
  const rawUser = localStorage.getItem('alphavox_user');
  const user = rawUser ? JSON.parse(rawUser) : { name: 'User', created: new Date().toISOString() };

  const savedPrefs = localStorage.getItem('alphavox_prefs');
  const [prefs, setPrefs] = useState<Prefs>(savedPrefs ? JSON.parse(savedPrefs) : DEFAULT_PREFS);
  const [saved, setSaved] = useState(false);

  const update = (key: keyof Prefs, value: Prefs[keyof Prefs]) => {
    setPrefs(p => ({ ...p, [key]: value }));
    setSaved(false);
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('alphavox_prefs', JSON.stringify(prefs));
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="container" style={{ paddingTop: '1.5rem' }}>
      <div className="mb-4">
        <h1 className="display-5 mb-1">User Profile</h1>
        <p className="lead">Customize your communication preferences</p>
      </div>

      <div className="row">
        {/* Preferences form */}
        <div style={{ flex: '1 1 520px', minWidth: 0 }}>
          <div className="system-card mb-4">
            <div className="card-header-cyber">Preferences</div>
            <div className="card-body-cyber">
              <form onSubmit={handleSave}>

                <h6 className="cyber-title mb-3" style={{ fontSize: '0.82rem' }}>Input Sensitivity</h6>
                <div className="row mb-4">
                  <div className="col">
                    <SliderRow label="Gesture Sensitivity" id="gesture-s"
                      min={0.1} max={1.0} step={0.1} value={prefs.gesture_sensitivity}
                      onChange={v => update('gesture_sensitivity', v)} />
                  </div>
                  <div className="col">
                    <SliderRow label="Eye Tracking Sensitivity" id="eye-s"
                      min={0.1} max={1.0} step={0.1} value={prefs.eye_tracking_sensitivity}
                      onChange={v => update('eye_tracking_sensitivity', v)} />
                  </div>
                  <div className="col">
                    <SliderRow label="Sound Sensitivity" id="sound-s"
                      min={0.1} max={1.0} step={0.1} value={prefs.sound_sensitivity}
                      onChange={v => update('sound_sensitivity', v)} />
                  </div>
                </div>

                <h6 className="cyber-title mb-3" style={{ fontSize: '0.82rem' }}>Output Settings</h6>
                <div className="row mb-4">
                  <div className="col">
                    <label className="form-label-cyber">Voice Type</label>
                    <select className="cyber-select" value={prefs.voice_type}
                      onChange={e => update('voice_type', e.target.value)}>
                      <option value="default">Default</option>
                      <option value="child">Child</option>
                      <option value="male">Adult Male</option>
                      <option value="female">Adult Female</option>
                    </select>
                  </div>
                  <div className="col">
                    <SliderRow label="Speech Rate" id="speech-rate"
                      min={0.5} max={1.5} step={0.1} value={prefs.response_speed}
                      onChange={v => update('response_speed', v)} />
                  </div>
                </div>

                <h6 className="cyber-title mb-3" style={{ fontSize: '0.82rem' }}>System Preferences</h6>
                <div className="row mb-4">
                  <div className="col">
                    <label className="form-label-cyber">Symbol System</label>
                    <select className="cyber-select" value={prefs.symbol_system}
                      onChange={e => update('symbol_system', e.target.value)}>
                      <option value="default">Default</option>
                      <option value="pcs">PCS (Picture Communication Symbols)</option>
                      <option value="arasaac">ARASAAC</option>
                      <option value="bliss">Blissymbols</option>
                    </select>
                  </div>
                  <div className="col">
                    <div className="mb-3">
                      <label className="form-label-cyber mb-2">Display Options</label>
                      <div className="d-flex flex-column gap-2">
                        <label className="d-flex align-items-center gap-2" style={{ cursor: 'pointer', fontSize: '0.88rem' }}>
                          <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: 16, height: 16 }}
                            checked={prefs.preferred_emotion_display}
                            onChange={e => update('preferred_emotion_display', e.target.checked)} />
                          Show Emotion Indicators
                        </label>
                        <label className="d-flex align-items-center gap-2" style={{ cursor: 'pointer', fontSize: '0.88rem' }}>
                          <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: 16, height: 16 }}
                            checked={prefs.multimodal_processing}
                            onChange={e => update('multimodal_processing', e.target.checked)} />
                          Enable Multimodal Processing
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="d-flex justify-content-end gap-2">
                  {saved && <span className="badge-success" style={{ padding: '0.4rem 0.8rem', borderRadius: 6 }}>✓ Saved!</span>}
                  <button type="submit" className="neural-btn">
                    <FontAwesomeIcon icon={faSave} /> Save Preferences
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div style={{ flex: '0 0 280px', minWidth: 240 }}>
          {/* User info */}
          <div className="system-card mb-4">
            <div className="card-header-cyber">User Information</div>
            <div className="card-body-cyber">
              <h4 className="mb-2">{user.name}</h4>
              <p className="small text-muted mb-1">Member since: {new Date(user.created || Date.now()).toLocaleDateString()}</p>
              <hr style={{ borderColor: 'var(--border-color)', margin: '0.75rem 0' }} />
              <p className="small text-muted mb-2">Your profile contains preferences that help AlphaVox adapt to your communication style.</p>
              <p className="small text-muted d-flex gap-2 align-items-start">
                <FontAwesomeIcon icon={faSync} style={{ color: 'var(--primary-color)', flexShrink: 0, marginTop: 2 }} />
                <span><strong>Adaptive Learning:</strong> AlphaVox learns from your interactions and may suggest preference updates.</span>
              </p>
              <Link to="/dashboard" className="cyber-btn w-100 mt-3" style={{ justifyContent: 'center' }}>
                <FontAwesomeIcon icon={faArrowLeft} /> Back to Home
              </Link>
            </div>
          </div>

          {/* Recent activity */}
          <div className="system-card">
            <div className="card-header-cyber">Recent Activity</div>
            <ul className="list-cyber">
              {RECENT_ACTIVITY.map((a, i) => (
                <li key={i} style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '0.15rem' }}>
                  <div className="d-flex justify-content-between w-100">
                    <span className="fw-500" style={{ fontSize: '0.83rem' }}>{a.action}</span>
                    <span className="small text-muted">{a.time}</span>
                  </div>
                  <span className="small text-muted">{a.detail}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
