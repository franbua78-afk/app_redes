import os
import uuid
import boto3
from ..settings import settings


class S3Storage:
    def __init__(self):
        self.bucket = settings.S3_BUCKET
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            region_name=settings.AWS_REGION,
        )

    def upload_file(self, path: str) -> str:
        key = f"media/{uuid.uuid4().hex}/{os.path.basename(path)}"
        self.client.upload_file(path, self.bucket, key)
        return key

    def get_url(self, key: str) -> str:
        if settings.AWS_S3_ENDPOINT_URL and "http" in settings.AWS_S3_ENDPOINT_URL:
            return f"{settings.AWS_S3_ENDPOINT_URL}/{self.bucket}/{key}"
        return self.client.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=3600)

