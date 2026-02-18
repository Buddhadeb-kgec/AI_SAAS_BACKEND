from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base
from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.ai import router as ai_router


app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS configuration
origins = [
    "http://localhost:5173",
    "https://ai-saas-backend-ewnp.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(ai_router)


@app.get("/")
def read_root():
    return {"message": "AI SaaS Backend is running 🚀"}
