from __future__ import annotations

import os
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from models import Book, BookCreate, BookUpdate, LoginRequest, LoginResponse, PublicBookFlag


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR.parent / "data" / "tasks.db"))
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "electolibrary-admin-token")

app = FastAPI(title="ElectoLibrary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def row_to_book(row: sqlite3.Row) -> Book:
    data = dict(row)
    data["is_favorite"] = bool(data["is_favorite"])
    data["is_reserved"] = bool(data["is_reserved"])
    return Book(**data)


def require_admin(authorization: str = Header(default="")) -> None:
    expected = f"Bearer {ADMIN_TOKEN}"
    if authorization != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется вход в админку")


async def parse_book_update_request(request: Request) -> BookUpdate:
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Тело запроса должно быть JSON")

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            raise HTTPException(status_code=422, detail="JSON-строка внутри body некорректна")

    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="Тело запроса должно быть JSON-объектом")

    try:
        return BookUpdate.model_validate(payload)
    except ValidationError as error:
        raise HTTPException(status_code=422, detail=error.errors())


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                description TEXT NOT NULL,
                cover TEXT,
                publisher TEXT NOT NULL,
                category TEXT NOT NULL,
                year INTEGER NOT NULL,
                isbn TEXT DEFAULT '',
                theme TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'available',
                is_favorite INTEGER NOT NULL DEFAULT 0,
                is_reserved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS api_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )

        count = connection.execute("SELECT COUNT(*) AS count FROM books").fetchone()["count"]
        if count == 0:
            created_at = now_iso()
            seed_books = [
                {
                    "title": "Чапаев и Пустота",
                    "author": "В. О. Пелевин",
                    "description": "Роман о столкновении исторической памяти, мифа и личного поиска смысла.",
                    "publisher": "Эксмо",
                    "category": "16+",
                    "year": 1996,
                    "isbn": "978-5-04-099999-1",
                    "theme": "Современная проза",
                    "status": "available",
                    "is_favorite": 1,
                    "is_reserved": 0,
                },
                {
                    "title": "Мастер и Маргарита",
                    "author": "М. А. Булгаков",
                    "description": "Классический роман о Москве, свободе, любви и цене человеческого выбора.",
                    "publisher": "АСТ",
                    "category": "16+",
                    "year": 1967,
                    "isbn": "978-5-17-118366-0",
                    "theme": "Классика",
                    "status": "available",
                    "is_favorite": 0,
                    "is_reserved": 1,
                },
                {
                    "title": "Vue.js в действии",
                    "author": "Э. Ханчард",
                    "description": "Практическое руководство по созданию интерфейсов и компонентов на Vue.",
                    "publisher": "Питер",
                    "category": "12+",
                    "year": 2019,
                    "isbn": "978-5-4461-1234-5",
                    "theme": "Веб-разработка",
                    "status": "unavailable",
                    "is_favorite": 0,
                    "is_reserved": 0,
                },
            ]

            for book in seed_books:
                connection.execute(
                    """
                    INSERT INTO books (
                        title, author, description, cover, publisher, category, year, isbn, theme,
                        status, is_favorite, is_reserved, created_at, updated_at
                    )
                    VALUES (
                        :title, :author, :description, '', :publisher, :category, :year, :isbn,
                        :theme, :status, :is_favorite, :is_reserved, :created_at, :updated_at
                    )
                    """,
                    {**book, "created_at": created_at, "updated_at": created_at},
                )


def record_api_access() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO api_meta (key, value)
            VALUES ('last_api_request_at', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (now_iso(),),
        )


@app.middleware("http")
async def persist_api_access(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api"):
        record_api_access()
    return response


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "database": str(DB_PATH)}


@app.post("/api/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    if payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль")

    return LoginResponse(token=ADMIN_TOKEN)


@app.get("/api/books", response_model=list[Book])
def list_books() -> list[Book]:
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM books ORDER BY datetime(created_at) DESC").fetchall()
    return [row_to_book(row) for row in rows]


def get_book_or_404(book_id: int) -> Book:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    return row_to_book(row)


@app.get("/api/books/{book_id}", response_model=Book)
@app.get("/api/boooks/{book_id}", response_model=Book, include_in_schema=False)
def get_book(book_id: int) -> Book:
    return get_book_or_404(book_id)


@app.post("/api/books", response_model=Book, status_code=201, dependencies=[Depends(require_admin)])
def create_book(book: BookCreate) -> Book:
    timestamp = now_iso()
    payload = book.model_dump()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO books (
                title, author, description, cover, publisher, category, year, isbn, theme,
                status, is_favorite, is_reserved, created_at, updated_at
            )
            VALUES (
                :title, :author, :description, :cover, :publisher, :category, :year,
                '', :theme, :status, :is_favorite, :is_reserved, :created_at, :updated_at
            )
            """,
            {
                **payload,
                "is_favorite": int(payload["is_favorite"]),
                "is_reserved": int(payload["is_reserved"]),
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )
        book_id = cursor.lastrowid

    return get_book_or_404(book_id)


@app.put("/api/books/{book_id}", response_model=Book, dependencies=[Depends(require_admin)])
async def update_book(book_id: int, request: Request) -> Book:
    book = await parse_book_update_request(request)
    get_book_or_404(book_id)
    payload = book.model_dump()

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE books
            SET
                title = :title,
                author = :author,
                description = :description,
                cover = :cover,
                publisher = :publisher,
                category = :category,
                year = :year,
                theme = :theme,
                status = :status,
                is_favorite = :is_favorite,
                is_reserved = :is_reserved,
                updated_at = :updated_at
            WHERE id = :id
            """,
            {
                **payload,
                "id": book_id,
                "is_favorite": int(payload["is_favorite"]),
                "is_reserved": int(payload["is_reserved"]),
                "updated_at": now_iso(),
            },
        )

    return get_book_or_404(book_id)


@app.patch("/api/books/{book_id}/favorite", response_model=Book)
def set_favorite(book_id: int, payload: PublicBookFlag) -> Book:
    get_book_or_404(book_id)
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE books
            SET is_favorite = ?, updated_at = ?
            WHERE id = ?
            """,
            (int(payload.value), now_iso(), book_id),
        )

    return get_book_or_404(book_id)


@app.patch("/api/books/{book_id}/reserve", response_model=Book)
def set_reservation(book_id: int, payload: PublicBookFlag) -> Book:
    book = get_book_or_404(book_id)
    if payload.value and book.status != "available":
        raise HTTPException(status_code=400, detail="Книга сейчас не в наличии")

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE books
            SET is_reserved = ?, updated_at = ?
            WHERE id = ?
            """,
            (int(payload.value), now_iso(), book_id),
        )

    return get_book_or_404(book_id)


@app.delete(
    "/api/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_book(book_id: int):
    get_book_or_404(book_id)
    with get_connection() as connection:
        connection.execute("DELETE FROM books WHERE id = ?", (book_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
