from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(128), unique=True, index=True, nullable=False)
    title = Column(String(512), nullable=False)
    authors = Column(String(512), nullable=True)
    thumbnail = Column(String(1024), nullable=True)
    published_date = Column(String(64), nullable=True)
    description = Column(Text, nullable=True)

    entry = relationship(
        "LibraryEntry",
        back_populates="book",
        uselist=False,
        cascade="all, delete-orphan",
    )


class LibraryEntry(Base):
    __tablename__ = "library_entries"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(128), ForeignKey("books.google_id", ondelete="CASCADE"), index=True, nullable=False)
    status = Column(String(32), nullable=False, default="to_read")
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    my_rating = Column(Integer, nullable=True)
    my_notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    book = relationship("Book", back_populates="entry")


