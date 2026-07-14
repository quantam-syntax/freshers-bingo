import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import './AdminDashboard.css'

export default function AdminDashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [challenges, setChallenges] = useState([])
  const [newChallenge, setNewChallenge] = useState('')
  const [editId, setEditId] = useState(null)
  const [editText, setEditText] = useState('')
  const [picking, setPicking] = useState(false)
  const [lastPicked, setLastPicked] = useState(null)
  const [tab, setTab] = useState('challenges')
  const [freshers, setFreshers] = useState([])
  const [loadingFreshers, setLoadingFreshers] = useState(false)

  useEffect(() => {
    loadStats()
    loadChallenges()
    loadFreshers()
  }, [])

  useEffect(() => {
    if (tab === 'freshers') {
      loadFreshers()
    }
  }, [tab])

  async function loadFreshers() {
    setLoadingFreshers(true)
    try {
      const data = await api.getFreshers()
      setFreshers(data)
    } catch (err) { /* ignore */ }
    finally { setLoadingFreshers(false) }
  }

  async function loadStats() {
    try {
      const data = await api.getStats()
      setStats(data)
    } catch (err) { /* ignore */ }
  }

  async function loadChallenges() {
    try {
      const data = await api.getChallenges()
      setChallenges(data)
    } catch (err) { /* ignore */ }
  }

  async function handleAddChallenge(e) {
    e.preventDefault()
    if (!newChallenge.trim()) return
    try {
      await api.addChallenge(newChallenge.trim())
      setNewChallenge('')
      loadChallenges()
      loadStats()
    } catch (err) { /* ignore */ }
  }

  async function handleDelete(id) {
    try {
      await api.deleteChallenge(id)
      loadChallenges()
      loadStats()
    } catch (err) { /* ignore */ }
  }

  async function handleUpdate(id) {
    if (!editText.trim()) return
    try {
      await api.updateChallenge(id, editText.trim())
      setEditId(null)
      setEditText('')
      loadChallenges()
    } catch (err) { /* ignore */ }
  }

  async function handlePick() {
    setPicking(true)
    try {
      const data = await api.pickChallenge()
      setLastPicked(data.challenge)
      loadChallenges()
      loadStats()
    } catch (err) {
      alert(err.error || 'No unused challenges')
    } finally {
      setPicking(false)
    }
  }

  async function handleUndo(id) {
    try {
      await api.undoChallenge(id)
      loadChallenges()
      loadStats()
    } catch (err) { /* ignore */ }
  }

  function handleLogout() {
    logout()
    navigate('/admin')
  }

  const unusedCount = challenges.filter(c => !c.is_used).length
  const usedChallenges = challenges.filter(c => c.is_used)

  return (
    <div className="page-container admin-dashboard">
      <div className="dashboard-topbar">
        <div className="user-info">
          <span className="user-name">Admin: {user?.username}</span>
        </div>
        <div className="topbar-actions">
          <button className="btn-primary btn-sm" onClick={() => navigate('/winners')}>
            🏆 Winners
          </button>
          <button className="btn-danger btn-sm" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{stats.freshers_registered}</div>
            <div className="stat-label">Freshers</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.challenges_used}</div>
            <div className="stat-label">Challenges Used</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.bingo_completions}</div>
            <div className="stat-label">Bingo Done</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.winners_count}</div>
            <div className="stat-label">Winners</div>
          </div>
        </div>
      )}

      <div className="pick-section">
        <button
          id="pick-challenge-btn"
          className="btn-mustard pick-btn animate-pulse"
          onClick={handlePick}
          disabled={picking || unusedCount === 0}
        >
          {picking ? '🎰 Picking...' : `🎲 Pick Random Challenge (${unusedCount} left)`}
        </button>
        {lastPicked && (
          <div className="last-picked polaroid-card">
            <p className="last-picked-label">Last picked:</p>
            <p className="last-picked-text">{lastPicked.text}</p>
          </div>
        )}
      </div>

      <div className="admin-tabs">
        <button
          className={`tab-btn ${tab === 'challenges' ? 'active' : ''}`}
          onClick={() => setTab('challenges')}
        >
          Challenge Bank ({challenges.length})
        </button>
        <button
          className={`tab-btn ${tab === 'used' ? 'active' : ''}`}
          onClick={() => setTab('used')}
        >
          Used ({usedChallenges.length})
        </button>
        <button
          className={`tab-btn ${tab === 'freshers' ? 'active' : ''}`}
          onClick={() => setTab('freshers')}
        >
          Registered Freshers ({freshers.length})
        </button>
      </div>

      {tab === 'challenges' && (
        <div className="challenges-section">
          <form onSubmit={handleAddChallenge} className="add-challenge-form">
            <input
              id="new-challenge-input"
              className="input-field"
              placeholder="Add a new challenge..."
              value={newChallenge}
              onChange={(e) => setNewChallenge(e.target.value)}
            />
            <button type="submit" className="btn-primary">Add</button>
          </form>
          <div className="challenge-list">
            {challenges.map((c) => (
              <div key={c.id} className={`challenge-item ${c.is_used ? 'used' : ''}`}>
                {editId === c.id ? (
                  <div className="edit-row">
                    <input
                      className="input-field"
                      value={editText}
                      onChange={(e) => setEditText(e.target.value)}
                    />
                    <button className="btn-primary btn-sm" onClick={() => handleUpdate(c.id)}>Save</button>
                    <button className="btn-sm" onClick={() => setEditId(null)} style={{ color: 'var(--brown-soft)' }}>Cancel</button>
                  </div>
                ) : (
                  <div className="challenge-row">
                    <span className="challenge-text-item">
                      {c.is_used && <span className="used-badge">USED</span>}
                      {c.text}
                    </span>
                    <div className="challenge-actions">
                      {!c.is_used && (
                        <button className="action-btn" onClick={() => { setEditId(c.id); setEditText(c.text) }}>✏️</button>
                      )}
                      {c.is_used && (
                        <button className="action-btn" onClick={() => handleUndo(c.id)} title="Undo">↩️</button>
                      )}
                      <button className="action-btn delete" onClick={() => handleDelete(c.id)}>🗑️</button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === 'used' && (
        <div className="challenges-section">
          <div className="challenge-list">
            {usedChallenges.map((c) => (
              <div key={c.id} className="challenge-item used">
                <div className="challenge-row">
                  <span className="challenge-text-item">{c.text}</span>
                  <button className="action-btn" onClick={() => handleUndo(c.id)} title="Undo">↩️</button>
                </div>
              </div>
            ))}
            {usedChallenges.length === 0 && (
              <p className="empty-text">No challenges have been picked yet</p>
            )}
          </div>
        </div>
      )}

      {tab === 'freshers' && (
        <div className="challenges-section">
          {loadingFreshers ? (
            <p className="empty-text">Loading freshers...</p>
          ) : freshers.length === 0 ? (
            <p className="empty-text">No registered freshers yet</p>
          ) : (
            <div className="fresher-list-container">
              <table className="fresher-table">
                <thead>
                  <tr>
                    <th>Roll No</th>
                    <th>Name</th>
                    <th>Instagram</th>
                    <th>LinkedIn</th>
                  </tr>
                </thead>
                <tbody>
                  {freshers.map((f) => (
                    <tr key={f.id}>
                      <td><strong>{f.roll_no}</strong></td>
                      <td>{f.name}</td>
                      <td>
                        {f.socials?.instagram ? (
                          <a
                            href={`https://instagram.com/${f.socials.instagram.replace('@', '')}`}
                            target="_blank"
                            rel="noreferrer"
                            className="social-link"
                          >
                            {f.socials.instagram}
                          </a>
                        ) : '-'}
                      </td>
                      <td>
                        {f.socials?.linkedin ? (
                          <a
                            href={f.socials.linkedin.startsWith('http') ? f.socials.linkedin : `https://${f.socials.linkedin}`}
                            target="_blank"
                            rel="noreferrer"
                            className="social-link"
                          >
                            Link
                          </a>
                        ) : '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
