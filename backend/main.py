import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EDINET_API_KEY", "")
BASE_URL = "https://edinetdb.jp"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

HEADERS = {"X-API-Key": API_KEY}


@app.get("/api/search")
async def search(q: str = Query(..., description="企業名・EDINETコード・証券コード")):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/v1/search", params={"q": q}, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@app.get("/api/financials/{code}")
async def financials(code: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/v1/companies/{code}/financials",
            headers=HEADERS,
            timeout=10,
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
