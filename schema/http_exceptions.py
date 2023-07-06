from typing import List, Optional
from pydantic import BaseModel, Field


class HttpException(BaseModel):
    error: str = "500 Internal Error."
    message: Optional[str]

class BadRequestHttpException(HttpException):
    class Error(BaseModel):
        message: str = Field(alias="msg")
        type: str
        location: List[str] = Field(alias="loc")

    message: Optional[str] = "A validation error occurred."
    error: str = "400 Bad Request."
    errors: Optional[List[Error]]

class NotFoundHttpException(HttpException):
    error: str = "404 Not Found."

class ConflictHttpException(HttpException):
    error: str = "409 Conflict."
