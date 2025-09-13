import os
from ..settings import settings


class TTSService:
    def synthesize(self, text: str, voice: str) -> str:
        # If ElevenLabs/OpenAI keys absent, fallback to a generated sine tone with subtitles pacing
        out = "/app/tmp/narration.mp3"
        os.makedirs("/app/tmp", exist_ok=True)
        if not settings.ELEVENLABS_API_KEY and not settings.OPENAI_API_KEY:
            # Generate a 30s silent audio as placeholder
            os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -q:a 9 -acodec libmp3lame {out} -y >/dev/null 2>&1")
            return out
        try:
            import httpx
            if settings.ELEVENLABS_API_KEY:
                # Simple ElevenLabs tts endpoint
                voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice if not mapped
                headers = {"xi-api-key": settings.ELEVENLABS_API_KEY}
                payload = {"text": text, "model_id": "eleven_multilingual_v2"}
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                with httpx.stream("POST", url, headers=headers, json=payload, timeout=120.0) as r:
                    r.raise_for_status()
                    with open(out, "wb") as f:
                        for chunk in r.iter_bytes():
                            f.write(chunk)
                return out
            # OpenAI TTS (if available)
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            resp = httpx.post(
                "https://api.openai.com/v1/audio/speech",
                headers=headers,
                json={"model": "gpt-4o-mini-tts", "voice": "alloy", "input": text},
                timeout=120.0,
            )
            resp.raise_for_status()
            with open(out, "wb") as f:
                f.write(resp.content)
            return out
        except Exception:
            os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 30 -q:a 9 -acodec libmp3lame {out} -y >/dev/null 2>&1")
            return out

