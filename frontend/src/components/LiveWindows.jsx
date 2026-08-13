export default function LiveWindows({ windows }) {
  if (!windows || windows.length === 0) {
    return <div className="page-placeholder">No active windows yet — waiting for truck events…</div>
  }

  return (
    <div className="live-windows-panel">
      <div className="live-windows-grid">
        {windows.map((w) => (
          <div key={`${w.truck_id}-${w.window_start}`} className="live-window-card">
            <div className="live-window-card__truck">Truck {w.truck_id}</div>
            <div className="live-window-card__temp">{w.current_avg_temp}°C</div>
            <div className="live-window-card__meta">
              {w.event_count} event{w.event_count !== 1 ? 's' : ''} in current window
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}