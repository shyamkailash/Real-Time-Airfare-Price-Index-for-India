import React, { useEffect, useState } from 'react'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import { getAirlines, getIndexHistory } from '../../services/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { ArrowUpRight } from 'lucide-react'

export default function AirlineAnalysis(){
  const [airlines, setAirlines] = useState([])
  const [history, setHistory] = useState([])
  const [selected, setSelected] = useState(null)

  useEffect(()=>{
    getAirlines().then(r=>setAirlines(r.data))
    getIndexHistory().then(r=>setHistory(r.data))
  },[])

  useEffect(()=>{
    if(airlines.length) setSelected(airlines[0].id)
  },[airlines])

  return (
    <Layout>
      <PageHeader 
        title="Airline Analysis" 
        description="Compare airline-level fares and performance metrics."
      />

      <div className="space-y-6">
        {/* Airline Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {airlines.map(a=> (
            <div key={a.id} className="bg-white rounded-lg border border-border-light p-5 shadow-sm hover:shadow-md transition-shadow">
              <h3 className="text-sm font-semibold text-primary-text">{a.name}</h3>
              <div className="mt-3 space-y-2">
                <div>
                  <p className="text-xs text-secondary-text">Average Fare</p>
                  <p className="text-xl font-bold text-primary-text mt-1">₹{a.averageFare.toLocaleString('en-IN')}</p>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-secondary-text">Index</p>
                    <p className="text-lg font-bold text-primary-text">{a.index}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-secondary-text">YoY</p>
                    <p className="text-lg font-bold text-success-green flex items-center justify-end gap-1">
                      <ArrowUpRight className="w-4 h-4" />
                      {a.yoyChange}%
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Fare Comparison */}
          <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
            <h3 className="text-base font-semibold text-primary-text mb-4">Airline Market Comparison</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={airlines} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <XAxis dataKey="name" tick={{fill: '#64748B', fontSize: 12}} angle={-45} textAnchor="end" height={80} />
                  <YAxis tick={{fill: '#64748B'}} />
                  <Tooltip contentStyle={{backgroundColor: '#FFFFFF', border: '1px solid #E2E8F0'}} />
                  <Bar dataKey="averageFare" fill="#1769E0" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Index Trend */}
          <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
            <h3 className="text-base font-semibold text-primary-text mb-4">Index Historical Trend</h3>
            <div className="mb-4">
              <label className="text-xs font-semibold text-secondary-text">Airline</label>
              <select 
                value={selected||''} 
                onChange={e=>setSelected(e.target.value)} 
                className="w-full mt-2 px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue"
              >
                {airlines.map(a=> <option key={a.id} value={a.id}>{a.name}</option>)}
              </select>
            </div>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={history.map(h=>({date:h.date, value:h.value}))}>
                  <XAxis dataKey="date" tick={{fill: '#64748B'}} />
                  <YAxis tick={{fill: '#64748B'}} />
                  <Tooltip contentStyle={{backgroundColor: '#FFFFFF', border: '1px solid #E2E8F0'}} />
                  <Bar dataKey="value" fill="#00BFA6" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Performance Table */}
        <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
          <h3 className="text-base font-semibold text-primary-text mb-4">Airline Performance Table</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border-light">
                  <th className="text-left py-3 px-3 font-semibold text-primary-text">Airline</th>
                  <th className="text-right py-3 px-3 font-semibold text-primary-text">Avg Fare</th>
                  <th className="text-center py-3 px-3 font-semibold text-primary-text">Index</th>
                  <th className="text-center py-3 px-3 font-semibold text-primary-text">YoY Change</th>
                  <th className="text-right py-3 px-3 font-semibold text-primary-text">Market Share</th>
                </tr>
              </thead>
              <tbody>
                {airlines.map(a=> (
                  <tr key={a.id} className="border-b border-border-light hover:bg-body-bg transition-colors">
                    <td className="py-3 px-3 text-primary-text font-medium">{a.name}</td>
                    <td className="py-3 px-3 text-right text-secondary-text">₹{a.averageFare.toLocaleString('en-IN')}</td>
                    <td className="py-3 px-3 text-center text-primary-text font-medium">{a.index}</td>
                    <td className="py-3 px-3 text-center">
                      <span className="text-success-green font-medium flex items-center justify-center gap-1">
                        <ArrowUpRight className="w-4 h-4" />
                        {a.yoyChange}%
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right text-secondary-text">~{Math.round(100/airlines.length)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  )
}
