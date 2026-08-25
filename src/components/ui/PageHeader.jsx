import React from 'react'
import { useLocation } from 'react-router-dom'
import BackButton from './BackButton'

export default function PageHeader({ title, description, children }){
  const location = useLocation()
  const isOverview = location.pathname === '/'
  
  return (
    <div className="mb-8">
      {!isOverview && (
        <div className="mb-4">
          <BackButton />
        </div>
      )}
      <h1 className="text-3xl font-bold text-primary-text">{title}</h1>
      <p className="text-secondary-text text-sm mt-2">{description}</p>
      <div className="mt-4">{children}</div>
    </div>
  )
}
