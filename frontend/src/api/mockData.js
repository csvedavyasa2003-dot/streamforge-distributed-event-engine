export const mockStats = {
  totalTrucks: 1000000,
  eventsPerSecond: 30000,
  averageTemp: 28,
  alertCount: 3,
}

export const mockWorkers = [
  { id: 'Worker 1', status: 'ok' },
  { id: 'Worker 2', status: 'ok' },
  { id: 'Worker 3', status: 'ok' },
  { id: 'Worker 4', status: 'ok' },
]

export const mockTemperatureSeries = [
  { time: '10:00', avgTemp: 26 },
  { time: '10:01', avgTemp: 27 },
  { time: '10:02', avgTemp: 29 },
  { time: '10:03', avgTemp: 28 },
  { time: '10:04', avgTemp: 30 },
  { time: '10:05', avgTemp: 28 },
]

export const mockRecentEvents = [
  { truckId: 1001, temp: 28, timestamp: '10:05:01' },
  { truckId: 1002, temp: 31, timestamp: '10:05:02' },
  { truckId: 1003, temp: 26, timestamp: '10:05:02' },
  { truckId: 1004, temp: 29, timestamp: '10:05:03' },
]

export const mockAlerts = [
  {
    id: 1,
    truckId: 1002,
    temp: 31,
    threshold: 30,
    timestamp: '10:05:02',
    severity: 'warning',
  },
  {
    id: 2,
    truckId: 1047,
    temp: 34,
    threshold: 30,
    timestamp: '10:04:41',
    severity: 'critical',
  },
  {
    id: 3,
    truckId: 1090,
    temp: 32,
    threshold: 30,
    timestamp: '10:03:58',
    severity: 'warning',
  },
]
export const mockPartitions = [
  { id: 0, assignedWorker: 'Worker 1', status: 'active', lag: 12 },
  { id: 1, assignedWorker: 'Worker 2', status: 'active', lag: 8 },
  { id: 2, assignedWorker: 'Worker 3', status: 'active', lag: 45 },
  { id: 3, assignedWorker: 'Worker 4', status: 'rebalancing', lag: 0 },
]