import { Link, useLocation, useNavigate } from 'react-router-dom'

const NAV_ITEMS = [
  { label: 'Home',             path: '/' },
  { label: 'Symbols',          path: '/symbols' },
  { label: 'Colors',           path: '/colors' },
  { label: 'AI Control',       path: '/ai-control' },
  { label: 'Caregiver',        path: '/caregiver' },
  { label: 'Learning Hub',     path: '/learning' },
  { label: 'Behavior Capture', path: '/behavior' },
]

export default function NavBar() {
  const location = useLocation()
  const navigate  = useNavigate()
  const user = localStorage.getItem('alphavox_user')

  return (
    <nav style={s.nav}>
      <Link to="/" style={s.logo}>
        <span style={s.bolt}>⚡</span>
        AlphaVox <span style={s.ver}>V2.5</span>
      </Link>

      <div style={s.links}>
        {NAV_ITEMS.map(({ label, path }) => {
          const active = location.pathname === path
          return (
            <Link
              key={path}
              to={path}
              style={{ ...s.link, ...(active ? s.active : {}) }}
            >
              {label}
            </Link>
          )
        })}
      </div>

      <div>
        {user ? (
          <button
            style={s.userBtn}
            onClick={() => { localStorage.removeItem('alphavox_user'); navigate('/') }}
          >
            {user} &times;
          </button>
        ) : (
          <Link to="/" style={s.initBtn}>INIT</Link>
        )}
      </div>
    </nav>
  )
}

const s: Record<string, React.CSSProperties> = {
  nav: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '1rem',
    padding: '0.6rem 1.25rem',
    background: 'var(--surface)',
    borderBottom: '1px solid var(--border)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.4rem',
    fontSize: '1rem',
    fontWeight: 700,
    color: 'var(--primary)',
    whiteSpace: 'nowrap',
  },
  bolt: { fontSize: '1.1rem' },
  ver: { fontSize: '0.7rem', opacity: 0.6, marginLeft: '2px' },
  links: {
    display: 'flex',
    gap: '0.15rem',
    flexWrap: 'wrap',
    flex: 1,
    justifyContent: 'center',
  },
  link: {
    padding: '0.3rem 0.6rem',
    borderRadius: '0.3rem',
    fontSize: '0.8rem',
    color: 'var(--muted)',
    transition: 'color 0.15s',
    whiteSpace: 'nowrap',
  },
  active: {
    color: 'var(--primary)',
    background: 'var(--primary-dim)',
  },
  initBtn: {
    padding: '0.35rem 0.9rem',
    borderRadius: '0.3rem',
    background: 'var(--primary)',
    color: 'var(--surface)',
    fontWeight: 700,
    fontSize: '0.8rem',
  },
  userBtn: {
    padding: '0.35rem 0.9rem',
    borderRadius: '0.3rem',
    background: 'transparent',
    border: '1px solid var(--border)',
    color: 'var(--muted)',
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
}
