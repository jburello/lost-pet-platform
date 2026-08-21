from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.app.database import get_db
from backend.app.schemas import UserCreate, UserUpdate, UserResponse
from backend.app.models import User

router = APIRouter(prefix="/users", tags=["Users"])

#Users Endpoints

@router.post("/", status_code=201, response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        display_name=user_data.display_name,
        email=user_data.email,
        phone_number=user_data.phone_number
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email or Phone number already in use"
        )

    db.refresh(new_user)
    return new_user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: UUID,
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

    db.delete(user)
    db.commit()

    
@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    query = select(User)
    result = db.execute(query)
    return result.scalars().all()



