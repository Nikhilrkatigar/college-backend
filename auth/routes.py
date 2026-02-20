from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import users_collection
from auth.auth_utils import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(request: LoginRequest):
    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(status_code=422, detail="Username and password required")

    user = users_collection.find_one({"username": username})

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": username,
        "role": user.get("role"),
    }
