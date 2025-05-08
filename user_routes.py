# user_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import Client

router = APIRouter()
supabase: Client = None  # Will be initialized in main

class User(BaseModel):
    user_id: int
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str

class ReadBookAdd(BaseModel):
    user_id: int
    bookID: int

@router.post("/users/", response_model=User)
def create_user(user: UserCreate):
    data = supabase.table("users").insert(user.dict()).execute()
    if data.data:
        return data.data[0]
    raise HTTPException(status_code=400, detail="User could not be created")

@router.post("/users/read_books/")
def add_read_book(entry: ReadBookAdd):
    data = supabase.table("user_read_books").insert(entry.dict()).execute()
    if data.data:
        return {"message": "Book added to user's read list"}
    raise HTTPException(status_code=400, detail="Could not add book to read list")

@router.get("/books/")
def read_books():
    data = supabase.table("books").select("*").execute()
    if data.data:
        return data.data
    raise HTTPException(status_code=404, detail="No books found")

@router.get("/books/{book_id}")
def read_book(book_id: int):
    data = supabase.table("books").select("*").eq("bookID", book_id).execute()
    if data.data:
        return data.data[0]
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/books_search/")
def search_books(query: str):
    data = supabase.table("books").select("*").ilike("title", f"%{query}%").execute()
    results = data.data
    if not results:
        data = supabase.table("books").select("*").ilike("authors", f"%{query}%").execute()
        results = data.data
    if results:
        return results
    raise HTTPException(status_code=404, detail="No matching books found")

@router.get("/books_by_year/")
def books_by_year(year: str):
    data = supabase.table("books").select("*").ilike("publication_date", f"%{year}%").execute()
    if data.data:
        return data.data
    raise HTTPException(status_code=404, detail="No books found for that year")
