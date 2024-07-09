import io
from uuid import uuid4, UUID

from minio import Minio

from src.config.minio import MINIO_CONFIG


class MemeDAO:
    def __init__(self):
        self.minio = Minio(MINIO_CONFIG.endpoint(), MINIO_CONFIG.access_key, MINIO_CONFIG.secret_key, secure=False)
        self.bucket_name = 'meme'
        if not self.minio.bucket_exists(self.bucket_name):
            self.minio.make_bucket(self.bucket_name)

    def create(self, meme: bytes) -> UUID:
        name = f'{uuid4()}'
        file = io.BytesIO(meme)
        self.minio.put_object(self.bucket_name, name, file, file.getbuffer().nbytes)
        return UUID(name)

    def get_by_name(self, filename: UUID) -> bytes:
        meme = self.minio.get_object(
            self.bucket_name,
            str(filename)
        ).data
        return meme
