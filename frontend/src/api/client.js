import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
})
export const resetEvents = () => client.delete('/events/reset')

export const getStats = () => client.get('/events/stats')
export const getEvents = () => client.get('/events/')
export const getAlerts = () => client.get('/events/alerts')
export const getWorkers = () => client.get('/events/workers')
export const getLiveWindows = () => client.get('/events/live-windows')

export default client