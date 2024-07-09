from fastapi import HTTPException, status


class MemeExceptions:
    NotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Meme not found.'
    )