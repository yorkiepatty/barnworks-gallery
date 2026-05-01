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

function RequireAuth({ children }: { children: React.ReactNode }) {
  const user = localStorage.getItem('alphavox_user');
  return user ? <>{children}</> : <Navigate to="/" replace />;
}

export default function App() {
  return (
    <Layout>
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
    </Layout>
  );
}
