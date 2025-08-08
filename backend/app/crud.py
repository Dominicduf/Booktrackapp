from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from . import models, schemas


def normalize_authors(authors: Optional[Iterable[str]]) -> Optional[str]:
    if authors is None:
        return None
    return ", ".join([a for a in authors if a]) or None


def split_authors(authors_str: Optional[str]) -> Optional[list[str]]:
    if authors_str is None:
        return None
    return [a.strip() for a in authors_str.split(",") if a.strip()]


def upsert_book(db: Session, book_in: schemas.BookCreate) -> models.Book:
    existing = db.scalar(select(models.Book).where(models.Book.google_id == book_in.google_id))
    if existing:
        # Update metadata if we received newer info
        existing.title = book_in.title
        existing.authors = normalize_authors(book_in.authors)
        existing.thumbnail = book_in.thumbnail
        existing.published_date = book_in.published_date
        existing.description = book_in.description
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    book = models.Book(
        google_id=book_in.google_id,
        title=book_in.title,
        authors=normalize_authors(book_in.authors),
        thumbnail=book_in.thumbnail,
        published_date=book_in.published_date,
        description=book_in.description,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_google_id(db: Session, google_id: str) -> Optional[models.Book]:
    return db.scalar(select(models.Book).where(models.Book.google_id == google_id))


def get_or_create_entry(
    db: Session, *, google_id: str, status: str = "to_read"
) -> models.LibraryEntry:
    entry = db.scalar(select(models.LibraryEntry).where(models.LibraryEntry.google_id == google_id))
    if entry:
        return entry
    entry = models.LibraryEntry(google_id=google_id, status=status)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def update_entry(db: Session, google_id: str, update_in: schemas.LibraryEntryUpdate) -> Optional[models.LibraryEntry]:
    entry = db.scalar(select(models.LibraryEntry).where(models.LibraryEntry.google_id == google_id))
    if not entry:
        return None
    if update_in.status is not None:
        entry.status = update_in.status
    if update_in.started_at is not None:
        entry.started_at = update_in.started_at
    if update_in.finished_at is not None:
        entry.finished_at = update_in.finished_at
    if update_in.my_rating is not None:
        entry.my_rating = update_in.my_rating
    if update_in.my_notes is not None:
        entry.my_notes = update_in.my_notes
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def delete_entry(db: Session, google_id: str) -> bool:
    entry = db.scalar(select(models.LibraryEntry).where(models.LibraryEntry.google_id == google_id))
    if not entry:
        # Still attempt to delete book too if exists
        book = db.scalar(select(models.Book).where(models.Book.google_id == google_id))
        if book:
            db.delete(book)
            db.commit()
        return False
    book = entry.book
    db.delete(entry)
    # Also delete the book row to keep DB tidy
    if book:
        db.delete(book)
    db.commit()
    return True


def list_entries(db: Session, status: Optional[str] = None) -> list[tuple[models.Book, models.LibraryEntry]]:
    stmt = select(models.Book, models.LibraryEntry).join(models.LibraryEntry, models.Book.google_id == models.LibraryEntry.google_id)
    if status:
        stmt = stmt.where(models.LibraryEntry.status == status)
    rows = db.execute(stmt).all()
    return [(b, e) for b, e in rows]


def get_entry(db: Session, google_id: str) -> Optional[tuple[models.Book, models.LibraryEntry]]:
    stmt = (
        select(models.Book, models.LibraryEntry)
        .join(models.LibraryEntry, models.Book.google_id == models.LibraryEntry.google_id)
        .where(models.Book.google_id == google_id)
    )
    row = db.execute(stmt).first()
    if not row:
        return None
    book, entry = row
    return book, entry


