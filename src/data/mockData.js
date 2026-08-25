export const index = {
  index: 128.42,
  yoyChange: 8.42,
  momChange: 1.72,
  basePeriod: '2025-01',
  lastUpdated: '2026-08-24T11:58:00'
}

export const indexHistory = [
  { date: '2025-01-01', value: 100 },
  { date: '2025-02-01', value: 101.2 },
  { date: '2025-03-01', value: 102.4 },
  { date: '2025-04-01', value: 103.1 },
  { date: '2025-05-01', value: 104.6 },
  { date: '2025-06-01', value: 105.3 },
  { date: '2025-07-01', value: 106.7 },
  { date: '2025-08-01', value: 107.5 },
  { date: '2025-09-01', value: 108.8 },
  { date: '2025-10-01', value: 110.2 },
  { date: '2025-11-01', value: 111.4 },
  { date: '2025-12-01', value: 112.1 },
  { date: '2026-01-01', value: 113.6 },
  { date: '2026-02-01', value: 114.8 },
  { date: '2026-03-01', value: 116.1 },
  { date: '2026-04-01', value: 118.3 },
  { date: '2026-05-01', value: 120.4 },
  { date: '2026-06-01', value: 122.7 },
  { date: '2026-07-01', value: 125.9 },
  { date: '2026-08-01', value: 128.42 }
]

export const routes = [
  { id: 'DEL-BOM', origin: 'DEL', destination: 'BOM', averageFare: 5482, index: 126.4, yoyChange: 12.4, momChange: 1.7, observations: 3842 },
  { id: 'DEL-BLR', origin: 'DEL', destination: 'BLR', averageFare: 6210, index: 130.2, yoyChange: 18.2, momChange: 2.1, observations: 1842 },
  { id: 'BOM-DEL', origin: 'BOM', destination: 'DEL', averageFare: 5810, index: 127.1, yoyChange: 9.7, momChange: 1.0, observations: 2942 }
]

export const airlines = [
  { id: 'indigo', name: 'IndiGo', averageFare: 5240, index: 124.8, yoyChange: 8.2, momChange: 1.4, observations: 5642 },
  { id: 'airindia', name: 'Air India', averageFare: 6140, index: 131.4, yoyChange: 11.7, momChange: 2.0, observations: 4821 },
  { id: 'akasa', name: 'Akasa Air', averageFare: 4980, index: 119.3, yoyChange: 5.6, momChange: 1.1, observations: 2981 },
  { id: 'spicejet', name: 'SpiceJet', averageFare: 4620, index: 117.1, yoyChange: 6.8, momChange: 0.9, observations: 2431 }
]

export const flightObservations = [
  { timestamp: '2026-08-24T11:58:00', airline: 'IndiGo', route: 'DEL-BOM', flightNumber: '6E123', travelDate: '2026-08-30', fare: 5482, currency: 'INR', stops: 0, source: 'Airline' },
  { timestamp: '2026-08-24T12:05:00', airline: 'Air India', route: 'DEL-BOM', flightNumber: 'AI101', travelDate: '2026-08-30', fare: 6140, currency: 'INR', stops: 0, source: 'Airline' }
]

export const collectionStatus = [
  { source: 'IndiGo', status: 'Active', records: 5642, success: 99.1 },
  { source: 'Air India', status: 'Active', records: 4821, success: 98.7 },
  { source: 'Akasa Air', status: 'Active', records: 2981, success: 98.9 },
  { source: 'SpiceJet', status: 'Active', records: 2431, success: 97.8 },
  { source: 'OTA Source', status: 'Active', records: 4241, success: 98.1 }
]

export const methodology = {
  overview: 'This prototype demonstrates a reproducible approach to constructing an Airfare Price Index using automated price observations, cleaning, route-level aggregation and weighting. Data shown is demo data.',
  basePeriod: 'January 2025',
  routeBasket: ['DEL-BOM','DEL-BLR','BOM-DEL','DEL-HYD','BOM-BLR'],
  weights: [
    { route: 'DEL-BOM', weight: 0.25 },
    { route: 'DEL-BLR', weight: 0.2 },
    { route: 'BOM-DEL', weight: 0.2 },
    { route: 'DEL-HYD', weight: 0.2 },
    { route: 'BOM-BLR', weight: 0.15 }
  ]
}

export default { index, indexHistory, routes, airlines, flightObservations, collectionStatus, methodology }
