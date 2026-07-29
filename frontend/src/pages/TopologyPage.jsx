import ReactFlow, { Background, Controls } from 'reactflow'
import { topologyNodes, topologyEdges } from '../api/topologyData.js'

export default function TopologyPage() {
  return (
    <div className="topology-panel">
      <ReactFlow
        nodes={topologyNodes}
        edges={topologyEdges}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#232c3a" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  )
}