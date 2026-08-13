import { useInView } from '../hooks/useInView.js'
import { timeAgo } from '../utils/formatTime.js'

export default function AlertCard({ alert, index = 0, onDismiss }) {
  const [ref, isInView] = useInView({ threshold: 0.2 })

  return (
    <div
      ref={ref}
      className={`alert-card alert-card--${alert.severity} ${isInView ? 'reveal--visible' : 'reveal'}`}
      style={{ transitionDelay: `${index * 0.08}s` }}
    >
      <div className="alert-card__icon">
        {alert.severity === 'critical' ? '🔴' : '🟡'}
      </div>
      <div className="alert-card__body">
        <div className="alert-card__title">
          Truck {alert.truckId} exceeded temperature threshold
        </div>
        <div className="alert-card__meta">
          {alert.temp}°C (limit {alert.threshold}°C) · {timeAgo(alert.timestamp)}
        </div>
      </div>
      <div className={`alert-card__badge alert-card__badge--${alert.severity}`}>
        {alert.severity}
      </div>
      <button
        className="alert-card__dismiss"
        onClick={() => onDismiss(alert.id)}
        title="Dismiss alert"
      >
        ✕
      </button>
    </div>
  )
}