import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import openai
from openai import OpenAI
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPEN_AI")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "project_workflow"

# Initialize Flask app
app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# Initialize MongoDB client
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]

# Utility: Save data to the database
def save_to_db(collection_name, data):
    db = get_db()
    collection = db[collection_name]
    result = collection.insert_one(data)
    return str(result.inserted_id)

# Utility: Retrieve data by ID
def get_from_db(collection_name, doc_id):
    db = get_db()
    collection = db[collection_name]
    return collection.find_one({"_id": ObjectId(doc_id)})

# Initialize project state in the database
@app.route('/initialize', methods=['POST'])
def initialize_project():
    project_state = {
        "context": "",
        "questions_asked": 0,
        "stories": None,
        "parsed_stories": None,
        "selected_story": None,
        "user_flow": [],
        "agent_responses": {},
        "tasks": {}
    }
    project_id = save_to_db("project_states", project_state)
    return jsonify({"state_id": project_id}), 201

# Update project state in the database
def update_project_state(state_id, updates):
    db = get_db()
    collection = db["project_states"]
    collection.update_one({"_id": ObjectId(state_id)}, {"$set": updates})

# Query OpenAI GPT model
def query_gpt(prompt, model="gpt-4o-mini", max_tokens=500, temperature=0.7):

    """
    Query the OpenAI GPT model with a given prompt.
    Args:
        prompt (str): The input prompt for the GPT model.
    Returns:
        str: The generated response from the GPT model.
    """
    response = client.chat.completions.create(
        model=model,  # or another appropriate model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content

# Ask a question and update context
@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.json
    state_id = data.get("state_id")
    custom_question = data.get("custom_question")
    state = get_from_db("project_states", state_id)

    if state["questions_asked"] == 0:
        question = "What kind of application do you want to build? Please provide a detailed description."
    elif custom_question:
        question = custom_question
        
    else:
        prompt = f"Based on this context, ask a clarifying question:\n\n{state['context']}"
        question = query_gpt(prompt)

    answer = data.get("answer")
    context_update = f"Q{state['questions_asked'] + 1}: {question}\nA{state['questions_asked'] + 1}: {answer}\n"

    state["context"] += context_update
    state["questions_asked"] += 1
    state["user_flow"].append({"question": question, "answer": answer})

    update_project_state(state_id, state)
    return jsonify({"state_id": state_id, "question": question}), 200

# Generate user stories
@app.route('/generate_stories', methods=['POST'])
def generate_stories():
    data = request.json
    state_id = data.get("state_id")
    state = get_from_db("project_states", state_id)
    prompt = f"""Based on this context, generate 5 distinct user stories.
    Format each story exactly like this:

    [STORY_TITLE]: <creative theme or say or expression based on the context of the user story>
    [USER_TYPE]: <type of user this story is about>
    [USER_NEED]: <3-4 sentences what the user wants to accomplish>
    [ACCEPTANCE_CRITERIA]: <key requirements for the story to be complete>
    [VALUE]: <business value or user benefit>

    Context:
    {state['context']}"""

    stories = query_gpt(prompt, max_tokens=800)
    parsed_stories = parse_stories(stories)

    state["stories"] = stories
    state["parsed_stories"] = parsed_stories
    update_project_state(state_id, state)
    return jsonify({"state_id": state_id, "stories": parsed_stories}), 200

# Parse stories into structured format
def parse_stories(stories_text):
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

# Generate development plans
@app.route('/generate_development_plans', methods=['POST'])
def generate_development_plans():
    data = request.json
    state_id = data.get("state_id")
    state = get_from_db("project_states", state_id)
    agent_types = ['frontend', 'backend', 'design', 'product', 'ai']
    responses = {}
    tasks = {}

    for agent_type in agent_types:
        prompt = f"As a {agent_type} developer, what are the key components needed for the project?\n\nContext:\n{state['context']}"
        response = query_gpt(prompt)
        responses[agent_type] = response
        tasks[agent_type] = extract_tasks(response)

    state["agent_responses"] = responses
    state["tasks"] = tasks
    update_project_state(state_id, state)
    return jsonify({"state_id": state_id, "agent_responses": responses, "tasks": tasks}), 200

# Extract tasks from a response
def extract_tasks(response):
    tasks = []
    for line in response.split('\n'):
        line = line.strip()
        if line.startswith(('-', '*', '1.', '2.', '3.')) or ':' in line:
            tasks.append(line.lstrip('-*123456789. ').strip())
    return tasks

if __name__ == "__main__":
    app.run(debug=True)
