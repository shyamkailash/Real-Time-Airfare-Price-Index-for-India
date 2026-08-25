import React from 'react'

export default function Skeleton({ className='' }){
  return <div className={`animate-pulse bg-slate-700 rounded ${className}`}></div>
}
