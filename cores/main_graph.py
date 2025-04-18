from cores.negative_agent import realist_stoic_agent, RealistStoicResponse
from cores.positive_agent import hopeless_romantic_agent, HopelessRomanticResponse
from cores.balanced_agent import balanced_mediator_agent, BalancedMediatorResponse

from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from typing import TypedDict, List, Dict, Any, Optional
import asyncio


# --- Main GraphMessage to be passed around ---
class GraphMessage(TypedDict):
    """
    Represents the main message passed around LangGraph
    """

    background_info: str = Field(
        description="Background information about the relationship"
    )
    negative_response: List[RealistStoicResponse]
    positive_response: List[HopelessRomanticResponse]
    balanced_response: List[BalancedMediatorResponse]
    error: Optional[str]


# --- Node 1.1:  Positive ---
async def positive_node(message: GraphMessage) -> dict:
    """
    Positive Node: Hopeless Romantic Agent
    """

    # Extract contextual info
    background = message["background_info"]

    # agent
    try:
        print(f"--- Hopeless Romantic ---")
        response = await hopeless_romantic_agent.run(background)
        response = response.data

        positive_response = message["positive_response"]
        positive_response.append(
            HopelessRomanticResponse(
                positive_interpretations=response.positive_interpretations,
                downplayed_negatives=response.downplayed_negatives,
                key_breadcrumbs=response.key_breadcrumbs,
                overall_summary=response.overall_summary,
            )
        )
        print(f"Completed")

        return {
            "positive_response": positive_response,
        }

    except Exception as e:
        print(f"Error in Hopeless Romantic Agent: {e}")
        return {"error": f"Error in Hopeless Romantic Agent: {e}"}


# --- Node 1.2:  Negative ---
async def negative_node(message: GraphMessage) -> dict:
    """
    Negative Node: Realist Stoic Agent
    """

    # Extract contextual info
    background = message["background_info"]

    # agent
    try:
        print(f"--- Realist Stoic ---")
        response = await realist_stoic_agent.run(background)
        response = response.data

        negative_response = message["negative_response"]
        negative_response.append(
            RealistStoicResponse(
                red_flags=response.red_flags,
                identified_tactics=response.identified_tactics,
                unanswered_questions=response.unanswered_questions,
                overall_summary=response.overall_summary,
            )
        )
        print(f"Completed")

        return {
            "negative_response": negative_response,
        }

    except Exception as e:
        print(f"Error in Realist Stoic Agent: {e}")
        return {"error": f"Error in Realist Stoic Agent: {e}"}


# --- Node 2: Balanced ---
async def balanced_node(message: GraphMessage) -> dict:
    """
    Balanced Node: Balanced Mediator Agent
    """
    # 1. Extract info from state message
    background = message["background_info"]
    if (not message["positive_response"]) or (not message["negative_response"]):
        return {"error": "No positive or negative response available."}

    # Get the latest responses
    positive_response: HopelessRomanticResponse = message["positive_response"][-1]
    negative_response: RealistStoicResponse = message["negative_response"][-1]

    # 2. format input
    stoic_input_str = f"""
        Overall Summary: {negative_response.overall_summary}
        Red Flags Identified: {negative_response.red_flags if hasattr(negative_response, 'red_flags') else 'N/A'}
        Identified Tactics: {negative_response.identified_tactics if hasattr(negative_response, 'identified_tactics') else 'N/A'}
        Unanswered Questions: {negative_response.unanswered_questions if hasattr(negative_response, 'unanswered_questions') else 'N/A'}
        """

    romantic_input_str = f"""
        Overall Summary: {positive_response.overall_summary}
        Positive Interpretations: {positive_response.positive_interpretations if hasattr(positive_response, 'positive_interpretations') else 'N/A'}
        Downplayed Negatives: {positive_response.downplayed_negatives if hasattr(positive_response, 'downplayed_negatives') else 'N/A'}
        Key Breadcrumbs: {positive_response.key_breadcrumbs if hasattr(positive_response, 'key_breadcrumbs') else 'N/A'}
        """

    combined_input = f"""
        Background: {background}
        Stoic Input: {stoic_input_str}
        Romantic Input: {romantic_input_str}
        """

    # 3. agent invocation
    try:
        print(f"--- Balanced Mediator ---")
        response = await balanced_mediator_agent.run(combined_input)
        response = response.data

        balanced_response = message["balanced_response"]
        balanced_response.append(
            BalancedMediatorResponse(
                romantic_view_summary=response.romantic_view_summary,
                stoic_view_summary=response.stoic_view_summary,
                points_of_contention=response.points_of_contention,
                suggested_next_steps=response.suggested_next_steps,
                retrieved_resources=response.retrieved_resources,
            )
        )
        print(f"Completed")

        return {
            "balanced_response": balanced_response,
        }

    except Exception as e:
        print(f"Error in Balanced Mediator Agent: {e}")
        return {"error": f"Error in Balanced Mediator Agent: {e}"}


def create_graph():
    """
    Creates the main graph for the LangGraph
    """
    # --- Main Graph ---
    builder = StateGraph(GraphMessage)

    # adding nodes
    builder.add_node(positive_node, "positive_node")
    builder.add_node(negative_node, "negative_node")
    builder.add_node(balanced_node, "balanced_node")
    # adding edges
    builder.add_edge(START, "positive_node")
    builder.add_edge("positive_node", "negative_node")
    builder.add_edge("negative_node", "balanced_node")
    builder.add_edge("balanced_node", END)
    # compilation
    graph = builder.compile()

    return graph


async def run_graph_async(intial_state):
    print("STARTING GRAPH")
    final_state_output = None

    app = create_graph()

    async for event in app.astream_events(intial_state):
        event_type = event["event"]
        event_name = event["name"]

        if event_type == "on_chain_start":
            print(f"\n >> {event_name}")

        if event_type == "on_chain_end" and event_name == "LangGraph":  # complete
            final_state_output = event["data"]

    return final_state_output


if __name__ == "__main__":
    # Example usage
    initial_state = {
        "background_info": "A couple is facing challenges in their relationship.",
        "negative_response": [],
        "positive_response": [],
        "balanced_response": [],
        "error": None,
    }

    final_state = asyncio.run(run_graph_async(initial_state))
    print(final_state)
