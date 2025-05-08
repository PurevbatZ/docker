# user_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import Client

router = APIRouter()
supabase: Client = None  # Will be initialized in main

class UserCreate(BaseModel):
    username: str
    password: str

class ReadBookAdd(BaseModel):
    username: str
    password: str
    bookID: int

class UserFavorite(BaseModel):
    username: str

@router.post("/users/", response_model=dict)
def create_user(user: UserCreate):
    data = supabase.table("users").insert(user.dict()).execute()
    if data.data:
        return {"message": "User created successfully", "user": data.data[0]}
    raise HTTPException(status_code=400, detail="User could not be created")

@router.post("/users/read_books/")
def add_read_book(entry: ReadBookAdd):
    # Authenticate user
    user_data = supabase.table("users").select("id").eq("username", entry.username).eq("password", entry.password).execute()
    if not user_data.data:
        raise HTTPException(status_code=403, detail="Invalid username or password")

    user_id = user_data.data[0]["id"]
    # Add book to read list
    data = supabase.table("user_read_books").insert({"user_id": user_id, "bookID": entry.bookID}).execute()
    if data.data:
        return {"message": "Book added to user's read list"}
    raise HTTPException(status_code=400, detail="Could not add book to read list")

@router.get("/users/{username}/read_list/")
def get_user_read_list(username: str):
    # Fetch user data
    user_data = supabase.table("users").select("id").eq("username", username).execute()
    if not user_data.data:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user_data.data[0]["id"]

    # Fetch favorite books
    books_data = supabase.table("user_read_books").select("bookID").eq("user_id", user_id).execute()

    if not books_data.data:
        raise HTTPException(status_code=404, detail="No books listed to read")

    book_ids = [entry["bookID"] for entry in books_data.data]
    books = supabase.table("books").select("*").in_("bookID", book_ids).execute()

    if books.data:
        return books.data
    raise HTTPException(status_code=404, detail="No books found")

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