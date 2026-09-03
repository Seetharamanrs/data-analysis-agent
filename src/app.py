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
tools = [
    {
        "type": "function",
        "function": {
            "name": "database_tool",
            "description": "Query the sales database to retrieve current business information. Use this tool when the user asks about customers, products, orders, sales, revenue, cities, or other information stored in the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A read-only SQLite SELECT query to retrieve the required information."
                    }
                },
                "required": ["query"]
            }
        }
    }
]



messages = [
    {
        "role": "system",
        "content": """
        You are a helpful data analysis assistant.

        You have access to a sales database tool.

        Use the database tool whenever the user asks for
        information that needs to be retrieved from the database.

        Do not invent database information.
        """
    },
    {
        "role": "user",
        "content": "Which city generated the highest sales?"
    }
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tools_choice="auto"
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
# query = """
# DELETE FROM customers;
# """
# result = query_database(query)
# print(result)

message= response.choices[0].message
print("LLM response:")
print(message)
