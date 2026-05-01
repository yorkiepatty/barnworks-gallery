import { Link, useLocation, useNavigate } from 'react-router-dom'

const NAV_ITEMS = [
  { label: 'Home',      path: '/' },
  { label: 'Symbols',   path: '/symbols' },
  { label: 'Colors',    path: '/colors' },
  { label: 'AI',        path: '/ai-control' },
  { label: 'Caregiver', path: '/caregiver' },
  { label: 'Learning',  path: '/learning' },
  { label: 'Behavior',  path: '/behavior' },
]

export default function NavBar() {
  const location = useLocation()
  const navigate  = useNavigate()
  const user      = localStorage.getItem('alphavox_user')

  return (
    <>
      {/* ── Top bar ── */}
      <nav style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0.6rem 1.25rem',
        background: 'var(--card-bg, #1a1a2e)',
        borderBottom: '1px solid var(--border-color, rgba(0,180,216,0.25))',
        position: 'sticky', top: 0, zIndex: 200,
      }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '1rem', fontWeight: 700, color: '#00b4d8', whiteSpace: 'nowrap' }}>
          ⚡ AlphaVox <span style={{ fontSize: '0.7rem', opacity: 0.6 }}>V2.5</span>
        </Link>

        {/* Desktop links — hidden on mobile */}
        <div className="nav-desktop-links">
          {NAV_ITEMS.map(({ label, path }) => {
            const active = location.pathname === path
            return (
              <Link key={path} to={path} style={{
                padding: '0.3rem 0.6rem', borderRadius: '0.3rem', fontSize: '0.8rem',
                color: active ? '#00b4d8' : 'rgba(255,255,255,0.5)',
                background: active ? 'rgba(0,180,216,0.12)' : 'transparent',
                whiteSpace: 'nowrap',
              }}>
                {label}
              </Link>
            )
          })}
        </div>

        {user ? (
          <button onClick={() => { localStorage.removeItem('alphavox_user'); navigate('/') }} style={{
            padding: '0.3rem 0.7rem', borderRadius: '0.3rem', background: 'transparent',
            border: '1px solid rgba(255,255,255,0.2)', color: 'rgba(255,255,255,0.5)',
            cursor: 'pointer', fontSize: '0.8rem', whiteSpace: 'nowrap',
          }}>
            {user} ×
          </button>
        ) : (
          <Link to="/" style={{ padding: '0.3rem 0.8rem', borderRadius: '0.3rem', background: '#00b4d8', color: '#000', fontWeight: 700, fontSize: '0.8rem' }}>INIT</Link>
        )}
      </nav>

      {/* ── Mobile scrollable nav strip — visible only on small screens ── */}
      <div className="nav-mobile-strip">
        {NAV_ITEMS.map(({ label, path }) => {
          const active = location.pathname === path
          return (
            <Link key={path} to={path} style={{
              padding: '0.5rem 1rem',
              fontSize: '0.85rem',
              whiteSpace: 'nowrap',
              color: active ? '#00b4d8' : 'rgba(255,255,255,0.6)',
              borderBottom: active ? '2px solid #00b4d8' : '2px solid transparent',
              fontWeight: active ? 600 : 400,
            }}>
              {label}
            </Link>
          )
        })}
      </div>
    </>
  )
}
