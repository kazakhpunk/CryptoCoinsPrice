from sqlalchemy import Column, Integer, String, Float

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    

class Coin(Base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True, index=True)
    coin = Column(String, index=True) 
    usd = Column(Float, nullable=True)
    usd_market_cap = Column(Float, nullable=True)
    usd_24h_vol = Column(Float, nullable=True)
    usd_24h_change = Column(Float, nullable=True)
    last_updated_at = Column(Integer, nullable=True)