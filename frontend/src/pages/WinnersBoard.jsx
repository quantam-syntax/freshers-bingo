import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import WinnerCard from '../components/WinnerCard'
import { useAuth } from '../context/AuthContext'
import './WinnersBoard.css'

export default function WinnersBoard() {
  const [winners, setWinners] = useState([])
  const [loading, setLoading] = useState(true)
  const { isAuthenticated, isFresher, isAdmin } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    loadWinners()
    const interval = setInterval(loadWinners, 10000)
    return () => clearInterval(interval)
  }, [])

  async function loadWinners() {
    try {
      const data = await api.getWinners()
      setWinners(data)
    } catch (err) { /* ignore */ }
    finally { setLoading(false) }
  }

  function goBack() {
    if (isAdmin) navigate('/admin/dashboard')
    else if (isFresher) navigate('/dashboard')
    else navigate('/')
  }

  return (
    <div className="page-container winners-page">
      <div className="winners-header">
        <button className="btn-primary btn-sm" onClick={goBack}>← Back</button>
        <div className="washi-tape">🏆 Winners Board</div>
        <div style={{ width: 80 }} />
      </div>

      {loading ? (
        <div className="loading-text">Loading winners...</div>
      ) : winners.length === 0 ? (
        <div className="no-winners">
          <p className="no-winners-text">No winners yet — be the first to complete your bingo card!</p>
        </div>
      ) : (
        <div className="winners-grid">
          {winners.map((w) => (
            <WinnerCard key={w.id} winner={w} />
          ))}
        </div>
      )}

      <p className="winners-cap-note">First 20 to complete their card win! 🎯</p>
    </div>
  )
}
