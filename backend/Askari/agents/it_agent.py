from llm_client import call_llm
from agent_state import AgentState

async def it_agent_node(state: AgentState, trace=None) -> dict:
    it_input = state.it_message
    print(f"[IT Agent] Input: {it_input}")

    if not it_input:
        return state.dict()

    # Start a new span under the parent trace
    span = trace.span(name="IT Agent") if trace else None

    try:
        # LLM call with trace tracking
        response = await call_llm(f"ITBot: {it_input}", trace=trace, span_name="IT LLM Call")

        print(f"[IT Agent] Output: {response}")

        # Close span on success
        if span:
            span.end(output={"response": response})

        return {
            **state.dict(),
            "it_response": response.strip()
        }

    except Exception as e:
        # Close span with error details
        if span:
            span.end(output={"error": str(e)}, level="ERROR")
        print(f"[IT Agent] Error: {e}")
        raise
