from minio import Minio

from src.config.minio import MINIO_CONFIG


minio_session = Minio(MINIO_CONFIG.endpoint(), MINIO_CONFIG.access_key, MINIO_CONFIG.secret_key, secure=False)
