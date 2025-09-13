export function LoginPage() {
  return (
    <div className="min-h-screen grid place-items-center">
      <div className="bg-white p-8 rounded-lg shadow w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6">Login</h1>
        <form className="space-y-4" onSubmit={async (e)=>{
          e.preventDefault();
          const form = e.target as HTMLFormElement;
          const email = (form.elements.namedItem('email') as HTMLInputElement).value;
          const password = (form.elements.namedItem('password') as HTMLInputElement).value;
          const res = await fetch('/api/auth/login', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email, password})});
          const data = await res.json();
          if(data.access_token){ localStorage.setItem('token', data.access_token); window.location.href = '/'; }
        }}>
          <input name="email" className="w-full border rounded px-3 py-2" placeholder="Email" />
          <input name="password" className="w-full border rounded px-3 py-2" placeholder="Password" type="password" />
          <button className="w-full bg-blue-600 text-white rounded px-4 py-2">Login</button>
        </form>
        <div className="mt-4 grid gap-2">
          <button className="w-full border rounded px-4 py-2">Continue with Google</button>
        </div>
      </div>
    </div>
  )
}

