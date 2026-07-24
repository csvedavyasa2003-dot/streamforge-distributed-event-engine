export default function StatCard({ label, value, icon, accent = 'default' }) {
  return (
    <div className={`stat-card stat-card--${accent}`}>
      <div className="stat-card__top">
        <span className="stat-card__icon">{icon}</span>
        <span className="stat-card__label">{label}</span>
      </div>
      <div className="stat-card__value">{value}</div>
    </div>
  )
}

