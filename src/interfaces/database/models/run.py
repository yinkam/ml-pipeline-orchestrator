from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.interfaces.database.core import Base
from src.interfaces.database.models.audit_mixin import TimestampMixin


class Run(TimestampMixin, Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pipeline_id: Mapped[int] = mapped_column(ForeignKey("pipelines.id"))
    status: Mapped[str] = mapped_column(default="Pending")
    metadata_: Mapped[str] = mapped_column(nullable=True)  # metadata is being used in DeclarativeBase/Base class
    workflow_snapshot: Mapped[str] = mapped_column(nullable=True)
    duration: Mapped[int] = mapped_column(default=300)
    started_at: Mapped[datetime] = mapped_column(default=func.now())
    ended_at: Mapped[datetime] = mapped_column(nullable=True)

    # pipeline = relationship("Pipeline", back_populates="runs")