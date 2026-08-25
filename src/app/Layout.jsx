import React from 'react'
import Sidebar from './Sidebar'
import Navbar from './Navbar'
import { useState } from 'react'

export default function Layout({ children, title, description }){
  const [mobileOpen, setMobileOpen] = useState(false)
  return (
    <div className="min-h-screen flex text-primary-text bg-body-bg">
      {/* Fixed sidebar */}
      <Sidebar mobileOpen={mobileOpen} onMobileClose={()=>setMobileOpen(false)} />
      
      {/* The desktop content only reserves room for the collapsed rail. */}
      <div className="flex-1 min-w-0 flex flex-col md:ml-[72px] relative">
        <Navbar onToggleMobileSidebar={()=>setMobileOpen(v=>!v)} />
        <main className="flex-1 p-4 sm:p-6 bg-body-bg overflow-x-hidden">
          {children}
        </main>
      </div>
    </div>
  )
}
