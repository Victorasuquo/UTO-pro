import streamlit as st
import openai
import os
from dotenv import load_dotenv
from agents import create_agent

load_dotenv()
openai.api_key = os.getenv("OPEN_AI")

def query_gpt(prompt):
    """
    Generic function to query GPT model
    - Takes a prompt as input
    - Uses GPT-4o-mini to generate responses for project requirement gathering
    - Returns the AI response as a string
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that asks relevant questions to gather project requirements."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

def generate_stories(context):
    """
    Generate 5 user stories based on the provided context
    - Takes project context as input
    - Uses a specific format for story generation
    - Returns formatted user stories with titles, user types, needs, criteria, and value
    """
    story_prompt = f"""Based on this context, generate 5 distinct user stories. 
    Format each story exactly like this:
    
    [STORY_TITLE]: <clear, concise theme or say or expression based on the context of the user story>
    [USER_TYPE]: <type of user this story is about>
    [USER_NEED]: <what the user wants to accomplish>
    [ACCEPTANCE_CRITERIA]: <key requirements for the story to be complete>
    [VALUE]: <business value or user benefit>

    Example format:
    [STORY_TITLE]: shop like a pro
    [USER_TYPE]: Online Shopper
    [USER_NEED]: As a shopper, I want to filter products by multiple criteria so that I can find exactly what I'm looking for
    [ACCEPTANCE_CRITERIA]: - Filter by price range, category, brand, ratings
    - Multiple filters can be applied simultaneously
    - Clear all filters with one click
    [VALUE]: Improved user experience and faster product discovery

    Use the exact tags as they will be parsed.
    Ensure each story is focused on a specific user need.

    Context:
    {context}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a user story generator. Create clear, specific, and actionable user stories following agile principles."},
            {"role": "user", "content": story_prompt}
        ],
        max_tokens=100,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

def parse_stories(stories_text):
    """
    Parse the AI-generated stories text into a structured format
    - Converts raw text into a list of dictionaries
    - Each dictionary contains story components (title, user type, need, etc.)
    - Handles empty lines and story separation
    """
    stories = []
    current_story = {}
    
    for line in stories_text.split('\n'):
        line = line.strip()
        if not line:
            if current_story:
                stories.append(current_story)
                current_story = {}
            continue
            
        for tag in ['STORY_TITLE', 'USER_TYPE', 'USER_NEED', 'ACCEPTANCE_CRITERIA', 'VALUE']:
            if line.startswith(f'[{tag}]:'):
                current_story[tag] = line.split(':', 1)[1].strip()
                break
    
    if current_story:
        stories.append(current_story)
    
    return stories

def query_specialized_agent(agent_type, context, selected_story):
    """
    Query specific agent (frontend/backend/design/product/ai) for development recommendations
    - Takes agent type, context, and selected story as inputs
    - Creates specialized agent using factory pattern
    - Returns agent-specific recommendations
    """
    agent = create_agent(agent_type)
    return agent.query(f"Story: {selected_story}\n\nContext: {context}")

