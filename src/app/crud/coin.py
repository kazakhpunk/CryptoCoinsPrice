from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update, delete
from app.schema import CoinCreate, CoinUpdate, PriceResponse
from app.models import Coin
class CoinCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_coin(self, price_data: PriceResponse) -> CoinCreate:
        new_coin = Coin(
            coin=price_data.coin,
            usd=price_data.usd,
            usd_market_cap=price_data.usd_market_cap,
            usd_24h_vol=price_data.usd_24h_vol,
            usd_24h_change=price_data.usd_24h_change,
            last_updated_at=price_data.last_updated_at
        )
        self.db.add(new_coin)
        await self.db.commit()
        await self.db.refresh(new_coin)
        return new_coin

    async def get_coin(self, coin_id: int) -> Coin:
        result = await self.db.execute(select(Coin).where(Coin.id == coin_id))
        coin = result.scalars().first()
        if not coin:
            raise NoResultFound(f"Coin with id {coin_id} not found")
        return coin

    async def get_coin_by_name(self, coin_name: str) -> Coin:
        result = await self.db.execute(select(Coin).where(Coin.coin == coin_name))
        coin = result.scalars().first()
        if not coin:
            raise NoResultFound(f"Coin with name {coin_name} not found")
        return coin

    async def get_all_coins(self) -> list[Coin]:
        result = await self.db.execute(select(Coin))
        return result.scalars().all()

    async def update_coin(self, coin_name: str, price_data: CoinUpdate) -> CoinUpdate:
        result = await self.db.execute(select(Coin).where(Coin.coin == coin_name))
        coin = result.scalars().first()
        
        if not coin:
            return await self.create_coin(price_data)
        
        coin.usd = price_data.usd
        coin.usd_market_cap = price_data.usd_market_cap
        coin.usd_24h_vol = price_data.usd_24h_vol
        coin.usd_24h_change = price_data.usd_24h_change
        coin.last_updated_at = price_data.last_updated_at
        
        await self.db.commit()
        await self.db.refresh(coin)
        return coin
    
    async def patch_coin(self, coin_name: str, price_data: CoinUpdate) -> CoinUpdate:
        result = await self.db.execute(select(Coin).where(Coin.coin == coin_name))
        coin = result.scalars().first()
        
        if not coin:
            return await self.create_coin(price_data)
        
        update_data = price_data.model_dump(exclude_unset=True)
            
        for field, value in update_data.items():
            setattr(coin, field, value)

        await self.db.commit()
        await self.db.refresh(coin)
        return coin

    async def delete_coin(self, coin_id: int) -> None:
        result = await self.db.execute(select(Coin).where(Coin.id == coin_id))
        coin = result.scalars().first()
        if not coin:
            raise NoResultFound(f"Coin with id {coin_id} not found")
        
        await self.db.execute(delete(Coin).where(Coin.id == coin_id))
        await self.db.commit()

    async def delete_coin_by_name(self, coin_name: str) -> None:
        result = await self.db.execute(select(Coin).where(Coin.coin == coin_name))
        coin = result.scalars().first()
        if not coin:
            raise NoResultFound(f"Coin with name {coin_name} not found")
        
        await self.db.execute(delete(Coin).where(Coin.coin == coin_name))
        await self.db.commit()