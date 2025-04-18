from typing import List, Any, Literal, Set

from pydantic import BaseModel, Field
from pydantic_ai import Agent


class HopelessRomanticResponse(BaseModel):
    """
    Represents the response of a hopeless romantic to a given situation.
    """

    # positive_interpretations, romantic_potential, downplayed_negatives, key_breadcrumbs, and overall_summary.
    positive_interpretations: str
    romantic_potential: str
    downplayed_negatives: str
    key_breadcrumbs: str
    overall_summary: str


class RealistStoicResponse(BaseModel):
    """
    Represents the response of a practical stoic to a given situation.
    """

    # red_flags, identified_tactics, direct_interpretation, unanswered_questions, and overall_summary.
    red_flags: str
    identified_tactics: str
    direct_interpretation: str
    unanswered_questions: str
    overall_summary: str


class WiseMediatorResponse(BaseModel):
    """
    Represents the response of a wise mediator to a given situation.
    """

    analysis: str = Field(description="A detailed analysis of the situation")
