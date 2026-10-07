# Data Analysis Agent

An AI-powered data analysis agent that allows users to ask questions about sales data using natural language.

The agent uses a Large Language Model (LLM) to understand the user's question, decide which tool is required, retrieve data from a database, perform statistical analysis when necessary, and generate a natural-language response.

---

## Project Overview

The goal of this project is to understand and implement the core concepts of **Agentic AI** from scratch without relying on agent frameworks such as LangChain.

The agent can:

- Understand natural-language questions
- Decide when to use a database tool
- Generate read-only SQL queries
- Retrieve data from SQLite
- Perform statistical calculations using Python
- Use multiple tools when required
- Chain tool calls
- Maintain short-term conversation history
- Handle tool and database errors
- Provide a final natural-language answer

---

## Architecture

```text
                    User
                     |
                     v
              +-------------+
              |     LLM     |
              |    Qwen     |
              +-------------+
                     |
                     v
             Decide what to do
                     |
          +----------+----------+
          |                     |
          v                     v
   database_tool          analysis_tool
          |                     |
          v                     v
       SQLite                Python
      Database            Calculations
          |                     |
          +----------+----------+
                     |
                     v
                    LLM
                     |
                     v
              Final Response
