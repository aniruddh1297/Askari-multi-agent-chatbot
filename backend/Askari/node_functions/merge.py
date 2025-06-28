from Askari.agent_state import AgentState
from Askari.llm_client import call_llm

async def merge_node(state: AgentState, trace=None) -> dict:
    print("[MERGE NODE] Incoming state:", state.dict())

    current_state = state.dict()

    # Only create fallback response if no route matched
    if state.route == "none":
        print("[MERGE NODE] No specific agent found — falling back to general LLM.")

        fallback_prompt = f"""
No specialized department matched the following query:

\"{state.input}\"

Please provide a helpful general answer.
""".strip()

        try:
            fallback_response = await call_llm(
                fallback_prompt,
                trace=trace,
                span_name="Fallback LLM Call"  
            )
            current_state["final_response"] = f"Assistant :\n{fallback_response.strip()}"

        except Exception as e:
            print(f"[MERGE NODE] Fallback error: {e}")
            current_state["final_response"] = "Sorry, we were unable to process your request."

    print("[MERGE NODE] Final merged state:", current_state)
    return current_state
