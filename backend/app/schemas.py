from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    google_id: str
    title: str
    authors: Optional[List[str]] = Field(default=None, description="List of author names")
    thumbnail: Optional[str] = None
    published_date: Optional[str] = None
    description: Optional[str] = None


class BookCreate(BookBase):
    status: Optional[str] = Field(default="to_read", description="Reading status for the library entry")


class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True


class LibraryEntryBase(BaseModel):
    status: Optional[str] = Field(default="to_read")
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    my_rating: Optional[int] = Field(default=None, ge=1, le=5)
    my_notes: Optional[str] = None


class LibraryEntryCreate(LibraryEntryBase):
    google_id: str


class LibraryEntryUpdate(BaseModel):
    status: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    my_rating: Optional[int] = Field(default=None, ge=1, le=5)
    my_notes: Optional[str] = None


class LibraryEntryOut(LibraryEntryBase):
    id: int
    google_id: str
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LibraryItemOut(BaseModel):
    book: BookOut
    entry: LibraryEntryOut


class SearchItem(BaseModel):
    google_id: str
    title: str
    authors: Optional[List[str]] = None
    thumbnail: Optional[str] = None
    published_date: Optional[str] = None
    description: Optional[str] = None


