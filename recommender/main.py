# app/main.py
# uvicorn recommender.main:app --host 0.0.0.0 --port 8000

from .database import get_db , engine
from fastapi import FastAPI, Request, Response, HTTPException, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from passlib.context import CryptContext
import secrets
from fastapi import Form , Request
import logging
from sqlalchemy.orm import Session , relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .recommender import DraftRecommender  # Your existing recommender import
from .models import User , Base
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Response, Depends, Form, HTTPException
from sqlalchemy.orm import Session
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)
app = FastAPI()
SECRET_KEY = "verystrongkey"  # Use a strong secret key & keep private
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# CORS settings (adjust origins as needed)
origins = [
    "http://localhost:5173",  # Vue default dev server port
    "http://127.0.0.1:5173",
    "http://localhost:8080"   # If your frontend uses 8080, add here
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://special-memory-q7qr5w74g7vfx99j-5175.app.github.dev"
    ],  # whitelist frontend origins explicitly
    allow_credentials=True,   # THIS IS REQUIRED for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize recommender (your existing setup)
recommender = DraftRecommender(
    'recommender/winrate_data.csv',
    'recommender/herodata.json'
)

# --- Models for recommender ---

class Pick(BaseModel):
    pick_order: int
    Team: str
    Hero: str
    first_pick: int


class RecommendRequest(BaseModel):
    picks: List[Pick]

# --- Models for auth ---

class UserCreate(BaseModel):
    email: str  # no email format validation
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# --- Auth backend setup ---

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_db = {}  # In-memory user store, replace with real DB in prod

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token: missing email")
        return email
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
def get_current_user_from_token(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/user/characters/save")
async def save_characters(selected_chars: List[str], 
                          current_user: User = Depends(get_current_user_from_token), 
                          db: Session = Depends(get_db)):
    from .db_character_selections import save_user_characters
    save_user_characters(db, current_user.id, selected_chars)
    return {"message": "Characters saved"}

@app.get("/user/characters")
async def get_characters(current_user: User = Depends(get_current_user_from_token), 
                         db: Session = Depends(get_db)):
    from .db_character_selections import get_user_characters
    chars = get_user_characters(db, current_user.id)
    
    return {"characters": [c.character_id for c in chars]}
# --- Auth endpoints ---
@app.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered"}


@app.post("/auth/jwt/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),

    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.email == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"email": db_user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none"  ,   secure=True)
    return {"message": "Login successful"}

@app.get("/auth/me")
async def get_current_user(request: Request , access_token: Optional[str] = Cookie(None)):
    print("Cookies received:", request.cookies.items())
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    email = verify_token(access_token)

    return {"email": email}

@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=True,
        samesite="none"
    )
    return {"detail": "Logged out"}

@app.post("/recommend")
async def recommend_team(req: RecommendRequest):
    logger.debug(f"Received request: {req.dict()}")  # Log the received data


    picks = [p.dict() for p in req.picks]
    try:
        top_5 = recommender.recommend(picks)
        return {
            "recommendations": top_5
        }
    except Exception as e:
        logger.error(f"Error during recommendation: {str(e)}")
        return {"error": "An internal error occurred", "details": str(e)}
# --- Root endpoint ---

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )