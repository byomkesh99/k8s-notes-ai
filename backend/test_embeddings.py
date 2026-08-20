import os
from pathlib import Path

from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
api_key = os.environ["AZURE_FOUNDRY_API_KEY"]
model_name = os.environ["AZURE_EMBEDDING_MODEL"]

client = EmbeddingsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key),
    model=model_name,
)

response = client.embed(
    input=[
        "Kubernetes deployment rollback using kubectl rollout undo"
    ]
)

embedding = response.data[0].embedding

print("Embedding request succeeded")
print(f"Model: {response.model}")
print(f"Vector dimensions: {len(embedding)}")
print(f"First five values: {embedding[:5]}")
print(f"Usage: {response.usage}")