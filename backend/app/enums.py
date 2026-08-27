from enum import Enum

class ReportType(Enum):
    FOUND = "found"
    SIGHTING = "sighting"

class PetSex(Enum):
    MALE = "male"
    FEMALE = "female"

class CaseStatus(Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"

class LocationVisibility(str, Enum):
    PRECISE = "precise"
    APPROXIMATE = "approximate"