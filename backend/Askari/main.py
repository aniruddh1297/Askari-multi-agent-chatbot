# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langraph_builder import run_agent_flow
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    # Run LangGraph agent flow
    result = await run_agent_flow(chat_input.message)

    # Return the final combined response
    return {
        "final_response": result.get("final_response", "No valid response generated."),
        "route": result.get("route", "unknown"),
        "hr_response": result.get("hr_response", None),
        "it_response": result.get("it_response", None)
    }
