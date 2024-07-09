from fastapi import HTTPException, status


class MemeExceptions:
    NotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Meme not found.'
    )

    NotSaved = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Error on saving file.'
    )

    FileNotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='File not found.'
    )