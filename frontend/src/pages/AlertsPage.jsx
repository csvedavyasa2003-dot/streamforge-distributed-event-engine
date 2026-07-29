import AlertCard from '../components/AlertCard.jsx'
import { mockAlerts } from '../api/mockData.js'

export default function AlertsPage() {
  return (
    <div className="alerts-page">
      <div className="alerts-page__title">
        Active Alerts ({mockAlerts.length})
      </div>
      <div className="alerts-list">
        {mockAlerts.length === 0 ? (
          <div className="page-placeholder">No active alerts.</div>
        ) : (
          mockAlerts.map((alert) => <AlertCard key={alert.id} alert={alert} />)
        )}
      </div>
    </div>
  )
}