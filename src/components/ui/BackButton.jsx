import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'

export default function BackButton(){
  const navigate = useNavigate()

  function handleBack(){
    navigate(-1)
  }

  return (
    <button
      onClick={handleBack}
      className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-border-light bg-white hover:bg-body-bg text-secondary-text hover:text-primary-blue transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary-blue focus:ring-offset-2"
      aria-label="Go to previous page"
    >
      <ArrowLeft size={16} />
      <span className="text-sm font-medium">Back</span>
    </button>
  )
}
