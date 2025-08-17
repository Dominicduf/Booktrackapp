# BookTrack App

A simple book tracking application that allows users to search for books using the Google Books API and manage their personal reading library.

## Features

- Search for books using Google Books API
- Add books to your personal library
- Track reading status (to read, reading, completed)
- Simple web interface with responsive design

## Project Structure

```
Booktrackapp/
├── backend/           # FastAPI backend server
│   └── app/
│       ├── main.py    # Main FastAPI application
│       ├── config.py  # Configuration and environment variables
│       ├── database.py # SQLAlchemy database setup
│       ├── models.py  # Database models
│       ├── schemas.py # Pydantic schemas
│       ├── crud.py    # Database operations
│       └── google_client.py # Google Books API client
├── frontend/          # Static HTML/CSS/JS frontend
│   ├── index.html     # Search page
│   ├── library.html   # Library management page
│   ├── book.html      # Individual book details
│   └── static/        # CSS and JavaScript files
└── requirements.txt   # Python dependencies
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Books API key (optional, for book search functionality)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Booktrackapp
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration (Optional)

Create a `.env` file in the project root to configure environment variables:

```bash
# .env file (optional)
GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here
APP_HOST=127.0.0.1
APP_PORT=8000
```

**Getting a Google Books API Key:**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Books API
4. Create credentials (API Key)
5. Add the API key to your `.env` file

*Note: The app will work without an API key, but book search functionality will be limited.*

### 5. Database Setup

The application uses SQLite, and the database will be created automatically when you first run the server. No additional setup is required.

## Running the Application

### Start the Backend Server

From the project root directory, make sure your virtual environment is activated:

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Then start the server
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Access

The frontend is served directly by the FastAPI backend server. **No separate frontend server is needed** - the HTML, CSS, and JavaScript files are served as static files by FastAPI.

Once the backend server is running, the frontend is automatically available at:

- **Main Application (Search Page)**: http://127.0.0.1:8000/
- **Library Page**: http://127.0.0.1:8000/library  
- **Book Details Page**: http://127.0.0.1:8000/book

### API Documentation

- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Alternative API Docs**: http://127.0.0.1:8000/redoc

## Usage

1. **Search for Books**: Use the search page (/) to find books by title, author, or keywords
2. **Add to Library**: Click "Add to Library" on any search result to save it to your collection
3. **Manage Library**: Visit the library page (/library) to view and manage your saved books
4. **Update Status**: Change reading status between "to read", "reading", and "completed"

## API Endpoints

- `GET /api/search?q={query}` - Search for books
- `GET /api/library` - Get all library items
- `POST /api/library` - Add a book to library
- `GET /api/library/{google_id}` - Get specific library item
- `PATCH /api/library/{google_id}` - Update library item status
- `DELETE /api/library/{google_id}` - Remove book from library

## Development

### Running in Development Mode

The `--reload` flag enables auto-reloading when code changes are detected:

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

### Database Location

The SQLite database is stored at `backend/app/booktrack.db` and will be created automatically on first run.

## Troubleshooting

### Common Issues

1. **Port already in use**: If port 8000 is busy, change the port:
   ```bash
   uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001
   ```

2. **Module not found errors**: Ensure you're in the project root and have activated your virtual environment

3. **API key issues**: Book search will work with limited functionality without an API key

### Logs

Check the terminal where you're running uvicorn for server logs and error messages.

## Dependencies

- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server for FastAPI
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **Requests**: HTTP client for Google Books API
- **python-dotenv**: Environment variable management