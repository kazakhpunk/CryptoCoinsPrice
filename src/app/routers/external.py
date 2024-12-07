from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from app.schema import StatusResponse, PriceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_db
from app.crud.coin import CoinCrud
from app.models import User
from auth.dependencies import get_current_user 
import httpx
import os

router = APIRouter()

headers = {
    "x-cg-demo-api-key": os.getenv('GECKO_API_KEY'),
    "accept": "application/json"
}

@router.get("/status")
async def get_status() -> StatusResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.coingecko.com/api/v3/ping", headers=headers)
        print("Status Code:", response.status_code) 
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("Response:", json_response)
                return {"status": "ok"}
            except httpx.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from CoinGecko API")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to ping CoinGecko API")

@router.get("/coins")
async def get_coins() -> list[dict]:
    async with httpx.AsyncClient() as client:
        
        response = await client.get(f"https://api.coingecko.com/api/v3/coins/list", headers=headers)
        print("Response:", response.json())
        if response.status_code == 200:
            try:
                json_response = response.json()
                return json_response
            except httpx.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from CoinGecko API")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to get price from CoinGecko API")

@router.get("/price/{coin}")
async def get_price(
    coin: str = Path(..., description="The coin to get the price for"),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
) -> PriceResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={coin}"
            "&vs_currencies=usd" 
            "&include_market_cap=true"
            "&include_24hr_vol=true"
            "&include_24hr_change=true"
            "&include_last_updated_at=true",
            headers=headers
        )

        print("Response:", response.json())
        if response.status_code == 200:
            try:
                json_response = response.json()

                if coin not in json_response:
                    raise HTTPException(status_code=404, detail=f"Coin '{coin}' not found")
                
                price_data = PriceResponse(coin=coin, **json_response[coin])

                coin_crud = CoinCrud(db)
                await coin_crud.update_coin(coin, price_data)

                return price_data
            except ValueError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from CoinGecko API")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to get price from CoinGecko API")