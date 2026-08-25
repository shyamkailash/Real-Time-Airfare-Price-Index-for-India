import React from 'react'
import Card from '../../components/ui/Card'

export default function StatCard({ icon, label, value, caption }){
  return (
    <Card className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-md bg-slate-800 flex items-center justify-center text-teal">{icon}</div>
      <div>
        <div className="text-sm text-stext">{label}</div>
        <div className="text-lg font-semibold">{value}</div>
        {caption && <div className="text-xs text-stext">{caption}</div>}
      </div>
    </Card>
  )
}
