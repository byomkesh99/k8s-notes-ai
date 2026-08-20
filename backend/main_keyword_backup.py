import os

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Kubernetes Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEILISEARCH_URL = os.getenv(
    "MEILISEARCH_URL",
    "http://localhost:7700",
)

MEILISEARCH_KEY = os.getenv(
    "MEILISEARCH_KEY",
    "dev-master-key-change-later",
)

INDEX_NAME = "k8s-notes"


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/search")
async def search(request: SearchRequest):
    url = f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/search"

    headers = {
        "Authorization": f"Bearer {MEILISEARCH_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "q": request.query,
        "limit": request.limit,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload,
        )

    response.raise_for_status()
    return response.json()