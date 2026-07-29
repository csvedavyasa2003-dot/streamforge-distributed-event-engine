import { useInView } from '../hooks/useInView.js'

const STATUS_LABEL = {
  active: 'Active',
  rebalancing: 'Rebalancing',
  down: 'Down',
}

export default function PartitionStatus({ partitions }) {
  const [ref, isInView] = useInView({ threshold: 0.3 })

  return (
    <div ref={ref} className={`partition-panel ${isInView ? 'reveal--visible' : 'reveal'}`}>
      <div className="partition-panel__title">Kafka Partitions</div>
      <table className="partition-table">
        <thead>
          <tr>
            <th>Partition</th>
            <th>Assigned Worker</th>
            <th>Status</th>
            <th>Lag</th>
          </tr>
        </thead>
        <tbody>
          {partitions.map((p) => (
            <tr key={p.id}>
              <td>#{p.id}</td>
              <td>{p.assignedWorker}</td>
              <td>
                <span className={`partition-badge partition-badge--${p.status}`}>
                  {STATUS_LABEL[p.status]}
                </span>
              </td>
              <td className={p.lag > 30 ? 'lag-high' : ''}>{p.lag}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}