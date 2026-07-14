import './WinnerCard.css'

export default function WinnerCard({ winner }) {
  const rotation = ((winner.rank * 7 + 3) % 7) - 3

  return (
    <div className="winner-card polaroid-card" style={{ transform: `rotate(${rotation}deg)` }}>
      <div className="winner-photo-wrap">
        {winner.solo_selfie_url ? (
          <img src={winner.solo_selfie_url} alt={winner.fresher_name} className="winner-photo" />
        ) : (
          <div className="winner-photo-placeholder">📸</div>
        )}
      </div>
      <div className="winner-info">
        <span className="winner-rank">#{winner.rank}</span>
        <span className="winner-name">{winner.fresher_name}</span>
        <span className="winner-roll">{winner.fresher_roll_no}</span>
      </div>
    </div>
  )
}
