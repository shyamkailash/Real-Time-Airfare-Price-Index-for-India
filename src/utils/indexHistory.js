export function filterIndexHistory(history, timeRange) {
  if (timeRange === 'ALL' || history.length === 0) return history

  const months = { '3M': 3, '6M': 6, '1Y': 12 }[timeRange]
  const latest = new Date(history[history.length - 1].date)
  const cutoff = new Date(latest)
  cutoff.setMonth(cutoff.getMonth() - (months - 1))

  return history.filter((point) => new Date(point.date) >= cutoff)
}
