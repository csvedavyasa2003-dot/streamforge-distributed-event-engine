export default function EventsTable({ events }) {
  return (
    <div className="table-panel">
      <div className="table-panel__title">Recent Events</div>
      <table className="events-table">
        <thead>
          <tr>
            <th>Truck ID</th>
            <th>Temp</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event, idx) => (
            <tr key={idx}>
              <td>{event.truckId}</td>
              <td className={event.temp > 30 ? 'temp-high' : ''}>
                {event.temp}°C
              </td>
              <td>{event.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}