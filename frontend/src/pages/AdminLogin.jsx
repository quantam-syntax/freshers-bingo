import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import './AdminLogin.css'

export default function AdminLogin() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { loginAdmin } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    if (!username.trim() || !password) {
      setError('Username and password are required')
      return
    }
    setLoading(true)
    setError('')
    try {
      const result = await api.adminLogin(username.trim(), password)
      loginAdmin(result.admin, result.token)
      navigate('/admin/dashboard')
    } catch (err) {
      setError(err.error || 'Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="admin-login-card card-container animate-slide-in">
        <div className="admin-login-header">
          <div className="washi-tape washi-tape-sm">Admin Login 🔐</div>
        </div>
        <form onSubmit={handleSubmit} className="admin-form">
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              id="admin-username"
              className="input-field"
              type="text"
              placeholder="admin"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              id="admin-password"
              className="input-field"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {error && <div className="form-error">{error}</div>}
          <button
            id="admin-submit"
            type="submit"
            className="btn-primary admin-submit-btn"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div className="admin-back">
          <a href="/" className="admin-link">← Back to Fresher Signup</a>
        </div>
      </div>
    </div>
  )
}
