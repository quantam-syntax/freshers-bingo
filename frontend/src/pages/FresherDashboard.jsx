import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useSocket } from '../hooks/useSocket'
import { useBingoCard } from '../hooks/useBingoCard'
import BingoCard from '../components/BingoCard'
import Passport from '../components/Passport'
import ChallengePopup from '../components/ChallengePopup'
import { useNavigate } from 'react-router-dom'
import './FresherDashboard.css'

export default function FresherDashboard() {
  const { user, logout } = useAuth()
  const { card, loading, uploading, error, uploadPhoto } = useBingoCard()
  const { challengePopup, dismissPopup } = useSocket()
  const [activeTab, setActiveTab] = useState('bingo')
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/')
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-text">Loading your bingo card...</div>
      </div>
    )
  }

  return (
    <div className="page-container fresher-dashboard">
      <div className="dashboard-topbar">
        <div className="user-info">
          <span className="user-name">{user?.name}</span>
          <span className="user-roll">{user?.roll_no}</span>
        </div>
        <div className="topbar-actions">
          <button className="btn-primary btn-sm" onClick={() => navigate('/winners')}>
            🏆 Winners
          </button>
          <button className="btn-danger btn-sm" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab-btn ${activeTab === 'bingo' ? 'active' : ''}`}
          onClick={() => setActiveTab('bingo')}
        >
          🎯 Bingo Grid
        </button>
        <button 
          className={`tab-btn ${activeTab === 'passport' ? 'active' : ''}`}
          onClick={() => setActiveTab('passport')}
        >
          🎟️ My Passport
        </button>
      </div>

      {error && <div className="form-error" style={{ marginBottom: 16 }}>{error}</div>}

      {activeTab === 'bingo' && card && (
        <BingoCard card={card} onUpload={uploadPhoto} uploadingCell={uploading} />
      )}

      {activeTab === 'passport' && (
        <Passport user={user} card={card} />
      )}

      {card?.completed_at && activeTab === 'bingo' && (
        <div className="bingo-complete-banner animate-pop-in">
          <div className="washi-tape">🎉 BINGO COMPLETE! 🎉</div>
        </div>
      )}

      {challengePopup && (
        <ChallengePopup data={challengePopup} onDismiss={dismissPopup} />
      )}
    </div>
  )
}
