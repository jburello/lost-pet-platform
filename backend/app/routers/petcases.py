from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from geoalchemy2.elements import WKTElement
from datetime import datetime

from backend.app.database import get_db
from backend.app.schemas import PetCaseCreate, PetCaseResponse
from backend.app.models import PetCase, Pet
from backend.app.enums import CaseStatus

router = APIRouter(prefix="/cases", tags=["Pet Cases"])

@router.post("/{pet_id}", status_code=201, response_model=PetCaseResponse)
def create_case(
    pet_id: UUID,
    pet_case_data: PetCaseCreate,
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


    query_case = select(PetCase)
    query_case = query_case.where(PetCase.pet_id == pet_id, PetCase.status == CaseStatus.ACTIVE.value)
    result_case = db.execute(query_case)
    pet_case = result_case.scalars().first()

    if pet_case is not None:
        raise HTTPException(
                status_code=409,
                detail="pet has an ACTIVE case already"
            )



    new_case = PetCase(
        pet_id=pet_id,
        last_seen_location_private=pet_case_data.last_seen_location_private,
        latitude=pet_case_data.latitude,
        longitude=pet_case_data.longitude,
        lost_at=pet_case_data.lost_at,
        description=pet_case_data.description,
        status=CaseStatus.ACTIVE.value,
        public_area=pet_case_data.public_area,
        location_point=WKTElement(f"POINT({pet_case_data.longitude} {pet_case_data.latitude})",srid=4326)
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    
    return new_case

@router.get("/{case_id}",response_model=PetCaseResponse)
def get_case_by_case_id(
    case_id: UUID,
    db: Session = Depends(get_db)
):
    query = select(PetCase)
    query = query.where(PetCase.case_id == case_id)
    result = db.execute(query)
    case = result.scalars().first()

    if case is None:
            raise HTTPException(
                status_code=404,
                detail="Pet case not found"
            )

    return case


@router.get("/pet/{pet_id}", response_model=list[PetCaseResponse])
def get_cases_by_pet_id(
     pet_id: UUID,
     db: Session = Depends(get_db)
):
    pet_query = select(Pet)
    pet_query = pet_query.where(Pet.pet_id == pet_id)
    result = db.execute(pet_query)
    pet = result.scalars().first()
    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )
    
    query = select(PetCase)
    query = query.where(PetCase.pet_id == pet_id)
    result = db.execute(query)
    pet_cases = result.scalars().all()
    
    return pet_cases




@router.patch("/{case_id}/resolve", response_model=PetCaseResponse)
def resolve_pet_case(
     case_id:UUID,
     db: Session = Depends(get_db)
):
    query = select(PetCase)
    query = query.where(PetCase.case_id == case_id)
    result = db.execute(query)
    case = result.scalars().first()
    
    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Pet case not found"
        )

    if case.status == CaseStatus.RESOLVED.value:
            raise HTTPException(
                    status_code=409,
                    detail="Pet case is already resolved"
            )

    case.status = CaseStatus.RESOLVED.value
    case.resolved_at = datetime.now()
    
    db.commit()
    db.refresh(case)

    return case