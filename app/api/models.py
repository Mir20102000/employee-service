from pydantic import BaseModel
from typing import List, Optional


class FootballerIn(BaseModel):
    name: str
    surname: str
    age: int
    goals: int
    clubs_id: int


class FootballerOut(FootballerIn):
    id: int


class FootballerUpdate(FootballerIn):
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None
    goals: Optional[int] = None
    clubs_id: Optional[int] = None
