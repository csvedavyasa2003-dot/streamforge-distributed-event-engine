import { useInView } from '../hooks/useInView.js'

export default function WorkerStatus({ workers }) {
  const [ref, isInView] = useInView({ threshold: 0.3 })

  return (
    <div ref={ref} className={`worker-panel ${isInView ? 'reveal--visible' : 'reveal'}`}>
      <div className="worker-panel__title">Worker Status</div>
      <div className="worker-grid">
        {workers.map((worker) => (
          <div key={worker.id} className="worker-chip">
            <span className={`worker-dot worker-dot--${worker.status}`} />
            <span className="worker-chip__label">{worker.id}</span>
            <span className="worker-chip__icon">
              {worker.status === 'ok' ? '✓' : '✗'}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}