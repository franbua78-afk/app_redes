from sqlalchemy.orm import Session
from ..db.models import Video
from ..settings import settings
from .script import ScriptService
from .tts import TTSService
from .visuals import VisualService
from .editor import EditorService
from ..storage.s3 import S3Storage


class VideoPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.script = ScriptService()
        self.tts = TTSService()
        self.visuals = VisualService()
        self.editor = EditorService()
        self.storage = S3Storage()

    def generate(self, video: Video):
        text = self.script.generate(video.topic, video.params)
        video.script_text = text
        self.db.commit()

        audio_path = self.tts.synthesize(text, video.params["voice"])
        visual_paths = self.visuals.generate(video.topic, video.params)
        result_path, thumb_path = self.editor.compose(audio_path, visual_paths, video.params)

        video_key = self.storage.upload_file(result_path)
        thumb_key = self.storage.upload_file(thumb_path)
        video.audio_s3_key = self.storage.upload_file(audio_path)
        video.video_s3_key = video_key
        video.thumbnail_s3_key = thumb_key
        self.db.commit()

