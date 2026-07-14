import { useState, useEffect, useCallback } from 'react'
import { api } from '../services/api'

export function useBingoCard() {
  const [card, setCard] = useState(null)
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(null)
  const [error, setError] = useState(null)

  const fetchCard = useCallback(async () => {
    try {
      setLoading(true)
      const data = await api.getMyCard()
      setCard(data)
      setError(null)
    } catch (err) {
      setError(err.error || 'Failed to load card')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchCard()
  }, [fetchCard])

  const uploadPhoto = useCallback(async (cellId, file) => {
    try {
      setUploading(cellId)
      const data = await api.uploadCellPhoto(cellId, file)
      setCard(data.card)
      return data.winner
    } catch (err) {
      setError(err.error || 'Upload failed')
      return null
    } finally {
      setUploading(null)
    }
  }, [])

  return { card, loading, uploading, error, uploadPhoto, refetch: fetchCard }
}
