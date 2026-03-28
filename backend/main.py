from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from processor import process_text, process_audio, process_image_ocr, process_news_url
from gemini_client import process_with_gemini, process_image_with_gemini
from history import save_to_history, load_history

app = FastAPI(title="Universal AI Bridge", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0"}

@app.post("/process/text")
async def handle_text(text: str = Form(...)):
    structured = process_text(text)
    result = process_with_gemini(structured)
    save_to_history(structured, result)
    return JSONResponse(content=result)

@app.post("/process/voice")
async def handle_voice(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    structured = process_audio(audio_bytes)
    result = process_with_gemini(structured)
    save_to_history(structured, result)
    return JSONResponse(content=result)

@app.post("/process/image")
async def handle_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    structured = process_image_ocr(image_bytes)
    if structured.get("ocr_text", "").strip():
        result = process_with_gemini(structured)
    else:
        result = process_image_with_gemini(image_bytes, file.content_type)
    save_to_history(structured, result)
    return JSONResponse(content=result)

@app.post("/process/news")
async def handle_news(url: str = Form(...)):
    structured = process_news_url(url)
    result = process_with_gemini(structured)
    save_to_history(structured, result)
    return JSONResponse(content=result)

@app.get("/history")
async def get_history():
    return load_history()

@app.delete("/history")
async def clear_history():
    import os
    if os.path.exists("chat_history.json"):
        os.remove("chat_history.json")
    return {"status": "cleared"}

from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str
