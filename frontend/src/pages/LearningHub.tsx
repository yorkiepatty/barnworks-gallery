const TOPICS = [
  { title: 'Nonverbal Communication',  icon: '🤝', progress: 65, lessons: 8 },
  { title: 'AAC Systems Overview',     icon: '⊞', progress: 42, lessons: 12 },
  { title: 'Assistive Technology',     icon: '🖥', progress: 80, lessons: 6 },
  { title: 'Autism & Communication',   icon: '🧩', progress: 55, lessons: 10 },
  { title: 'Symbol-Based Language',    icon: '🔷', progress: 30, lessons: 9 },
  { title: 'Eye Gaze Communication',   icon: '👁', progress: 20, lessons: 7 },
  { title: 'Gesture Recognition',      icon: '✋', progress: 70, lessons: 5 },
  { title: 'Caregiver Training',       icon: '👤', progress: 90, lessons: 4 },
]

export default function LearningHub() {
  return (
    <div style={s.page}>
      <div style={s.header}>
        <h1 style={s.heading}>Learning Hub</h1>
        <p style={s.sub}>Educational resources on AAC, nonverbal communication, and assistive technology</p>
      </div>

      {/* Stats */}
      <div style={s.statsRow}>
        {[
          { label: 'Topics',          val: '15' },
          { label: 'Lessons',         val: '61' },
          { label: 'Avg Progress',    val: '57%' },
          { label: 'Achievements',    val: '12' },
        ].map(stat => (
          <div key={stat.label} style={s.statCard}>
            <span style={s.statVal}>{stat.val}</span>
            <span style={s.statLabel}>{stat.label}</span>
          </div>
        ))}
      </div>

      {/* Topics grid */}
      <h2 style={s.sectionTitle}>Learning Journey</h2>
      <div style={s.grid}>
        {TOPICS.map(t => (
          <div key={t.title} style={s.topicCard}>
            <div style={s.topicHeader}>
              <span style={{ fontSize: '1.5rem' }}>{t.icon}</span>
              <span style={s.lessons}>{t.lessons} lessons</span>
            </div>
            <h3 style={s.topicTitle}>{t.title}</h3>
            <div style={s.barTrack}>
              <div style={{ ...s.barFill, width: `${t.progress}%` }} />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={s.muted}>Progress</span>
              <span style={{ ...s.muted, color: 'var(--primary)' }}>{t.progress}%</span>
            </div>
            <button style={s.btn}>{t.progress > 0 ? 'Continue' : 'Start'}</button>
          </div>
        ))}
      </div>
    </div>
  )
}

const s: Record<string, React.CSSProperties> = {
  page: { padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '1000px', margin: '0 auto' },
  header: { paddingBottom: '0.5rem', borderBottom: '1px solid var(--border)' },
  heading: { fontSize: '1.4rem', fontWeight: 700 },
  sub: { fontSize: '0.85rem', color: 'var(--muted)', marginTop: '0.25rem' },
  statsRow: { display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' },
  statCard: { background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '0.6rem', padding: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem' },
  statVal: { fontSize: '1.6rem', fontWeight: 700, color: 'var(--primary)' },
  statLabel: { fontSize: '0.75rem', color: 'var(--muted)' },
  sectionTitle: { fontSize: '0.85rem', fontWeight: 600, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1rem' },
  topicCard: { background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '0.6rem', padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.6rem' },
  topicHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' },
  lessons: { fontSize: '0.72rem', color: 'var(--muted)', background: 'var(--surface2)', padding: '0.15rem 0.4rem', borderRadius: '0.3rem' },
  topicTitle: { fontSize: '0.88rem', fontWeight: 600 },
  barTrack: { height: '6px', background: 'var(--surface3)', borderRadius: '3px', overflow: 'hidden' },
  barFill: { height: '100%', background: 'var(--primary)', borderRadius: '3px' },
  muted: { fontSize: '0.75rem', color: 'var(--muted)' },
  btn: { padding: '0.4rem', borderRadius: '0.3rem', border: 'none', background: 'var(--primary-dim)', color: 'var(--primary)', fontWeight: 600, fontSize: '0.78rem', cursor: 'pointer', marginTop: '0.25rem' },
}
