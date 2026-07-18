export const mockStats = {
  totalTrucks: 50000,
  eventsPerSecond: 150000,
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