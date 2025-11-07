from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables, init_sample_data
from routers import quotes
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Random Quote API",
    description="A complete API system for managing and retrieving random quotes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quotes.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database and sample data on startup"""
    create_tables()
    init_sample_data()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Random Quote API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "quotes": "/quotes/",
            "random_quote": "/quotes/random",
            "categories": "/quotes/categories/list"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Random Quote API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )