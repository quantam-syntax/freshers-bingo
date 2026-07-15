import { useRef } from 'react'
import './BingoCell.css'

export default function BingoCell({ cell, onUpload, isUploading }) {
  const fileRef = useRef(null)
  const isCenter = cell.position === 12
  const isFilled = !!cell.photo_url
  const rotation = cell._rotation || 0

  function handleClick() {
    if (!isUploading) fileRef.current?.click()
  }

  function handleFile(e) {
    const file = e.target.files?.[0]
    if (file) onUpload(cell.id, file)
  }

  return (
    <div
      className={`bingo-cell ${isFilled ? 'filled' : ''} ${isCenter ? 'center-cell' : ''}`}
      style={{ transform: `rotate(${rotation}deg)` }}
      onClick={handleClick}
    >
      <div className="cell-pin" />
      {isFilled ? (
        <div className="cell-photo-wrap">
          <img src={cell.photo_url} alt="uploaded" className="cell-photo" />
        </div>
      ) : (
        <div className="cell-content">
          {isCenter ? (
            <>
              <span className="cell-letter">📸</span>
              <span className="cell-hint">Solo selfie!</span>
            </>
          ) : (
            <span className="cell-task">{cell.task_text || cell.letter}</span>
          )}
        </div>
      )}
      {isUploading && (
        <div className="cell-loading">
          <div className="cell-spinner" />
        </div>
      )}
      <input
        ref={fileRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFile}
        hidden
      />
    </div>
  )
}
