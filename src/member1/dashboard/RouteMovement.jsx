import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight } from 'lucide-react'

export default function RouteMovement({ routes }){
  const displayRoutes = routes.slice(0, 5)

  return (
    <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
      <h3 className="text-base font-semibold text-primary-text mb-4">Route Movement (YoY)</h3>
      <div className="space-y-3">
        {displayRoutes.map(r=> (
          <div key={r.id} className="flex items-center justify-between py-2 border-b border-border-light last:border-0">
            <div className="flex-1">
              <div className="text-sm font-medium text-primary-text">{r.origin} → {r.destination}</div>
              <div className="text-xs text-secondary-text">₹{new Intl.NumberFormat('en-IN').format(r.averageFare)}</div>
            </div>
            <div className={`flex items-center gap-1 text-sm font-medium ${r.yoyChange>=0 ? 'text-success-green' : 'text-error-red'}`}>
              <ArrowUpRight className="w-4 h-4" />
              {r.yoyChange>=0? `+${r.yoyChange}%` : `${r.yoyChange}%`}
            </div>
          </div>
        ))}
      </div>
      <Link to="/routes" className="mt-4 inline-block text-sm font-medium text-primary-blue hover:text-bright-blue transition-colors">
        View All →
      </Link>
    </div>
  )
}
