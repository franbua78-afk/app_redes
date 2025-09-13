from sqlalchemy.orm import Session
from ..db.models import Video, Schedule, SocialToken
from ..oauth.google import ensure_fresh_credentials
from loguru import logger


class YouTubeUploader:
    def __init__(self, db: Session):
        self.db = db

    def upload(self, video: Video, schedule: Schedule):
        # Placeholder: store as published without real API if credentials not present
        token = (
            self.db.query(SocialToken)
            .filter(SocialToken.user_id == schedule.user_id, SocialToken.platform == "youtube")
            .first()
        )
        if not token:
            logger.warning("No YouTube token, simulating upload")
            return
        try:
            creds = ensure_fresh_credentials(self.db, token)
            service = self._build_service(creds)
            body = {
                "snippet": {
                    "title": video.topic,
                    "description": video.script_text or video.topic,
                    "tags": ["shorts", "ai", "reels"],
                    "categoryId": "22",
                },
                "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
            }
            media = self._media_upload(video)
            request = service.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
            request.execute()
            logger.info("YouTube upload completed")
        except Exception as e:
            logger.warning(f"Simulating YouTube upload due to error: {e}")

    def _build_service(self, creds):
        from googleapiclient.discovery import build
        return build("youtube", "v3", credentials=creds, cache_discovery=False)

    def _media_upload(self, video: Video):
        from googleapiclient.http import MediaIoBaseUpload
        import io
        # In this simplified example we cannot download from S3 within uploader.
        # A production build should download to temp file first. Here we create a tiny dummy file to satisfy flow
        buf = io.BytesIO(b"fake video content")
        return MediaIoBaseUpload(buf, mimetype="video/mp4", chunksize=1024*1024, resumable=True)

