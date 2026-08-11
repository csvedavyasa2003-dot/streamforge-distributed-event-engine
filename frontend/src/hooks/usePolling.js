import { useEffect, useState, useCallback } from 'react'

export function usePolling(fetchFn, intervalMs = 5000) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchData = useCallback(async () => {
    try {
      const res = await fetchFn()
      setData(res.data)
      setError(null)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }, [fetchFn])

  useEffect(() => {
    fetchData()
    const id = setInterval(fetchData, intervalMs)
    return () => clearInterval(id)
  }, [fetchData, intervalMs])

  return { data, loading, error }
}