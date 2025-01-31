# Project Workflow Documentation

This documentation provides a detailed overview of the code and instructions on how to use it. The code is a Flask application that integrates with MongoDB and OpenAI's GPT model to manage a project workflow.

![API calls](image.png)
*Figure 1: API calls*
## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Endpoints](#endpoints)
7. [Code Explanation](#code-explanation)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

This Flask application is designed to manage a project workflow by interacting with a MongoDB database and OpenAI's GPT model. It provides endpoints to initialize a project, ask questions, generate user stories, and generate development plans.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- MongoDB instance running
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory of the project.
2. Add the following environment variables to the `.env` file:

```env
OPEN_AI=your_openai_api_key
MONGO_URI=your_mongodb_uri
```

## Usage

1. Start the Flask application:

```bash
python app.py
```

2. The application will be running on `http://127.0.0.1:5000/`.

## Endpoints

### Initialize Project

- **URL:** `/initialize`
- **Method:** `POST`
- **Description:** Initializes a new project state in the database.
- **Response:**

```json
{
  "state_id": "project_id"
}
```

### Ask Question

- **URL:** `/ask_question`
- **Method:** `POST`
- **Description:** Asks a question and updates the project context.
- **Request Body:**

```json
{
  "state_id": "project_id",
  "custom_question": "optional_custom_question",
  "answer": "user_answer"
}
```

- **Response:**

```json
{
  "state_id": "project_id",
  "question": "generated_question"
}
```

### Generate User Stories

- **URL:** `/generate_stories`
- **Method:** `POST`
- **Description:** Generates user stories based on the project context.
- **Request Body:**

```json
{
  "state_id": "project_id"
}
```

- **Response:**

```json
{
  "state_id": "project_id",
  "stories": "generated_stories"
}
```

### Generate Development Plans

- **URL:** `/generate_development_plans`
- **Method:** `POST`
- **Description:** Generates development plans based on the project context.
- **Request Body:**

```json
{
  "state_id": "project_id"
}
```

- **Response:**

```json
{
  "state_id": "project_id",
  "agent_responses": "generated_responses",
  "tasks": "generated_tasks"
}
```

## Code Explanation

### Imports

```python
import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify
```

### Load Environment Variables

```python
load_dotenv()
openai.api_key = os.getenv("OPEN_AI")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "project_workflow"
```

### Initialize Flask App

```python
app = Flask(__name__)
```

### Initialize MongoDB Client

```python
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]
```

### Utility Functions

#### Save Data to the Database

```python
def save_to_db(collection_name, data):
    db = get_db()
    collection = db[collection_name]
    result = collection.insert_one(data)
    return str(result.inserted_id)
```

#### Retrieve Data by ID

```python
def get_from_db(collection_name, doc_id):
    db = get_db()
    collection = db[collection_name]
    return collection.find_one({"_id": ObjectId(doc_id)})
```

### Initialize Project State

```python
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
```

### Update Project State

```python
def update_project_state(state_id, updates):
    db = get_db()
    collection = db["project_states"]
    collection.update_one({"_id": ObjectId(state_id)}, {"$set": updates})
```

### Query OpenAI GPT Model

```python
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
```

### Ask a Question and Update Context

```python
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
```

### Generate User Stories

```python
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
```

### Parse Stories into Structured Format

```python
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
```

### Generate Development Plans

```python
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
```

### Extract Tasks from a Response

```python
def extract_tasks(response):
    tasks = []
    for line in response.split('\n'):
        line = line.strip()
        if line.startswith(('-', '*', '1.', '2.', '3.')) or ':' in line:
            tasks.append(line.lstrip('-*123456789. ').strip())
    return tasks
```

### Run the Application

```python
if __name__ == "__main__":
    app.run(debug=True)
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.