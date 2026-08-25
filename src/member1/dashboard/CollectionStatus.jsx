import React from 'react'

export default function CollectionStatus({ status }){
  return (
    <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
      <h3 className="text-base font-semibold text-primary-text mb-4">Data Collection Status</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border-light">
              <th className="text-left py-3 px-3 font-semibold text-primary-text">Source</th>
              <th className="text-center py-3 px-3 font-semibold text-primary-text">Status</th>
              <th className="text-right py-3 px-3 font-semibold text-primary-text">Last Collection</th>
              <th className="text-right py-3 px-3 font-semibold text-primary-text">Records</th>
              <th className="text-right py-3 px-3 font-semibold text-primary-text">Success Rate</th>
            </tr>
          </thead>
          <tbody>
            {status.map(s=> (
              <tr key={s.source} className="border-b border-border-light hover:bg-body-bg transition-colors">
                <td className="py-3 px-3 text-primary-text font-medium">{s.source}</td>
                <td className="py-3 px-3 text-center">
                  <div className="flex items-center justify-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${s.status==='Active'? 'bg-success-green': s.status==='Delayed'? 'bg-warning-amber': 'bg-error-red'} animate-pulse`}></span>
                    <span className={`text-xs font-medium ${s.status==='Active'? 'text-success-green': s.status==='Delayed'? 'text-warning-amber': 'text-error-red'}`}>{s.status}</span>
                  </div>
                </td>
                <td className="py-3 px-3 text-secondary-text text-right">{s.lastCollection || '11:58 AM'}</td>
                <td className="py-3 px-3 text-secondary-text text-right">{s.records || '0'}</td>
                <td className="py-3 px-3 text-right">
                  <span className="badge badge-success">{s.success || '0'}%</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
