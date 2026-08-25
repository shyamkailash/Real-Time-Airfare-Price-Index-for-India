import React from 'react'

export default function ErrorState({ title='Unable to load data', message='', onRetry }){
  return (
    <div className="p-6 surface-card rounded-lg text-center">
      <div className="text-lg font-semibold">{title}</div>
      {message && <div className="mt-2 text-stext">{message}</div>}
      {onRetry && <button onClick={onRetry} className="mt-4 px-3 py-2 bg-amber rounded">Retry</button>}
    </div>
  )
}
