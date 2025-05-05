from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.interfaces.database.core import Base
from src.interfaces.database.models.audit_mixin import TimestampMixin
from src.interfaces.database.models.run import Run


class Pipeline(TimestampMixin, Base):
    __tablename__ = "pipelines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    workflow: Mapped[str] = mapped_column(nullable=True)
    # runs: Mapped[List["Run"]] = relationship()
