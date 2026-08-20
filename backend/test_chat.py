import os
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)

endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
api_key = os.environ["AZURE_FOUNDRY_API_KEY"]
chat_model = os.environ["AZURE_CHAT_MODEL"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key),
    model=chat_model,
)

response = client.complete(
    messages=[
        SystemMessage(
            content="You are a concise Kubernetes assistant."
        ),
        UserMessage(
            content="Use kubectl rollout undo"
        ),
    ],
    temperature=0.2,
    max_tokens=200,
)

print(response.choices[0].message.content)