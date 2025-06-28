from Askari.agent_state import AgentState

async def final_response_builder(state: AgentState) -> dict:
    state_dict = state.dict()

    # ✅ If already set by fallback LLM (route == "none"), pass through unchanged
    if state_dict.get("final_response"):
        return state_dict

    messages = []

    # Add agent responses only if they exist
    if state_dict.get("hr_response"):
        messages.append("HR :\n" + state_dict["hr_response"])
    if state_dict.get("it_response"):
        messages.append("IT :\n" + state_dict["it_response"])

    # Fallback default if agents return nothing
    final = "\n\n".join(messages) if messages else "🟡 Sorry, no department could answer that."

    return {
        **state_dict,
        "final_response": final
    }