def main():
    """
    Main application flow:
    1. Initial Setup:
        - Initializes session state variables for tracking progress
        - Sets up the UI title and description
    
    2. Question Phase:
        - Asks 3 questions to gather project requirements
        - Stores responses in context
    
    3. Story Generation:
        - Uses context to generate user stories
        - Parses and displays stories for selection
    
    4. Development Planning:
        - Once story is selected, generates specialized plans
        - Creates development plans using different agents (frontend, backend, etc.)
        - Displays plans with task tracking functionality
    
    5. Reset Functionality:
        - Allows starting a new project by resetting all state
    """
    st.title("Utom Work Lab")
    st.write("Utom assistant helps create comprehensive development plans using specialized agents.")

    if "questions_asked" not in st.session_state:
        st.session_state.questions_asked = 0

    if "context" not in st.session_state:
        st.session_state.context = ""

    if "stories" not in st.session_state:
        st.session_state.stories = None

    if "parsed_stories" not in st.session_state:
        st.session_state.parsed_stories = None

    if "selected_story" not in st.session_state:
        st.session_state.selected_story = None

    if "agent_responses" not in st.session_state:
        st.session_state.agent_responses = {}

    if "tasks" not in st.session_state:
        st.session_state.tasks = {}

    # Initial questions phase
    if st.session_state.questions_asked < 3 and not st.session_state.stories:
        if st.session_state.questions_asked == 0:
            question = "What kind of application do you want to build? Please provide a detailed description."
        else:
            flow_steps_prompt = (
                f"Based on this context, ask a clarifying question to better understand the feature:\n\n{st.session_state.context}"
            )
            question = query_gpt(flow_steps_prompt)

        st.write(f"Assistant: {question}")

        user_response = st.text_input("Your Response:", key=f"response_{st.session_state.questions_asked}")

        if st.button("Submit Response", key=f"submit_{st.session_state.questions_asked}"):
            st.session_state.context += f"Q{st.session_state.questions_asked + 1}: {question}\nA{st.session_state.questions_asked + 1}: {user_response}\n"
            st.session_state.questions_asked += 1

    # Generate stories
    elif not st.session_state.stories:
        with st.spinner("Generating user stories based on your inputs..."):
            st.session_state.stories = generate_stories(st.session_state.context)
            st.session_state.parsed_stories = parse_stories(st.session_state.stories)
        
    # Display stories and let user select one
    if st.session_state.parsed_stories and not st.session_state.selected_story:
        st.subheader("Select a User Story to Develop")
        
        # Create story selection dropdown
        story_titles = [story['STORY_TITLE'] for story in st.session_state.parsed_stories]
        selected_title = st.selectbox("Choose a user story:", story_titles)
        
        # Display selected story details
        if selected_title:
            selected_story = next(story for story in st.session_state.parsed_stories 
                                if story['STORY_TITLE'] == selected_title)
            
            with st.expander("User Story Details", expanded=True):
                st.markdown(f"### {selected_story['STORY_TITLE']}")
                st.markdown(f"**User Type:** {selected_story['USER_TYPE']}")
                st.markdown(f"**User Need:** {selected_story['USER_NEED']}")
                st.markdown(f"**Acceptance Criteria:** {selected_story['ACCEPTANCE_CRITERIA']}")
                st.markdown(f"**Business Value:** {selected_story['VALUE']}")
            
            if st.button("Develop This Story"):
                st.session_state.selected_story = selected_story

    # Generate specialized recommendations for selected story
    if st.session_state.selected_story and not st.session_state.agent_responses:
        st.write("Generating development plans...")
        
        agent_types = ['frontend', 'backend', 'design', 'product', 'ai']
        progress_bar = st.progress(0)
        
        for idx, agent_type in enumerate(agent_types):
            with st.spinner(f"Generating {agent_type.title()} plan..."):
                response = query_specialized_agent(
                    agent_type, 
                    st.session_state.context, 
                    st.session_state.selected_story['STORY_TITLE']
                )
                st.session_state.agent_responses[agent_type] = response
                st.session_state.tasks[agent_type] = extract_tasks(response)
                progress_bar.progress((idx + 1) / len(agent_types))

    # Display results with task tracking
    if st.session_state.agent_responses:
        st.subheader(f"Development Plans for: {st.session_state.selected_story['STORY_TITLE']}")
        
        for agent_type, response in st.session_state.agent_responses.items():
            with st.expander(f"{agent_type.upper()} Development Plan", expanded=True):
                st.markdown(response)
                
                # Task tracking section
                st.subheader("Tasks")
                for task in st.session_state.tasks[agent_type]:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(task)
                    with col2:
                        task_key = f"{agent_type}_{task}"
                        status = st.selectbox(
                            "Status",
                            ["Not Started", "In Progress", "Done"],
                            key=task_key
                        )

    if st.button("Start New Project", key="restart"):
        # Reset all session state variables explicitly
        st.session_state.questions_asked = 0
        st.session_state.context = ""
        st.session_state.stories = None
        st.session_state.parsed_stories = None
        st.session_state.selected_story = None
        st.session_state.agent_responses = {}
        st.session_state.tasks = {}
        # Force a rerun to refresh the page
        st.rerun()

def extract_tasks(response):
    """
    Extract individual tasks from agent responses
    - Parses response text to find bullet points
    - Converts them into a list of tasks
    - Used for task tracking functionality
    """
    # Simple task extraction - you might want to make this more sophisticated
    tasks = []
    lines = response.split('\n')
    for line in lines:
        if line.strip().startswith('- '):
            tasks.append(line.strip()[2:])
    return tasks

if __name__ == "__main__":
    main()