from fastapi import APIRouter, HTTPException, Depends, Query
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from geoalchemy2.elements import WKTElement


from backend.app.enums import ReportType
from backend.app.schemas import ReportCreate, ReportUpdate, ReportResponse, NearbyReportResponse
from backend.app.database import get_db 
from backend.app.models import Report

router = APIRouter(prefix="/reports", tags=["Reports"])

#Reports Endpoints

@router.get("/", response_model=list[NearbyReportResponse | ReportResponse])
def get_reports(
    db: Session = Depends(get_db),
    report_type: ReportType | None = None,
    latitude: float | None = Query(default=None, ge=-90, le=90),
    longitude: float | None = Query(default=None, ge=-180, le=180),
    radius_miles: float | None = Query(default=None, gt=0)
):
    query = select(Report)

    if report_type is not None: #filter for report types
        query = query.where(Report.report_type == report_type.value)

    has_latitude = latitude is not None
    has_longitude = longitude is not None
    has_radius = radius_miles is not None

    if any([has_latitude, has_longitude, has_radius]) and not all([has_latitude, has_longitude, has_radius]):
        raise HTTPException(
            status_code=400,
            detail="latitude, longitude, and radius_miles must be provided together"
        )

    if latitude is not None and longitude is not None and radius_miles is not None: #filter for nearby reports, user is able to pick the radius
        search_point = WKTElement(f"POINT({longitude} {latitude})",srid=4326)
        radius_meters = radius_miles * 1609.34
        distance = func.ST_Distance(
                                        Report.location_point,
                                        search_point
                                        )
        query = query.add_columns(distance)
        query = query.where(func.ST_DWithin         #func to find if the reports locations are in the radius of the specified search point radius
            (
                Report.location_point,
                search_point,
                radius_meters
            )
        )
        query = query.order_by(distance)
        result = db.execute(query)
        result = result.all()
        nearby_response_list = []
        for report, distance_meters in result:

            validated_report = ReportResponse.model_validate(report) #Report object is now converted to a ReporResponse model

            report_data = validated_report.model_dump() # turns pydantic object into hmap

            report_data["distance_miles"] = distance_meters / 1609.34 #conversion of meters to miles for distance

            nearby_response_list.append(NearbyReportResponse(**report_data))
        return nearby_response_list


    result = db.execute(query)
    return result.scalars().all()

@router.post("/",  status_code=201, response_model=ReportResponse)
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
        location_point = WKTElement(f"POINT({report_data.longitude} {report_data.latitude})",srid=4326),
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

@router.get("/{report_id}", response_model=ReportResponse)
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

@router.delete("/{report_id}", status_code=204)
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


@router.patch("/{report_id}", response_model=ReportResponse)
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
