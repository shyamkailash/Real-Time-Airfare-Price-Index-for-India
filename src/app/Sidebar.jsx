import { Link, useLocation } from 'react-router-dom'
import { Plane, BarChart2, MapPin, Layers, Database, FileText, Eye, Settings, X } from 'lucide-react'
import { useState } from 'react'

const navItems = [
  { id: 1, icon: Eye, label: 'Overview', url: '/' },
  { id: 2, icon: BarChart2, label: 'Airfare Index', url: '/airfare-index' },
  { id: 3, icon: MapPin, label: 'Route Analysis', url: '/routes' },
  { id: 4, icon: Layers, label: 'Airline Analysis', url: '/airlines' },
  { id: 5, icon: Database, label: 'Data Explorer', url: '/data-explorer' },
  { id: 6, icon: FileText, label: 'Methodology', url: '/methodology' },
  { id: 7, icon: BarChart2, label: 'Reports', url: '/reports' },
  { id: 8, icon: Settings, label: 'Settings', url: '/settings' }
]

export default function Sidebar({ mobileOpen, onMobileClose }) {
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-30 md:hidden"
          onClick={onMobileClose}
        />
      )}

      {/* Desktop sidebar - fixed */}
      <aside
        className="hidden md:flex fixed left-0 top-0 z-50 h-screen flex-col overflow-visible border-r border-sidebar-secondary bg-sidebar-dark shadow-[4px_0_14px_rgba(7,26,53,0.16)] transition-[width] duration-250 ease-out"
        style={{ width: sidebarOpen ? '230px' : '72px' }}
      >
        {/* Logo section */}
        <div className="flex items-start gap-3 px-3 py-5 border-b border-sidebar-secondary">
          <button
            type="button"
            onClick={() => setSidebarOpen((open) => !open)}
            className="flex-shrink-0 rounded-lg p-1 text-airtn-teal transition-colors hover:bg-sidebar-secondary focus:outline-none focus:ring-2 focus:ring-airtn-teal"
            aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
            title={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            <Plane className="w-6 h-6 text-airtn-teal" />
          </button>
          {sidebarOpen && (
            <div className="animate-fadeIn min-w-0 pt-0.5">
              <div className="text-white text-sm font-bold">AIRTN</div>
              <div className="mt-1 text-xs leading-4 text-gray-300">Airfare Intelligence &amp;<br />Real-time Tracking</div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto overflow-x-visible">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.url
            return (
              <Link
                key={item.id}
                to={item.url}
                aria-label={item.label}
                title={!sidebarOpen ? item.label : undefined}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 text-sm ${
                  isActive
                    ? 'bg-bright-blue text-white'
                    : 'text-gray-300 hover:bg-sidebar-secondary'
                }`}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && (
                  <span className="animate-fadeIn whitespace-nowrap">{item.label}</span>
                )}
              </Link>
            )
          })}
        </nav>

        {/* LIVE indicator */}
        <div className="px-3 py-4 border-t border-sidebar-secondary flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-success-green animate-pulse"></div>
          {sidebarOpen && <span className="text-xs text-gray-300 animate-fadeIn">LIVE</span>}
        </div>
      </aside>

      {/* Mobile drawer */}
      <aside
        className={`fixed left-0 top-0 h-screen w-[230px] flex flex-col bg-sidebar-dark z-50 md:hidden transform transition-transform duration-300 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Mobile header */}
        <div className="flex items-center justify-between px-4 py-4 border-b border-sidebar-secondary">
          <div className="flex items-center gap-2">
            <Plane className="w-6 h-6 text-airtn-teal" />
            <div>
              <div className="text-white text-sm font-bold">AIRTN</div>
              <div className="text-xs leading-4 text-gray-300">Airfare Intelligence &amp;<br />Real-time Tracking</div>
            </div>
          </div>
          <button
            onClick={onMobileClose}
            className="text-gray-400 hover:text-white"
            aria-label="Close menu"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Mobile navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.url
            return (
              <Link
                key={item.id}
                to={item.url}
                onClick={onMobileClose}
                aria-label={item.label}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm ${
                  isActive
                    ? 'bg-bright-blue text-white'
                    : 'text-gray-300 hover:bg-sidebar-secondary'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>

        {/* Mobile LIVE indicator */}
        <div className="px-3 py-4 border-t border-sidebar-secondary flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-success-green animate-pulse"></div>
          <span className="text-xs text-gray-300">LIVE</span>
        </div>
      </aside>
    </>
  )
}
