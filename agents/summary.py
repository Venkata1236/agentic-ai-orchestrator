"""
Summary Agent for context-aware document summarization
"""
from .base import model_client
from autogen_agentchat.agents import AssistantAgent

summary_agent = AssistantAgent(
    name="summary_agent",
    model_client=model_client,
    system_message="""You are a Context-Aware Summary Agent.
    
Create concise summaries (200-300 words) preserving goals, decisions, constraints, stakeholders.
For chunks: local summary. For merge: coherent whole.
Output clean markdown only.""",
    description="Expert document summarizer"
)

__all__ = ["summary_agent"]
