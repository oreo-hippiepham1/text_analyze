import streamlit as st
import time  # Used for placeholder delay

from cores.main_graph import create_graph, GraphMessage
import asyncio

# --- Placeholder Data Structures (Mimicking Pydantic models for display) ---
# In your actual app, you'd import your Pydantic models.
# These are just dicts for the placeholder function.


# --- Initialize Session State ---
def initialize_state():
    """Initializes Streamlit session state variables if they don't exist."""
    if "stage" not in st.session_state:
        st.session_state.stage = "input"  # Stages: 'input', 'analysis'
    if "background_info" not in st.session_state:
        st.session_state.background_info = ""
    if "conversation" not in st.session_state:
        # Stores list of {'sender': str, 'message': str}
        st.session_state.conversation = []
    if "analysis_results" not in st.session_state:
        # Stores the dict returned by the analysis function/graph
        st.session_state.analysis_results = None
    if "sender_choice" not in st.session_state:
        st.session_state.sender_choice = "Me"  # Default sender
    if "message_text" not in st.session_state:
        st.session_state.message_text = ""


# --- Placeholder for Agent Invocation ---
# Replace this with your actual LangGraph invocation logic.
# This function simulates the delay and returns dummy structured data.
def run_analysis_placeholder(background, conversation_list):
    """
    Placeholder function to simulate running the LangGraph analysis.
    In a real app, this would call your graph.ainvoke() or graph.stream().
    """
    print("Placeholder: Simulating analysis run...")
    print("Background:", background)
    print("Conversation:", conversation_list)

    # Simulate network/processing delay
    time.sleep(3)

    # Return dummy results matching the expected structure from GraphMessage
    # (Using dicts here instead of actual Pydantic models for simplicity in placeholder)
    return {
        "positive_response": [
            {
                "overall_summary": "Looks like true love! They seem really into you based on the subtle cues.",
                "positive_interpretations": [
                    "'See you soon' definitely means they miss you and can't wait!",
                    "The heart emoji is a clear sign of affection.",
                ],
                "key_breadcrumbs": [
                    "They remembered your favorite coffee order!",
                    "Replied within 5 minutes.",
                ],
                "downplayed_negatives": [
                    "The 'maybe' about Friday just means they're busy but trying to make it work."
                ],
                "romantic_potential": "Very High",
            }
        ],
        "negative_response": [
            {
                "overall_summary": "Several inconsistencies and potential red flags detected. Proceed with caution.",
                "red_flags": [
                    "Avoids direct questions about commitment ('Let's just see how it goes').",
                    "Cancels plans last minute with vague excuses.",
                    "Takes hours or days to respond sometimes.",
                ],
                "identified_tactics": [
                    "Possible gaslighting when questioned about past statements.",
                    "Uses guilt-trips ('You know how stressed I am').",
                ],
                "unanswered_questions": [
                    "What is the actual status of this relationship?",
                    "Are they seeing other people?",
                ],
            }
        ],
        "balanced_response": [
            {
                "romantic_view_summary": "The optimistic perspective highlights frequent communication and shared jokes as signs of connection.",
                "stoic_view_summary": "The critical perspective points to a lack of clear commitment and potentially manipulative language.",
                "points_of_contention": [
                    "Interpretation of vague future plans.",
                    "Significance of response times.",
                    "Whether excuses for cancelled plans are valid.",
                ],
                "suggested_next_steps": "Consider having an open conversation about relationship expectations. Observe if actions consistently match words over the next few weeks.",
                "retrieved_resources": None,  # Example: ["Link to article on 'breadcrumbing'"] if you implement search
            }
        ],
        "error": None,  # Set to an error message string if something goes wrong
    }


def run_graph_analysis(background: str, conversation: list) -> dict:
    """
    Compiles the graph and runs it with the provided input.
    Handles the async graph invocation.
    """
    try:
        graph = create_graph()

        # Prepare the initial state for the graph invocation
        graph_input = GraphMessage(
            background_info=background,
            # conversation_data=conversation, # Include if state/nodes use it
            positive_response=[],
            negative_response=[],
            balanced_response=[],
            error=None,
        )

        print("Invoking graph...")
        # Run the async graph.ainvoke() function using asyncio.run()
        # This blocks until the async function completes.
        final_state = asyncio.run(graph.ainvoke(graph_input))
        print("Graph invocation complete.")
        return final_state

    except Exception as e:
        print(f"Error during graph creation or invocation: {e}")
        import traceback

        traceback.print_exc()
        # Return an error structure consistent with GraphMessage
        return {"error": f"Failed to run graph analysis: {e}"}


