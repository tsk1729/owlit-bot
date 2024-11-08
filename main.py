import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request, x_hub_signature: str = Header(None)):
    # Extract and log incoming JSON data
    data = await request.json()
    print("Received webhook data:", data)

    # Verify using the token (replace 'your_token_here' with your token)
    if x_hub_signature != "your_token_here":
        raise HTTPException(status_code=403, detail="Invalid token")

    # Process the webhook event
    return {"status": "Webhook received successfully"}

@app.get("/")
async def root():
    return {"message": "Hello, Vercel!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
