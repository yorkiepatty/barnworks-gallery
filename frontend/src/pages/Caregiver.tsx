import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faDownload, faShareAlt, faSmile, faFrown,
  faExclamationCircle, faMeh, faChevronDown,
  faCommentDots, faTrophy, faLightbulb,
} from '@fortawesome/free-solid-svg-icons';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, PointElement, LineElement,
  ArcElement, Tooltip, Legend, Filler,
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Tooltip, Legend, Filler);

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const COMM_DATA = [12, 19, 8, 15, 22, 18, 25];

const LINE_DATA = {
  labels: DAYS,
  datasets: [{
    label: 'Communications',
    data: COMM_DATA,
    borderColor: '#00b4d8',
    backgroundColor: 'rgba(0, 180, 216, 0.1)',
    tension: 0.4,
    fill: true,
    pointBackgroundColor: '#00b4d8',
    pointRadius: 4,
  }],
};

const DOUGHNUT_DATA = {
  labels: ['Text', 'Gestures', 'Symbols', 'Voice'],
  datasets: [{
    data: [35, 25, 30, 10],
    backgroundColor: ['#00b4d8', '#2ec4b6', '#f9c74f', '#ef233c'],
    borderColor: '#1a1a2e',
    borderWidth: 2,
  }],
};

const CHART_OPTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { labels: { color: '#ffffff', font: { size: 11 } } } },
  scales: {
    x: { ticks: { color: '#6c757d' }, grid: { color: 'rgba(255,255,255,0.05)' } },
    y: { ticks: { color: '#6c757d' }, grid: { color: 'rgba(255,255,255,0.05)' } },
  },
};

const DOUGHNUT_OPTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' as const, labels: { color: '#ffffff', font: { size: 11 }, padding: 16 } } },
};

const INTERACTIONS = [
  { time: '14:32 - 28 Feb', type: 'text',    content: 'I am hungry',           intent: 'need_food',    emotion: 'positive' },
  { time: '14:15 - 28 Feb', type: 'gesture',  content: 'thumbs_up',             intent: 'like',         emotion: 'positive' },
  { time: '13:48 - 28 Feb', type: 'symbol',   content: 'food',                  intent: 'hungry',       emotion: 'neutral'  },
  { time: '13:20 - 28 Feb', type: 'text',    content: 'I need help with this', intent: 'need_help',    emotion: 'urgent'   },
  { time: '12:55 - 28 Feb', type: 'symbol',   content: 'bathroom',              intent: 'bathroom',     emotion: 'neutral'  },
];

const FREQUENT_EXPRESSIONS = [
  { text: 'I need help', count: 8 },
  { text: 'I am hungry', count: 6 },
  { text: 'Yes', count: 15 },
  { text: 'No', count: 11 },
  { text: 'I want to play', count: 4 },
];

const PROGRESS = [
  { label: 'Vocabulary Growth', value: 72, color: 'var(--primary-color)' },
  { label: 'Expression Complexity', value: 58, color: 'var(--success-color)' },
  { label: 'Multimodal Usage', value: 85, color: 'var(--warning-color)' },
];

const AI_SUGGESTIONS = [
  'Continue encouraging use of the symbol board for daily needs.',
  'Consider introducing more complex sentence structures.',
  'The user responds well to gesture-based communication in the mornings.',
];

function TypeBadge({ type }: { type: string }) {
  const map: Record<string, string> = { text: 'badge-cyber', gesture: 'badge-success', symbol: 'badge-info', voice: 'badge-warning' };
  return <span className={`badge-cyber ${map[type] ?? 'badge-secondary'}`} style={{ textTransform: 'capitalize' }}>{type}</span>;
}

function EmotionIcon({ emotion }: { emotion: string }) {
  if (emotion === 'positive') return <FontAwesomeIcon icon={faSmile} style={{ color: 'var(--success-color)' }} />;
  if (emotion === 'negative') return <FontAwesomeIcon icon={faFrown} style={{ color: 'var(--warning-color)' }} />;
  if (emotion === 'urgent')   return <FontAwesomeIcon icon={faExclamationCircle} style={{ color: 'var(--danger-color)' }} />;
  return <FontAwesomeIcon icon={faMeh} style={{ color: 'var(--muted-color)' }} />;
}