# --- Streamlit App UI ---

st.set_page_config(layout="centered")  # Use "wide" if you prefer more space
st.title("💬 Conversation Analyzer Test UI")

# Initialize state variables
initialize_state()

# --- Stage 1: Input Collection ---
if st.session_state.stage == "input":
    st.header("Step 1: Provide Context and Conversation")
    st.caption("Enter the background details and then add messages one by one.")

    # --- Background Input ---
    st.subheader("Background Information")
    st.session_state.background_info = st.text_area(
        "Enter context about the relationship, the people involved, the situation, etc.",
        value=st.session_state.background_info,
        height=150,
        key="bg_info_input",  # Unique key
    )

    # --- Conversation Input ---
    st.subheader("Add Conversation Messages")

    # Use columns for layout
    col1, col2 = st.columns([1, 3])

    with col1:
        # Radio button for sender selection
        st.session_state.sender_choice = st.radio(
            "Sender:",
            ["Me", "SO"],
            key="sender_radio",
            index=["Me", "SO"].index(
                st.session_state.sender_choice
            ),  # Maintain selection
        )

    with col2:
        # Text input for the message
        st.session_state.message_text = st.text_input(
            "Enter message:",
            value=st.session_state.message_text,
            key="message_text_input",  # Unique key
        )

    # Button to add the message to the conversation list
    if st.button("Add Message", key="add_msg_button"):
        if st.session_state.message_text:
            st.session_state.conversation.append(
                {
                    "sender": st.session_state.sender_choice,
                    "message": st.session_state.message_text,
                }
            )
            # Clear the message input field after adding
            st.session_state.message_text = ""
            # Reset sender to default or keep last? Let's reset for now.
            # st.session_state.sender_choice = "Person A"
            st.rerun()  # Rerun to update display and clear input visually
        else:
            st.warning("Please enter a message text.")

    # --- Display Current Conversation ---
    st.subheader("Current Conversation Log")
    if not st.session_state.conversation:
        st.caption("No messages added yet.")
    else:
        # Display conversation in a scrollable box
        with st.container(height=300):
            for i, msg in enumerate(st.session_state.conversation):
                if msg["sender"] == "Me":
                    st.markdown(
                        f"<div style='text-align: right; margin-bottom: 5px;'><span style='background-color: #3A59D1; color: #F1EFEC; padding: 5px 10px; border-radius: 10px;'>{msg['message']}</span></div>",
                        unsafe_allow_html=True,
                    )
                else:  # SO
                    st.markdown(
                        f"<div style='text-align: left; margin-bottom: 5px;'><span style='background-color: #F1EFEC; color: #030303; padding: 5px 10px; border-radius: 10px;'>{msg['message']}</span></div>",
                        unsafe_allow_html=True,
                    )

    st.divider()

    # --- Proceed Button ---
    if st.button("✅ Done - Proceed to Analysis", key="proceed_button"):
        if not st.session_state.background_info:
            st.warning("Please provide some background information before proceeding.")
        elif not st.session_state.conversation:
            st.warning(
                "Please add at least one conversation message before proceeding."
            )
        else:
            # Move to the next stage
            st.session_state.stage = "analysis"
            st.rerun()  # Rerun script to render the analysis stage

