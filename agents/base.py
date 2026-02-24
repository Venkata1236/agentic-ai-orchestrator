"""
Shared base components for all agents
"""
import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

# Global model client
model_client = OpenAIChatCompletionClient(
    model="gpt-3.5-turbo",
    api_key=os.environ["OPENAI_API_KEY"]
)

class ActionItem(BaseModel):
    id: str = Field(..., description="A1, A2")
    description: str = Field(...)
    owner: str = Field(...)
    deadline: str = Field(...)
    dependencies: List[str] = Field(default_factory=list)
    priority: str = Field(...)

class RiskItem(BaseModel):
    id: str = Field(..., description="R1, R2")
    type: str = Field(...)  # risk, open_question, assumption
    description: str = Field(...)
    impact: str = Field(...)
    mitigation: str = Field(...)
