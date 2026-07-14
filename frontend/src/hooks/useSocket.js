import { useState, useEffect, useCallback } from 'react'
import { getSocket } from '../services/socket'

export function useSocket() {
  const [challengePopup, setChallengePopup] = useState(null)
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    const socket = getSocket()

    socket.on('challenge:picking', (data) => {
      setIsAnimating(true)
      setChallengePopup(data)
    })

    socket.on('challenge:picked', (challenge) => {
      setTimeout(() => {
        setIsAnimating(false)
      }, 3000)
    })

    return () => {
      socket.off('challenge:picking')
      socket.off('challenge:picked')
    }
  }, [])

  const dismissPopup = useCallback(() => {
    setChallengePopup(null)
    setIsAnimating(false)
  }, [])

  return { challengePopup, isAnimating, dismissPopup }
}
