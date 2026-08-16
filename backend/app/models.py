from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, DateTime, func
from datetime import datetime
from uuid import UUID, uuid4

from backend.app.enums import ReportType

class Base(DeclarativeBase):
    pass

class Report(Base):
    __tablename__ = "reports"
    report_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4

                                            )
    animal_type: Mapped[str] = mapped_column(Text)
    report_type: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    event_time: Mapped[datetime] = mapped_column(DateTime)
    report_created_dt: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
        )

    #Optional attributes

    name: Mapped[str | None] = mapped_column(Text)
    breed: Mapped[str | None] = mapped_column(Text)
    sex: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(Text)