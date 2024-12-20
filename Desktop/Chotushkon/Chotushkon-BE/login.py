from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import secrets
from pydantic import BaseModel
import os 

# Define the Pydantic model for login data
class LoginRequest(BaseModel):
    username: str
    password: str

app = FastAPI()

# Middleware for handling CORS and sessions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sk = secrets.token_hex(32)
app.add_middleware(SessionMiddleware, secret_key=sk)

# Mock user database (replace with real database)
USER_DB = {
    "testuser": "password123",
    "johndoe": "mypassword",
}

# Setting up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Endpoint to render the login page
TEMPLATES_DIR = r"C:\Users\great computer\Desktop\Land\Chotushkon-FE"
templates = Jinja2Templates(directory=TEMPLATES_DIR)
@app.get("/", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to handle login and create session
@app.post("/login")
async def login(request: Request, data: LoginRequest):
    username = data.username
    password = data.password

    if username in USER_DB and USER_DB[username] == password:
        request.session["user"] = username
        TEMPLATES_DIR = r"C:\Users\great computer\Desktop\Land\Chotushkon-FE"
        templates = Jinja2Templates(directory=TEMPLATES_DIR)
        
        return templates.TemplateResponse("userdash.html", {"request": request})

    return JSONResponse({"error": "Invalid username or password"}, status_code=401)
@app.get("/userdash", response_class=HTMLResponse)
async def render_dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("userdash.html", {"request": request, "username": user})

# Endpoint to handle logout
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
