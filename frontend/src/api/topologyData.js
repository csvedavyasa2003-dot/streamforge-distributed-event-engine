export const topologyNodes = [
  {
    id: 'producer',
    position: { x: 0, y: 100 },
    data: { label: 'Truck Producer' },
    style: nodeStyle(),
  },
  {
    id: 'kafka',
    position: { x: 220, y: 100 },
    data: { label: 'Kafka' },
    style: nodeStyle(),
  },
  {
    id: 'worker1',
    position: { x: 440, y: 0 },
    data: { label: 'Worker 1' },
    style: nodeStyle(),
  },
  {
    id: 'worker2',
    position: { x: 440, y: 80 },
    data: { label: 'Worker 2' },
    style: nodeStyle(),
  },
  {
    id: 'worker3',
    position: { x: 440, y: 160 },
    data: { label: 'Worker 3' },
    style: nodeStyle(),
  },
  {
    id: 'worker4',
    position: { x: 440, y: 240 },
    data: { label: 'Worker 4' },
    style: nodeStyle(),
  },
  {
    id: 'fastapi',
    position: { x: 660, y: 120 },
    data: { label: 'FastAPI' },
    style: nodeStyle(),
  },
  {
    id: 'dashboard',
    position: { x: 880, y: 120 },
    data: { label: 'Dashboard' },
    style: nodeStyle(),
  },
]

export const topologyEdges = [
  { id: 'e1', source: 'producer', target: 'kafka', animated: true },
  { id: 'e2', source: 'kafka', target: 'worker1', animated: true },
  { id: 'e3', source: 'kafka', target: 'worker2', animated: true },
  { id: 'e4', source: 'kafka', target: 'worker3', animated: true },
  { id: 'e5', source: 'kafka', target: 'worker4', animated: true },
  { id: 'e6', source: 'worker1', target: 'fastapi' },
  { id: 'e7', source: 'worker2', target: 'fastapi' },
  { id: 'e8', source: 'worker3', target: 'fastapi' },
  { id: 'e9', source: 'worker4', target: 'fastapi' },
  { id: 'e10', source: 'fastapi', target: 'dashboard', animated: true },
]

function nodeStyle() {
  return {
    background: '#1a2230',
    border: '1px solid #232c3a',
    borderRadius: 8,
    color: '#e6ebf1',
    fontSize: 12,
    padding: 10,
  }
}