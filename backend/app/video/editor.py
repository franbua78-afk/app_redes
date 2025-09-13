import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image


class EditorService:
    def compose(self, audio_path: str, image_paths: list[str], params: dict) -> tuple[str, str]:
        os.makedirs("/app/tmp", exist_ok=True)
        duration = int(params.get("duration", 30))
        per_slide = max(duration / max(len(image_paths), 1), 1)

        clips = []
        for p in image_paths:
            clip = ImageClip(p).set_duration(per_slide).resize((1080, 1920))
            clips.append(clip)
        video_clip = concatenate_videoclips(clips, method="compose")

        audio = AudioFileClip(audio_path)
        video_clip = video_clip.set_audio(audio).set_duration(duration)

        out_path = "/app/tmp/result.mp4"
        video_clip.write_videofile(
            out_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            preset="veryfast",
            threads=2,
            verbose=False,
            logger=None,
        )

        # thumbnail from first frame
        thumb_path = "/app/tmp/thumb.jpg"
        Image.open(image_paths[0]).resize((1080, 1920)).save(thumb_path, quality=90)

        return out_path, thumb_path

