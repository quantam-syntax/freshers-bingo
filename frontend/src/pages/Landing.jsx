import { useNavigate } from 'react-router-dom'
import './Landing.css'

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div className="page-container landing-container">
      <div className="landing-card card-container animate-slide-in">
        <div className="landing-header">
          <div className="washi-tape font-large">SAFAR 2026 🎉</div>
        </div>
        
        <h1 className="landing-title">Human Bingo Challenge</h1>
        <p className="landing-subtitle">
          Break the ice, meet your peers, and win exciting prizes!
        </p>

        <div className="polaroid-collage animate-pulse">
          <div className="polaroid-preview">
            <span className="polaroid-emoji">📸</span>
            <p className="polaroid-caption">Snap Selfies</p>
          </div>
          <div className="polaroid-preview second">
            <span className="polaroid-emoji">🎯</span>
            <p className="polaroid-caption">Match Letters</p>
          </div>
        </div>

        <div className="rules-section">
          <h3>How to Play:</h3>
          <ul className="rules-list">
            <li>
              <span className="bullet">1</span>
              <div>
                <strong>Find Peer Matches:</strong> Find peers whose names start with the letters on your grid.
              </div>
            </li>
            <li>
              <span className="bullet">2</span>
              <div>
                <strong>Take a Selfie:</strong> Take a selfie together and upload it to the corresponding slot.
              </div>
            </li>
            <li>
              <span className="bullet">3</span>
              <div>
                <strong>Get Bingo:</strong> Complete a row, column, or diagonal to claim your spot in the Top 20!
              </div>
            </li>
          </ul>
        </div>

        <div className="landing-actions">
          <button 
            id="landing-enter" 
            className="btn-mustard btn-large"
            onClick={() => navigate('/signup')}
          >
            Enter the Challenge 🎯
          </button>
          
          <button 
            className="btn-primary"
            onClick={() => navigate('/winners')}
          >
            🏆 View Live Winners
          </button>
        </div>

        <div className="landing-footer">
          <a href="/admin" className="admin-link">Organizers / Admin Login →</a>
        </div>
      </div>
    </div>
  )
}
