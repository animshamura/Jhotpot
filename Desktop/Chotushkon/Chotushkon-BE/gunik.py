from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

# Initialize the FastAPI app
app = FastAPI(title="Rumor Scanner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the input and output models
class RumorRequest(BaseModel):
    text: str

class RumorResponse(BaseModel):
    text: str
    is_rumor: bool
    confidence: float

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the Gunik - Rumor Scanner API!"}

# Endpoint to scan rumor
@app.post("/scan-rumor", response_model=RumorResponse)
def scan_rumor(request: RumorRequest):
    """
    Endpoint to analyze if a given text is a rumor.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Rumor text cannot be empty.")

    # Simulate rumor detection logic
    is_rumor = random.choice([True, False])  # Randomly decide if it's a rumor
    confidence = round(random.uniform(0.7, 1.0), 2)  # Simulate confidence between 0.7 and 1.0

    return RumorResponse(
        text=request.text,
        is_rumor=is_rumor,
        confidence=confidence
    )
