const SCHEMES = [
  { name: 'Ocean Blue',   primary: '#00d4ff', accent: '#ff8f00', bg: '#0d1824' },
  { name: 'Forest Green', primary: '#38a169', accent: '#a13870', bg: '#0d1a12' },
  { name: 'Sunset Red',   primary: '#e53e3e', accent: '#3de5e5', bg: '#1a0d0d' },
  { name: 'Royal Purple', primary: '#805ad5', accent: '#d69e2e', bg: '#120d1a' },
  { name: 'Warm Amber',   primary: '#d69e2e', accent: '#4299e1', bg: '#1a160d' },
  { name: 'Soft Pink',    primary: '#ed64a6', accent: '#48bb78', bg: '#1a0d14' },
]

export default function Colors() {
  return (
    <div style={s.page}>
      <div style={s.header}>
        <h1 style={s.heading}>Color Templates</h1>
        <p style={s.sub}>Customize AlphaVox appearance for accessibility and personal preference</p>
      </div>

      <div style={s.grid}>
        {SCHEMES.map(sc => (
          <div key={sc.name} style={s.card}>
            <div style={{ ...s.preview, background: sc.bg }}>
              <div style={{ ...s.previewBtn, background: sc.primary }}>Primary</div>
              <div style={{ ...s.previewBtn, background: sc.accent }}>Accent</div>
            </div>
            <div style={s.cardBody}>
              <span style={s.name}>{sc.name}</span>
              <button style={{ ...s.applyBtn, background: sc.primary }}>Apply</button>
            </div>
          </div>
        ))}
      </div>

      <div style={s.section}>
        <h2 style={s.sectionTitle}>Accessibility Options</h2>
        <div style={s.optGrid}>
          {['High Contrast', 'Colorblind Mode', 'Large Text', 'Reduced Motion'].map(opt => (
            <label key={opt} style={s.optLabel}>
              <input type="checkbox" style={{ accentColor: 'var(--primary)' }} />
              <span style={{ color: 'var(--muted)', fontSize: '0.85rem' }}>{opt}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  )
}

const s: Record<string, React.CSSProperties> = {
  page: { padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '900px', margin: '0 auto' },
  header: { paddingBottom: '0.5rem', borderBottom: '1px solid var(--border)' },
  heading: { fontSize: '1.4rem', fontWeight: 700 },
  sub: { fontSize: '0.85rem', color: 'var(--muted)', marginTop: '0.25rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' },
  card: { background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '0.6rem', overflow: 'hidden' },
  preview: { height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' },
  previewBtn: { padding: '0.25rem 0.6rem', borderRadius: '0.3rem', fontSize: '0.72rem', color: '#fff', fontWeight: 600 },
  cardBody: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.75rem 1rem' },
  name: { fontSize: '0.85rem', fontWeight: 600 },
  applyBtn: { padding: '0.3rem 0.8rem', borderRadius: '0.3rem', border: 'none', color: 'var(--surface)', fontWeight: 600, fontSize: '0.75rem', cursor: 'pointer' },
  section: { background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '0.6rem', padding: '1.25rem' },
  sectionTitle: { fontSize: '0.85rem', fontWeight: 600, color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1rem' },
  optGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '0.75rem' },
  optLabel: { display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' },
}
