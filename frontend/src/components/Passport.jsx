import { useMemo } from 'react'
import './Passport.css'

export default function Passport({ user, card }) {
  const centerCell = useMemo(() => {
    if (!card?.cells) return null
    return card.cells.find(c => c.is_center || c.position === 12)
  }, [card])

  const photoUrl = centerCell?.photo_url

  return (
    <div className="passport-wrapper animate-slide-in">
      <div className="passport-ticket">
        {/* Ticket Header */}
        <div className="ticket-header">
          <div className="ticket-title-group">
            <span className="ticket-badge">OFFICIAL PASS</span>
            <h2>SAFAR 2026</h2>
          </div>
          <span className="ticket-serial">#SF-{user?.roll_no?.substring(user.roll_no.length - 4) || '2026'}</span>
        </div>

        {/* Ticket Body */}
        <div className="ticket-body">
          {/* Photo Section */}
          <div className="ticket-photo-section">
            <div className={`ticket-polaroid ${photoUrl ? 'has-photo' : 'no-photo'}`}>
              {photoUrl ? (
                <img src={photoUrl} alt="Selfie" className="ticket-selfie" />
              ) : (
                <div className="ticket-selfie-placeholder">
                  <span className="placeholder-emoji">👤</span>
                  <p className="placeholder-text">Selfie Required</p>
                </div>
              )}
              <div className="polaroid-pin"></div>
            </div>
            {!photoUrl && (
              <span className="photo-hint">
                ⚠️ Upload center selfie (★) on Bingo grid to link photo
              </span>
            )}
          </div>

          {/* Details Section */}
          <div className="ticket-details">
            <div className="detail-item">
              <span className="detail-label">CONTESTANT NAME</span>
              <span className="detail-value">{user?.name}</span>
            </div>
            
            <div className="detail-item">
              <span className="detail-label">ROLL NUMBER</span>
              <span className="detail-value code-font">{user?.roll_no}</span>
            </div>

            <div className="detail-row">
              <div className="detail-item">
                <span className="detail-label">BATCH</span>
                <span className="detail-value">Freshers 2026</span>
              </div>
              
              <div className="detail-item">
                <span className="detail-label">SECTOR</span>
                <span className="detail-value">CAMPUS ENTRY</span>
              </div>
            </div>

            <div className="barcode-container">
              <div className="barcode"></div>
              <span className="barcode-text">*{user?.roll_no}*</span>
            </div>
          </div>
        </div>

        {/* Passport Stamp overlay */}
        {card?.completed_at ? (
          <div className="passport-stamp verified animate-stamp">
            <span className="stamp-text-outer">SAFAR 2026</span>
            <span className="stamp-text-inner">VERIFIED WINNER</span>
          </div>
        ) : (
          <div className="passport-stamp active animate-stamp">
            <span className="stamp-text-outer">SAFAR 2026</span>
            <span className="stamp-text-inner">CONTESTANT</span>
          </div>
        )}
      </div>
    </div>
  )
}
