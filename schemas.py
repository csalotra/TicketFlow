from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request Models
class TicketCreate(BaseModel):
    """
    Fields required when a user creates a ticket
    """
    title: str
    description: str


# Response Models
class TicketRead(BaseModel):
    """
    Fields returned when reading ticket data
    """
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True  # Returns SQLModel objects

class Token(BaseModel):
    """
    JWT Token response model
    """
    access_token: str
    token_type: str = "bearer"
