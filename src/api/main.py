from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Slide Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.get("/search")
async def search_slides(query: str):
    return {"query": query}

@app.get("/slides/{slide_id}")
async def get_slide(slide_id: str):
    return {"slide_id": slide_id}

@app.get("/slides")
async def list_slides():
    return {"slides": []}

@app.get("/slides/{slide_id}/content")
async def get_slide_content(slide_id: str):
    return {"content": "This is the content of slide 1"}

@app.get("/slides/{slide_id}/images")
async def get_slide_images(slide_id: str):
    return {"images": []}

@app.get("/slides/{slide_id}/notes")
async def get_slide_notes(slide_id: str):
    return {"notes": "This is the notes of slide 1"}

@app.get("/slides/{slide_id}/topics")
async def get_slide_topics(slide_id: str):
    return {"topics": ["Topic 1", "Topic 2"]}

@app.get("/slides/{slide_id}/related")
async def get_related_slides(slide_id: str):
    return {"related_slides": ["Slide 2", "Slide 3"]}

@app.get("/slides/{slide_id}/related")
async def get_related_slides(slide_id: str):