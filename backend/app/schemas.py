from pydantic import BaseModel, Field
from backend.app.enums import ReportType, PetSex
from datetime import datetime
from uuid import UUID
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

#User Schemas
class UserCreate(BaseModel):
     display_name: str
     email: EmailStr
     phone_number: PhoneNumber


class UserUpdate(BaseModel):
    display_name: str | None = None
    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None

class UserResponse(BaseModel):
    user_id: UUID
    display_name: str

#Pet Schemas
class PetCreate(BaseModel):
    animal_type: str
    name: str
    sex: PetSex | None = None
    age: int | None = Field(default=None, ge=0)
    breed: str | None = None
    color: str | None = None

class PetUpdate(BaseModel):
    animal_type: str | None = None
    name: str | None = None
    sex: PetSex | None = None
    age: int | None = Field(default=None, ge=0)
    breed: str | None = None
    color: str | None = None


class PetResponse(BaseModel):
    pet_id: UUID
    animal_type: str
    name: str
    sex: PetSex | None = None
    age: int | None = Field(default=None, ge=0)
    breed: str | None = None
    color: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


#Report Schemas
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
        model_config = ConfigDict(from_attributes=True) # Lets pydantic read data from SQLAlchemy object attributes (report.name, report.location, etc.)

class NearbyReportResponse(ReportResponse):
     distance_miles: float