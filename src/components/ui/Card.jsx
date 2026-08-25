import React from 'react'

export default function Card({ children, className='' }){
  return (
    <div className={`rounded-lg p-4 surface-card ${className}`}>{children}</div>
  )
}
