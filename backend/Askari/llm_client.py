import asyncio
import os
from dotenv import load_dotenv
from langfuse import Langfuse  # ✅ ONLY import Langfuse
import openai

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Get API keys
api_key = os.getenv("OPENROUTER_API_KEY")
model_id = os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct:free")

if not api_key:
    raise RuntimeError("❌ OPENROUTER_API_KEY not found in .env")

# Configure OpenRouter
openai.api_key = api_key
openai.api_base = "https://openrouter.ai/api/v1"

# Langfuse setup
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# LLM Call with optional parent trace
# ✅ Updated llm_client.py
async def call_llm(prompt: str, trace=None, span_name="LLM Call") -> str:
    try:
        # Group under existing trace if provided
        if trace:
            span = trace.span(name=span_name)
        else:
            trace = langfuse.trace(name="Askari LLM Call", input={"prompt": prompt})
            span = trace.span(name=span_name)

        response = await openai.ChatCompletion.acreate(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content.strip()

        span.end(output={"response": answer})
        trace.update(output={"response": answer}, status="SUCCESS")

        return answer

    except Exception as e:
        print("❌ Langfuse+LLM Error:", e)
        if "span" in locals():
            span.end(output={"error": str(e)}, level="ERROR")
        if "trace" in locals():
            trace.update(output={"error": str(e)}, status="ERROR")
        raise