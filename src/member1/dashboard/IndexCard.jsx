import React from 'react'
import Card from '../../components/ui/Card'
import { LineChart, Line, ResponsiveContainer } from 'recharts'

export default function IndexCard({ index, history }){
  return (
    <Card className="flex flex-col lg:flex-row items-start gap-6">
      <div className="flex-1">
        <div className="text-sm text-stext">INDIA AIRFARE PRICE INDEX</div>
        <div className="text-5xl font-semibold mt-2">{index.index.toFixed(2)}</div>
        <div className="text-sm text-stext mt-2">
          <span className="text-emerald">▲ {index.yoyChange}% YoY</span>
          <span className="ml-3 text-stext">▲ {index.momChange}% MoM</span>
        </div>
        <div className="text-xs text-stext mt-3">Base Period<br/>{index.basePeriod}</div>
        <div className="text-xs text-stext">Last Updated<br/>{new Date(index.lastUpdated).toLocaleString()}</div>
      </div>
      <div className="w-full md:w-64 h-36">
        <ResponsiveContainer>
          <LineChart data={history}>
            <Line type="monotone" dataKey="value" stroke="#14B8A6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}
