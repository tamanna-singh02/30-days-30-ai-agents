from typing import TypedDict
from agents.day_02_dynamic_prompt_synthesizer.schemas import PromptStrategy

class AgentState(TypedDict):
    user_input: str
    strategy: PromptStrategy
    final_prompt: str
    response: str

    
