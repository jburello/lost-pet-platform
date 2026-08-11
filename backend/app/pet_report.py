from enum import Enum
from uuid import uuid4
import datetime

class ReportType(Enum):
    FOUND = "found"
    LOST = "lost"
    SIGHTING = "sighting"

class PetReport:
    
    def __init__(self, report_type, animal_type, location, description, event_time, name=None, breed=None, sex=None, color=None):
        self.report_id = uuid4()
        self.report_type = report_type
        self.animal_type =  animal_type
        self.location = location
        self.description = description
        self.event_time = event_time
        self.name = name
        self.breed = breed
        self.sex = sex
        self.color = color
        self.report_created_dt = datetime.datetime.now()

