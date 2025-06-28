from langgraph.graph import StateGraph
from Askari.node_functions.router import router_node
from Askari.node_functions.merge import merge_node
from Askari.node_functions.final_response import final_response_builder
from Askari.node_functions.both import both_node
from Askari.agent_registry import AGENT_REGISTRY
from Askari.agent_state import AgentState
from Askari.llm_client import langfuse  # ✅ Import Langfuse instance

def route_handler(state: AgentState) -> str:
    return state.route or "none"

async def run_agent_flow(message: str):
    # ✅ Create trace at the start
    trace = langfuse.trace(name="Askari Agent Flow", input={"input": message})

    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("merge", merge_node)
    builder.add_node("final_response_node", final_response_builder)

    for agent_key, config in AGENT_REGISTRY.items():
        builder.add_node(agent_key, config["node"])

    builder.add_node("both", both_node)

    builder.set_entry_point("router")

    builder.add_conditional_edges(
        "router",
        route_handler,
        {
            "hr": "hr",
            "it": "it",
            "both": "both",
            "none": "merge"
        }
    )

    builder.add_edge("hr", "merge")
    builder.add_edge("it", "merge")
    builder.add_edge("both", "merge")
    builder.add_edge("merge", "final_response_node")
    builder.set_finish_point("final_response_node")

    graph = builder.compile()

    # ✅ Pass trace into LangGraph run
    return await graph.ainvoke({"input": message}, config={"trace": trace})
