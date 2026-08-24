import axios from 'axios'
import mock from '../data/mockData'

const base = import.meta.env.VITE_API_BASE_URL || ''
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
  let data = mock.flightObservations.slice()
  if(params){
    if(params.q){
      const q = params.q.toLowerCase()
      data = data.filter(f => (f.airline||'').toLowerCase().includes(q) || (f.flightNumber||'').toLowerCase().includes(q) || (f.route||'').toLowerCase().includes(q))
    }
    if(params.origin){
      data = data.filter(f => f.route && f.route.startsWith(params.origin))
    }
    if(params.destination){
      data = data.filter(f => f.route && f.route.endsWith(params.destination))
    }
    if(params.airline){
      data = data.filter(f => f.airline===params.airline)
    }
    if(params.from || params.to){
      data = data.filter(f => {
        const ts = new Date(f.timestamp).getTime()
        if(params.from && ts < new Date(params.from).getTime()) return false
        if(params.to && ts > new Date(params.to).getTime()) return false
        return true
      })
    }
  }
  const page = params?.page||1
  const pageSize = params?.pageSize||10
  const start = (page-1)*pageSize
  const paged = data.slice(start, start+pageSize)
  return Promise.resolve({ data: paged, total: data.length })
}
export async function getDataStatus(){
  return Promise.resolve({ data: mock.collectionStatus })
}

export async function getMethodology(){
  return Promise.resolve({ data: mock.methodology })
}

export default client
