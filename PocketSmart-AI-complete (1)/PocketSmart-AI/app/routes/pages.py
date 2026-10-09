from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router=APIRouter()
templates=Jinja2Templates(directory="app/templates")

@router.get("/",response_class=HTMLResponse)
def index(request:Request): return templates.TemplateResponse("index.html",{"request":request})
@router.get("/login",response_class=HTMLResponse)
def login_page(request:Request): return templates.TemplateResponse("login.html",{"request":request})
@router.get("/register",response_class=HTMLResponse)
def register_page(request:Request): return templates.TemplateResponse("register.html",{"request":request})
@router.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request): return templates.TemplateResponse("dashboard.html",{"request":request})
@router.get("/history-page",response_class=HTMLResponse)
def history_page(request:Request): return templates.TemplateResponse("history.html",{"request":request})
@router.get("/planner/home",response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse("home_planner.html",{"request":request})
@router.get("/planner/party",response_class=HTMLResponse)
def party(request:Request): return templates.TemplateResponse("party_planner.html",{"request":request})
@router.get("/planner/jewelry",response_class=HTMLResponse)
def jewelry(request:Request): return templates.TemplateResponse("jewelry_planner.html",{"request":request})
