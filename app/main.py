from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, users, discussions, comments, search

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="3.0.1",
    description="Tangerines API Service",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(discussions.router, prefix=f"{settings.API_V1_STR}/discussions", tags=["discussions"])
app.include_router(comments.router, prefix=f"{settings.API_V1_STR}/comments", tags=["comments"])
app.include_router(search.router, prefix=f"{settings.API_V1_STR}/search", tags=["search"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Tangerines API, You'r not supposed to use this!!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
