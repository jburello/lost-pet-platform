from fastapi import FastAPI, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from datetime import datetime

from backend.app.enums import ReportType
from backend.app.schemas import ReportCreate, ReportUpdate, ReportResponse
from backend.app.database import get_db 
from backend.app.models import Report

app = FastAPI()

#note: uvicorn backend.app.main:app --reload to run uvicorn


@app.get("/reports", response_model=list[ReportResponse])
def get_reports(
    db: Session = Depends(get_db),
    report_type: ReportType | None = None
):
    query = select(Report)

    if report_type is not None:
        query = query.where(Report.report_type == report_type.value)

    result = db.execute(query)
    return result.scalars().all()

@app.post("/reports",  status_code=201, response_model=ReportResponse)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db)
):
    new_report = Report(
        report_type=report_data.report_type.value,
        animal_type=report_data.animal_type,
        location=report_data.location,
        latitude=report_data.latitude,
        longitude=report_data.longitude,
        description=report_data.description,
        event_time=report_data.event_time,
        name=report_data.name,
        breed=report_data.breed,
        sex=report_data.sex,
        color=report_data.color
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report

@app.get("/reports/{report_id}", response_model=ReportResponse)
def get_report_with_id(
    report_id: UUID, 
    db: Session = Depends(get_db)
    ):

    query = select(Report)
    query = query.where(Report.report_id == report_id)


    result = db.execute(query)
    report = result.scalars().first()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        ) 
    return report

@app.delete("/reports/{report_id}", status_code=204)
def delete_report(
    report_id: UUID,
    db: Session = Depends(get_db)
    ):
    query = select(Report)
    query = query.where(Report.report_id == report_id)
    result = db.execute(query)
    report = result.scalars().first()
    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    db.delete(report)
    db.commit()


@app.patch("/reports/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: UUID,
    report_data: ReportUpdate,
    db: Session = Depends(get_db)
    ):

    query = select(Report)
    query = query.where(Report.report_id == report_id)
    
    result = db.execute(query)
    report = result.scalars().first()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    
    updates = report_data.model_dump(exclude_unset=True)

    if "report_type" in updates:
        updates["report_type"] = updates["report_type"].value

    for field,value in updates.items(): #loops through the report_data dict
        setattr(report,field,value) #updates values

    db.commit()
    db.refresh(report)
    
    return report

