import StatCard from '../components/StatCard.jsx'
import WorkerStatus from '../components/WorkerStatus.jsx'
import PartitionStatus from '../components/PartitionStatus.jsx'
import TemperatureChart from '../components/TemperatureChart.jsx'
import EventsTable from '../components/EventsTable.jsx'
import {
  mockStats,
  mockWorkers,
  mockPartitions,
  mockTemperatureSeries,
  mockRecentEvents,
} from '../api/mockData.js'

export default function DashboardPage() {
  return (
    <div className="dashboard">
      <div className="stat-grid">
        <StatCard label="Total Trucks" value={mockStats.totalTrucks} icon="🚚" animate />
        <StatCard label="Events/sec" value={mockStats.eventsPerSecond} icon="⚡" animate />
        <StatCard label="Average Temp" value={`${mockStats.averageTemp}°C`} icon="🌡️" />
        <StatCard
          label="Alerts"
          value={mockStats.alertCount}
          icon="🚨"
          accent={mockStats.alertCount > 0 ? 'warn' : 'default'}
          animate
        />
      </div>

      <section className="dashboard-section">
        <h2 className="section-title">Worker Health</h2>
        <WorkerStatus workers={mockWorkers} />
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Kafka Partitions</h2>
        <PartitionStatus partitions={mockPartitions} />
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Temperature Trend</h2>
        <TemperatureChart data={mockTemperatureSeries} />
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Live Feed</h2>
        <EventsTable events={mockRecentEvents} />
      </section>
    </div>
  )
}