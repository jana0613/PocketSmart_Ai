from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(RegisterRequest):
    pass

class HomeItem(BaseModel):
    room: Literal["Living Room", "Bedroom", "Kitchen", "Dining Room", "Study", "Bathroom", "Other"]
    item: str = Field(min_length=2, max_length=80)
    quantity: int = Field(ge=1, le=50)
    style: str = Field(default="Modern", max_length=60)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    items: list[HomeItem] = Field(min_length=1, max_length=30)
    priorities: list[str] = Field(default_factory=list, max_length=10)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    event_type: str = Field(min_length=2, max_length=60)
    guests: int = Field(ge=1, le=5000)
    venue: str = Field(min_length=2, max_length=120)
    date: Optional[str] = Field(default=None, max_length=30)
    preferences: list[str] = Field(default_factory=list, max_length=10)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    occasion: str = Field(min_length=2, max_length=60)
    style: str = Field(default="Elegant", max_length=60)
    metal: str = Field(default="Any", max_length=40)
    outfit_notes: str = Field(default="", max_length=1000)

class RecommendationItem(BaseModel):
    name: str
    category: str
    platform: str
    estimated_price: float
    reason: str
    url: str

class RecommendationResponse(BaseModel):
    planner: str
    summary: str
    budget: float
    currency: str
    allocated_total: float
    remaining_budget: float
    tips: list[str]
    recommendations: list[RecommendationItem]
    source: Literal["gemini", "fallback"]
    history_id: Optional[int] = None
