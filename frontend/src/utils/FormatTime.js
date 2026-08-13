export function timeAgo(timestamp) {
  const eventTime = new Date(timestamp)
  const now = new Date()

  const diffMs = now - eventTime
  const diffMin = Math.floor(diffMs / 60000)

  if (diffMin < 1) return 'just now'
  if (diffMin === 1) return '1 min ago'
  if (diffMin < 60) return `${diffMin} min ago`

  const diffHr = Math.floor(diffMin / 60)
  if (diffHr === 1) return '1 hr ago'
  return `${diffHr} hrs ago`
}