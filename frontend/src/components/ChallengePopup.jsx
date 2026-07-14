import { useState, useEffect, useRef } from 'react'
import ConfettiEffect from './ConfettiEffect'
import './ChallengePopup.css'

export default function ChallengePopup({ data, onDismiss }) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isSettled, setIsSettled] = useState(false)
  const [showConfetti, setShowConfetti] = useState(false)
  const intervalRef = useRef(null)
  const timeoutRef = useRef(null)

  useEffect(() => {
    if (!data?.reel) return

    const reel = data.reel
    const finalIdx = data.final_index
    let idx = 0
    let delay = 80

    function step() {
      idx++
      if (idx >= reel.length) {
        setCurrentIndex(finalIdx)
        setIsSettled(true)
        setShowConfetti(true)
        timeoutRef.current = setTimeout(() => onDismiss(), 10000)
        return
      }
      setCurrentIndex(idx)
      delay = idx > reel.length - 5 ? delay + 60 : delay + 15
      intervalRef.current = setTimeout(step, delay)
    }

    intervalRef.current = setTimeout(step, delay)

    return () => {
      clearTimeout(intervalRef.current)
      clearTimeout(timeoutRef.current)
    }
  }, [data])

  if (!data?.reel) return null

  const reel = data.reel

  return (
    <div className="challenge-overlay" onClick={isSettled ? onDismiss : undefined}>
      {showConfetti && <ConfettiEffect />}
      <div className="challenge-modal" onClick={(e) => e.stopPropagation()}>
        <div className="challenge-reel-window">
          <div className="reel-tape-top" />
          {reel.map((text, i) => (
            <div
              key={i}
              className={`reel-item ${i === currentIndex ? 'active' : ''} ${
                i === currentIndex && isSettled ? 'settled' : ''
              }`}
            >
              {text}
            </div>
          ))}
          <div className="reel-tape-bottom" />
        </div>
        {isSettled && (
          <div className="challenge-final animate-stamp">
            <div className="washi-tape washi-tape-sm">🎯 Challenge!</div>
            <p className="challenge-text">{reel[data.final_index]}</p>
            <button className="btn-primary" onClick={onDismiss}>Got it!</button>
          </div>
        )}
        {!isSettled && (
          <p className="picking-label">Picking a challenge...</p>
        )}
      </div>
    </div>
  )
}
