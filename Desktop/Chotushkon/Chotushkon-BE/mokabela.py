from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import random


def is_fraudulent(request: Dict) -> bool:
 
    return random.random() < 0.1

# Relief request model
class ReliefRequest(BaseModel):
    name: str
    location: str
    description: str
    requested_amount: float

# Fundraising data
funds_raised = {}

app = FastAPI()

@app.post("/relief-request")
async def post_relief_request(request: ReliefRequest):
    """
    Accepts a relief request, checks for fraud, and initiates fundraising if valid.
    """
    # Check for fraud
    if is_fraudulent(request.dict()):
        raise HTTPException(status_code=400, detail="Fraudulent request detected.")

    # Save the request and start fundraising
    funds_raised[request.name] = {
        "location": request.location,
        "description": request.description,
        "requested_amount": request.requested_amount,
        "raised_amount": 0.0
    }

    return {"message": "Relief request accepted and fundraising started.", "data": funds_raised[request.name]}

@app.get("/funds/{name}")
async def get_fund_status(name: str):
    """
    Get the fundraising status for a specific request.
    """
    if name not in funds_raised:
        raise HTTPException(status_code=404, detail="Request not found.")

    return funds_raised[name]

@app.post("/donate")
async def donate_to_request(name: str, amount: float):
    """
    Donate to a specific relief request.
    """
    if name not in funds_raised:
        raise HTTPException(status_code=404, detail="Request not found.")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Donation amount must be greater than zero.")

    funds_raised[name]["raised_amount"] += amount

    return {
        "message": f"Thank you for your donation of {amount} to {name}.",
        "updated_data": funds_raised[name]
    }
