import { useEffect, useState } from 'react'
import ReactFlow, { Background, Controls } from 'reactflow'
import { topologyNodes, topologyEdges } from '../api/topologyData.js'

export default function TopologyPage() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 50)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className={`topology-panel ${isVisible ? 'reveal--visible' : 'reveal'}`}>
      <ReactFlow
        nodes={topologyNodes}
        edges={topologyEdges}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#262f4d" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  )
}