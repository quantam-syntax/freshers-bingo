import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Signup from './pages/Signup'
import AdminLogin from './pages/AdminLogin'
import FresherDashboard from './pages/FresherDashboard'
import AdminDashboard from './pages/AdminDashboard'
import WinnersBoard from './pages/WinnersBoard'

function ProtectedFresher({ children }) {
  const { isAuthenticated, isFresher, loading } = useAuth()
  if (loading) return null
  if (!isAuthenticated || !isFresher) return <Navigate to="/" replace />
  return children
}

function ProtectedAdmin({ children }) {
  const { isAuthenticated, isAdmin, loading } = useAuth()
  if (loading) return null
  if (!isAuthenticated || !isAdmin) return <Navigate to="/admin" replace />
  return children
}

function AutoRedirect({ children }) {
  const { isAuthenticated, isFresher, isAdmin, loading } = useAuth()
  if (loading) return null
  if (isAuthenticated && isFresher) return <Navigate to="/dashboard" replace />
  if (isAuthenticated && isAdmin) return <Navigate to="/admin/dashboard" replace />
  return children
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AutoRedirect><Signup /></AutoRedirect>} />
          <Route path="/admin" element={<AutoRedirect><AdminLogin /></AutoRedirect>} />
          <Route
            path="/dashboard"
            element={<ProtectedFresher><FresherDashboard /></ProtectedFresher>}
          />
          <Route
            path="/admin/dashboard"
            element={<ProtectedAdmin><AdminDashboard /></ProtectedAdmin>}
          />
          <Route path="/winners" element={<WinnersBoard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
