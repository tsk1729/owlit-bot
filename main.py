import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# The verification token you set in the Facebook App Dashboard
VERIFY_TOKEN = "your_verify_token_here"  # This should be the same as what you use in the webhook config

@app.get("/webhook")
async def verify_webhook(hub_mode: str, hub_verify_token: str, hub_challenge: str):
    # Check the verify token matches the one set in Facebook App Dashboard
    if hub_verify_token == VERIFY_TOKEN:
        return JSONResponse(content={"hub.challenge": hub_challenge})
    else:
        raise HTTPException(status_code=403, detail="Invalid verify token")

@app.post("/webhook")
async def webhook(request: Request, x_hub_signature: str = Header(None)):
    # Extract and log incoming JSON data
    data = await request.json()
    print("Received webhook data:", data)

    # Verify using the token (replace 'your_token_here' with your actual token)
    if x_hub_signature != "your_token_here":
        raise HTTPException(status_code=403, detail="Invalid token")

    # Process the webhook event
    return {"status": "Webhook received successfully"}

@app.get("/")
async def root():
    return {"message": "Hello, Vercel!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
