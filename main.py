from fastapi import FastAPI
import httpx
import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

logging.basicConfig(level=logging.INFO)

WAKEUP_URL = os.getenv("WAKEUP_URL", "http://localhost:8000/")

async def wakeup_task():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(WAKEUP_URL)
                if response.status_code == 200:
                    logging.info("Server is awake ✅")
                else:
                    logging.warning(f"Server responded with status: {response.status_code}")
        except Exception as e:
            logging.error(f"Error while waking up server: {e}")
        
        await asyncio.sleep(5 * 60)  # Sleep for 5 minutes

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(wakeup_task())

@app.get("/")
async def root():
    return {"message": "FastAPI wakeup server is running."}
