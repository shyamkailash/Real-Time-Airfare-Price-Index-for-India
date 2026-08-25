import React, { useEffect, useState } from 'react'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import { getRoutes, getRouteDetails } from '../../services/api'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'
import { ArrowUpRight } from 'lucide-react'

export default function RouteAnalysis(){
  const [routes, setRoutes] = useState([])
  const [selected, setSelected] = useState(null)
  const [details, setDetails] = useState(null)

  useEffect(()=>{
    getRoutes().then(r=>{ setRoutes(r.data); if(r.data[0]) setSelected(r.data[0].id) })
  },[])

  useEffect(()=>{
    if(selected) getRouteDetails(selected).then(r=>setDetails(r.data))
  },[selected])

  return (
    <Layout>
      <PageHeader 
        title="Route Analysis" 
        description="Analyze airfare trends across domestic routes."
      />

      <div className="space-y-6">
        {/* Filter bar */}
        <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-secondary-text mb-2">Select Route</label>
              <select 
                value={selected||''} 
                onChange={e=>setSelected(e.target.value)} 
                className="w-full px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue"
              >
                {routes.map(r=> <option key={r.id} value={r.id}>{r.origin} → {r.destination}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-secondary-text mb-2">Travel Date</label>
              <input 
                type="date" 
                className="w-full px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue"
              />
            </div>
            <div className="flex items-end">
              <button className="w-full px-4 py-2 bg-primary-blue text-white rounded-lg font-medium hover:bg-bright-blue transition-colors">
                Apply Filters
              </button>
            </div>
          </div>
        </div>

        {details && (
          <div className="space-y-6">
            {/* Route Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
                <p className="text-xs font-semibold text-secondary-text uppercase">Average Fare</p>
                <p className="text-2xl font-bold text-primary-text mt-2">₹{details.averageFare.toLocaleString('en-IN')}</p>
              </div>
              <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
                <p className="text-xs font-semibold text-secondary-text uppercase">Route Index</p>
                <p className="text-2xl font-bold text-primary-text mt-2">{details.index}</p>
              </div>
              <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
                <p className="text-xs font-semibold text-secondary-text uppercase">YoY Change</p>
                <div className="text-2xl font-bold text-success-green mt-2 flex items-center gap-1">
                  <ArrowUpRight className="w-5 h-5" />
                  {details.yoyChange}%
                </div>
              </div>
              <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
                <p className="text-xs font-semibold text-secondary-text uppercase">Observations</p>
                <p className="text-2xl font-bold text-primary-text mt-2">{details.observations}</p>
              </div>
            </div>

            {/* Chart and Performance */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Fare Trend Chart */}
              <div className="lg:col-span-2 bg-white rounded-lg border border-border-light p-6 shadow-sm">
                <h3 className="text-base font-semibold text-primary-text mb-4">Fare Trend</h3>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={[
                      {date:'Jan', avg: details.averageFare-400},
                      {date:'Feb', avg: details.averageFare-200},
                      {date:'Mar', avg: details.averageFare}
                    ]}>
                      <defs>
                        <linearGradient id="colorFare" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#1769E0" stopOpacity={0.1}/>
                          <stop offset="95%" stopColor="#1769E0" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <XAxis dataKey="date" tick={{fill: '#64748B'}} />
                      <YAxis tick={{fill: '#64748B'}} />
                      <Tooltip />
                      <Area type="monotone" dataKey="avg" stroke="#1769E0" fillOpacity={1} fill="url(#colorFare)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Route Performance */}
              <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
                <h3 className="text-base font-semibold text-primary-text mb-4">Route Performance</h3>
                <div className="space-y-3">
                  <div className="py-3 border-b border-border-light">
                    <p className="text-xs text-secondary-text">Cheapest Fare</p>
                    <p className="text-lg font-bold text-primary-text mt-1">₹3,842</p>
                  </div>
                  <div className="py-3 border-b border-border-light">
                    <p className="text-xs text-secondary-text">Highest Fare</p>
                    <p className="text-lg font-bold text-primary-text mt-1">₹7,842</p>
                  </div>
                  <div className="py-3 border-b border-border-light">
                    <p className="text-xs text-secondary-text">Average Fare</p>
                    <p className="text-lg font-bold text-primary-text mt-1">₹{details.averageFare.toLocaleString('en-IN')}</p>
                  </div>
                  <div className="py-3 border-b border-border-light">
                    <p className="text-xs text-secondary-text">Fare Volatility</p>
                    <p className="text-lg font-bold text-warning-amber mt-1">High</p>
                  </div>
                  <div className="py-3">
                    <p className="text-xs text-secondary-text">Load Factor</p>
                    <p className="text-lg font-bold text-primary-text mt-1">78%</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}
