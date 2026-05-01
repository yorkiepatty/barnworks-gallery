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
    <div style={{ position: 'sticky', top: 0, zIndex: 200 }}>
      {/* Top bar */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0.6rem 1.25rem',
        background: '#111827',
        borderBottom: '1px solid rgba(0,180,216,0.2)',
      }}>
        <Link to="/" style={{ fontWeight: 700, fontSize: '1rem', color: '#00b4d8', whiteSpace: 'nowrap' }}>
          ⚡ AlphaVox
        </Link>
        {user ? (
          <button onClick={() => { localStorage.removeItem('alphavox_user'); navigate('/') }} style={{
            padding: '0.3rem 0.7rem', borderRadius: '0.3rem', background: 'transparent',
            border: '1px solid rgba(255,255,255,0.2)', color: 'rgba(255,255,255,0.6)',
            cursor: 'pointer', fontSize: '0.8rem',
          }}>
            {user} ×
          </button>
        ) : (
          <Link to="/" style={{ padding: '0.3rem 0.8rem', borderRadius: '0.3rem', background: '#00b4d8', color: '#000', fontWeight: 700, fontSize: '0.8rem' }}>INIT</Link>
        )}
      </div>

      {/* Nav links — always visible, scrollable on mobile */}
      <div style={{
        display: 'flex',
        overflowX: 'auto',
        background: '#0f172a',
        borderBottom: '1px solid rgba(0,180,216,0.15)',
        WebkitOverflowScrolling: 'touch',
        scrollbarWidth: 'none',
      }}>
        {NAV_ITEMS.map(({ label, path }) => {
          const active = location.pathname === path
          return (
            <Link
              key={path}
              to={path}
              style={{
                padding: '0.6rem 1.1rem',
                whiteSpace: 'nowrap',
                fontSize: '0.85rem',
                color: active ? '#00b4d8' : 'rgba(255,255,255,0.55)',
                borderBottom: active ? '2px solid #00b4d8' : '2px solid transparent',
                fontWeight: active ? 600 : 400,
                flexShrink: 0,
              }}
            >
              {label}
            </Link>
          )
        })}
      </div>
    </div>
  )
}
