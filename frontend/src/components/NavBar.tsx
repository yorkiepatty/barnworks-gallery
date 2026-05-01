import { useState } from 'react'
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
  const user      = localStorage.getItem('alphavox_user')
  const [open, setOpen] = useState(false)

  const close = () => setOpen(false)

  return (
    <>
      <nav style={s.nav}>
        <Link to="/" style={s.logo} onClick={close}>
          <span>⚡</span>
          AlphaVox <span style={s.ver}>V2.5</span>
        </Link>

        {/* Desktop links — hidden on mobile via CSS */}
        <div className="nav-desktop" style={s.links}>
          {NAV_ITEMS.map(({ label, path }) => {
            const active = location.pathname === path
            return (
              <Link key={path} to={path} style={{ ...s.link, ...(active ? s.active : {}) }}>
                {label}
              </Link>
            )
          })}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {user ? (
            <button style={s.userBtn} onClick={() => { localStorage.removeItem('alphavox_user'); navigate('/') }}>
              {user} &times;
            </button>
          ) : (
            <Link to="/" style={s.initBtn}>INIT</Link>
          )}

          {/* Hamburger — shown on mobile via CSS */}
          <button
            className="nav-hamburger"
            onClick={() => setOpen(o => !o)}
            aria-label="Open menu"
          >
            <span style={{ ...s.bar, transform: open ? 'rotate(45deg) translate(5px,5px)' : 'none' }} />
            <span style={{ ...s.bar, opacity: open ? 0 : 1 }} />
            <span style={{ ...s.bar, transform: open ? 'rotate(-45deg) translate(5px,-5px)' : 'none' }} />
          </button>
        </div>
      </nav>

      {/* Mobile drawer */}
      {open && (
        <div className="nav-drawer-open">
          {NAV_ITEMS.map(({ label, path }) => {
            const active = location.pathname === path
            return (
              <Link
                key={path}
                to={path}
                onClick={close}
                style={{
                  padding: '1rem 1.5rem',
                  fontSize: '1rem',
                  color: active ? 'var(--primary-color, #00b4d8)' : 'rgba(255,255,255,0.7)',
                  background: active ? 'rgba(0,180,216,0.1)' : 'transparent',
                  borderBottom: '1px solid rgba(255,255,255,0.07)',
                  fontWeight: active ? 600 : 400,
                }}
              >
                {label}
              </Link>
            )
          })}
        </div>
      )}
    </>
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
    zIndex: 200,
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
  ver: { fontSize: '0.7rem', opacity: 0.6, marginLeft: '2px' },
  links: {
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
  bar: {
    display: 'block',
    width: '22px',
    height: '3px',
    background: '#00b4d8',
    borderRadius: '2px',
    transition: 'all 0.25s ease',
  },
}
