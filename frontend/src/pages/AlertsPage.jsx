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

// Keep only the single most recent alert per truck
const latestPerTruck = {}
alerts.forEach((a) => {
  if (!latestPerTruck[a.truckId]) {
    latestPerTruck[a.truckId] = a
  }
})
const dedupedAlerts = Object.values(latestPerTruck)