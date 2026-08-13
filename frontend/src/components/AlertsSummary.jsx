export default function AlertsSummary({ alerts }) {
  const critical = alerts.filter((a) => a.severity === 'critical').length
  const warning = alerts.filter((a) => a.severity === 'warning').length

  return (
    <div className="alerts-summary">
      <div className="alerts-summary__item">
        <span className="alerts-summary__dot alerts-summary__dot--critical" />
        <span className="alerts-summary__count">{critical}</span>
        <span className="alerts-summary__label">Critical</span>
      </div>
      <div className="alerts-summary__item">
        <span className="alerts-summary__dot alerts-summary__dot--warning" />
        <span className="alerts-summary__count">{warning}</span>
        <span className="alerts-summary__label">Warning</span>
      </div>
      <div className="alerts-summary__item">
        <span className="alerts-summary__count">{alerts.length}</span>
        <span className="alerts-summary__label">Total Active</span>
      </div>
    </div>
  )
}