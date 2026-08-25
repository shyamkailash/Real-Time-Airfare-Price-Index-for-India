import axios from 'axios'
import mock from '../data/mockData'

const base = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const client = axios.create({ baseURL: base })

export async function getCurrentIndex(){
  // replace with: return client.get('/index/current')
  return Promise.resolve({ data: mock.index })
}
export async function getIndexHistory(){
  return Promise.resolve({ data: mock.indexHistory })
}
export async function getRoutes(){
  return Promise.resolve({ data: mock.routes })
}
export async function getRouteDetails(id){
  const item = mock.routes.find(r=>r.id===id)
  return Promise.resolve({ data: item })
}
export async function getAirlines(){
  return Promise.resolve({ data: mock.airlines })
}
export async function getFlights(params){
  // params: { page, pageSize, q, origin, destination, airline, source, from, to }
  const response = await client.get('/api/observations', {
    params: {
      page: params?.page || 1,
      page_size: params?.pageSize || 10,
      q: params?.q || undefined,
      origin: params?.origin || undefined,
      destination: params?.destination || undefined,
      airline: params?.airline || undefined,
      source: params?.source || undefined,
    },
  })

  return {
    data: response.data.data.map(observation => ({
      id: observation.id,
      timestamp: observation.collected_at,
      route: `${observation.origin}-${observation.destination}`,
      flightNumber: observation.flight_number,
      travelDate: observation.travel_date,
      fare: observation.fare,
      currency: observation.currency,
      stops: observation.stops,
      source: observation.source,
      airline: observation.airline,
    })),
    total: response.data.total,
  }
}
export async function getDataStatus(){
  return Promise.resolve({ data: mock.collectionStatus })
}

export async function getMethodology(){
  return Promise.resolve({ data: mock.methodology })
}

export default client
