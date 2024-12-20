from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI()

# Define a model for the security request
class SecurityRequest(BaseModel):
    title: str
    description: Optional[str] = None
    urgency: int  # 1 (Low) to 5 (High)
    location: str

# Function to check if a title is a rumor using an external API
async def is_rumor(title: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://rumor-scanner-api/check", json={"text": title})
            response.raise_for_status()
            result = response.json()
            return result.get("is_rumor", False)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to rumor scanner API: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"Rumor scanner API error: {str(e)}")

# Endpoint to post a security request
@app.post("/security-requests/")
async def post_security_request(security_request: SecurityRequest):
    # Check if the title is a rumor
    if await is_rumor(security_request.title):
        raise HTTPException(status_code=400, detail="The request appears to be based on a rumor.")

    # If not a rumor, proceed to handle the request
    return {"message": "Security request created successfully!", "data": security_request}
