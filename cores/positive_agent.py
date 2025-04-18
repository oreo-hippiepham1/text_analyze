from cores.prompts import HOPELESS_ROMANTIC_PROMPT

from typing import List, Set, Literal, Dict, Any

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from dotenv import load_dotenv

load_dotenv()


class HopelessRomanticResponse(BaseModel):
    """
    Represents the response of a hopeless romantic to a given situation.
    """

    # positive_interpretations, romantic_potential, downplayed_negatives, key_breadcrumbs, and overall_summary.
    positive_interpretations: List[str] = Field(
        description="List of positive interpretations of the situation."
    )
    key_breadcrumbs: List[str] = Field(
        description="List of key breadcrumbs that are collected."
    )
    downplayed_negatives: List[str] = Field(description="List of downplayed negatives.")
    overall_summary: str = Field(
        description="Overall summary of the romantic potential of the situation."
    )


model = OpenAIModel(model_name="gpt-4o-mini")

hopeless_romantic_agent = Agent(
    model=model,
    system_prompt=HOPELESS_ROMANTIC_PROMPT,
    result_type=HopelessRomanticResponse,
)
