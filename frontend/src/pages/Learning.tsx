import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faGraduationCap, faStar, faBookOpen, faHandPaper,
  faMusic, faLeaf, faUtensils, faHeart, faArrowRight,
} from '@fortawesome/free-solid-svg-icons';

interface Topic {
  id: string;
  icon: typeof faStar;
  name: string;
  description: string;
  progress: number;
  color: string;
  level: string;
}

const TOPICS: Topic[] = [
  { id: 'basic_words',    icon: faBookOpen,   name: 'Basic Words',      description: 'Start with everyday words and simple expressions for common needs.',       progress: 85, color: 'var(--primary-color)',  level: 'Beginner' },
  { id: 'greetings',     icon: faHandPaper,  name: 'Greetings',        description: 'Learn to say hello, goodbye, and express common social pleasantries.',     progress: 92, color: 'var(--success-color)',  level: 'Beginner' },
  { id: 'feelings',      icon: faHeart,      name: 'Feelings',         description: 'Express emotions and feelings clearly to caregivers and friends.',          progress: 68, color: 'var(--danger-color)',   level: 'Beginner' },
  { id: 'food_drink',    icon: faUtensils,   name: 'Food & Drink',     description: 'Communicate food preferences, hunger, and thirst effectively.',             progress: 74, color: 'var(--warning-color)', level: 'Intermediate' },
  { id: 'activities',    icon: faLeaf,       name: 'Activities',       description: 'Talk about things you want to do, games, and outdoor activities.',          progress: 45, color: 'var(--success-color)',  level: 'Intermediate' },
  { id: 'music_sounds',  icon: faMusic,      name: 'Music & Sounds',   description: 'Express preferences for music, sounds, and auditory experiences.',          progress: 30, color: 'var(--accent-color)',   level: 'Intermediate' },
  { id: 'sentences',     icon: faBookOpen,   name: 'Simple Sentences', description: 'Combine words into simple sentences to express complex thoughts.',          progress: 22, color: 'var(--primary-color)',  level: 'Advanced' },
  { id: 'stories',       icon: faStar,       name: 'Stories',          description: 'Follow along and engage with simple stories and narratives.',                progress: 10, color: 'var(--warning-color)', level: 'Advanced' },
];

const RECOMMENDED = [
  { id: 'greetings',  name: 'Greetings',        reason: 'Based on your symbol board usage' },
  { id: 'feelings',   name: 'Feelings',          reason: 'Great for expressing emotions' },
  { id: 'activities', name: 'Activities',        reason: 'Matches your communication patterns' },
];

const LEVELS = ['All', 'Beginner', 'Intermediate', 'Advanced'];

