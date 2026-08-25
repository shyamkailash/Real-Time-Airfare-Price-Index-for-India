import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Area, AreaChart } from 'recharts'

const formatMonth = (date) => new Intl.DateTimeFormat('en-IN', {
  month: 'short',
  year: 'numeric'
}).format(new Date(date))

export default function IndexTrendChart({ data }){
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="colorIndex" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#1769E0" stopOpacity={0.1}/>
              <stop offset="95%" stopColor="#1769E0" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#E8EEF5" vertical={false} />
          <XAxis 
            dataKey="date" 
            tickFormatter={formatMonth}
            tick={{fill: '#64748B', fontSize: 12}} 
            axisLine={{stroke: '#E2E8F0'}}
            tickLine={{stroke: '#E2E8F0'}}
          />
          <YAxis 
            domain={['auto', 'auto']}
            tick={{fill: '#64748B', fontSize: 12}}
            axisLine={{stroke: '#E2E8F0'}}
            tickLine={{stroke: '#E2E8F0'}}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #E2E8F0',
              borderRadius: '8px',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.07)'
            }}
            labelStyle={{color: '#172033'}}
            labelFormatter={formatMonth}
          />
          <Area type="monotone" dataKey="value" stroke="#1769E0" strokeWidth={2} fillOpacity={1} fill="url(#colorIndex)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
