import React, { useEffect, useState } from 'react'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import Table from '../../components/ui/Table'
import EmptyState from '../../components/ui/EmptyState'
import ErrorState from '../../components/ui/ErrorState'
import Skeleton from '../../components/ui/Skeleton'
import { getFlights } from '../../services/api'
import { csvFromArray, inr } from '../../utils/format'
import { Search, Download } from 'lucide-react'

export default function DataExplorer(){
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [data, setData] = useState([])
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [total, setTotal] = useState(0)
  const [q, setQ] = useState('')

  useEffect(()=>{
    load()
  },[page, pageSize, q])

  function load(){
    setLoading(true)
    setError(null)
    getFlights({ page, pageSize, q }).then(r=>{
      setData(r.data)
      setTotal(r.total || r.data.length)
      setLoading(false)
    }).catch(e=>{
      setError(e.message||'Error')
      setLoading(false)
    })
  }

  function exportCsv(){
    if(!data.length) return
    const csv = csvFromArray(data.map(d=>({ timestamp: d.timestamp, airline: d.airline, route: d.route, flightNumber: d.flightNumber, travelDate: d.travelDate, fare: d.fare, currency: d.currency, stops: d.stops, source: d.source })))
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'airtn-data-export.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  const columns = [
    { key: 'timestamp', title: 'Timestamp', render: r=> new Date(r.timestamp).toLocaleString() },
    { key: 'airline', title: 'Airline' },
    { key: 'route', title: 'Route' },
    { key: 'flightNumber', title: 'Flight No.' },
    { key: 'travelDate', title: 'Travel Date' },
    { key: 'fare', title: 'Fare', render: r=> inr(r.fare) },
    { key: 'stops', title: 'Stops' },
    { key: 'source', title: 'Source' }
  ]

  return (
    <Layout>
      <PageHeader 
        title="Data Explorer" 
        description="Explore raw airfare observations for transparency and verification."
      />

      {/* Filter Bar */}
      <div className="mb-6 bg-white rounded-lg border border-border-light p-4 shadow-sm">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1">
            <label className="block text-xs font-semibold text-secondary-text mb-2">Search</label>
            <input 
              type="text"
              placeholder="Search airline, flight, route..." 
              value={q} 
              onChange={(e)=>setQ(e.target.value)} 
              className="w-full px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue" 
            />
          </div>
          <div className="flex items-end gap-2">
            <button 
              onClick={()=>{ setPage(1); load() }} 
              className="px-4 py-2 bg-primary-blue text-white rounded-lg font-medium hover:bg-bright-blue transition-colors flex items-center gap-2"
            >
              <Search className="w-4 h-4" />
              Search
            </button>
            <button 
              onClick={()=>{ setQ(''); setPage(1) }} 
              className="px-4 py-2 bg-body-bg text-secondary-text rounded-lg font-medium hover:bg-border-light transition-colors"
            >
              Reset
            </button>
            <button 
              onClick={exportCsv} 
              className="px-4 py-2 bg-airtn-teal text-white rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export
            </button>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-lg border border-border-light shadow-sm overflow-hidden">
        {loading && (
          <div className="p-6 space-y-3">
            <Skeleton className="h-6 w-1/3" />
            <Skeleton className="h-40 w-full" />
          </div>
        )}

        {error && (
          <div className="p-6">
            <ErrorState message={error} onRetry={load} />
          </div>
        )}

        {!loading && !error && data.length===0 && (
          <div className="p-12">
            <EmptyState 
              title="No airfare observations found" 
              message="Try changing your search criteria or filters." 
              action={
                <button 
                  onClick={()=>{ setQ(''); setPage(1); load() }} 
                  className="px-4 py-2 bg-primary-blue text-white rounded-lg font-medium hover:bg-bright-blue transition-colors"
                >
                  Clear Filters
                </button>
              } 
            />
          </div>
        )}

        {!loading && !error && data.length>0 && (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-body-bg border-b border-border-light">
                  <tr>
                    {columns.map(col=> (
                      <th key={col.key} className="text-left py-3 px-4 font-semibold text-primary-text">{col.title}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, idx)=> (
                    <tr key={idx} className="border-b border-border-light hover:bg-body-bg transition-colors">
                      {columns.map(col=> (
                        <td key={col.key} className="py-3 px-4 text-secondary-text">
                          {col.render ? col.render(row) : row[col.key]}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 border-t border-border-light">
              <div className="text-xs text-secondary-text">
                Showing {((page-1)*pageSize)+1} - {Math.min(page*pageSize, total)} of {total} results
              </div>
              <div className="flex items-center gap-2">
                <label className="text-xs font-semibold text-secondary-text">Per page:</label>
                <select 
                  value={pageSize} 
                  onChange={e=>{ setPageSize(Number(e.target.value)); setPage(1) }} 
                  className="px-3 py-1 border border-border-light rounded text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue text-sm"
                >
                  <option value={5}>5</option>
                  <option value={10}>10</option>
                  <option value={25}>25</option>
                  <option value={50}>50</option>
                </select>
                <button 
                  onClick={()=>setPage(p=>Math.max(1,p-1))} 
                  disabled={page===1}
                  className="px-3 py-1 border border-border-light rounded text-primary-text bg-white hover:bg-body-bg transition-colors disabled:opacity-50 text-sm font-medium"
                >
                  ← Prev
                </button>
                <div className="px-2 py-1 text-xs font-semibold text-primary-text">Page {page}</div>
                <button 
                  onClick={()=>setPage(p=>p+1)} 
                  disabled={page*pageSize >= total}
                  className="px-3 py-1 border border-border-light rounded text-primary-text bg-white hover:bg-body-bg transition-colors disabled:opacity-50 text-sm font-medium"
                >
                  Next →
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </Layout>
  )
}
