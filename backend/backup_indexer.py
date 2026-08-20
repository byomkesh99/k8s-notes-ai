from __future__ import annotations
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

import hashlib
import os
import re
from pathlib import Path

import httpx


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = PROJECT_ROOT / "notes"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)

AZURE_INFERENCE_ENDPOINT = os.environ[
    "AZURE_INFERENCE_ENDPOINT"
]

AZURE_FOUNDRY_API_KEY = os.environ[
    "AZURE_FOUNDRY_API_KEY"
]

AZURE_EMBEDDING_MODEL = os.environ[
    "AZURE_EMBEDDING_MODEL"
]

MEILISEARCH_URL = os.getenv(
    "MEILISEARCH_URL",
    "http://localhost:7700",
)

MEILISEARCH_KEY = os.getenv(
    "MEILISEARCH_KEY",
    "dev-master-key-change-later",
)

INDEX_NAME = "k8s-notes"

HEADINGS_PATTERN = re.compile(
    r"(?m)^(#{1,6})[ \t]+(.+?)[ \t]*$"
)


def create_document_id(source: str, section: str) -> str:
    value = f"{source}:{section}"
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def split_markdown(content: str, source: str) -> list[dict]:
    matches = list(HEADINGS_PATTERN.finditer(content))

    if not matches:
        return [
            {
                "section": "Full document",
                "content": content.strip(),
            }
        ]

    sections = []

    for index, match in enumerate(matches):
        heading = match.group(2).strip()
        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(content)
        )

        section_content = content[start:end].strip()

        if section_content:
            sections.append(
                {
                    "section": heading,
                    "content": section_content,
                }
            )

    return sections


def split_text(content: str) -> list[dict]:
    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", content)
        if paragraph.strip()
    ]

    if not paragraphs:
        return []

    sections = []

    for index, paragraph in enumerate(paragraphs, start=1):
        sections.append(
            {
                "section": f"Section {index}",
                "content": paragraph,
            }
        )

    return sections


def build_documents() -> list[dict]:
    documents = []

    note_files = sorted(
        path
        for path in NOTES_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".md", ".txt"}
    )

    for note_file in note_files:
        content = note_file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

        if not content:
            continue

        source = note_file.name

        if note_file.suffix.lower() == ".md":
            sections = split_markdown(content, source)
        else:
            sections = split_text(content)

        topic = note_file.stem.replace("_", " ").replace("-", " ")

        for section in sections:
            section_name = section["section"]
            section_content = section["content"]

            documents.append(
                {
                    "id": create_document_id(source, section_name),
                    "title": section_name,
                    "content": section_content,
                    "source": source,
                    "section": section_name,
                    "topic": topic,
                    "file_type": note_file.suffix.lower().replace(".", ""),
                }
            )

    return documents


def meilisearch_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {MEILISEARCH_KEY}",
        "Content-Type": "application/json",
    }


def create_index(client: httpx.Client) -> None:
    response = client.post(
        f"{MEILISEARCH_URL}/indexes",
        headers=meilisearch_headers(),
        json={
            "uid": INDEX_NAME,
            "primaryKey": "id",
        },
    )

    if response.status_code not in {201, 202, 400}:
        response.raise_for_status()

# Before Embedding feature added
#def configure_index(client: httpx.Client) -> None:
#    response = client.patch(
#        f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/settings",
#        headers=meilisearch_headers(),
#        json={
#            "searchableAttributes": [
#                "title",
#                "content",
#                "topic",
#                "section",
#                "source",
#            ],
#            "filterableAttributes": [
#                "topic",
#                "source",
#                "file_type",
#            ],
#            "displayedAttributes": [
#                "id",
#                "title",
#                "content",
#                "source",
#                "section",
#                "topic",
#                "file_type",
#            ],
#        },
#    )
#
#    response.raise_for_status()
#

# After Embedding feature added
def configure_index(client: httpx.Client) -> None:
    response = client.patch(
        f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/settings",
        headers=meilisearch_headers(),
        json={
            "searchableAttributes": [
                "title",
                "content",
                "topic",
                "section",
                "source",
            ],
            "filterableAttributes": [
                "topic",
                "source",
                "file_type",
            ],
            "displayedAttributes": [
                "id",
                "title",
                "content",
                "source",
                "section",
                "topic",
                "file_type",
            ],
            "embedders": {
                "default": {
                    "source": "userProvided",
                    "dimensions": 1536
                }
            }
        },
    )

    response.raise_for_status()


def upload_documents(
    client: httpx.Client,
    documents: list[dict],
) -> None:
    response = client.post(
        f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/documents",
        headers=meilisearch_headers(),
        json=documents,
    )

    response.raise_for_status()
    print(response.json())

# Before Embedding feature added
# def main() -> None:
#     documents = build_documents()
# 
#     if not documents:
#         raise RuntimeError(
#             f"No .md or .txt files found in {NOTES_DIR}"
#         )
# 
#     print(f"Found {len(documents)} searchable sections.")
# 
#     with httpx.Client(timeout=60.0) as client:
#         create_index(client)
#         configure_index(client)
#         upload_documents(client, documents)
# 
#     print("Indexing task submitted successfully.")

# After Embedding feature added
def main() -> None:
    documents = build_documents()

    if not documents:
        raise RuntimeError(
            f"No .md or .txt files found in {NOTES_DIR}"
        )

    print(f"Found {len(documents)} searchable sections.")

    embedding_client = create_embedding_client()

    print("Generating Azure OpenAI embeddings...")
    add_embeddings(documents, embedding_client)

    with httpx.Client(timeout=60.0) as client:
        create_index(client)
        configure_index(client)
        upload_documents(client, documents)

    print("Indexing task submitted successfully.")

# After Embedding feature added
def create_embedding_client() -> EmbeddingsClient:
    return EmbeddingsClient(
        endpoint=AZURE_INFERENCE_ENDPOINT,
        credential=AzureKeyCredential(
            AZURE_FOUNDRY_API_KEY
        ),
        model=AZURE_EMBEDDING_MODEL,
    )

# After Embedding feature added
def add_embeddings(
    documents: list[dict],
    embedding_client: EmbeddingsClient,
    batch_size: int = 32,
) -> None:
    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]

        texts = [
            f"{document['title']}\n\n{document['content']}"
            for document in batch
        ]

        response = embedding_client.embed(input=texts)

        if len(response.data) != len(batch):
            raise RuntimeError(
                "Embedding count does not match document count."
            )

        for document, embedding_item in zip(
            batch,
            response.data,
        ):
            document["_vectors"] = {
                "default": embedding_item.embedding
            }

        print(
            f"Embedded {min(start + batch_size, len(documents))}"
            f"/{len(documents)} sections"
        )

if __name__ == "__main__":
    main()