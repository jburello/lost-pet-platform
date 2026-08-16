from pydantic import BaseModel
from backend.app.enums import ReportType
from datetime import datetime

class ReportCreate(BaseModel):
    report_type: ReportType
    animal_type: str
    location: str               #later probably update to a better option for location or geolocation
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
    description: str | None = None
    event_time: datetime | None = None
    name: str | None = None
    breed: str | None = None
    sex: str | None = None
    color: str | None = None