export default function Learning() {
  const rawUser = localStorage.getItem('alphavox_user');
  const user = rawUser ? JSON.parse(rawUser) : { name: 'User' };

  const [activeLevel, setLevel]     = useState('All');
  const [activeTopic, setTopic]     = useState<Topic | null>(null);

  const topicsFiltered = TOPICS.filter(t => activeLevel === 'All' || t.level === activeLevel);
  const totalProgress = Math.round(TOPICS.reduce((a, t) => a + t.progress, 0) / TOPICS.length);
  const factsLearned  = Math.round(totalProgress * 0.8);

  return (
    <div className="container" style={{ paddingTop: '1.5rem' }}>
      <div className="mb-4 text-center">
        <h1 className="display-5 mb-1">
          <FontAwesomeIcon icon={faGraduationCap} className="me-2" style={{ color: 'var(--primary-color)' }} />
          Learning Hub
        </h1>
        <p className="lead">Explore topics, track your progress, and grow with AlphaVox!</p>
      </div>

      {/* Progress Overview */}
      <div className="system-card mb-5">
        <div className="processor-bar" />
        <div className="card-body-cyber">
          <div className="row">
            <div className="col">
              <p className="small text-muted mb-1">Welcome, {user.name}!</p>
              <div className="d-flex gap-4 flex-wrap">
                <div>
                  <p className="small text-muted">Topics Explored</p>
                  <p className="fw-bold" style={{ fontSize: '1.5rem', color: 'var(--primary-color)' }}>
                    {TOPICS.filter(t => t.progress > 0).length}
                  </p>
                </div>
                <div>
                  <p className="small text-muted">Facts Learned</p>
                  <p className="fw-bold" style={{ fontSize: '1.5rem', color: 'var(--success-color)' }}>{factsLearned}</p>
                </div>
                <div>
                  <p className="small text-muted">Overall Progress</p>
                  <p className="fw-bold" style={{ fontSize: '1.5rem', color: 'var(--warning-color)' }}>{totalProgress}%</p>
                </div>
              </div>
            </div>
            <div className="col">
              <p className="small text-muted mb-2">Overall Progress</p>
              <div className="progress-cyber" style={{ height: 12 }}>
                <div className="progress-bar-cyber" style={{ width: `${totalProgress}%` }} />
              </div>
              <p className="small text-muted mt-1 text-right">{totalProgress}% complete</p>
            </div>
          </div>
        </div>
      </div>

      {/* Topic View */}
      {activeTopic ? (
        <div className="system-card mb-5">
          <div className="card-header-cyber">
            <button className="cyber-btn" onClick={() => setTopic(null)}>← Back</button>
            <span style={{ color: activeTopic.color }}>{activeTopic.name}</span>
          </div>
          <div className="card-body-cyber" style={{ minHeight: 300 }}>
            <div className="text-center" style={{ padding: '2rem' }}>
              <FontAwesomeIcon icon={activeTopic.icon} style={{ fontSize: '4rem', color: activeTopic.color, marginBottom: '1rem' }} />
              <h2 className="cyber-title mb-3">{activeTopic.name}</h2>
              <p className="lead mb-4">{activeTopic.description}</p>
              <div className="progress-cyber mb-4" style={{ maxWidth: 360, margin: '0 auto 1rem' }}>
                <div className="progress-bar-cyber" style={{ width: `${activeTopic.progress}%`, background: activeTopic.color }} />
              </div>
              <p className="small text-muted mb-4">{activeTopic.progress}% complete · {activeTopic.level}</p>
              <button className="neural-btn lg">
                <FontAwesomeIcon icon={faArrowRight} />
                {activeTopic.progress > 0 ? 'Continue Learning' : 'Start Topic'}
              </button>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Level filter */}
          <div className="d-flex gap-2 flex-wrap mb-3">
            {LEVELS.map(l => (
              <button key={l} className={activeLevel === l ? 'neural-btn' : 'cyber-btn'}
                onClick={() => setLevel(l)}>{l}</button>
            ))}
          </div>

          {/* Topics grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '1rem', marginBottom: '2.5rem' }}>
            {topicsFiltered.map(topic => (
              <button
                key={topic.id}
                className="cyber-card"
                style={{ padding: '1.25rem', textAlign: 'left', border: '1px solid var(--border-color)', cursor: 'pointer', background: 'var(--surface-color)' }}
                onClick={() => setTopic(topic)}
              >
                <div className="d-flex align-items-center gap-3 mb-3">
                  <FontAwesomeIcon icon={topic.icon} style={{ fontSize: '1.75rem', color: topic.color }} />
                  <div>
                    <h5 className="mb-0" style={{ fontSize: '0.95rem' }}>{topic.name}</h5>
                    <span className="badge-cyber" style={{ fontSize: '0.68rem' }}>{topic.level}</span>
                  </div>
                </div>
                <p className="small text-muted mb-3">{topic.description.substring(0, 80)}…</p>
                <div className="progress-cyber mb-1">
                  <div className="progress-bar-cyber" style={{ width: `${topic.progress}%`, background: topic.color }} />
                </div>
                <p className="small text-muted text-right">{topic.progress}%</p>
              </button>
            ))}
          </div>

          {/* Recommended */}
          <div>
            <h2 className="cyber-title mb-4" style={{ fontSize: '1.1rem' }}>Recommended for You</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1rem' }}>
              {RECOMMENDED.map(r => {
                const topic = TOPICS.find(t => t.id === r.id)!;
                return (
                  <button
                    key={r.id}
                    className="cyber-card"
                    style={{ padding: '1.25rem', textAlign: 'left', cursor: 'pointer', background: 'var(--surface-color)', border: '1px solid var(--border-color)' }}
                    onClick={() => setTopic(topic)}
                  >
                    <div className="d-flex align-items-center gap-2 mb-2">
                      <FontAwesomeIcon icon={topic.icon} style={{ color: topic.color, fontSize: '1.4rem' }} />
                      <h5 className="mb-0" style={{ fontSize: '0.9rem' }}>{r.name}</h5>
                    </div>
                    <p className="small text-muted mb-0">{r.reason}</p>
                  </button>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
