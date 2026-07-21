import StatCard from '../components/StatCard.jsx'
import WorkerStatus from '../components/WorkerStatus.jsx'
import TemperatureChart from '../components/TemperatureChart.jsx'
import EventsTable from '../components/EventsTable.jsx'
import {
  mockStats,
  mockWorkers,
  mockTemperatureSeries,
  mockRecentEvents,
} from '../api/mockData.js'

export default function DashboardPage() {
  return (
    <div className="dashboard">
      <div className="stat-grid">
        <StatCard label="Total Trucks" value={mockStats.totalTrucks.toLocaleString()} />
        <StatCard label="Events/sec" value={mockStats.eventsPerSecond.toLocaleString()} />
        <StatCard label="Average Temp" value={`${mockStats.averageTemp}°C`} />
        <StatCard
          label="Alerts"
          value={mockStats.alertCount}
          icon="🚨"
          accent={mockStats.alertCount > 0 ? 'warn' : 'default'}
        />
      </div>

      <WorkerStatus workers={mockWorkers} />
      <TemperatureChart data={mockTemperatureSeries} />
      <EventsTable events={mockRecentEvents} />
    </div>
  )
}