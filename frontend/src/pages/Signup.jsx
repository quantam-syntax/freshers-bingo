import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import './Signup.css'

export default function Signup() {
  const [rollNo, setRollNo] = useState('')
  const [name, setName] = useState('')
  const [instagram, setInstagram] = useState('')
  const [linkedin, setLinkedin] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { loginFresher } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    if (!rollNo.trim() || !name.trim()) {
      setError('Roll number and name are required')
      return
    }
    setLoading(true)
    setError('')
    try {
      const socials = {}
      if (instagram.trim()) socials.instagram = instagram.trim()
      if (linkedin.trim()) socials.linkedin = linkedin.trim()
      const result = await api.signup(
        rollNo.trim(),
        name.trim(),
        Object.keys(socials).length > 0 ? socials : null
      )
      loginFresher(result.fresher, result.token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.error || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="signup-card card-container animate-slide-in">
        <div className="signup-header">
          <div className="washi-tape">Welcome, Fresher! 🎉</div>
        </div>
        <p className="signup-subtitle">Sign up to join the Human Bingo challenge</p>
        <form onSubmit={handleSubmit} className="signup-form">
          <div className="form-group">
            <label className="form-label">Roll Number *</label>
            <input
              id="signup-roll-no"
              className="input-field"
              type="text"
              placeholder="e.g. CS2026001"
              value={rollNo}
              onChange={(e) => setRollNo(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Your Name *</label>
            <input
              id="signup-name"
              className="input-field"
              type="text"
              placeholder="e.g. Aarav Sharma"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Instagram <span className="optional">(optional)</span></label>
            <input
              id="signup-instagram"
              className="input-field"
              type="text"
              placeholder="@yourhandle"
              value={instagram}
              onChange={(e) => setInstagram(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label className="form-label">LinkedIn <span className="optional">(optional)</span></label>
            <input
              id="signup-linkedin"
              className="input-field"
              type="text"
              placeholder="linkedin.com/in/you"
              value={linkedin}
              onChange={(e) => setLinkedin(e.target.value)}
            />
          </div>
          {error && <div className="form-error">{error}</div>}
          <button
            id="signup-submit"
            type="submit"
            className="btn-mustard signup-btn"
            disabled={loading}
          >
            {loading ? 'Joining...' : "Let's Go! 🎯"}
          </button>
        </form>
        <div className="signup-footer">
          <a href="/admin" className="admin-link">Admin? Login here →</a>
        </div>
      </div>
    </div>
  )
}
