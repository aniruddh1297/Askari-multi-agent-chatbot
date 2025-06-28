from agent_registry import AGENT_REGISTRY
from agent_state import AgentState

async def both_node(state: AgentState, trace=None) -> dict:
    print("[BOTH NODE] Running all matched agents")

    current_state = state.dict()

    for key in AGENT_REGISTRY:
        if current_state.get(f"{key}_message"):
            print(f"[BOTH NODE] Calling {key.upper()} Agent")
            result = await AGENT_REGISTRY[key]["node"](AgentState(**current_state), trace=trace)  
            current_state.update(result)

    return current_state
