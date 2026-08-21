from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.database import get_db
from backend.app.schemas import PetCreate, PetUpdate, PetResponse
from backend.app.enums import PetSex
from backend.app.models import Pet, User

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.post("/{user_id}", status_code=201, response_model=PetResponse)
def create_pet(
    user_id: UUID,
    pet_data: PetCreate,
    db: Session = Depends(get_db)
):
    query = select(User)
    query = query.where(User.user_id == user_id)
    result = db.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_pet = Pet(
        user_id=user_id,
        animal_type=pet_data.animal_type,
        name=pet_data.name,
        sex=pet_data.sex.value if pet_data.sex is not None else None,
        age=pet_data.age,
        breed=pet_data.breed,
        color=pet_data.color
    )
    

    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet

@router.get("/users/{user_id}", response_model=list[PetResponse])
def get_user_pets(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    user_query = select(User)
    user_query = user_query.where(User.user_id == user_id)
    result = db.execute(user_query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    query = select(Pet)
    query = query.where(Pet.user_id == user_id)
    result = db.execute(query)
    return result.scalars().all()

@router.get("/{pet_id}", response_model=PetResponse)
def get_pet_by_id(
    pet_id: UUID,
    db: Session = Depends(get_db)
):  
    query = select(Pet)
    query = query.where(Pet.pet_id == pet_id)
    result = db.execute(query)
    pet = result.scalars().first()

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    return pet


@router.patch("/{pet_id}", response_model=PetResponse)
def update_pet(
    pet_id: UUID,
    pet_data: PetUpdate,
    db: Session = Depends(get_db)
):
    query = select(Pet)
    query = query.where(Pet.pet_id == pet_id)

    result = db.execute(query)
    pet = result.scalars().first()

    if pet is None:
            raise HTTPException(
                status_code=404,
                detail="Pet not found"
            )

    updates = pet_data.model_dump(exclude_unset=True)

    if "sex" in updates and updates["sex"] is not None:
         updates["sex"] = updates["sex"].value

    for field, value in updates.items():
         setattr(pet,field,value)


    db.commit()
    db.refresh(pet)

    return pet


@router.delete("/{pet_id}", status_code=204)
def delete_pet(
     pet_id: UUID,
     db: Session = Depends(get_db)
):
    query = select(Pet)
    query = query.where(Pet.pet_id == pet_id)
    result = db.execute(query)
    pet = result.scalars().first()
    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="pet not found"
        )
    
    db.delete(pet)
    db.commit()
    