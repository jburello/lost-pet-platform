from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, DateTime, func, Float, ForeignKey, Integer
from datetime import datetime
from uuid import UUID, uuid4
from geoalchemy2 import Geography

from backend.app.enums import ReportType, PetSex

class Base(DeclarativeBase):
    pass

#User Base Model
class User(Base):
    __tablename__ = "users"
    user_id: Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    display_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    phone_number: Mapped[str] = mapped_column(Text, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


#Pet Base Model
class Pet(Base):
    __tablename__ = "pets"
    pet_id: Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"), )
    animal_type: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    #optional fields
    sex: Mapped[str | None] = mapped_column(Text)
    age: Mapped[int | None] = mapped_column(Integer)
    breed: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(Text)



#Report Base Model
class Report(Base):
    __tablename__ = "reports"
    report_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4

                                            )
    animal_type: Mapped[str] = mapped_column(Text)
    report_type: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    location_point = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326
        ),
        nullable=False
    )
    description: Mapped[str] = mapped_column(Text)
    event_time: Mapped[datetime] = mapped_column(DateTime)
    report_created_dt: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
        )

    #Optional fields

    name: Mapped[str | None] = mapped_column(Text)
    breed: Mapped[str | None] = mapped_column(Text)
    sex: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(Text)






