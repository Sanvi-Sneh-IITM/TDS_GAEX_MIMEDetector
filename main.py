from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(
    title="MIME Detector API",
    description="Detects MIME top-level type from data URI strings.",
    version="1.0.0"
)

# ✅ Allow all origins for browser POST requests (fix for 405 OPTIONS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # includes OPTIONS for preflight
    allow_headers=["*"],
)

# ✅ Expected input format
class Attachment(BaseModel):
    url: str

class RequestBody(BaseModel):
    attachments: Attachment

def detect_mime_type(data_uri: str) -> str:
    # Regex to extract top-level MIME category like "image", "text"
    match = re.match(r"data:(.*?)/", data_uri)
    
    if match:
        top_type = match.group(1)
        if top_type in ["image", "text", "application"]:
            return top_type
    
    return "unknown"

@app.post("/file")
async def file_detector(body: RequestBody):
    data_uri = body.attachments.url
    
    if not data_uri.startswith("data:"):
        return {"type": "unknown"}

    mime_type = detect_mime_type(data_uri)
    
    return {"type": mime_type}

@app.get("/")
def root():
    return {"status": "running", "hint": "POST to /file with data URI"}
