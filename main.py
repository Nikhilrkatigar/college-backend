from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

# ---- LOAD ENV ----
load_dotenv()

# ---- IMPORT ROUTERS ----
from auth.routes import router as auth_router
from users.routes import router as users_router
from colleges.routes import router as colleges_router
from extractor.routes import router as extract_router
from locations.routes import router as locations_router

# ---- IMPORT DATABASE ----
from database import users_collection

# ---- PASSWORD HASHING ----
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ---- APP INIT ----
app = FastAPI(title="College Placement Contact Extractor")

# ===============================
#            CORS
# ===============================

FRONTEND_URL = os.getenv("FRONTEND_URL")

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

if FRONTEND_URL:
    allowed_origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
#        AUTO ADMIN CREATION
# ===============================

@app.on_event("startup")
async def create_admin_on_startup():
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    existing_admin = users_collection.find_one({"username": admin_username})

    if not existing_admin:
        hashed_password = pwd_context.hash(admin_password)

        users_collection.insert_one({
            "username": admin_username,
            "password": hashed_password,
            "role": "admin"
        })

        print("✓ Default admin created")
    else:
        print("✓ Admin already exists")

# ===============================
#          ROUTERS
# ===============================

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(colleges_router, prefix="/api")
app.include_router(extract_router, prefix="/api")
app.include_router(locations_router, prefix="/api")

# ===============================
#        HEALTH CHECK
# ===============================

@app.get("/")
def root():
    return {"status": "Backend running"}
