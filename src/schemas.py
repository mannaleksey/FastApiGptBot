from typing import TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar('T')


class Messages(BaseModel):
    role: str
    msg: str


class MsgDB(BaseModel):
    user_id: str
    messages: List[Messages]


class Msg(BaseModel):
    user_id: str
    msg: str


class RequestUser(BaseModel):
    id: str = None
    user_id: str
    request: str
    size: str = None


class RequestUserError(BaseModel):
    id: str = None
    user_id: str
    request: str
    size: str = None


class UpdateData(BaseModel):
    id: str
    status: str
    answer: str


class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None
