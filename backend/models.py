from __future__ import annotations

import json
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


BookStatus = Literal["available", "unavailable"]


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    author: str = Field(min_length=1, max_length=160)
    description: str = Field(min_length=20, max_length=3000)
    cover: Optional[str] = None
    publisher: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=2, max_length=4)
    year: int = Field(ge=1450, le=2100)
    theme: Optional[str] = Field(default="", max_length=120)
    status: BookStatus = "available"
    is_favorite: bool = False
    is_reserved: bool = False

    @model_validator(mode="before")
    @classmethod
    def parse_stringified_json(cls, data):
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data

        return data


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    created_at: str
    updated_at: str


class LoginRequest(BaseModel):
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    token: str


class PublicBookFlag(BaseModel):
    value: bool
