export default function StatCard({ label, value, accent = 'default' }) {
  return (
    <div className={`stat-card stat-card--${accent}`}>
      <div className="stat-card__label">{label}</div>
      <div className="stat-card__value">{value}</div>
    </div>
  )
}