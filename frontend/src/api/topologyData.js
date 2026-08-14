export const nodeDetails = {
  producer: {
    title: 'Truck Producer',
    description: 'Simulates 10 trucks sending sensor telemetry every 10 seconds.',
    stats: [
      { label: 'Trucks Simulated', value: '10' },
      { label: 'Interval', value: '10s' },
      { label: 'Topic', value: 'truck-events' },
    ],
  },
  kafka: {
    title: 'Kafka Broker',
    description: 'Message broker that ingests and buffers the incoming truck event stream.',
    stats: [
      { label: 'Topic', value: 'truck-events' },
      { label: 'Port', value: 'localhost:9092' },
      { label: 'Status', value: 'Running' },
    ],
  },
  worker1: {
    title: 'Worker 1',
    description: 'Consumes events, computes rolling temperature stats and alert flags.',
    stats: [
      { label: 'Status', value: 'Healthy' },
      { label: 'Consumer Group', value: 'truck-consumer-group' },
    ],
  },
  worker2: {
    title: 'Worker 2',
    description: 'Consumes events, computes rolling temperature stats and alert flags.',
    stats: [{ label: 'Status', value: 'Healthy' }],
  },
  worker3: {
    title: 'Worker 3',
    description: 'Consumes events, computes rolling temperature stats and alert flags.',
    stats: [{ label: 'Status', value: 'Healthy' }],
  },
  worker4: {
    title: 'Worker 4',
    description: 'Consumes events, computes rolling temperature stats and alert flags.',
    stats: [{ label: 'Status', value: 'Rebalancing' }],
  },
  fastapi: {
    title: 'FastAPI',
    description: 'Serves aggregated stats and events to the dashboard via REST endpoints.',
    stats: [
      { label: 'Port', value: 'localhost:8000' },
      { label: 'Status', value: 'In development' },
    ],
  },
  dashboard: {
    title: 'Dashboard',
    description: 'This React app — visualizes live fleet stats, worker health, and alerts.',
    stats: [{ label: 'Framework', value: 'React + Vite' }],
  },
}

export const topologyNodes = [
  {
    id: 'producer',
    position: { x: 0, y: 100 },
    data: { label: '🚚 Truck Producer' },
    style: nodeStyle('source'),
  },
  {
    id: 'kafka',
    position: { x: 220, y: 100 },
    data: { label: '📨 Kafka' },
    style: nodeStyle('source'),
  },
  {
    id: 'worker1',
    position: { x: 440, y: 0 },
    data: { label: '⚙️ Worker 1' },
    style: nodeStyle('worker'),
  },
  {
    id: 'worker2',
    position: { x: 440, y: 80 },
    data: { label: '⚙️ Worker 2' },
    style: nodeStyle('worker'),
  },
  {
    id: 'worker3',
    position: { x: 440, y: 160 },
    data: { label: '⚙️ Worker 3' },
    style: nodeStyle('worker'),
  },
  {
    id: 'worker4',
    position: { x: 440, y: 240 },
    data: { label: '⚙️ Worker 4' },
    style: nodeStyle('worker'),
  },
  {
    id: 'fastapi',
    position: { x: 660, y: 120 },
    data: { label: '🔌 FastAPI' },
    style: nodeStyle('sink'),
  },
  {
    id: 'dashboard',
    position: { x: 880, y: 120 },
    data: { label: '📊 Dashboard' },
    style: nodeStyle('sink'),
  },
]

export const topologyEdges = [
  { id: 'e1', source: 'producer', target: 'kafka', animated: true, style: edgeStyle('cyan') },
  { id: 'e2', source: 'kafka', target: 'worker1', animated: true, style: edgeStyle('violet') },
  { id: 'e3', source: 'kafka', target: 'worker2', animated: true, style: edgeStyle('violet') },
  { id: 'e4', source: 'kafka', target: 'worker3', animated: true, style: edgeStyle('violet') },
  { id: 'e5', source: 'kafka', target: 'worker4', animated: true, style: edgeStyle('violet') },
  { id: 'e6', source: 'worker1', target: 'fastapi', style: edgeStyle('dim') },
  { id: 'e7', source: 'worker2', target: 'fastapi', style: edgeStyle('dim') },
  { id: 'e8', source: 'worker3', target: 'fastapi', style: edgeStyle('dim') },
  { id: 'e9', source: 'worker4', target: 'fastapi', style: edgeStyle('dim') },
  { id: 'e10', source: 'fastapi', target: 'dashboard', animated: true, style: edgeStyle('success') },
]

function edgeStyle(variant) {
  const colors = {
    cyan: '#22d3ee',
    violet: '#a78bfa',
    success: '#34d399',
    dim: '#3a4a7a',
  }
  return { stroke: colors[variant], strokeWidth: 2 }
}

function nodeStyle(variant = 'default') {
  const variants = {
    default: {
      background: 'linear-gradient(135deg, #1b2440 0%, #131a2e 100%)',
      border: '1px solid #262f4d',
    },
    source: {
      background: 'linear-gradient(135deg, rgba(34, 211, 238, 0.18), #131a2e)',
      border: '1px solid rgba(34, 211, 238, 0.4)',
    },
    worker: {
      background: 'linear-gradient(135deg, rgba(167, 139, 250, 0.18), #131a2e)',
      border: '1px solid rgba(167, 139, 250, 0.4)',
    },
    sink: {
      background: 'linear-gradient(135deg, rgba(52, 211, 153, 0.18), #131a2e)',
      border: '1px solid rgba(52, 211, 153, 0.4)',
    },
  }

  return {
    ...variants[variant],
    borderRadius: 10,
    color: '#eef1fb',
    fontSize: 12,
    fontFamily: "'Space Grotesk', sans-serif",
    fontWeight: 600,
    padding: '12px 16px',
    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
  }
}