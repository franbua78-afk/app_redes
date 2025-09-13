from ..settings import settings


class ScriptService:
    def generate(self, topic: str, params: dict) -> str:
        # Minimal viable script if no AI key provided
        base = f"Video corto sobre: {topic}."
        if not settings.OPENAI_API_KEY:
            return f"{base}\n1) Gancho poderoso.\n2) 3 tips prácticos.\n3) Llamado a la acción."
        try:
            import httpx
            prompt = (
                f"Escribe un guion conciso y motivador en español para un video vertical de {params.get('duration',30)} segundos sobre '{topic}'. "
                "Incluye gancho, 3 puntos clave y cierre con llamada a la acción."
            )
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            # Using responses compatible with OpenAI v1
            resp = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "Eres un guionista experto en videos cortos."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                },
                timeout=60.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return f"{base}\n1) Gancho.\n2) 3 puntos clave.\n3) Cierre."

