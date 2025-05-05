from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


# Sample Audit Trail/Logging: This would ideally contain all models and fields necessary for to accomplish it

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())
