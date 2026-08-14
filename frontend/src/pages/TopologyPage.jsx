import { useEffect, useState } from 'react'
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow'
import { topologyNodes, topologyEdges } from '../api/topologyData.js'
import NodeDetailPanel from '../components/NodeDetailPanel.jsx'

export default function TopologyPage() {
  const [isVisible, setIsVisible] = useState(false)
  const [selectedNode, setSelectedNode] = useState(null)

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
        onNodeClick={(_, node) => setSelectedNode(node)}
        onPaneClick={() => setSelectedNode(null)}
      >
        <Background color="#262f4d" gap={16} />
        <Controls />
        <MiniMap
          nodeColor="#1b2440"
          nodeStrokeColor="#22d3ee"
          maskColor="rgba(10, 14, 26, 0.7)"
          style={{ background: '#131a2e', border: '1px solid #262f4d' }}
        />
      </ReactFlow>

      {selectedNode && (
        <NodeDetailPanel node={selectedNode} onClose={() => setSelectedNode(null)} />
      )}
    </div>
  )
}