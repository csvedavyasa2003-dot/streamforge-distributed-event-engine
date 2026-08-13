import StatCard from '../components/StatCard.jsx'
import WorkerStatus from '../components/WorkerStatus.jsx'
import PartitionStatus from '../components/PartitionStatus.jsx'
import LiveWindows from '../components/LiveWindows.jsx'
import TemperatureChart from '../components/TemperatureChart.jsx'
import ThroughputChart from '../components/ThroughputChart.jsx'
import EventsTable from '../components/EventsTable.jsx'
import { usePolling } from '../hooks/usePolling.js'
import {
  getStats,
  getWorkers,
  getEvents,
  getAlerts,
  getLiveWindows,
} from '../api/client.js'

export default function DashboardPage() {
  const { data: stats, loading: statsLoading, error: statsError } = usePolling(getStats, 4000)
  const { data: workers, loading: workersLoading } = usePolling(getWorkers, 8000)
  const { data: events, loading: eventsLoading } = usePolling(getEvents, 5000)
  const { data: alerts } = usePolling(getAlerts, 6000)
  const { data: liveWindows, loading: liveWindowsLoading } = usePolling(getLiveWindows, 2000)

  if (statsError) {
    return (
      <div className="error-banner">
        Couldn't reach the API at {import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}.
        Make sure FastAPI, Kafka, the producer, and the consumer are all running.
      </div>
    )
  }

  const alertCount = alerts ? alerts.length : 0
  const eventsList = events || []
  const recentEvents = [...eventsList].slice(-10).reverse()

  const workerList = workers
    ? workers.map((w) => ({
        id: `Worker ${w.worker_id}`,
        status: w.status === 'Running' ? 'ok' : 'down',
      }))
    : []

  const partitionList = workers
    ? workers.map((w) => ({
        id: w.worker_id,
        assignedWorker: `Worker ${w.worker_id}`,
        status: w.status === 'Running' ? 'active' : 'rebalancing',
        lag: w.processed_events ? Math.max(0, 50 - (w.processed_events % 50)) : 0,
      }))
    : []

  const temperatureSeries = eventsList.slice(-15).map((e) => ({
    time: e.timestamp ? e.timestamp.slice(11, 19) : `#${e.id}`,
    avgTemp: e.temperature,
  }))

  const throughputMap = {}
  eventsList.slice(-20).forEach((e) => {
    throughputMap[e.truck_id] = (throughputMap[e.truck_id] || 0) + 1
  })
  const throughputSeries = Object.entries(throughputMap).map(([truckId, count]) => ({
    time: `Truck ${truckId}`,
    eventsPerSec: count,
  }))

  return (
    <div className="dashboard">
      <div className="stat-grid">
        <StatCard
          label="Total Trucks"
          value={statsLoading ? 0 : stats.total_events}
          icon="🚚"
          animate
        />
        <StatCard
          label="Events/sec"
          value={statsLoading ? 0 : stats.total_events}
          icon="⚡"
          animate
        />
        <StatCard
          label="Average Temp"
          value={statsLoading ? '—' : `${stats.average_temperature}°C`}
          icon="🌡️"
        />
        <StatCard
          label="Alerts"
          value={alertCount}
          icon="🚨"
          accent={alertCount > 0 ? 'warn' : 'default'}
          animate
        />
      </div>

      <section className="dashboard-section">
        <h2 className="section-title">Live Windows (In Progress)</h2>
        {liveWindowsLoading ? (
          <div className="page-placeholder">Loading live windows…</div>
        ) : (
          <LiveWindows windows={liveWindows} />
        )}
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Worker Health</h2>
        {workersLoading ? (
          <div className="page-placeholder">Loading workers…</div>
        ) : (
          <WorkerStatus workers={workerList} />
        )}
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Kafka Partitions</h2>
        {workersLoading ? (
          <div className="page-placeholder">Loading partitions…</div>
        ) : (
          <PartitionStatus partitions={partitionList} />
        )}
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Temperature Trend</h2>
        {eventsLoading ? (
          <div className="page-placeholder">Loading temperature data…</div>
        ) : (
          <TemperatureChart data={temperatureSeries} />
        )}
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Processing Throughput</h2>
        {eventsLoading ? (
          <div className="page-placeholder">Loading throughput data…</div>
        ) : (
          <ThroughputChart data={throughputSeries} />
        )}
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Live Feed</h2>
        {eventsLoading ? (
          <div className="page-placeholder">Loading events…</div>
        ) : (
          <EventsTable
            events={recentEvents.map((e) => ({
              truckId: e.truck_id,
              temp: e.temperature,
              timestamp: e.timestamp,
            }))}
          />
        )}
      </section>
    </div>
  )
}