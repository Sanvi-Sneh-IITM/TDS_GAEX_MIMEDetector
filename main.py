from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class Attachment(BaseModel):
    url: str

class RequestBody(BaseModel):
    attachments: Attachment

def detect_mime_type(data_uri: str) -> str:
    match = re.match(r"data:(.*?)/", data_uri)
    if match:
        top_type = match.group(1)
        if top_type in ["image", "text", "application"]:
            return top_type
    return "unknown"

@app.post("/file")
def file_detector(body: RequestBody):
    data_uri = body.attachments.url
    mime_type = detect_mime_type(data_uri)
    return {"type": mime_type}
