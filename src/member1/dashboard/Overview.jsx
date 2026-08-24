import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import IndexTrendChart from './IndexTrendChart'
import RouteMovement from './RouteMovement'
import CollectionStatus from './CollectionStatus'
import { getCurrentIndex, getIndexHistory, getRoutes, getDataStatus } from '../../services/api'
import { TrendingUp, ArrowUpRight, Calendar, Database, Plane, BarChart2, Layers } from 'lucide-react'
import { filterIndexHistory } from '../../utils/indexHistory'

export default function Overview(){
  const [index, setIndex] = useState(null)
  const [history, setHistory] = useState([])
  const [routes, setRoutes] = useState([])
  const [status, setStatus] = useState([])
  const [timeRange, setTimeRange] = useState('1Y')

  useEffect(()=>{
    getCurrentIndex().then(r=>setIndex(r.data))
    getIndexHistory().then(r=>setHistory(r.data))
    getRoutes().then(r=>setRoutes(r.data))
    getDataStatus().then(r=>setStatus(r.data))
  },[])

  const primaryIndex = index?.index ?? 128.42
  const yoyChange = 8.42
  const momChange = 1.72
  const chartHistory = filterIndexHistory(history, timeRange)

  return (
    <Layout>
      <PageHeader 
        title="Overview" 
        description="Real-time Airfare Intelligence Dashboard"
      />

      <div className="space-y-6">
        {/* Primary KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Main Index Card */}
          <div className="md:col-span-1 bg-white rounded-lg border border-border-light p-6 shadow-sm">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">India Airfare Price Index</p>
                <div className="text-4xl font-bold text-primary-text mt-3">{primaryIndex.toFixed(2)}</div>
              </div>
              <div className="p-2 bg-primary-blue/10 rounded-lg">
                <TrendingUp className="w-5 h-5 text-primary-blue" />
              </div>
            </div>
            <div className="pt-4 border-t border-border-light">
              <p className="text-xs text-secondary-text">Base Period: <span className="font-medium text-primary-text">January 2025</span></p>
              <p className="text-xs text-secondary-text mt-1">(Jan 2025 = 100)</p>
            </div>
          </div>

          {/* YoY Change Card */}
          <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Year-on-Year (YoY)</p>
                <div className="text-3xl font-bold text-success-green mt-3 flex items-center gap-2">
                  <ArrowUpRight className="w-6 h-6" />
                  {yoyChange.toFixed(2)}%
                </div>
              </div>
            </div>
            <div className="pt-4 border-t border-border-light">
              <p className="text-xs text-secondary-text">Compared to Aug 2025</p>
            </div>
          </div>

          {/* MoM Change Card */}
          <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Month-on-Month (MoM)</p>
                <div className="text-3xl font-bold text-success-green mt-3 flex items-center gap-2">
                  <ArrowUpRight className="w-6 h-6" />
                  {momChange.toFixed(2)}%
                </div>
              </div>
            </div>
            <div className="pt-4 border-t border-border-light">
              <p className="text-xs text-secondary-text">Compared to Jul 2026</p>
            </div>
          </div>
        </div>

        {/* Secondary KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Avg. Airfare</p>
              <Plane className="w-4 h-4 text-secondary-text" />
            </div>
            <p className="text-2xl font-bold text-primary-text">₹5,842</p>
            <p className="text-xs text-secondary-text mt-2">Across all routes</p>
          </div>

          <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Total Observations</p>
              <Database className="w-4 h-4 text-secondary-text" />
            </div>
            <p className="text-2xl font-bold text-primary-text">24,821</p>
            <p className="text-xs text-secondary-text mt-2">Today</p>
          </div>

          <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Routes Covered</p>
              <BarChart2 className="w-4 h-4 text-secondary-text" />
            </div>
            <p className="text-2xl font-bold text-primary-text">24</p>
            <p className="text-xs text-secondary-text mt-2">Domestic Routes</p>
          </div>

          <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Airlines Tracked</p>
              <Layers className="w-4 h-4 text-secondary-text" />
            </div>
            <p className="text-2xl font-bold text-primary-text">7</p>
            <p className="text-xs text-secondary-text mt-2">Active Airlines</p>
          </div>

          <div className="bg-white rounded-lg border border-border-light p-4 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Data Sources</p>
              <Database className="w-4 h-4 text-secondary-text" />
            </div>
            <p className="text-2xl font-bold text-primary-text">5</p>
            <p className="text-xs text-secondary-text mt-2">Airlines + OTAs</p>
          </div>
        </div>

        {/* Main Grid - Charts and Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - 65% */}
          <div className="lg:col-span-2 space-y-6">
            {/* Index Trend Chart */}
            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <h3 className="text-base font-semibold text-primary-text mb-4">Airfare Price Index Trend</h3>
              <div className="flex gap-2 mb-4">
                {['3M', '6M', '1Y', 'ALL'].map(period => (
                  <button 
                    key={period}
                    className={`px-3 py-1 text-xs font-medium rounded ${
                      period === timeRange
                        ? 'bg-primary-blue text-white' 
                        : 'bg-body-bg text-secondary-text hover:bg-border-light'
                    }`}
                    onClick={() => setTimeRange(period)}
                  >
                    {period === 'ALL' ? 'All' : period}
                  </button>
                ))}
              </div>
              <IndexTrendChart data={chartHistory.map(h=>({date: h.date, value: h.value}))} />
            </div>

            {/* Data Collection Status */}
            <CollectionStatus status={status} />
          </div>

          {/* Right Column - 35% */}
          <div className="space-y-6">
            {/* Route Movement */}
            <RouteMovement routes={routes} />

            {/* About AIRTN */}
            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <h3 className="text-base font-semibold text-primary-text mb-3">About AIRTN</h3>
              <p className="text-sm text-secondary-text leading-relaxed mb-4">
                AIRTN is an analytical platform designed to monitor real-time airfare movements across Indian domestic routes and provide statistical insights through automated data collection, route analysis and airfare index construction.
              </p>
              <Link to="/methodology" className="text-sm font-medium text-primary-blue hover:text-bright-blue transition-colors">
                Learn Methodology →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
