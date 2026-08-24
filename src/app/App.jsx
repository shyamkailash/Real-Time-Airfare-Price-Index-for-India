import React, { Suspense, lazy } from 'react'
import { Routes, Route } from 'react-router-dom'
import Overview from '../member1/dashboard/Overview'
import AirfareIndex from '../member1/airfare-index/AirfareIndex'
import RouteAnalysis from '../member2/routes/RouteAnalysis'
import AirlineAnalysis from '../member2/airlines/AirlineAnalysis'
import DataExplorer from '../member2/data-explorer/DataExplorer'
import Methodology from '../member2/methodology/Methodology'
import Reports from '../member2/reports/Reports'
import Settings from '../member2/settings/Settings'
import NotFound from '../pages/NotFound'

export default function App(){
  return (
    <Suspense fallback={<div className="p-6">Loading…</div>}>
      <Routes>
        <Route path="/" element={<Overview/>} />
        <Route path="/airfare-index" element={<AirfareIndex/>} />
        <Route path="/routes" element={<RouteAnalysis/>} />
        <Route path="/airlines" element={<AirlineAnalysis/>} />
        <Route path="/data-explorer" element={<DataExplorer/>} />
        <Route path="/methodology" element={<Methodology/>} />
        <Route path="/reports" element={<Reports/>} />
        <Route path="/settings" element={<Settings/>} />
        <Route path="*" element={<NotFound/>} />
      </Routes>
    </Suspense>
  )
}
