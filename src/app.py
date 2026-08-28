from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)
model = "Qwen/Qwen2.5-7B-Instruct-1M"
messages = [
    {
        "role": "user",
        "content": "What is machine learning?"
    }
]
response = client.chat.completions.create(
    model=model,
    messages=messages
)
print(response.choices[0].message.content)