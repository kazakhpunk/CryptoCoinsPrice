from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_db
from app.crud.coin import CoinCrud
from app.schema import CoinBase, CoinUpdate
from auth.dependencies import get_current_user
from app.models import User

router = APIRouter()

@router.get("/coins")
async def get_db_coins(db: AsyncSession = Depends(get_async_db)):
    coin_crud = CoinCrud(db)
    return {"message": "Coins retrieved successfully", "coins": await coin_crud.get_all_coins()}

@router.get("/coin/{coin_name}")
async def get_coin(coin_name: str, db: AsyncSession = Depends(get_async_db)):
    coin_crud = CoinCrud(db)
    return {"message": "Coin retrieved successfully", "coin": await coin_crud.get_coin_by_name(coin_name)}

@router.post("/coin")
async def create_coin(
    coin: CoinBase = Body(...), 
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    coin_crud = CoinCrud(db)
    return {"message": "Coin created successfully", "new_coin": await coin_crud.create_coin(coin)}

@router.put("/coin/{coin_name}")
async def update_coin(
    coin_name: str, 
    coin: CoinUpdate = Body(...), 
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    coin_crud = CoinCrud(db)
    return {"message": "Coin updated successfully", "updated_coin": await coin_crud.update_coin(coin_name, coin)}

@router.patch("/coin/{coin_name}")
async def update_coin(
    coin_name: str, 
    coin: CoinUpdate = Body(...), 
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    coin_crud = CoinCrud(db)
    return {"message": "Coin patched successfully", "updated_coin": await coin_crud.patch_coin(coin_name, coin)}

@router.delete("/coin/{coin_name}")
async def delete_coin(
    coin_name: str, 
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    coin_crud = CoinCrud(db)
    coin_temp = await coin_crud.get_coin_by_name(coin_name)
    await coin_crud.delete_coin_by_name(coin_name)
    return {"message": "Coin deleted successfully", "deleted_coin": coin_temp}