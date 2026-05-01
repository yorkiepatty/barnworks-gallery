import { useState, useCallback } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faUtensils, faTint, faToilet, faPills,
  faSmile, faSadTear, faExclamationTriangle, faBed,
  faCheckCircle, faTimesCircle, faHandsHelping, faQuestion,
  faGamepad, faMusic, faBook, faLeaf,
  faPaperPlane, faVolumeUp, faTrash, faPlusCircle,
} from '@fortawesome/free-solid-svg-icons';
import { synthesizeTTS } from '../services/api';

interface SymbolItem {
  id: string;
  icon: typeof faUtensils;
  label: string;
  phrase: string;
  color: string;
  category: string;
  custom?: boolean;
}

const DEFAULT_SYMBOLS: SymbolItem[] = [
  // Basic Needs
  { id: 'food',     icon: faUtensils,          label: 'Food',      phrase: 'I am hungry, I need food.',       color: 'var(--warning-color)', category: 'Basic Needs' },
  { id: 'drink',    icon: faTint,               label: 'Drink',     phrase: 'I am thirsty, I need a drink.',   color: 'var(--primary-color)', category: 'Basic Needs' },
  { id: 'bathroom', icon: faToilet,             label: 'Bathroom',  phrase: 'I need to use the bathroom.',     color: 'var(--success-color)', category: 'Basic Needs' },
  { id: 'medicine', icon: faPills,              label: 'Medicine',  phrase: 'I need my medicine.',             color: 'var(--danger-color)',  category: 'Basic Needs' },
  // Feelings
  { id: 'happy',   icon: faSmile,              label: 'Happy',     phrase: 'I am feeling happy.',             color: 'var(--warning-color)', category: 'Feelings' },
  { id: 'sad',     icon: faSadTear,            label: 'Sad',       phrase: 'I am feeling sad.',               color: 'var(--primary-color)', category: 'Feelings' },
  { id: 'pain',    icon: faExclamationTriangle,label: 'Pain',      phrase: 'I am in pain, I need help.',      color: 'var(--danger-color)',  category: 'Feelings' },
  { id: 'tired',   icon: faBed,                label: 'Tired',     phrase: 'I am tired, I need rest.',        color: 'var(--muted-color)',   category: 'Feelings' },
  // Communication
  { id: 'yes',     icon: faCheckCircle,        label: 'Yes',       phrase: 'Yes.',                            color: 'var(--success-color)', category: 'Communication' },
  { id: 'no',      icon: faTimesCircle,        label: 'No',        phrase: 'No.',                             color: 'var(--danger-color)',  category: 'Communication' },
  { id: 'help',    icon: faHandsHelping,       label: 'Help',      phrase: 'I need help please.',             color: 'var(--primary-color)', category: 'Communication' },
  { id: 'question',icon: faQuestion,           label: 'Question',  phrase: 'I have a question.',              color: 'var(--warning-color)', category: 'Communication' },
  // Activities
  { id: 'play',    icon: faGamepad,            label: 'Play',      phrase: 'I want to play.',                 color: 'var(--success-color)', category: 'Activities' },
  { id: 'music',   icon: faMusic,              label: 'Music',     phrase: 'I want to listen to music.',      color: 'var(--primary-color)', category: 'Activities' },
  { id: 'book',    icon: faBook,               label: 'Book',      phrase: 'I want to read a book.',          color: 'var(--warning-color)', category: 'Activities' },
  { id: 'outside', icon: faLeaf,              label: 'Outside',   phrase: 'I want to go outside.',           color: 'var(--success-color)', category: 'Activities' },
];

const CATEGORIES = ['All', 'Basic Needs', 'Feelings', 'Communication', 'Activities', 'Custom'];

