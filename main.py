# main.py
from fastapi import FastAPI
from supabase import create_client
import admin_routes, user_routes

url: str = "https://sghpazfqcmxyqrgpymms.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNnaHBhemZxY214eXFyZ3B5bW1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY2NTExMTYsImV4cCI6MjA2MjIyNzExNn0.8oEIYH8nfjYCpbJu-yajX__CJ8o7urMw3f5-0w6eJHg"
supabase = create_client(url, key)

# Inject supabase instance into routers
admin_routes.supabase = supabase
user_routes.supabase = supabase

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is live on Render :)"}

app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
app.include_router(user_routes.router, prefix="/user", tags=["user"])
