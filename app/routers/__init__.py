from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.utilities.flash import get_flashed_messages
from jinja2 import Environment, FileSystemLoader
from app.config import get_settings

# Create these FIRST
router = APIRouter()
api_router = APIRouter()

template_env = Environment(
    loader=FileSystemLoader("app/templates"),
)

template_env.globals["get_flashed_messages"] = get_flashed_messages
template_env.globals["settings"] = get_settings()

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages
templates.env.globals["settings"] = get_settings()

static_files = StaticFiles(directory="app/static")

# Import route modules LAST
from . import index, login, register, admin_home, user_home, users, logout, workouts, routines, ai, presets