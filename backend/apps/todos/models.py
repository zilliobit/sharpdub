from datetime import datetime
from sqlalchemy import Boolean, String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Automatically sets when the row is created
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Automatically updates every time the row is changed
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now()
    )