const FILTERS = [
  { id: 'all', label: 'All' },
  { id: 'critical', label: 'Critical' },
  { id: 'warning', label: 'Warning' },
]

export default function AlertsFilter({ active, onChange }) {
  return (
    <div className="alerts-filter">
      {FILTERS.map((f) => (
        <button
          key={f.id}
          className={active === f.id ? 'filter-chip filter-chip--active' : 'filter-chip'}
          onClick={() => onChange(f.id)}
        >
          {f.label}
        </button>
      ))}
    </div>
  )
}