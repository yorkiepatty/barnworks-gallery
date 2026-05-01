import { useState, useEffect } from 'react'
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
  const location  = useLocation()
  const navigate  = useNavigate()
  const user      = localStorage.getItem('alphavox_user')
  const [open, setOpen] = useState(false)
  const [mobile, setMobile] = useState(window.innerWidth < 768)

  useEffect(() => {
    const onResize = () => setMobile(window.innerWidth < 768)
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])

  // Close menu when navigating
  useEffect(() => { setOpen(false) }, [location.pathname])

  return (
    <>
      <nav style={s.nav}>
        <Link to="/" style={s.logo}>
          <span style={s.bolt}>⚡</span>
          AlphaVox <span style={s.ver}>V2.5</span>
        </Link>

        {/* Desktop links */}
        {!mobile && (
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
        )}

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
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

          {/* Hamburger button — mobile only */}
          {mobile && (
            <button style={s.hamburger} onClick={() => setOpen(o => !o)} aria-label="Menu">
              <span style={{ ...s.bar, transform: open ? 'rotate(45deg) translate(5px,5px)' : 'none' }} />
              <span style={{ ...s.bar, opacity: open ? 0 : 1 }} />
              <span style={{ ...s.bar, transform: open ? 'rotate(-45deg) translate(5px,-5px)' : 'none' }} />
            </button>
          )}
        </div>
      </nav>

      {/* Mobile dropdown */}
      {mobile && open && (
        <div style={s.drawer}>
          {NAV_ITEMS.map(({ label, path }) => {
            const active = location.pathname === path
            return (
              <Link
                key={path}
                to={path}
                style={{ ...s.drawerLink, ...(active ? s.drawerActive : {}) }}
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
  bolt: { fontSize: '1.1rem' },
  ver:  { fontSize: '0.7rem', opacity: 0.6, marginLeft: '2px' },
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
  hamburger: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: '4px',
  },
  bar: {
    display: 'block',
    width: 22,
    height: 2,
    background: 'var(--primary)',
    borderRadius: 2,
    transition: 'all 0.25s ease',
  },
  drawer: {
    position: 'sticky',
    top: 49,
    zIndex: 199,
    background: 'var(--surface)',
    borderBottom: '1px solid var(--border)',
    display: 'flex',
    flexDirection: 'column',
  },
  drawerLink: {
    padding: '0.85rem 1.5rem',
    fontSize: '0.95rem',
    color: 'var(--muted)',
    borderBottom: '1px solid var(--border)',
    transition: 'background 0.15s',
  },
  drawerActive: {
    color: 'var(--primary)',
    background: 'var(--primary-dim)',
    fontWeight: 600,
  },
}
