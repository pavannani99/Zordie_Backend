from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.dashboard import router as dashboard_router

app = FastAPI(
    title="Zordie Dashboard",
    description="Dashboard for resume analysis",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only the dashboard router
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "Welcome to Zordie Dashboard"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.dashboard_app:app", host="0.0.0.0", port=8000, reload=True) 