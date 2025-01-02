from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, forms, submissions

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI()

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(forms.router, prefix="/forms", tags=["Forms"])
app.include_router(submissions.router, prefix="/forms/submissions", tags=["Submissions"])

@app.get("/")
def root():
    return {"message": "Welcome to the Kraftbase Project"}
