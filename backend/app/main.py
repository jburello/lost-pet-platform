from fastapi import FastAPI, HTTPException
from uuid import UUID

from backend.app.pet_report import PetReport, ReportType
from backend.app.report_manager import ReportManager
from backend.app.schemas import ReportCreate, ReportUpdate

app = FastAPI()
manager = ReportManager()

#note: uvicorn backend.app.main:app --reload to run uvicorn


@app.get("/reports")
def get_reports(report_type: ReportType | None = None):
    if report_type is not None:
        return manager.filter_by_report_type(report_type)
    
    return manager.get_all_reports()

@app.post("/reports",  status_code=201)
def create_report(report_data: ReportCreate):
    new_report = PetReport(
        report_data.report_type,
        report_data.animal_type,
        report_data.location,
        report_data.description,
        report_data.event_time,
        report_data.name,
        report_data.breed,
        report_data.sex,
        report_data.color
    )
    manager.add_report(new_report)
    return new_report

@app.get("/reports/{report_id}")
def get_report_with_id(report_id : UUID):
    report= manager.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        ) 
    return report

@app.delete("/reports/{report_id}", status_code=204)
def delete_report(report_id : UUID):
    report = manager.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    manager.delete_report(report_id)


@app.patch("/reports/{report_id}")
def update_report(report_id : UUID, report_data: ReportUpdate):

    report = manager.get_report_by_id(report_id)
    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    
    updates = report_data.model_dump(exclude_unset=True)
    updated_report = manager.update_report(report_id, updates)
    return updated_report

