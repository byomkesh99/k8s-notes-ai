import json
import os
from pathlib import Path
from typing import Any, Iterator

import httpx
from azure.ai.inference import ChatCompletionsClient, EmbeddingsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)

MEILISEARCH_URL = os.getenv(
    "MEILISEARCH_URL",
    "http://localhost:7700",
)
MEILISEARCH_KEY = os.environ["MEILISEARCH_KEY"]
INDEX_NAME = "k8s-notes"

AZURE_INFERENCE_ENDPOINT = os.environ["AZURE_INFERENCE_ENDPOINT"]
AZURE_FOUNDRY_API_KEY = os.environ["AZURE_FOUNDRY_API_KEY"]
AZURE_EMBEDDING_MODEL = os.environ["AZURE_EMBEDDING_MODEL"]
AZURE_CHAT_MODEL = os.environ["AZURE_CHAT_MODEL"]

embedding_client = EmbeddingsClient(
    endpoint=AZURE_INFERENCE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FOUNDRY_API_KEY),
    model=AZURE_EMBEDDING_MODEL,
)

chat_client = ChatCompletionsClient(
    endpoint=AZURE_INFERENCE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FOUNDRY_API_KEY),
    model=AZURE_CHAT_MODEL,
)

app = FastAPI(title="Kubernetes Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class AnswerRequest(BaseModel):
    query: str
    limit: int = 5


def sse_event(payload: dict[str, Any]) -> str:
    return f"data: {json.dumps(payload)}\n\n"


def source_list(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source": hit.get("source", "Unknown"),
            "section": hit.get("section", "Unknown"),
            "title": hit.get("title", "Unknown"),
        }
        for hit in hits
    ]


async def retrieve_hits(
    query: str,
    limit: int,
) -> list[dict[str, Any]]:
    embedding_response = embedding_client.embed(input=[query])
    query_vector = embedding_response.data[0].embedding

    search_url = f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/search"

    headers = {
        "Authorization": f"Bearer {MEILISEARCH_KEY}",
        "Content-Type": "application/json",
    }

    search_payload = {
        "q": query,
        "vector": query_vector,
        "hybrid": {
            "embedder": "default",
            "semanticRatio": 0.5,
        },
        "limit": limit,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            search_url,
            headers=headers,
            json=search_payload,
        )

    response.raise_for_status()

    search_data = response.json()
    return search_data.get("hits", [])


def create_context(hits: list[dict[str, Any]]) -> str:
    context_parts = []

    for index, hit in enumerate(hits, start=1):
        context_parts.append(
            f"[Source {index}]\n"
            f"File: {hit.get('source', 'Unknown')}\n"
            f"Section: {hit.get('section', 'Unknown')}\n"
            f"Content:\n{hit.get('content', '')}"
        )

    return "\n\n".join(context_parts)


def create_prompts(
    query: str,
    context: str,
) -> tuple[str, str]:
    system_prompt = """
You are a Kubernetes notes assistant.

Answer the user's question using only the supplied Kubernetes notes.

Rules:
- Do not invent information that is not present in the notes.
- If the notes do not contain enough information, say so clearly.
- Keep the answer concise and practical.
- Include Kubernetes commands in Markdown code blocks.
- Do not include [Source X] labels inside the answer.
- The application will display the source files separately.
"""

    user_prompt = f"""
Question:
{query}

Retrieved Kubernetes notes:
{context}
"""

    return system_prompt, user_prompt


def stream_answer(
    system_prompt: str,
    user_prompt: str,
    hits: list[dict[str, Any]],
) -> Iterator[str]:
    try:
        stream = chat_client.complete(
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt),
            ],
            temperature=0.2,
            max_tokens=500,
            stream=True,
        )

        for update in stream:
            if not update.choices:
                continue

            delta = update.choices[0].delta
            content = getattr(delta, "content", None)

            if content:
                yield sse_event(
                    {
                        "type": "content",
                        "text": content,
                    }
                )

        yield sse_event(
            {
                "type": "sources",
                "items": source_list(hits),
            }
        )

        yield sse_event({"type": "done"})

    except Exception as error:
        yield sse_event(
            {
                "type": "error",
                "message": str(error),
            }
        )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "search_mode": "hybrid",
    }


@app.post("/search")
async def search(request: SearchRequest):
    query = request.query.strip()

    if not query:
        return {
            "hits": [],
            "query": query,
            "estimatedTotalHits": 0,
        }

    hits = await retrieve_hits(query, request.limit)

    return {
        "hits": hits,
        "query": query,
        "estimatedTotalHits": len(hits),
    }


@app.post("/answer")
async def answer(request: AnswerRequest):
    query = request.query.strip()

    if not query:
        return {
            "answer": "Please provide a question.",
            "sources": [],
        }

    hits = await retrieve_hits(query, request.limit)

    if not hits:
        return {
            "answer": (
                "I could not find enough information in your "
                "Kubernetes notes to answer this question."
            ),
            "sources": [],
        }

    context = create_context(hits)
    system_prompt, user_prompt = create_prompts(query, context)

    chat_response = chat_client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt),
        ],
        temperature=0.2,
        max_tokens=500,
    )

    generated_answer = chat_response.choices[0].message.content

    return {
        "answer": generated_answer,
        "sources": source_list(hits),
    }


@app.post("/answer/stream")
async def answer_stream(request: AnswerRequest):
    query = request.query.strip()

    if not query:
        def empty_question_stream():
            yield sse_event(
                {
                    "type": "content",
                    "text": "Please provide a question.",
                }
            )
            yield sse_event(
                {
                    "type": "sources",
                    "items": [],
                }
            )
            yield sse_event({"type": "done"})

        return StreamingResponse(
            empty_question_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    hits = await retrieve_hits(query, request.limit)

    if not hits:
        def no_results_stream():
            yield sse_event(
                {
                    "type": "content",
                    "text": (
                        "I could not find enough information in your "
                        "Kubernetes notes to answer this question."
                    ),
                }
            )
            yield sse_event(
                {
                    "type": "sources",
                    "items": [],
                }
            )
            yield sse_event({"type": "done"})

        return StreamingResponse(
            no_results_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    context = create_context(hits)
    system_prompt, user_prompt = create_prompts(query, context)

    return StreamingResponse(
        stream_answer(system_prompt, user_prompt, hits),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )