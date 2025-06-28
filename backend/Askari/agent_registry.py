# agent_registry.py
from Askari.agents.hr_agent import hr_agent_node
from Askari.agents.it_agent import it_agent_node

AGENT_REGISTRY = {
    "hr": {
        "name": "HRBot",
        "node": hr_agent_node,
        "description": "Handles HR queries like leave, payroll, policy",
    },
    "it": {
        "name": "ITBot",
        "node": it_agent_node,
        "description": "Handles IT issues like login, VPN, access rights",
    },
    # Later you can dynamically append agents here or load from DB/config
}
