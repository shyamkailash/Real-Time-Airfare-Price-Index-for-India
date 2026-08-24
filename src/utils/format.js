export const inr = (v) => {
  if (v == null) return '-'
  return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(v).replace(/\B(?=(\d{3})+(?!\d))/g, ',').replace(/^/, '₹')
}

export const number = (v) => (v==null?'-': new Intl.NumberFormat('en-IN').format(v))

export function csvFromArray(rows){
  const esc = (v='') => `"${String(v).replace(/"/g,'""')}"`
  const header = Object.keys(rows[0]||{})
  const lines = [header.map(esc).join(',')]
  rows.forEach(r=> lines.push(header.map(h=>esc(r[h])).join(',')))
  return lines.join('\n')
}
