import { useEffect, useState } from 'react'

export function TemplatesPage() {
  const [items, setItems] = useState<any[]>([])
  useEffect(()=>{
    const token = localStorage.getItem('token') || ''
    fetch('/api/templates', { headers: { 'Authorization': `Bearer ${token}` }})
      .then(r=>r.json()).then(setItems).catch(()=>{})
  },[])
  return (
    <div>
      <h1 className="text-xl font-semibold mb-4">Templates</h1>
      <div className="grid gap-3">
        {items.map(t=> (
          <div key={t.id} className="bg-white border rounded p-3">
            <div className="font-medium">{t.name}</div>
            <pre className="text-xs text-gray-600 overflow-auto">{JSON.stringify(t.params, null, 2)}</pre>
          </div>
        ))}
        {items.length===0 && <p className="text-gray-600">No templates yet.</p>}
      </div>
    </div>
  )
}

