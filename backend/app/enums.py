from enum import Enum

class ReportType(Enum):
    FOUND = "found"
    LOST = "lost"
    SIGHTING = "sighting"

class PetSex(Enum):
    MALE = "male"
    FEMALE = "female"