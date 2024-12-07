from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        model_config = ConfigDict(from_attributes=True)

class StatusResponse(BaseModel):
    status: str

class PriceResponse(BaseModel):
    coin: str | None = None
    usd: float | None = None
    usd_market_cap: float | None = None
    usd_24h_vol: float | None = None
    usd_24h_change: float | None = None
    last_updated_at: int | None = None

class CoinBase(BaseModel):
    coin: str | None = None
    usd: float | None = None
    usd_market_cap: float | None = None
    usd_24h_vol: float | None = None
    usd_24h_change: float | None = None
    last_updated_at: int | None = None

class CoinCreate(CoinBase):
    pass

class CoinUpdate(BaseModel):
    usd: Optional[float] = None
    usd_market_cap: Optional[float] = None
    usd_24h_vol: Optional[float] = None
    usd_24h_change: Optional[float] = None
    last_updated_at: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class CoinResponse(CoinBase):
    id: int | None = None
    
    class Config:
        model_config = ConfigDict(from_attributes=True)