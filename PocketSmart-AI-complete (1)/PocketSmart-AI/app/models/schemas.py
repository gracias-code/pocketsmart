from typing import List
from pydantic import BaseModel, Field, EmailStr

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class Room(BaseModel):
    room_type: str = Field(min_length=2, max_length=60)
    quantity: int = Field(ge=1, le=20)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10000000)
    style: str = Field(default="Modern", min_length=2, max_length=60)
    rooms: List[Room] = Field(min_length=1, max_length=10)
    notes: str = Field(default="", max_length=1000)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10000000)
    guest_count: int = Field(gt=0, le=5000)
    event_type: str = Field(min_length=2, max_length=60)
    venue: str = Field(default="Flexible", max_length=120)
    food_preference: str = Field(default="Mixed", max_length=120)
    notes: str = Field(default="", max_length=1000)
