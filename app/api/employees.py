from typing import List
from fastapi import APIRouter, HTTPException
from app.api.models import FootballerOut, FootballerIn, FootballerUpdate
from app.api import db_manager
from app.api.service import is_club_present

footballers = APIRouter()

@footballers.post('/', response_model=FootballerOut, status_code=201) #localhost:8001/api/v1/footballers
async def create_footballer(payload: FootballerIn):
    for club_id in payload.clubs_id:
        if not is_club_present(club_id):
            raise HTTPException(status_code=404, detail=f"Club with given id:{club_id} not found")

    footballer_id = await db_manager.add_footballer(payload)
    response = {
        'id': footballer_id,
        **payload.dict()
    }

    return response

@footballers.get('/', response_model=List[FootballerOut]) #localhost:8001/api/v1/footballers
async def get_footballers():
    return await db_manager.get_all_footballers()

@footballers.get('/{id}/', response_model=FootballerOut) #localhost:8001/api/v1/footballers/1
async def get_footballer(id: int):
    footballer = await db_manager.get_footballer(id)
    if not footballer:
        raise HTTPException(status_code=404, detail="Footballer not found")
    return footballer

@footballers.put('/{id}/', response_model=FootballerOut) #localhost:8001/api/v1/footballers/1 - Обновит страницу
async def update_footballer(id: int, payload: FootballerUpdate):
    footballer = await db_manager.get_footballer(id)
    if not footballer:
        raise HTTPException(status_code=404, detail="Footballer not found")

    update_data = payload.dict(exclude_unset=True)

    if 'clubs_id' in update_data:
        for club_id in payload.clubs_id:
            if not is_club_present(club_id):
                raise HTTPException(status_code=404, detail=f"Club with given id:{club_id} not found")

    footballer_in_db = FootballerIn(**footballer)

    updated_footballer = footballer_in_db.copy(update=update_data)

    return await db_manager.update_footballer(id, updated_footballer)

@footballers.delete('/{id}/', response_model=None) #localhost:8001/api/v1/footballers/1 - Удалит страницу
async def delete_footballer(id: int):
    footballer = await db_manager.get_footballer(id)
    if not footballer:
        raise HTTPException(status_code=404, detail="Footballer not found")
    return await db_manager.delete_footballer(id)