from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import requests


def search_books(query: str, api_key: Optional[str] = None, max_results: int = 20) -> List[Dict[str, Any]]:
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params: Dict[str, Any] = {
        "q": query,
        "maxResults": max_results,
    }
    if api_key:
        params["key"] = api_key
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        # Rate limiting or other HTTP errors
        logging.warning("Google Books API HTTP error: %s", e)
        return []
    except requests.exceptions.RequestException as e:
        logging.warning("Google Books API request error: %s", e)
        return []

    items = data.get("items", [])
    results: List[Dict[str, Any]] = []
    for item in items:
        volume = item.get("volumeInfo", {})
        image_links = volume.get("imageLinks", {})
        results.append(
            {
                "google_id": item.get("id"),
                "title": volume.get("title", "Untitled"),
                "authors": volume.get("authors"),
                "thumbnail": image_links.get("thumbnail") or image_links.get("smallThumbnail"),
                "published_date": volume.get("publishedDate"),
                "description": volume.get("description"),
            }
        )
    return results


