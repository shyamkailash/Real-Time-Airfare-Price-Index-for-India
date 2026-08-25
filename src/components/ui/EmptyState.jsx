import React from 'react'

export default function EmptyState({ title='No results', message='', action }){
  return (
    <div className="text-center p-8 surface-card rounded-lg">
      <div className="text-xl font-semibold">{title}</div>
      {message && <div className="mt-2 text-stext">{message}</div>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
