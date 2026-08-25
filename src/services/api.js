import axios from 'axios'
import mock from '../data/mockData'

const base = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const client = axios.create({ baseURL: base })

export async function getCurrentIndex(){
  const response = await client.get('/api/index/current')
  return { data: response.data }
}
export async function getIndexHistory(){
  const response = await client.get('/api/index/history')
  return { data: response.data }
}
export async function getRoutes(){
  const response = await client.get('/api/routes')
  return { data: response.data.map(route => ({
    ...route,
    travelDate: route.travel_date,
  })) }
}
export async function getRouteDetails(id){
  const [origin, destination] = id.split('-')
  const route = await getRoutes().then(response => response.data.find(item => item.id === id))
  const response = await client.get(`/api/routes/${origin}/${destination}/${route.travel_date}`)
  const detail = response.data
  const fares = detail.observations.map(observation => observation.fare)
  return { data: {
    ...route,
    averageFare: detail.index?.historical_average || 0,
    index: detail.index?.price_index || 100,
    yoyChange: 0,
    observations: detail.index?.sample_count || fares.length,
    fareObservations: detail.observations,
  } }
}
export async function getAirlines(){
  const response = await client.get('/api/airlines')
  return { data: response.data.map(airline => ({
    ...airline,
    averageFare: airline.average_fare,
    observations: airline.observation_count,
    yoyChange: airline.yoyChange || 0,
  })) }
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
