from typing import Optional
from pydantic import BaseModel

class AgentState(BaseModel):
    input: str
    route: Optional[str] = None
    hr_message: Optional[str] = None   
    it_message: Optional[str] = None   
    hr_response: Optional[str] = None
    it_response: Optional[str] = None
    final_response: Optional[str] = None