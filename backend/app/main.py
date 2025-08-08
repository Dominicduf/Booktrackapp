from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .config import GOOGLE_BOOKS_API_KEY
from .database import Base, engine, get_db
from . import crud, models, schemas
from .google_client import search_books


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"


app = FastAPI(title="BookTrack App", version="0.1.0")


# Create tables on startup
Base.metadata.create_all(bind=engine)


# Static files and basic pages
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/library", include_in_schema=False)
def serve_library() -> FileResponse:
    return FileResponse(str(FRONTEND_DIR / "library.html"))


@app.get("/book", include_in_schema=False)
def serve_book() -> FileResponse:
    return FileResponse(str(FRONTEND_DIR / "book.html"))


# API Endpoints


@app.get("/api/search", response_model=List[schemas.SearchItem])
def api_search(q: str = Query(..., min_length=1), max_results: int = Query(20, ge=1, le=40)):
    results = search_books(q, GOOGLE_BOOKS_API_KEY, max_results=max_results)
    return results


@app.post("/api/library", response_model=schemas.LibraryItemOut)
def add_or_update_library_item(
    payload: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    book_in = payload
    book = crud.upsert_book(db, book_in)
    entry = crud.get_or_create_entry(db, google_id=book.google_id, status="to_read")
    return {
        "book": {
            "id": book.id,
            "google_id": book.google_id,
            "title": book.title,
            "authors": crud.split_authors(book.authors),
            "thumbnail": book.thumbnail,
            "published_date": book.published_date,
            "description": book.description,
        },
        "entry": entry,
    }


@app.get("/api/library", response_model=List[schemas.LibraryItemOut])
def list_library(status: Optional[str] = None, db: Session = Depends(get_db)):
    items = crud.list_entries(db, status=status)
    output: list[schemas.LibraryItemOut] = []
    for book, entry in items:
        output.append(
            schemas.LibraryItemOut(
                book=schemas.BookOut(
                    id=book.id,
                    google_id=book.google_id,
                    title=book.title,
                    authors=crud.split_authors(book.authors),
                    thumbnail=book.thumbnail,
                    published_date=book.published_date,
                    description=book.description,
                ),
                entry=entry,
            )
        )
    return output


@app.get("/api/library/{google_id}", response_model=schemas.LibraryItemOut)
def get_library_item(google_id: str, db: Session = Depends(get_db)):
    item = crud.get_entry(db, google_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    book, entry = item
    return {
        "book": {
            "id": book.id,
            "google_id": book.google_id,
            "title": book.title,
            "authors": crud.split_authors(book.authors),
            "thumbnail": book.thumbnail,
            "published_date": book.published_date,
            "description": book.description,
        },
        "entry": entry,
    }


@app.patch("/api/library/{google_id}", response_model=schemas.LibraryItemOut)
def patch_library_item(
    google_id: str,
    payload: schemas.LibraryEntryUpdate,
    db: Session = Depends(get_db),
):
    entry = crud.update_entry(db, google_id, payload)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    book = crud.get_book_by_google_id(db, google_id)
    return {
        "book": {
            "id": book.id,
            "google_id": book.google_id,
            "title": book.title,
            "authors": crud.split_authors(book.authors),
            "thumbnail": book.thumbnail,
            "published_date": book.published_date,
            "description": book.description,
        },
        "entry": entry,
    }


@app.delete("/api/library/{google_id}")
def delete_library_item(google_id: str, db: Session = Depends(get_db)):
    ok = crud.delete_entry(db, google_id)
    return {"ok": ok}


