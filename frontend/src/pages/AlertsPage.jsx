import { useState } from 'react'
import AlertCard from '../components/AlertCard.jsx'
import AlertsSummary from '../components/AlertsSummary.jsx'
import AlertsFilter from '../components/AlertsFilter.jsx'
import { usePolling } from '../hooks/usePolling.js'
import { getAlerts } from '../api/client.js'

export default function AlertsPage() {
  const { data: rawAlerts, loading, error } = usePolling(getAlerts, 3000)
  const [dismissedIds, setDismissedIds] = useState([])
  const [filter, setFilter] = useState('all')

  if (loading) return <div className="page-placeholder">Loading alerts…</div>
  if (error) {
    return (
      <div className="error-banner">
        Couldn't reach the API. Make sure FastAPI, Kafka, the producer, and the consumer are all running.
      </div>
    )
  }

  const alerts = rawAlerts
    .filter((e) => !dismissedIds.includes(e.id))
    .map((e) => ({
      id: e.id,
      truckId: e.truck_id,
      temp: e.temperature,
      threshold: 35,
      timestamp: e.timestamp,
      severity: e.temperature > 38 ? 'critical' : 'warning',
    }))
    .sort((a, b) => b.id - a.id) // most recent first

  // Keep only the single most recent alert per truck, so the list stays compact
  const latestPerTruck = {}
  alerts.forEach((a) => {
    if (!latestPerTruck[a.truckId]) {
      latestPerTruck[a.truckId] = a
    }
  })
  const dedupedAlerts = Object.values(latestPerTruck)

  const handleDismiss = (id) => setDismissedIds((prev) => [...prev, id])

  const visibleAlerts =
    filter === 'all' ? dedupedAlerts : dedupedAlerts.filter((a) => a.severity === filter)

  return (
    <div className="alerts-page">
      <AlertsSummary alerts={dedupedAlerts} />

      <div className="alerts-page__toolbar">
        <div className="alerts-page__title">Active Alerts ({visibleAlerts.length})</div>
        <AlertsFilter active={filter} onChange={setFilter} />
      </div>

      <div className="alerts-list">
        {visibleAlerts.length === 0 ? (
          <div className="alerts-empty">
            <div className="alerts-empty__icon">✅</div>
            <div className="alerts-empty__text">
              {dedupedAlerts.length === 0
                ? 'No active alerts. Fleet is healthy.'
                : 'No alerts match this filter.'}
            </div>
          </div>
        ) : (
          visibleAlerts.map((alert, idx) => (
            <AlertCard key={alert.id} alert={alert} index={idx} onDismiss={handleDismiss} />
          ))
        )}
      </div>
    </div>
  )
}