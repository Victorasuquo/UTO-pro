# Documentation for Python Script: Project Workflow Management

## Overview
This script implements a Flask web application that integrates OpenAI's GPT model and MongoDB for managing project workflows. It allows users to initialize a project state, ask questions regarding the project, generate user stories, and create development plans based on user inputs. The app interacts with MongoDB to store and retrieve project states and utilizes OpenAI's capabilities to assist in generating project-related content.

## Installation & Dependencies
To run this script, ensure you have Python installed along with the following dependencies:

- Flask
- pymongo
- python-dotenv
- openai

You can install the necessary packages using pip:

```bash
pip install Flask pymongo python-dotenv openai
```

Ensure you set the required environment variables in a `.env` file:

```
OPEN_AI=your_openai_api_key
MONGO_URI=your_mongodb_uri
```

## Usage
To run the script, simply execute it with Python. Make sure your MongoDB server is running and the environment variables are set correctly.

```bash
python your_script_name.py
```

### API Endpoints
- `/initialize`: POST request to create a new project state.
- `/ask_question`: POST request to ask a question about the project state.
- `/generate_stories`: POST request to generate user stories based on the project context.
- `/generate_development_plans`: POST request to create development plans based on user stories.

## Function/Class Documentation

### `get_db()`
- **Purpose**: Initializes and returns a connection to the MongoDB database.
- **Returns**: A MongoDB database object.

### `save_to_db(collection_name, data)`
- **Purpose**: Inserts the provided data into a specified MongoDB collection.
- **Input Parameters**:
  - `collection_name` (str): The name of the collection where data should be saved.
  - `data` (dict): The data to be saved in the collection.
- **Returns**: `str`: The ID of the inserted document.

### `get_from_db(collection_name, doc_id)`
- **Purpose**: Retrieves a document from a specified MongoDB collection by its ID.
- **Input Parameters**:
  - `collection_name` (str): The name of the collection to fetch data from.
  - `doc_id` (str): The ID of the document to retrieve.
- **Returns**: `dict` or `None`: The retrieved document or None if not found.

### `initialize_project()`
- **Purpose**: Creates and initializes a new project state in the database.
- **Returns**: JSON response containing the `state_id` of the new project state.

### `update_project_state(state_id, updates)`
- **Purpose**: Updates the project state with new information.
- **Input Parameters**:
  - `state_id` (str): ID of the project state to update.
  - `updates` (dict): The updates to apply to the project state.

### `query_gpt(prompt, model="gpt-4o-mini", max_tokens=500, temperature=0.7)`
- **Purpose**: Queries the OpenAI GPT model with a specified prompt.
- **Input Parameters**:
  - `prompt` (str): The input prompt for the GPT model.
  - `model` (str, optional): The model name to use for querying. Default is `"gpt-4o-mini"`.
  - `max_tokens` (int, optional): Maximum number of tokens in the response. Default is 500.
  - `temperature` (float, optional): Sampling temperature for randomness. Default is 0.7.
- **Returns**: `str`: The generated response from the GPT model.

### `ask_question()`
- **Purpose**: Handles a question-asking request from the user and updates the project state accordingly.
- **Returns**: JSON response with the current `state_id` and the question posed.

### `generate_stories()`
- **Purpose**: Generates user stories based on the project context.
- **Returns**: JSON response with the `state_id` and the generated user stories.

### `parse_stories(stories_text)`
- **Purpose**: Parses the generated user stories text into a structured format.
- **Input Parameters**:
  - `stories_text` (str): Raw text containing user stories.
- **Returns**: `list` of `dict`: A list of parsed user stories structured with keys like STORY_TITLE, USER_TYPE, USER_NEED, etc.

### `generate_development_plans()`
- **Purpose**: Generates development plans based on user responses.
- **Returns**: JSON response with the `state_id`, agent responses, and tasks.

### `extract_tasks(response)`
- **Purpose**: Extracts tasks from the response text.
- **Input Parameters**:
  - `response` (str): The response text containing tasks.
- **Returns**: `list`: A list of extracted tasks.

## Code Walkthrough
1. **Environment Setup**: The script starts by loading environment variables and initializing Flask and OpenAI clients.
2. **Database Functions**: Functions for connecting to MongoDB and performing CRUD operations (like saving and retrieving project states) are defined.
3. **API Endpoint Definitions**: The Flask app defines routes for initializing projects, asking questions, generating user stories, and creating development plans.
4. **GPT Querying**: Functions for constructing prompts and processing responses from the OpenAI API are included, allowing for dynamic interaction based on user inputs.

## Example Output
For the `/initialize` endpoint:

Request:
```json
POST /initialize
```

Response:
```json
{
  "state_id": "605c72a8bcf86f3f98ec2e2d"
}
```

For the `/ask_question` endpoint:
Request:
```json
POST /ask_question
{
  "state_id": "605c72a8bcf86f3f98ec2e2d",
  "answer": "A task management app."
}
```
Response:
```json
{
  "state_id": "605c72a8bcf86f3f98ec2e2d",
  "question": "What kind of application do you want to build? Please provide a detailed description."
}
```

## Error Handling
- The script does not explicitly handle HTTP errors, but MongoDB operations implicitly manage potential issues such as connection errors or invalid queries.
- In the `ask_question` endpoint, if the project state ID provided does not exist, there is no current error handling, which could be a point for improvement to return a proper error response (like HTTP 404).

This documentation provides a structured overview of the script, clarifying its purpose, usage, and function while offering insights into possible improvements and output expectations.