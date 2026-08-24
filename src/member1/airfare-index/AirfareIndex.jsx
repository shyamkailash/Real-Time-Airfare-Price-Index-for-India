import React, { useEffect, useState } from 'react'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import IndexTrendChart from '../dashboard/IndexTrendChart'
import { getCurrentIndex, getIndexHistory } from '../../services/api'
import { TrendingUp, ArrowUpRight } from 'lucide-react'
import { filterIndexHistory } from '../../utils/indexHistory'

function calcStats(history){
  const vals = history.map(h=>h.value)
  const sum = vals.reduce((a,b)=>a+b,0)
  const avg = vals.length? sum/vals.length:0
  const sd = Math.sqrt(vals.reduce((a,b)=>a+Math.pow(b-avg,2),0)/ (vals.length||1))
  return { highest: Math.max(...vals), lowest: Math.min(...vals), average: avg, stddev: sd }
}

export default function AirfareIndex(){
  const [index, setIndex] = useState(null)
  const [history, setHistory] = useState([])
  const [timeRange, setTimeRange] = useState('1Y')

  useEffect(()=>{
    getCurrentIndex().then(r=>setIndex(r.data))
    getIndexHistory().then(r=>setHistory(r.data))
  },[])

  const stats = calcStats(history)
  const currentIndex = index?.index || 128.42
  const yoyChange = index?.yoyChange || 8.42
  const momChange = index?.momChange || 1.72
  const chartHistory = filterIndexHistory(history, timeRange)

  return (
    <Layout>
      <PageHeader 
        title="Airfare Price Index" 
        description="Detailed Index Analysis and Historical Trends"
      />

      {index && (
        <div className="space-y-6">
          {/* Key metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide">Current Index</p>
                  <p className="text-4xl font-bold text-primary-text mt-3">{currentIndex.toFixed(2)}</p>
                </div>
                <div className="p-2 bg-primary-blue/10 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-primary-blue" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide mb-3">Year-on-Year (YoY)</p>
              <div className="text-3xl font-bold text-success-green flex items-center gap-2">
                <ArrowUpRight className="w-6 h-6" />
                {yoyChange.toFixed(2)}%
              </div>
            </div>

            <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <p className="text-xs font-semibold text-secondary-text uppercase tracking-wide mb-3">Month-on-Month (MoM)</p>
              <div className="text-3xl font-bold text-success-green flex items-center gap-2">
                <ArrowUpRight className="w-6 h-6" />
                {momChange.toFixed(2)}%
              </div>
            </div>
          </div>

          {/* Main grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Chart - 65% */}
            <div className="lg:col-span-2 bg-white rounded-lg border border-border-light p-6 shadow-sm">
              <h3 className="text-base font-semibold text-primary-text mb-4">Historical Index Movement</h3>
              <div className="mb-4 flex gap-2">
                {['3M', '6M', '1Y', 'ALL'].map((range) => (
                  <button
                    key={range}
                    type="button"
                    onClick={() => setTimeRange(range)}
                    className={`rounded px-3 py-1 text-xs font-medium ${timeRange === range ? 'bg-primary-blue text-white' : 'bg-body-bg text-secondary-text hover:bg-border-light'}`}
                  >
                    {range === 'ALL' ? 'All' : range}
                  </button>
                ))}
              </div>
              <IndexTrendChart data={chartHistory.map(h=>({date:h.date,value:h.value}))} />
            </div>

            {/* Right column - 35% */}
            <div className="space-y-6">
              {/* Index Statistics */}
              <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
                <h3 className="text-base font-semibold text-primary-text mb-4">Index Statistics</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between py-2 border-b border-border-light">
                    <span className="text-secondary-text">Base Period</span>
                    <span className="font-medium text-primary-text">January 2025</span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-border-light">
                    <span className="text-secondary-text">Base Index</span>
                    <span className="font-medium text-primary-text">100.00</span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-border-light">
                    <span className="text-secondary-text">Highest Index</span>
                    <span className="font-medium text-primary-text">{stats.highest? stats.highest.toFixed(2): '-'}</span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-border-light">
                    <span className="text-secondary-text">Lowest Index</span>
                    <span className="font-medium text-primary-text">{stats.lowest? stats.lowest.toFixed(2): '-'}</span>
                  </div>
                  <div className="flex justify-between py-2 border-b border-border-light">
                    <span className="text-secondary-text">Average Index</span>
                    <span className="font-medium text-primary-text">{stats.average? stats.average.toFixed(2): '-'}</span>
                  </div>
                  <div className="flex justify-between py-2">
                    <span className="text-secondary-text">Std. Deviation</span>
                    <span className="font-medium text-primary-text">{stats.stddev? stats.stddev.toFixed(2): '-'}</span>
                  </div>
                </div>
              </div>

              {/* Change Summary */}
              <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
                <h3 className="text-base font-semibold text-primary-text mb-4">Index Change Summary</h3>
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 bg-body-bg rounded-lg text-center">
                    <p className="text-xs text-secondary-text">1 Month</p>
                    <p className="text-lg font-bold text-success-green mt-1">+{momChange.toFixed(2)}%</p>
                  </div>
                  <div className="p-3 bg-body-bg rounded-lg text-center">
                    <p className="text-xs text-secondary-text">3 Months</p>
                    <p className="text-lg font-bold text-success-green mt-1">+4.91%</p>
                  </div>
                  <div className="p-3 bg-body-bg rounded-lg text-center">
                    <p className="text-xs text-secondary-text">6 Months</p>
                    <p className="text-lg font-bold text-success-green mt-1">+8.42%</p>
                  </div>
                  <div className="p-3 bg-body-bg rounded-lg text-center">
                    <p className="text-xs text-secondary-text">12 Months</p>
                    <p className="text-lg font-bold text-success-green mt-1">+28.42%</p>
                  </div>
                </div>
              </div>

              {/* Interpretation */}
              <div className="bg-blue-50 rounded-lg border border-blue-200 p-4">
                <h4 className="text-sm font-semibold text-primary-blue mb-2">Index Interpretation</h4>
                <p className="text-xs text-primary-text leading-relaxed">
                  An index value of {currentIndex.toFixed(2)} indicates that the monitored airfare level is approximately {(currentIndex - 100).toFixed(2)}% above the selected base period (January 2025).
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}
