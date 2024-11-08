import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request
import os
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse

app = FastAPI()

# Retrieve the token and app_secret from environment variables
APP_SECRET = os.getenv("APP_SECRET")  # For validating x_hub_signature
VERIFY_TOKEN = os.getenv("TOKEN")  # For validating the webhook verification request

@app.get("/webhook")
async def verify_webhook(hub_mode: str, hub_verify_token: str, hub_challenge: str):
    # Check if the verify token matches the one set in Facebook App Dashboard
    if hub_verify_token == VERIFY_TOKEN:
        return JSONResponse(content={"hub.challenge": hub_challenge})
    else:
        raise HTTPException(status_code=403, detail="Invalid verify token")

@app.post("/webhook")
async def webhook(request: Request, x_hub_signature: str = Header(None)):
    # Extract and log incoming JSON data
    data = await request.json()
    print("Received webhook data:", data)

    # Verify using the app secret for x_hub_signature
    if x_hub_signature != APP_SECRET:
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Process the webhook event
    return {"status": "Webhook received successfully"}

@app.get("/")
async def root():
    return {"message": "Hello, Vercel!"}

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy():
    # Read the privacy_policy.html file
    file_path = os.path.join(os.path.dirname(__file__), "privacy_policy.html")
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
