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
    <nav style={{
      position: 'sticky', top: 0, zIndex: 200,
      background: '#111827',
      borderBottom: '2px solid #00b4d8',
      display: 'flex', alignItems: 'center',
      padding: '0 0.75rem', gap: '0.5rem',
      minHeight: 52,
    }}>
      {/* Logo */}
      <Link to="/" style={{ fontWeight: 800, fontSize: '1rem', color: '#00b4d8', whiteSpace: 'nowrap', paddingRight: '0.5rem' }}>
        ⚡ AlphaVox
      </Link>

      {/* Scrollable nav links */}
      <div style={{
        display: 'flex', flex: 1,
        overflowX: 'auto', overflowY: 'visible',
        WebkitOverflowScrolling: 'touch',
        gap: 0,
        msOverflowStyle: 'none',
        scrollbarWidth: 'none',
      }}>
        {NAV_ITEMS.map(({ label, path }) => {
          const active = location.pathname === path
          return (
            <Link key={path} to={path} style={{
              display: 'block',
              padding: '14px 14px',
              whiteSpace: 'nowrap',
              fontSize: '0.9rem',
              fontWeight: active ? 700 : 400,
              color: active ? '#00b4d8' : 'rgba(255,255,255,0.65)',
              borderBottom: active ? '2px solid #00b4d8' : '2px solid transparent',
              flexShrink: 0,
            }}>
              {label}
            </Link>
          )
        })}
      </div>

      {/* User button */}
      {user ? (
        <button onClick={() => { localStorage.removeItem('alphavox_user'); navigate('/') }} style={{
          padding: '0.35rem 0.65rem', borderRadius: 6, background: 'transparent',
          border: '1px solid rgba(255,255,255,0.2)', color: 'rgba(255,255,255,0.5)',
          cursor: 'pointer', fontSize: '0.75rem', whiteSpace: 'nowrap', flexShrink: 0,
        }}>
          {user} ×
        </button>
      ) : (
        <Link to="/" style={{ padding: '0.35rem 0.75rem', borderRadius: 6, background: '#00b4d8', color: '#000', fontWeight: 700, fontSize: '0.8rem', whiteSpace: 'nowrap', flexShrink: 0 }}>INIT</Link>
      )}
    </nav>
  )
}
