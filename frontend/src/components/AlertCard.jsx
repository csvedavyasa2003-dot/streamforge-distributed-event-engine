export default function AlertCard({ alert }) {
  return (
    <div className={`alert-card alert-card--${alert.severity}`}>
      <div className="alert-card__icon">
        {alert.severity === 'critical' ? '🔴' : '🟡'}
      </div>
      <div className="alert-card__body">
        <div className="alert-card__title">
          Truck {alert.truckId} exceeded temperature threshold
        </div>
        <div className="alert-card__meta">
          {alert.temp}°C (limit {alert.threshold}°C) · {alert.timestamp}
        </div>
      </div>
    </div>
  )
}