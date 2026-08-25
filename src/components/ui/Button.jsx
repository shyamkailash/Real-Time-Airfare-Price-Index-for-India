import React from 'react'

export default function Button({ children, onClick, variant='primary', ...rest }){
  const base = 'px-3 py-2 rounded-md text-sm font-medium'
  const cls = variant==='primary' ? `${base} bg-teal text-black` : `${base} bg-surface text-ptext`
  return (
    <button onClick={onClick} className={cls} {...rest}>{children}</button>
  )
}
