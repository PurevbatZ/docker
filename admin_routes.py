# admin_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import Client

router = APIRouter()
supabase: Client = None  # Will be initialized in main

class Book(BaseModel):
    bookID: int
    title: str
    authors: str
    average_rating: float
    publication_date: str
    publisher: str

@router.post("/books/")
def create_book(book: Book):
    data = supabase.table("books").insert(book.dict()).execute()
    if data.data:
        return data.data
    raise HTTPException(status_code=400, detail="Book could not be created")

@router.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    data = supabase.table("books").update(book.dict()).eq("bookID", book_id).execute()
    if data.data:
        return data.data
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    data = supabase.table("books").delete().eq("bookID", book_id).execute()
    if data.data:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
