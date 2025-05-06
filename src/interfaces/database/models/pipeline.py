from typing import List

from sqlalchemy import Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.interfaces.database.core import Base
from src.interfaces.database.models.audit_mixin import TimestampMixin
from src.interfaces.database.models.run import Run


class Pipeline(TimestampMixin, Base):
    __tablename__ = "pipelines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    workflow: Mapped[dict] = mapped_column(Text, nullable=True) # Store the workflow dictionary as JSON string
    step_configs: Mapped[dict] = mapped_column(Text, nullable=True) # Store step configurations as JSON string
    version: Mapped[str] = mapped_column(default="1.0.0", nullable=True)
    # runs = relationship('Run')
