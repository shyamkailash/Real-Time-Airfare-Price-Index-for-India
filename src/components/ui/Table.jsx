import React from 'react'

export default function Table({ columns, data, className='' }){
  return (
    <div className={`overflow-auto ${className}`}>
      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr className="text-left text-stext text-sm">
            {columns.map(c=> <th key={c.key} className="px-3 py-2 border-b border-borders">{c.title}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i)=> (
            <tr key={i} className="hover:bg-slate-800">
              {columns.map(c=> <td key={c.key} className="px-3 py-2 align-top">{c.render? c.render(row): row[c.key]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
