
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import RedirectResponse

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse("/dashboard")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/ingredients", response_class=HTMLResponse)
async def ingredients_page(request: Request):
    return templates.TemplateResponse("ingredients.html", {"request": request})

@router.get("/meals", response_class=HTMLResponse)
async def meals_page(request: Request):
    return templates.TemplateResponse("meals.html", {"request": request})

@router.get("/serve", response_class=HTMLResponse)
async def serve_page(request: Request):
    return templates.TemplateResponse("serve.html", {"request": request})

@router.get("/report", response_class=HTMLResponse)
async def report_page(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
