import { useMemo } from 'react'
import BingoCell from './BingoCell'
import ProgressBar from './ProgressBar'
import './BingoCard.css'

export default function BingoCard({ card, onUpload, uploadingCell }) {
  const cellsWithRotation = useMemo(() => {
    if (!card?.cells) return []
    return card.cells.map((cell, i) => ({
      ...cell,
      _rotation: ((i * 7 + 3) % 9) - 4,
    }))
  }, [card])

  if (!card) return null

  return (
    <div className="bingo-card-wrapper">
      <div className="bingo-header">
        <div className="washi-tape">Human Bingo</div>
      </div>
      <p className="bingo-instructions">
        Each square has a letter. Find someone whose name starts with it,
        take a selfie together, and pin it up. Use a different person for every square!
      </p>
      <ProgressBar filled={card.filled_count} total={card.total_count} />
      <div className="bingo-grid">
        {cellsWithRotation.map((cell) => (
          <BingoCell
            key={cell.id}
            cell={cell}
            onUpload={onUpload}
            isUploading={uploadingCell === cell.id}
          />
        ))}
      </div>
    </div>
  )
}
