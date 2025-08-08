import os
from dotenv import load_dotenv


load_dotenv()


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value


GOOGLE_BOOKS_API_KEY: str | None = get_env("GOOGLE_BOOKS_API_KEY")
APP_HOST: str = get_env("APP_HOST", "127.0.0.1") or "127.0.0.1"
APP_PORT: int = int(get_env("APP_PORT", "8000") or "8000")


