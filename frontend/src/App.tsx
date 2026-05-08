import { Component, ReactNode } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Symbols from './pages/Symbols';
import Profile from './pages/Profile';
import Caregiver from './pages/Caregiver';
import Learning from './pages/Learning';
import AIControl from './pages/AIControl';
import BehaviorCapture from './pages/BehaviorCapture';
import Colors from './pages/Colors';

// ── Error Boundary ─────────────────────────────────────────────────────────────
// Catches any render crash in a page so the whole app never goes blank.

interface EBState { hasError: boolean; message: string }

class PageErrorBoundary extends Component<{ children: ReactNode }, EBState> {
  state: EBState = { hasError: false, message: '' };

  static getDerivedStateFromError(err: Error): EBState {
    return { hasError: true, message: err.message };
  }

  componentDidCatch(err: Error) {
    console.error('[AlphaVox] Page crashed:', err);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'center',
          justifyContent: 'center', minHeight: '60vh', gap: '1rem', padding: '2rem',
          color: 'var(--text-primary, #fff)',
        }}>
          <h2 style={{ fontSize: '1.4rem' }}>⚠️ Something went wrong on this page</h2>
          <p style={{ opacity: 0.6, fontSize: '0.9rem' }}>{this.state.message}</p>
          <button
            onClick={() => this.setState({ hasError: false, message: '' })}
            style={{
              padding: '0.6rem 1.4rem', borderRadius: 6, border: 'none',
              background: 'var(--primary-color, #0ff)', color: '#000', cursor: 'pointer',
            }}
          >
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// ── Auth guard ─────────────────────────────────────────────────────────────────

function RequireAuth({ children }: { children: ReactNode }) {
  const user = localStorage.getItem('alphavox_user');
  return user ? <>{children}</> : <Navigate to="/" replace />;
}

// ── App ────────────────────────────────────────────────────────────────────────

export default function App() {
  return (
    <Layout>
      <PageErrorBoundary>
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/dashboard" element={
            <RequireAuth><Dashboard /></RequireAuth>
          } />
          <Route path="/symbols" element={
            <RequireAuth><Symbols /></RequireAuth>
          } />
          <Route path="/profile" element={
            <RequireAuth><Profile /></RequireAuth>
          } />
          <Route path="/caregiver" element={
            <RequireAuth><Caregiver /></RequireAuth>
          } />
          <Route path="/learning" element={
            <RequireAuth><Learning /></RequireAuth>
          } />
          <Route path="/ai-control" element={
            <RequireAuth><AIControl /></RequireAuth>
          } />
          <Route path="/behavior" element={
            <RequireAuth><BehaviorCapture /></RequireAuth>
          } />
          <Route path="/colors" element={
            <RequireAuth><Colors /></RequireAuth>
          } />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </PageErrorBoundary>
    </Layout>
  );
}
