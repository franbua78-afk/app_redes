import { useState } from 'react'
import { useEffect } from 'react'

const durations = [10, 30, 60, 90]
const styles = ['slideshow', 'cinematic', 'meme', 'promo']
const voices = ['female-energetic-es', 'male-calm-en']
const musics = ['calm', 'upbeat', 'epic', 'funny']

export function DashboardPage() {
  const [form, setForm] = useState({
    topic: 'Motivación para estudiar',
    duration: 30,
    style: 'meme',
    voice: 'female-energetic-es',
    music: 'upbeat',
    captions: true,
    platforms: { youtube: true, tiktok: true, instagram: false },
    publish: 'now',
  })

  const [videos, setVideos] = useState<any[]>([])
  useEffect(()=>{
    const token = localStorage.getItem('token') || ''
    const fetchVideos = async ()=>{
      const res = await fetch('/api/videos', { headers: { 'Authorization': `Bearer ${token}` } })
      if(res.ok){ setVideos(await res.json()) }
    }
    fetchVideos()
    const id = setInterval(fetchVideos, 4000)
    return ()=> clearInterval(id)
  },[])

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const token = localStorage.getItem('token') || ''
    await fetch('/api/generate-video', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }, body: JSON.stringify(form) })
  }

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">Create New Video</h1>
      <form className="grid gap-4 max-w-3xl" onSubmit={submit}>
        <label className="grid gap-1">
          <span>Topic / Keywords</span>
          <input className="border rounded px-3 py-2" value={form.topic} onChange={e=>setForm(v=>({...v, topic:e.target.value}))}/>
        </label>
        <div className="grid grid-cols-2 gap-4">
          <label className="grid gap-1">
            <span>Duration</span>
            <select className="border rounded px-3 py-2" value={form.duration} onChange={e=>setForm(v=>({...v, duration:Number(e.target.value)}))}>
              {durations.map(d=> <option key={d} value={d}>{d}s</option>)}
            </select>
          </label>
          <label className="grid gap-1">
            <span>Style</span>
            <select className="border rounded px-3 py-2" value={form.style} onChange={e=>setForm(v=>({...v, style:e.target.value}))}>
              {styles.map(s=> <option key={s}>{s}</option>)}
            </select>
          </label>
          <label className="grid gap-1">
            <span>Voice</span>
            <select className="border rounded px-3 py-2" value={form.voice} onChange={e=>setForm(v=>({...v, voice:e.target.value}))}>
              {voices.map(v=> <option key={v}>{v}</option>)}
            </select>
          </label>
          <label className="grid gap-1">
            <span>Background Music</span>
            <select className="border rounded px-3 py-2" value={form.music} onChange={e=>setForm(v=>({...v, music:e.target.value}))}>
              {musics.map(m=> <option key={m}>{m}</option>)}
            </select>
          </label>
        </div>
        <label className="inline-flex items-center gap-2">
          <input type="checkbox" checked={form.captions} onChange={e=>setForm(v=>({...v, captions:e.target.checked}))}/>
          <span>Captions</span>
        </label>
        <div className="grid grid-cols-3 gap-4">
          {(['youtube','tiktok','instagram'] as const).map(p=> (
            <label key={p} className="inline-flex items-center gap-2">
              <input type="checkbox" checked={(form.platforms as any)[p]} onChange={e=>setForm(v=>({
                ...v, platforms: { ...v.platforms, [p]: e.target.checked }
              }))}/>
              <span className="capitalize">{p}</span>
            </label>
          ))}
        </div>
        <div className="inline-flex items-center gap-4">
          <label className="inline-flex items-center gap-2">
            <input type="radio" name="publish" checked={form.publish==='now'} onChange={()=>setForm(v=>({...v, publish:'now'}))}/>
            <span>Publish now</span>
          </label>
          <label className="inline-flex items-center gap-2">
            <input type="radio" name="publish" checked={form.publish==='schedule'} onChange={()=>setForm(v=>({...v, publish:'schedule'}))}/>
            <span>Schedule</span>
          </label>
        </div>
        <button className="bg-blue-600 text-white rounded px-4 py-2 w-max">Generate</button>
      </form>
      <div className="grid gap-3">
        <h2 className="text-lg font-semibold">Recent</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {videos.map(v=> (
            <div key={v.id} className="bg-white rounded shadow border overflow-hidden">
              {v.thumbnail_url ? <img src={v.thumbnail_url} alt="thumb" className="w-full aspect-[9/16] object-cover"/> : <div className="w-full aspect-[9/16] bg-gray-200"/>}
              <div className="p-3">
                <div className="text-sm text-gray-500">#{v.id} · {v.status}</div>
                <div className="font-medium line-clamp-2">{v.topic}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

