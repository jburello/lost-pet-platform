from pydantic import BaseModel, Field
from backend.app.enums import ReportType
from datetime import datetime
from uuid import UUID

class ReportCreate(BaseModel):
    report_type: ReportType
    animal_type: str
    location: str
    longitude: float = Field(ge=-180,le=180)
    latitude: float = Field(ge=-90,le=90)    
    description: str
    event_time: datetime
    name: str | None = None
    breed: str | None = None
    sex: str | None = None
    color: str | None = None


class ReportUpdate(BaseModel):
    report_type: ReportType | None = None
    animal_type: str | None = None
    location: str | None = None
    longitude: float | None = Field(default = None, ge=-180,le=180)
    latitude: float | None = Field(default = None, ge=-90,le=90)          
    description: str | None = None
    event_time: datetime | None = None
    name: str | None = None
    breed: str | None = None
    sex: str | None = None
    color: str | None = None


class ReportResponse(BaseModel):
        report_id: UUID
        report_type: ReportType
        animal_type: str
        location: str
        longitude: float = Field(ge=-180,le=180)
        latitude: float = Field(ge=-90,le=90)         
        description: str
        event_time: datetime
        report_created_dt: datetime
        name: str | None = None
        breed: str | None = None
        sex: str | None = None
        color: str | None = None