# src/api/server.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import json
import asyncio
from src.api.schemas import AnalysisRequest, AnalysisResponse
from src.crew.manager import OSSGuardianCrew
from src.utils.report_generator import generate_pdf
from pydantic import BaseModel
from src.crew.callbacks import current_status

# 載入環境變數
load_dotenv()

# DEBUG: 檢查 Key 狀態
gemini_key_status = "Loaded" if os.getenv("GEMINI_API_KEY") else "!!! MISSING !!!"
print(f"DEBUG: GEMINI_API_KEY Status: {gemini_key_status}")

app = FastAPI(
    title="OSS Guardian API",
    description="Automated Open Source Due Diligence System powered by Multi-Agents",
    version="1.0.0"
)

# Mount Static Files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

class PDFRequest(BaseModel):
    markdown: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_repo(request: AnalysisRequest):
    """
    Legacy endpoint. Use /stream_analysis for real-time updates.
    """
    try:
        crew_manager = OSSGuardianCrew()
        result = crew_manager.run(query=request.query)
        
        return AnalysisResponse(
            status="success",
            report=result
        )
        
    except Exception as e:
        print(f"Error executing crew: {e}")
        raise HTTPException(status_code=500, detail=f"Crew execution failed. Error: {e}")

@app.get("/stream_analysis")
async def stream_analysis(query: str):
    """
    SSE endpoint that streams agent status and final result.
    """
    async def event_generator():
        # Reset status
        current_status["step"] = "starting"
        current_status["message"] = f"Initializing Crew with Gemini..."
        
        # Start Crew in a separate thread so we can stream status
        # Pass provider to the Crew Manager
        crew_manager = OSSGuardianCrew()
        
        # Use asyncio.to_thread to run the blocking crew execution
        # We need a way to poll status while it runs. 
        # Since to_thread blocks this coroutine until done, we need a task.
        
        task = asyncio.create_task(asyncio.to_thread(crew_manager.run, query))
        
        while not task.done():
            # Yield current status
            data = json.dumps({
                "type": "status",
                "message": current_status["message"]
            })
            yield f"data: {data}\n\n"
            await asyncio.sleep(1) # Poll every 1s
            
        # Task done
        try:
            result = await task
            data = json.dumps({
                "type": "result",
                "report": result
            })
            yield f"data: {data}\n\n"
        except Exception as e:
            data = json.dumps({
                "type": "error",
                "message": str(e)
            })
            yield f"data: {data}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/report/pdf")
async def create_pdf(request: PDFRequest):
    """
    Generates a PDF report from the provided Markdown content.
    """
    try:
        # html = generate_html(request.markdown)  <-- Removed
        pdf_bytes = generate_pdf(request.markdown)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=report.pdf"}
        )
    except Exception as e:
        print(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

@app.get("/")
def read_root():
    return FileResponse('src/static/index.html')