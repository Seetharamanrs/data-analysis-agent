from huggingface_hub import InferenceClient
from database import query_database
from dotenv import load_dotenv
import os
from database import query_database
from analysis import calculate_statistics
import json

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)

# load_dotenv()
# HF_TOKEN = os.getenv("HF_TOKEN")
# client = InferenceClient(
#     provider="auto",
#     api_key=HF_TOKEN
# )
model = "Qwen/Qwen3-4B-Instruct-2507"
tools = [
    
    {
        "type": "function",
        "function": {
            "name": "database_tool",
            "description": """
        Retrieve information from the sales database.

        Use this tool when the user asks about:
        customers, products, orders, sales, revenue,
        cities, order status, or other information
        stored in the database.

        Only read-only SELECT queries are allowed.
        """,
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
    },{
    "type": "function",
    "function": {
        "name": "analysis_tool",
        "description": "Calculate statistical measures such as mean, median, minimum, maximum, and standard deviation for a list of numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "values": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "description": "A list of numerical values to analyze."
                }
            },
            "required": ["values"]
        }
    }
}
]
user_question = input(
    "Ask a question about the sales data: "
)

messages = [
    {
        "role": "system",
        "content": """
        You are a helpful data analysis assistant.

        You have access to a sales database.

        You have access to two tools:

1. database_tool
   - Use this when information must be retrieved from the sales database.
   - Use only read-only SELECT queries.
   - Do not modify, delete, or insert database data.

2. analysis_tool
   - Use this when numerical calculations or statistical analysis are required.
   - It can calculate count, mean, median, minimum, maximum, and standard deviation.

Follow these rules:

1. Understand what the user is asking.
2. Decide which tool is required.
3. Use database_tool when data must be retrieved from the database.
4. Use analysis_tool when numerical analysis is required.
5. If both data retrieval and calculation are required, use the tools in sequence.
6. Never invent database values.
7. Only use information returned by the tools.
8. If a tool returns an error, do not invent an answer. Explain the problem clearly.
"""
    },
    {
        "role": "user",
        "content": user_question
    }
]


response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto"
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
while True:
    message= response.choices[0].message
    if message.tool_calls:

        print("Tool requested by LLM.")

        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("Tool:", tool_name)
        print("Arguments:", arguments)

            # Adding  the assistant's tool-call message
        if tool_name == "database_tool":
            try:
                result = query_database(arguments["query"])   

            except Exception as e:

                result = {
                    "error": str(e)
                }


            print("\nDatabase result:")
            print(result)
        elif tool_name == "analysis_tool":
            result = calculate_statistics(arguments["values"])

        messages.append({
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(arguments)
                        }
                    }
                ]
            })
            # Add the tool result

        messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })


            # 10. Send result back to LLM
        final_response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
        # 11. Print final answer

    final_answer = (
            final_response
            .choices[0]
            .message
            .content
        )

    print("\nFinal Answer:")
    print(final_answer)


else:


    print("\nFinal Answer:")
    print(message.content)

