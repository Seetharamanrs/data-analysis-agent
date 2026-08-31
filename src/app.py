from huggingface_hub import InferenceClient
from database import query_database
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
# query = """
# SELECT
#     c.city,
#     SUM(oi.quantity * oi.unit_price) AS total_sales
# FROM customers c
# JOIN orders o
#     ON c.customer_id = o.customer_id
# JOIN order_items oi
#     ON o.order_id = oi.order_id
# WHERE o.order_status = 'Completed'
# GROUP BY c.city
# ORDER BY total_sales DESC;
# """
query = """
DELETE FROM customers;
"""
result = query_database(query)

print(result)