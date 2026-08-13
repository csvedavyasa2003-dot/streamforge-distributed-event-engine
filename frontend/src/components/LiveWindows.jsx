const WINDOW_SECONDS = 300 // 5 minutes

function getProgress(windowStart) {
  const now = Math.floor(Date.now() / 1000)
  const elapsed = now - windowStart
  const pct = Math.min(100, Math.max(0, (elapsed / WINDOW_SECONDS) * 100))
  const remaining = Math.max(0, WINDOW_SECONDS - elapsed)
  const minutes = Math.floor(remaining / 60)
  const seconds = remaining % 60
  return { pct, label: `${minutes}:${seconds.toString().padStart(2, '0')}` }
}

export default function LiveWindows({ windows }) {
  if (!windows || windows.length === 0) {
    return <div className="page-placeholder">No active windows yet — waiting for truck events…</div>
  }

  const latestPerTruck = {}
  windows.forEach((w) => {
    const existing = latestPerTruck[w.truck_id]
    if (!existing || w.window_start > existing.window_start) {
      latestPerTruck[w.truck_id] = w
    }
  })
  const deduped = Object.values(latestPerTruck).sort((a, b) =>
    a.truck_id.localeCompare(b.truck_id)
  )

  return (
    <div className="live-windows-panel">
      {deduped.map((w) => {
        const { pct, label } = getProgress(w.window_start)
        return (
          <div key={w.truck_id} className="live-window-row">
            <div className="live-window-row__truck">Truck {w.truck_id}</div>

            <div className="live-window-row__bar-track">
              <div
                className="live-window-row__bar-fill"
                style={{ width: `${pct}%` }}
              />
            </div>

            <div className="live-window-row__temp">{w.current_avg_temp}°C</div>
            <div className="live-window-row__count">{w.event_count} events</div>
            <div className="live-window-row__timer">{label}</div>
          </div>
        )
      })}
    </div>
  )
}