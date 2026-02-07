"""
Verifi Backend API - Main Application

This is the entry point for the FastAPI backend that connects:
- Frontend (React) → API → AI Core → Firebase → Blockchain
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import claims, tasks, users

# Create FastAPI app
app = FastAPI(
    title="Verifi API",
    description="Backend API for Verifi claim verification platform",
    version="1.0.0"
)

# Allow all origins for hackathon (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(claims.router, prefix="/claims", tags=["Claims"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "verifi-api", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "ai_core": "ready",
        "database": "connected"  # TODO: actual check
    }
