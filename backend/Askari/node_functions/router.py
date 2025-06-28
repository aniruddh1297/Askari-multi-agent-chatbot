import re
import json
from Askari.llm_client import call_llm
from Askari.agent_state import AgentState

def sanitize_json(text: str) -> str:
    text = re.sub(r"```json|```", "", text)
    text = text.replace("\n", " ").replace("\r", " ")
    return text.strip()

async def router_node(state: AgentState, trace=None) -> dict:
    user_input = state.input
    print(f"[RouterNode] Received input: {user_input}")

    span = trace.span(name="Router Node") if trace else None

    try:
        # Step 1: Ask LLM to classify the message into route
        route_prompt = f"""
You are a smart routing assistant.
Classify the following message into ONLY one of these categories:
- hr: For leave, payroll, HR policies
- it: For login, VPN, software issues
- both: If it belongs to both
- none: If irrelevant or general

Respond with ONLY ONE WORD: hr, it, both, or none.

Message: "{user_input}"
""".strip()

        raw_response = await call_llm(route_prompt, trace=trace, span_name="Route Classifier")
        cleaned = raw_response.strip().lower()
        print(f"[RouterNode] Raw LLM Output: '{cleaned}'")

        match = re.search(r"\b(hr|it|both|none)\b", cleaned)
        route = match.group(1) if match else "none"
        print(f"[RouterNode] Routing decision: '{route}'")

        hr_msg = it_msg = None

        # Step 2: Split message if it's for both HR and IT
        if route == "both":
            splitter_prompt = f"""
Split the following user message into two parts:
- HR-related message
- IT-related message

Respond in JSON format:
{{"hr": "...", "it": "..."}}

Message: "{user_input}"
""".strip()

            split_response = await call_llm(splitter_prompt, trace=trace, span_name="Message Splitter")
            print(f"[RouterNode] Split response: {split_response}")

            try:
                cleaned_split = sanitize_json(split_response)
                split = json.loads(cleaned_split)
                hr_msg = split.get("hr", user_input)
                it_msg = split.get("it", user_input)
            except Exception as e:
                print(f"[RouterNode] Split failed, fallback to original input: {e}")
                hr_msg = it_msg = user_input

        elif route == "hr":
            hr_msg = user_input
        elif route == "it":
            it_msg = user_input

        if span:
            span.end(output={"route": route, "hr_message": hr_msg, "it_message": it_msg})

        return {
            "input": user_input,
            "route": route,
            "hr_message": hr_msg,
            "it_message": it_msg
        }

    except Exception as e:
        print(f"[RouterNode] Error: {e}")
        if span:
            span.end(output={"error": str(e)}, level="ERROR")
        raise
