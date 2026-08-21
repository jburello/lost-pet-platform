from fastapi import FastAPI, HTTPException, Depends, Query
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from geoalchemy2.elements import WKTElement

from backend.app.enums import ReportType
from backend.app.schemas import ReportCreate, ReportUpdate, ReportResponse, NearbyReportResponse
from backend.app.database import get_db 
from backend.app.models import Report
from backend.app.routers import reports, users, pets

app = FastAPI()

app.include_router(reports.router)
app.include_router(users.router)
app.include_router(pets.router)
#note: uvicorn backend.app.main:app --reload to run uvicorn
