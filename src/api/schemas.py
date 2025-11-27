# src/api/schemas.py
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    query: str = Field(
        ..., 
        description="Target GitHub URL or a search topic (e.g., 'FastAPI auth library')",
        example="https://github.com/tiangolo/fastapi"
    )

class AnalysisResponse(BaseModel):
    status: str
    report: str
