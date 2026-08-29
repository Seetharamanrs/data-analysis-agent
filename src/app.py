from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)
model = "Qwen/Qwen3-4B-Instruct-2507"
messages = [
    {
        "role":"system",
        "content":"""
You are helpful data analysis assistant 
You help users to understand dataset and perform 
data analysis tasks.
Explain concpets clearly and precisely.
if you aren't sure of something reply that's i am out of content """
    },
    {
        "role": "user",
        "content": "What is the average of 10, 20, 30, 40 and 50?"
    }
]
response = client.chat.completions.create(
    model=model,
    messages=messages
)
print(response.choices[0].message.content)