export default function Symbols() {
  const saved = localStorage.getItem('alphavox_symbols');
  const [symbols, setSymbols]         = useState<SymbolItem[]>(saved ? JSON.parse(saved) : DEFAULT_SYMBOLS);
  const [selected, setSelected]       = useState<SymbolItem[]>([]);
  const [speaking, setSpeaking]       = useState<string | null>(null);
  const [activeCategory, setCategory] = useState('All');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newLabel, setNewLabel]       = useState('');
  const [newPhrase, setNewPhrase]     = useState('');

  const saveToStorage = (s: SymbolItem[]) => {
    localStorage.setItem('alphavox_symbols', JSON.stringify(s));
    setSymbols(s);
  };

  const speakPhrase = useCallback(async (phrase: string, id: string) => {
    setSpeaking(id);
    try {
      await synthesizeTTS({ text: phrase });
    } catch {
      // Fallback: browser TTS
      if ('speechSynthesis' in window) {
        const utt = new SpeechSynthesisUtterance(phrase);
        window.speechSynthesis.speak(utt);
      }
    } finally {
      setTimeout(() => setSpeaking(null), 1500);
    }
  }, []);

  const handleSymbolClick = (sym: SymbolItem) => {
    setSelected(prev => [...prev, sym]);
    speakPhrase(sym.phrase, sym.id);
  };

  const speakSelected = () => {
    if (!selected.length) return;
    const phrase = selected.map(s => s.phrase).join(' ');
    speakPhrase(phrase, '__combined__');
  };

  const clearSelected = () => setSelected([]);

  const addCustom = () => {
    if (!newLabel.trim()) return;
    const custom: SymbolItem = {
      id: `custom_${Date.now()}`,
      icon: faPlusCircle,
      label: newLabel.trim(),
      phrase: newPhrase.trim() || newLabel.trim(),
      color: 'var(--accent-color)',
      category: 'Custom',
      custom: true,
    };
    saveToStorage([...symbols, custom]);
    setNewLabel('');
    setNewPhrase('');
    setShowAddForm(false);
  };

  const removeSymbol = (id: string) => {
    saveToStorage(symbols.filter(s => s.id !== id));
    setSelected(prev => prev.filter(s => s.id !== id));
  };

  const visible = symbols.filter(s =>
    activeCategory === 'All' ||
    s.category === activeCategory ||
    (activeCategory === 'Custom' && s.custom)
  );

  const categoryGroups = activeCategory === 'All'
    ? CATEGORIES.slice(1).filter(c => visible.some(s => s.category === c || (c === 'Custom' && s.custom)))
    : [activeCategory];

  return (
    <div className="container" style={{ paddingTop: '1.5rem' }}>
      <div className="mb-4">
        <h1 className="display-5 mb-1 cyber-title">Symbol Communication</h1>
        <p className="lead">Select symbols to communicate your needs and thoughts</p>
      </div>

      <div className="row">
        {/* Left: Symbol board */}
        <div style={{ flex: '1 1 600px', minWidth: 0 }}>
          {/* Category tabs */}
          <div className="d-flex gap-2 flex-wrap mb-3">
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                className={activeCategory === cat ? 'neural-btn' : 'cyber-btn'}
                onClick={() => setCategory(cat)}
              >
                {cat}
              </button>
            ))}
            <button className="cyber-btn btn-success-cyber" onClick={() => setShowAddForm(f => !f)}>
              <FontAwesomeIcon icon={faPlusCircle} /> Add Symbol
            </button>
          </div>

          {/* Add custom form */}
          {showAddForm && (
            <div className="system-card p-4 mb-3">
              <div className="processor-bar mb-3" />
              <h6 className="cyber-title mb-3">New Custom Symbol</h6>
              <div className="row" style={{ gap: '0.75rem' }}>
                <div className="col">
                  <label className="form-label-cyber">Label</label>
                  <input className="cyber-input" placeholder="e.g. Water" value={newLabel} onChange={e => setNewLabel(e.target.value)} />
                </div>
                <div className="col">
                  <label className="form-label-cyber">Spoken phrase (optional)</label>
                  <input className="cyber-input" placeholder="e.g. I need water please" value={newPhrase} onChange={e => setNewPhrase(e.target.value)} />
                </div>
              </div>
              <div className="d-flex gap-2 mt-3">
                <button className="neural-btn" onClick={addCustom}>Save Symbol</button>
                <button className="cyber-btn" onClick={() => setShowAddForm(false)}>Cancel</button>
              </div>
            </div>
          )}

          {/* Symbol grid by category */}
          {categoryGroups.map(cat => {
            const catSymbols = visible.filter(s => s.category === cat || (cat === 'Custom' && s.custom));
            if (!catSymbols.length) return null;
            return (
              <div key={cat} className="mb-4">
                {activeCategory === 'All' && (
                  <p className="symbol-category-label">{cat}</p>
                )}
                <div className="symbol-grid">
                  {catSymbols.map(sym => (
                    <div key={sym.id} style={{ position: 'relative' }}>
                      <button
                        className={`symbol-card w-100 ${speaking === sym.id ? 'speaking' : ''}`}
                        onClick={() => handleSymbolClick(sym)}
                        aria-label={sym.label}
                      >
                        <FontAwesomeIcon icon={sym.icon} style={{ color: sym.color }} />
                        <span>{sym.label}</span>
                      </button>
                      {sym.custom && (
                        <button
                          onClick={() => removeSymbol(sym.id)}
                          style={{
                            position: 'absolute', top: 3, right: 3, background: 'none', border: 'none',
                            color: 'var(--danger-color)', cursor: 'pointer', fontSize: '0.7rem', padding: '2px',
                          }}
                          aria-label="Remove"
                        >✕</button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Right: Communication bar + selected */}
        <div style={{ flex: '0 0 280px', minWidth: 240 }}>
          {/* Communication bar */}
          <div className="system-card mb-3">
            <div className="card-header-cyber">
              <span><FontAwesomeIcon icon={faVolumeUp} className="me-2" />Selected Phrases</span>
            </div>
            <div className="card-body-cyber">
              {selected.length === 0 ? (
                <p className="small text-muted text-center" style={{ padding: '1rem 0' }}>
                  Tap symbols below to build a message
                </p>
              ) : (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '0.75rem' }}>
                  {selected.map((s, i) => (
                    <span key={i} className="badge-cyber" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                      <FontAwesomeIcon icon={s.icon} style={{ color: s.color, fontSize: '0.75rem' }} />
                      {s.label}
                    </span>
                  ))}
                </div>
              )}
              <div className="d-flex gap-2 flex-wrap">
                <button className="neural-btn" onClick={speakSelected} disabled={!selected.length}>
                  <FontAwesomeIcon icon={faPaperPlane} /> Speak
                </button>
                <button className="cyber-btn btn-danger-cyber" onClick={clearSelected} disabled={!selected.length}>
                  <FontAwesomeIcon icon={faTrash} /> Clear
                </button>
              </div>
            </div>
          </div>

          {/* Grid size hint */}
          <div className="system-card">
            <div className="card-header-cyber">Controls</div>
            <div className="card-body-cyber">
              <p className="small text-muted mb-2">Symbol System</p>
              <select className="cyber-select mb-3">
                <option>Default</option>
                <option>PCS (Picture Communication Symbols)</option>
                <option>ARASAAC</option>
                <option>Blissymbols</option>
              </select>
              <p className="small text-muted mb-2">Grid Size</p>
              <div className="d-flex gap-2">
                {['2×2','3×3','4×4'].map(g => (
                  <button key={g} className="cyber-btn" style={{ fontSize: '0.72rem', padding: '0.25rem 0.5rem' }}>{g}</button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
