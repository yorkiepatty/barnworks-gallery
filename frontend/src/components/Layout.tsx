import { NavLink, Link, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faMicrophoneAlt, faHome, faThLarge, faUserCog,
  faRobot, faChartLine, faGraduationCap, faVideo,
  faHandPaper, faEye, faVolumeUp, faSignOutAlt,
} from '@fortawesome/free-solid-svg-icons';

interface LayoutProps {
  children: React.ReactNode;
}

const NAV_LINKS = [
  { to: '/dashboard', icon: faHome,         label: 'Home' },
  { to: '/symbols',   icon: faThLarge,      label: 'Symbols' },
  { to: '/profile',   icon: faUserCog,      label: 'Profile' },
  { to: '/caregiver', icon: faChartLine,    label: 'Caregiver' },
  { to: '/learning',  icon: faGraduationCap,label: 'Learning Hub' },
  { to: '/ai-control',icon: faRobot,        label: 'Control Center' },
  { to: '/behavior',  icon: faVideo,        label: 'Behavior' },
];

export default function Layout({ children }: LayoutProps) {
  const navigate = useNavigate();
  const rawUser = localStorage.getItem('alphavox_user');
  const user = rawUser ? JSON.parse(rawUser) : null;

  const handleLogout = () => {
    localStorage.removeItem('alphavox_user');
    navigate('/');
  };

  return (
    <div className="app-wrapper">
      {/* ── Header ── */}
      <header className="av-header">
        <div className="av-header-inner">
          {/* Brand */}
          <Link to={user ? '/dashboard' : '/'} className="av-brand">
            <FontAwesomeIcon icon={faMicrophoneAlt} className="av-brand-icon" />
            <span className="av-brand-name">
              AlphaVox <span className="version-badge">v2.5</span>
            </span>
          </Link>

          {/* Nav */}
          {user && (
            <nav className="av-nav">
              {NAV_LINKS.map(({ to, icon, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  className={({ isActive }) => `av-nav-link${isActive ? ' active' : ''}`}
                >
                  <FontAwesomeIcon icon={icon} />
                  {label}
                </NavLink>
              ))}
            </nav>
          )}

          {/* User area */}
          {user && (
            <div className="av-user-area">
              <button className="av-user-btn" onClick={handleLogout} title="Sign out">
                <FontAwesomeIcon icon={faSignOutAlt} />
                <span>{user.name}</span>
              </button>
            </div>
          )}
        </div>
      </header>

      {/* ── Mobile nav strip ── */}
      {user && (
        <div className="av-mobile-nav" style={{ display: 'none' }}>
          {NAV_LINKS.map(({ to, icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `av-mobile-nav-link${isActive ? ' active' : ''}`}
            >
              <FontAwesomeIcon icon={icon} />
              {label}
            </NavLink>
          ))}
        </div>
      )}

      {/* ── Content ── */}
      <main className="main-content">
        {children}
      </main>

      {/* ── Footer ── */}
      <footer className="av-footer">
        <div className="av-footer-inner">
          <div>
            <p>© 2025 AlphaVox – Autonomous Communication Being</p>
            <p className="small text-muted mt-1">Multimodal communication for all</p>
          </div>
          <div className="av-footer-badges">
            <span className="cyber-badge"><FontAwesomeIcon icon={faHandPaper} /> Gestures</span>
            <span className="cyber-badge"><FontAwesomeIcon icon={faEye} /> Eye Tracking</span>
            <span className="cyber-badge"><FontAwesomeIcon icon={faVolumeUp} /> Voice</span>
            <span className="cyber-badge"><FontAwesomeIcon icon={faThLarge} /> Symbols</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
