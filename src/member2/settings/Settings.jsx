import React, { useEffect, useState } from 'react'
import Layout from '../../app/Layout'
import PageHeader from '../../components/ui/PageHeader'
import { Save } from 'lucide-react'

const STORAGE_KEY = 'airtn:settings'

export default function Settings(){
  const [prefs, setPrefs] = useState({ 
    defaultPeriod: '3M', 
    defaultRoute: 'DEL-BOM', 
    autoRefresh: false, 
    refreshInterval: 120,
    density: 'comfortable'
  })
  const [saved, setSaved] = useState(false)

  useEffect(()=>{
    const raw = localStorage.getItem(STORAGE_KEY)
    if(raw) setPrefs(JSON.parse(raw))
  },[])

  function save(){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs))
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  return (
    <Layout>
      <PageHeader 
        title="Settings" 
        description="Preferences for your dashboard and interface."
      />

      <div className="space-y-6 max-w-3xl">
        {/* Dashboard Preferences */}
        <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
          <h3 className="text-base font-semibold text-primary-text mb-4">Dashboard Preferences</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-primary-text mb-2">Default Time Period</label>
              <select 
                value={prefs.defaultPeriod} 
                onChange={e=>setPrefs(p=>({...p, defaultPeriod:e.target.value}))} 
                className="w-full px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue"
              >
                <option value="3M">3 Months</option>
                <option value="6M">6 Months</option>
                <option value="1Y">1 Year</option>
                <option value="ALL">All Time</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-primary-text mb-2">Default Route</label>
              <input 
                type="text"
                value={prefs.defaultRoute} 
                onChange={e=>setPrefs(p=>({...p, defaultRoute:e.target.value}))} 
                placeholder="e.g., DEL-BOM"
                className="w-full px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue"
              />
            </div>
            <div className="flex items-center justify-between p-4 bg-body-bg rounded-lg">
              <div>
                <p className="text-sm font-medium text-primary-text">Auto Refresh</p>
                <p className="text-xs text-secondary-text mt-1">Automatically refresh data when LIVE indicator is active</p>
              </div>
              <label className="flex items-center cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={prefs.autoRefresh} 
                  onChange={e=>setPrefs(p=>({...p, autoRefresh: e.target.checked}))} 
                  className="w-5 h-5 rounded accent-primary-blue cursor-pointer"
                />
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-primary-text mb-2">Refresh Interval (seconds)</label>
              <input 
                type="number" 
                min="30"
                max="600"
                step="30"
                value={prefs.refreshInterval} 
                onChange={e=>setPrefs(p=>({...p, refreshInterval: Number(e.target.value)}))} 
                className="w-full px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue"
              />
              <p className="text-xs text-secondary-text mt-1">Minimum 30 seconds, Maximum 600 seconds</p>
            </div>
          </div>
        </div>

        {/* Interface Preferences */}
        <div className="bg-white rounded-lg border border-border-light p-6 shadow-sm">
          <h3 className="text-base font-semibold text-primary-text mb-4">Interface Preferences</h3>
          <div>
            <label className="block text-sm font-medium text-primary-text mb-2">Display Density</label>
            <select 
              value={prefs.density} 
              onChange={e=>setPrefs(p=>({...p, density:e.target.value}))}
              className="w-full px-3 py-2 border border-border-light rounded-lg text-primary-text bg-white focus:outline-none focus:ring-2 focus:ring-primary-blue"
            >
              <option value="comfortable">Comfortable</option>
              <option value="compact">Compact</option>
            </select>
            <p className="text-xs text-secondary-text mt-1">Control the spacing and information density in tables and cards</p>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center gap-3">
          <button 
            onClick={save} 
            className="inline-flex items-center gap-2 px-6 py-2 bg-primary-blue text-white rounded-lg font-medium hover:bg-bright-blue transition-colors focus:outline-none focus:ring-2 focus:ring-primary-blue focus:ring-offset-2"
          >
            <Save className="w-4 h-4" />
            Save Preferences
          </button>
          {saved && (
            <div className="text-sm text-success-green font-medium">
              ✓ Preferences saved successfully
            </div>
          )}
        </div>

        {/* Info Section */}
        <div className="bg-gray-50 rounded-lg border border-gray-200 p-4">
          <h4 className="text-sm font-semibold text-primary-text mb-2">About Your Settings</h4>
          <p className="text-sm text-secondary-text">
            Your preferences are saved locally in your browser. Settings will persist when you revisit the dashboard.
          </p>
        </div>
      </div>
    </Layout>
  )
}
