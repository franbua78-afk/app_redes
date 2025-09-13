import os
from PIL import Image, ImageDraw, ImageFont


class VisualService:
    def generate(self, topic: str, params: dict) -> list[str]:
        # Fallback: create simple text slides using PIL
        os.makedirs("/app/tmp", exist_ok=True)
        slides = []
        lines = [
            f"{topic}",
            "Tip 1: Concéntrate en micro-objetivos",
            "Tip 2: Técnica Pomodoro",
            "Tip 3: Recompénsate",
        ]
        for i, text in enumerate(lines):
            path = f"/app/tmp/slide_{i}.png"
            img = Image.new("RGB", (1080, 1920), color=(20, 20, 24))
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            except Exception:
                font = ImageFont.load_default()
            w, h = draw.textsize(text, font=font)
            draw.text(((1080 - w) / 2, (1920 - h) / 2), text, font=font, fill=(240, 240, 240))
            img.save(path)
            slides.append(path)
        return slides

