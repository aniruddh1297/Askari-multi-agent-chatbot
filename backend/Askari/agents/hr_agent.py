from Askari.llm_client import call_llm
from Askari.agent_state import AgentState

async def hr_agent_node(state: AgentState, trace=None) -> dict:
    hr_input = state.hr_message
    print(f"[HR Agent] Input: {hr_input}")

    # Return early if input is missing
    if not hr_input:
        return state.dict()

    # Start a new span if trace exists
    span = trace.span(name="HR Agent") if trace else None

    try:
        # LLM call with trace
        response = await call_llm(f"HRBot: {hr_input}", trace=trace, span_name="HR LLM Call")

        print(f"[HR Agent] Output: {response}")

        # Close the Langfuse span on success
        if span:
            span.end(output={"response": response})

        return {
            **state.dict(),
            "hr_response": response.strip()
        }

    except Exception as e:
        # Close the span with error details
        if span:
            span.end(output={"error": str(e)}, level="ERROR")
        print(f"[HR Agent] Error: {e}")
        raise
