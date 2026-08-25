import React from 'react'
import { RefreshCw, Menu, Bell } from 'lucide-react'

export default function Navbar({ onToggleMobileSidebar }){
  const currentTime = new Date().toLocaleString('en-IN', { 
    dateStyle: 'short', 
    timeStyle: 'short' 
  })

  return (
    <header className="h-14 flex items-center justify-between px-4 md:px-6 bg-white border-b border-border-light sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <button 
          aria-label="Open sidebar" 
          onClick={onToggleMobileSidebar} 
          className="md:hidden p-2 rounded-lg hover:bg-body-bg transition-colors text-primary-text"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="hidden md:block">
          <div className="text-sm font-bold text-primary-text">AIRTN</div>
          <div className="text-xs text-secondary-text">Airfare Intelligence & Real-time Tracking</div>
        </div>
        <div className="md:hidden">
          <div className="text-sm font-bold text-primary-text">AIRTN</div>
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        {/* Status and time */}
        <div className="hidden sm:flex items-center gap-3 text-xs text-secondary-text border-r border-border-light pr-4">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-success-green animate-pulse"></span>
            <span className="font-medium text-primary-text">LIVE</span>
          </div>
          <div>Updated 2m ago</div>
          <div>{currentTime}</div>
        </div>

        {/* Mobile status */}
        <div className="sm:hidden flex items-center gap-2 text-xs text-secondary-text">
          <span className="w-2 h-2 rounded-full bg-success-green animate-pulse"></span>
          <span className="font-medium">LIVE</span>
        </div>

        {/* Action buttons */}
        <button 
          aria-label="Notifications" 
          className="p-2 rounded-lg hover:bg-body-bg transition-colors text-secondary-text hover:text-primary-text"
        >
          <Bell className="w-4 h-4" />
        </button>
        <button 
          aria-label="Refresh" 
          className="p-2 rounded-lg hover:bg-body-bg transition-colors text-secondary-text hover:text-primary-text"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>
    </header>
  )
}
