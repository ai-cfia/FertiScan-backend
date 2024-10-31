from http import HTTPStatus

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pipeline import GPT, OCR

from app.connection_manager import ConnectionManager
from app.controllers.users import sign_in
from app.exceptions import UserNotFoundError
from app.models.users import User

auth = HTTPBasic()


def get_connection_manager(request: Request) -> ConnectionManager:
    """
    Returns the app's ConnectionManager instance.
    """
    return request.app.connection_manager


def get_ocr(request: Request) -> OCR:
    """
    Returns the app's OCR instance.
    """
    return request.app.ocr


def get_gpt(request: Request) -> GPT:
    """
    Returns the app's GPT instance.
    """
    return request.app.gpt


def authenticate_user(credentials: HTTPBasicCredentials = Depends(auth)):
    """
    Authenticates a user.
    """
    if not credentials.username:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Missing email address!"
        )

    return User(username=credentials.username)


async def fetch_user(
    auth_user: User = Depends(authenticate_user),
    cm: ConnectionManager = Depends(get_connection_manager),
) -> User:
    """
    Fetches the authenticated user's info from db.
    """
    try:
        return await sign_in(cm, auth_user)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid username or password"
        )