export default function Caregiver() {
  const rawUser = localStorage.getItem('alphavox_user');
  const user = rawUser ? JSON.parse(rawUser) : { name: 'User', created: new Date().toISOString() };
  const [histFilter, setHistFilter] = useState<string>('all');

  const filteredInteractions = histFilter === 'all'
    ? INTERACTIONS
    : INTERACTIONS.filter(i => i.type === histFilter);

  return (
    <div className="container" style={{ paddingTop: '1.5rem' }}>
      <div className="mb-4 d-flex justify-content-between align-items-center flex-wrap gap-2">
        <div>
          <h1 className="display-5 mb-1">Caregiver Dashboard</h1>
          <p className="lead">Access communication analytics and user data for continued support</p>
        </div>
        <div className="d-flex gap-2">
          <button className="cyber-btn"><FontAwesomeIcon icon={faDownload} className="me-2" />Export Data</button>
          <button className="cyber-btn btn-success-cyber"><FontAwesomeIcon icon={faShareAlt} className="me-2" />Share with Provider</button>
        </div>
      </div>

      {/* User info */}
      <div className="system-card mb-4">
        <div className="card-header-cyber">User Information</div>
        <div className="card-body-cyber">
          <div className="row">
            <div className="col">
              <p className="small text-muted mb-1">Client Name</p>
              <h4 className="mb-3">{user.name}</h4>
              <p className="small text-muted mb-1">Using AlphaVox Since</p>
              <p>{new Date(user.created || Date.now()).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</p>
            </div>
            <div className="col">
              <p className="small text-muted mb-1">Communication Profile</p>
              <div className="d-flex gap-2 mb-3">
                <span className="badge-cyber">Text Primary</span>
                <span className="badge-secondary badge-cyber">Symbol Secondary</span>
              </div>
              <p className="small text-muted mb-1">Key Observations</p>
              <p className="small">Strong engagement with symbol board; improving text input usage over past week.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="row mb-4">
        <div className="col-half">
          <div className="system-card">
            <div className="card-header-cyber">
              <span>Communication Frequency</span>
              <div className="d-flex gap-1">
                {['Week','Month','Year'].map(p => (
                  <button key={p} className="cyber-btn" style={{ padding: '0.15rem 0.5rem', fontSize: '0.72rem' }}>{p}</button>
                ))}
              </div>
            </div>
            <div className="card-body-cyber" style={{ height: 280 }}>
              <Line data={LINE_DATA} options={CHART_OPTS as any} />
            </div>
          </div>
        </div>
        <div className="col-half">
          <div className="system-card">
            <div className="card-header-cyber">Communication Methods</div>
            <div className="card-body-cyber" style={{ height: 280 }}>
              <Doughnut data={DOUGHNUT_DATA} options={DOUGHNUT_OPTS} />
            </div>
          </div>
        </div>
      </div>

      {/* History + sidebar */}
      <div className="row mb-4">
        <div style={{ flex: '1 1 500px', minWidth: 0 }}>
          <div className="system-card">
            <div className="card-header-cyber">
              <span>Communication History</span>
              <div className="d-flex gap-1">
                {['all','text','gesture','symbol'].map(f => (
                  <button key={f} className={histFilter === f ? 'neural-btn' : 'cyber-btn'}
                    style={{ padding: '0.15rem 0.5rem', fontSize: '0.72rem', textTransform: 'capitalize' }}
                    onClick={() => setHistFilter(f)}>
                    {f === 'all' ? 'All' : f.charAt(0).toUpperCase() + f.slice(1)}
                  </button>
                ))}
              </div>
            </div>
            <div className="card-body-cyber overflow-auto">
              <table className="cyber-table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Type</th>
                    <th>Content</th>
                    <th>Intent</th>
                    <th>Emotion</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredInteractions.map((i, idx) => (
                    <tr key={idx}>
                      <td className="small text-muted">{i.time}</td>
                      <td><TypeBadge type={i.type} /></td>
                      <td className="small">{i.content}</td>
                      <td className="small text-muted">{i.intent}</td>
                      <td><EmotionIcon emotion={i.emotion} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="card-body-cyber" style={{ borderTop: '1px solid var(--border-color)', paddingTop: '0.75rem' }}>
              <button className="cyber-btn">
                Load More <FontAwesomeIcon icon={faChevronDown} className="ms-1" />
              </button>
            </div>
          </div>
        </div>

        <div style={{ flex: '0 0 280px', minWidth: 240 }}>
          {/* Frequent expressions */}
          <div className="system-card mb-3">
            <div className="card-header-cyber">
              <FontAwesomeIcon icon={faCommentDots} className="me-2" />Frequent Expressions
            </div>
            <ul className="list-cyber">
              {FREQUENT_EXPRESSIONS.map((e, i) => (
                <li key={i}>
                  <span>{e.text}</span>
                  <span className="badge-cyber">{e.count}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Progress indicators */}
          <div className="system-card mb-3">
            <div className="card-header-cyber">
              <FontAwesomeIcon icon={faTrophy} className="me-2" />Progress Indicators
            </div>
            <div className="card-body-cyber">
              {PROGRESS.map(({ label, value, color }) => (
                <div key={label} className="mb-3">
                  <div className="d-flex justify-content-between mb-1">
                    <span className="small">{label}</span>
                    <span className="small" style={{ color }}>{value}%</span>
                  </div>
                  <div className="progress-cyber">
                    <div className="progress-bar-cyber" style={{ width: `${value}%`, background: color }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Suggestions */}
          <div className="system-card">
            <div className="card-header-cyber">
              <FontAwesomeIcon icon={faLightbulb} className="me-2" />AI Suggestions
            </div>
            <ul className="list-cyber">
              {AI_SUGGESTIONS.map((s, i) => (
                <li key={i} style={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                  <span className="small">{s}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
