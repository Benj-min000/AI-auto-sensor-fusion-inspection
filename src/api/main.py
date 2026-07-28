from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from src.api.routes import inspection, analytics, report

# Initialize the FastAPI application
app = FastAPI(title="AI Quality Platform API")

templates = Jinja2Templates(directory="src/dashboard")

# Register the inspection routing
app.include_router(inspection.router, prefix="/api", tags=["inspection"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(report.router, prefix="/api", tags=["reports"])

# Basic health check endpoint
@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Quality Platform API is running"}

@app.get("/dashboard")
def read_dashboard(request: Request):
    # Updated for modern FastAPI/Starlette versions
    return templates.TemplateResponse(request=request, name="index.html")