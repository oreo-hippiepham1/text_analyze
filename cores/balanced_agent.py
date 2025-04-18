from cores.prompts import BALANCED_MEDIATOR_PROMPT

from typing import List, Set, Literal, Dict, Any, Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from dotenv import load_dotenv

import streamlit as st
import os

# from dotenv import load_dotenv

# load_dotenv()
# Set the OpenAI API key via environment variable
os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]


class BalancedMediatorResponse(BaseModel):
    """
    Represents the response of a balanced mediator to a given situation.
    """

    # romantic_view_summary, stoic_view_summary, points_of_contention,  suggested_next_steps, and retrieved_resources
    romantic_view_summary: str = Field(description="Summary of the romantic view.")
    stoic_view_summary: str = Field(description="Summary of the stoic view.")
    points_of_contention: List[str] = Field(description="List of points of contention.")
    suggested_next_steps: str
    retrieved_resources: Optional[List[str]]


model = OpenAIModel(model_name="gpt-4o-mini")

balanced_mediator_agent = Agent(
    model=model,
    system_prompt=BALANCED_MEDIATOR_PROMPT,
    result_type=BalancedMediatorResponse,
)
