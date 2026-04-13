import uvicorn
import os
import subprocess
import sys
from fastapi import FastAPI, Request, status
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import Session, select
from app.routers import templates, static_files, router, api_router
from app.config import get_settings
from contextlib import asynccontextmanager
from app.database import engine, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    
    with Session(engine) as session:
        from app.models.workout import Workout
        
        workout_count = len(session.exec(select(Workout)).all())
        
        if workout_count == 0:
            print("Database empty, seeding...")
            cli_path = os.path.join(os.path.dirname(__file__), "cli.py")
            subprocess.run([sys.executable, cli_path, "initialize"])
            print("Seeding complete.")
    
    yield


app = FastAPI(
    middleware=[
        Middleware(SessionMiddleware, secret_key=get_settings().secret_key)
    ],
    lifespan=lifespan
)   

app.include_router(router)
app.include_router(api_router)
app.mount("/static", static_files, name="static")


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_redirect_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request, 
        name="401.html",
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host=get_settings().app_host, 
        port=get_settings().app_port, 
        reload=get_settings().env.lower() != "production"
    )