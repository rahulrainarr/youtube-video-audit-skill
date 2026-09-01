from sqlalchemy import Column, Integer, String, Text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin


class ApplicationSetting(Base, TimestampMixin):
    __tablename__ = "application_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    data_type: Mapped[str] = mapped_column(String(50), nullable=False)  # string, int, bool, float, json
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # transcription, llm, teams, general

    def __repr__(self):
        return f"<ApplicationSetting(key={self.key}, data_type={self.data_type})>"
