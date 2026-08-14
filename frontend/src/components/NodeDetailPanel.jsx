import { nodeDetails } from '../api/topologyData.js'

export default function NodeDetailPanel({ node, onClose }) {
  const detail = nodeDetails[node.id]
  if (!detail) return null

  return (
    <div className="node-detail-panel">
      <div className="node-detail-panel__header">
        <span className="node-detail-panel__title">{detail.title}</span>
        <button className="node-detail-panel__close" onClick={onClose}>✕</button>
      </div>
      <p className="node-detail-panel__desc">{detail.description}</p>
      <div className="node-detail-panel__stats">
        {detail.stats.map((stat) => (
          <div key={stat.label} className="node-detail-panel__stat">
            <span className="node-detail-panel__stat-label">{stat.label}</span>
            <span className="node-detail-panel__stat-value">{stat.value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}