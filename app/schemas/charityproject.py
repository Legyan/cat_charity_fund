from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: int = 0

    @validator('full_amount')
    def validate_full_amount(cls, value):
        if value < 0:
            raise ValueError('full_amout cant be negative')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True