# --- Stage 2: Analysis ---
elif st.session_state.stage == "analysis":
    st.header("Step 2: Review Input & Run Analysis")

    # --- Display Collected Info ---
    st.subheader("Collected Information")
    with st.expander("Show Background and Conversation Log", expanded=False):
        st.markdown("**Background:**")
        st.markdown(
            st.session_state.background_info
            if st.session_state.background_info
            else "_No background provided._"
        )
        st.markdown("**Conversation Log:**")
        if not st.session_state.conversation:
            st.caption("No messages were added.")
        else:
            for msg in st.session_state.conversation:
                st.markdown(f"**{msg['sender']}:** {msg['message']}")

    st.divider()

    # --- Run Analysis Button ---
    if st.button("🚀 Run Analysis", key="run_analysis_button"):
        with st.spinner("🧠 Running analysis... Please wait."):
            # calling the graph
            st.session_state.analysis_results = run_graph_analysis(
                st.session_state.background_info, st.session_state.conversation
            )
        st.success("✅ Analysis Complete!")
        st.rerun()  # Rerun to display results below the button

    # --- Display Analysis Results ---
    if st.session_state.analysis_results:
        st.subheader("Analysis Results")

        results = st.session_state.analysis_results
        # Check for errors first
        if results.get("error"):
            st.error(f"⚠️ An error occurred during analysis: {results['error']}")
        else:
            # Use tabs for displaying the different perspectives
            tab1, tab2, tab3 = st.tabs(
                [
                    "💖 Hopeless Romantic View",
                    "🧐 Practical Stoic View",
                    "⚖️ Balanced Mediator View",
                ]
            )

            # --- Romantic Tab ---
            with tab1:
                if results.get("positive_response"):
                    # Assuming the list contains one response object (dict in this placeholder)
                    res = results["positive_response"][0]
                    # st.json(res)
                    # st.markdown(res.downplayed_negatives)
                    st.markdown(f"**Overall Summary:** {res.overall_summary}")
                    st.markdown("**Positive Interpretations Highlighted:**")
                    if res.positive_interpretations:
                        for item in res.positive_interpretations:
                            st.markdown(f"- {item}")
                    else:
                        st.caption("_None noted._")
                    st.markdown("**Key 'Breadcrumbs' Focused On:**")
                    if res.key_breadcrumbs:
                        for item in res.key_breadcrumbs:
                            st.markdown(f"- {item}")
                    else:
                        st.caption("_None noted._")
                    st.markdown("**Rationalized/Downplayed Negatives:**")
                    if res.downplayed_negatives:
                        for item in res.downplayed_negatives:
                            st.markdown(f"- {item}")
                    else:
                        st.caption("_None noted._")

                else:
                    st.warning("No data available for the Hopeless Romantic analysis.")

            # --- Stoic Tab ---
            with tab2:
                if results.get("negative_response"):
                    res = results["negative_response"][0]
                    st.markdown(f"**Overall Summary:** {res.overall_summary}")
                    st.markdown("**Potential Red Flags Identified:**")
                    if res.red_flags:
                        for item in res.red_flags:
                            st.markdown(f"- {item}")
                    else:
                        st.caption("_None noted._")
                    st.markdown("**Potential Manipulation Tactics Identified:**")
                    if res.identified_tactics:
                        for item in res.identified_tactics:
                            st.markdown(f"- {item}")
                    else:
                        st.caption("_None noted._")
                    st.markdown("**Unanswered Questions / Lack of Clarity:**")
                    if res.unanswered_questions:
                        for item in res.unanswered_questions:
                            st.markdown(f"- {item}")
                    else:
                        st.caption("_None noted._")
                else:
                    st.warning("No data available for the Practical Stoic analysis.")

            # --- Mediator Tab ---
            with tab3:
                if results.get("balanced_response"):
                    res = results["balanced_response"][0]
                    st.markdown(
                        f"**Summary of Romantic View:** {res.romantic_view_summary}"
                    )
                    st.markdown(f"**Summary of Stoic View:** {res.stoic_view_summary}")
                    st.markdown("**Key Points of Contention / Disagreement:**")
                    if res.points_of_contention:
                        for item in res.points_of_contention:
                            st.markdown(f"- {item}")
                    else:
                        st.caption("_None noted._")
                    st.markdown(
                        f"**Suggested Next Steps / Reflection Points:** {res.suggested_next_steps}"
                    )
                    # Display retrieved resources if implemented
                    if res.retrieved_resources:
                        st.markdown("**Related Resources Found:**")
                        for resource in res.retrieved_resources:
                            st.markdown(f"- {resource}")  # Adjust formatting as needed
                else:
                    st.warning("No data available for the Balanced Mediator analysis.")

    st.divider()

    # --- Button to Start Over ---
    if st.button("🔄 Start New Analysis", key="reset_button"):
        # Clear all relevant session state keys to reset the app
        keys_to_clear = [
            "stage",
            "background_info",
            "conversation",
            "analysis_results",
            "sender_choice",
            "message_text",
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        # Rerun the script to go back to the initial state
        st.rerun()
