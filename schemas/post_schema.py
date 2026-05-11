from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None


class CreatePost(Post):
    pass


class RequiredUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[float] = None


class ResponsePost(BaseModel):
    id: int
    title: str
    content: str
    rating: Optional[float] = None

    class Config:
        orm_mode = True


class ResponseById(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True
