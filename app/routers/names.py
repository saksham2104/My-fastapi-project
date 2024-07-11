from fastapi import APIRouter, Depends
from app.utils.security import get_current_user
from app.db.connector import database
from app.db.models import names
from pydantic import BaseModel
from typing import List

class NameItem(BaseModel):
    id: int
    name: str

class NamesResponse(BaseModel):
    names: List[NameItem]

router = APIRouter()

@router.get("/names", response_model=NamesResponse)
async def get_names(user: str = Depends(get_current_user)):
    query = names.select()
    result = await database.fetch_all(query)
    return {'names': result}
