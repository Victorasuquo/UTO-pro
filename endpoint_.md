# Project Workflow Automation API Documentation

This document provides a detailed explanation of the Python script which implements a Flask-based API for managing a project workflow. The API integrates with MongoDB for data persistence and uses OpenAI's GPT model to generate responses and user stories.

---

## Table of Contents

- [Overview](#overview)
- [Installation & Dependencies](#installation--dependencies)
- [Usage](#usage)
- [Endpoints and Functionality](#endpoints-and-functionality)
  - [Database Utilities](#database-utilities)
  - [OpenAI GPT Integration](#openai-gpt-integration)
  - [API Endpoints](#api-endpoints)
- [Code Walkthrough](#code-walkthrough)
- [Example Output](#example-output)
- [Error Handling](#error-handling)

---

## Overview

This script creates a web service that assists with project workflow management. It provides endpoints to initialize a project state, ask user-related questions, generate user stories, and create development plans based on responses from an OpenAI GPT model. It leverages MongoDB for storing the project state and integrates environment variables for configuration purposes.

---

## Installation & Dependencies

### Required Dependencies

- Python 3.7+
- Flask
- pymongo
- python-dotenv
- openai
- bson

### Installation Steps

1. Install Python 3.7 or higher if not already installed.
2. Install the required Python packages using pip:

   ```bash
   pip install Flask pymongo python-dotenv openai bson
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root.
   - Include the following keys and set appropriate values:

     ```
     OPEN_AI=<your_openai_api_key>
     OPENAI_API_KEY=<your_openai_api_key>
     MONGO_URI=<your_mongodb_connection_uri>
     ```

---

## Usage

1. **Run the Flask Application**

   Execute the script to start the Flask server:

   ```bash
   python <script_filename>.py
   ```

   The server will start in debug mode on the default port (5000).

2. **Access API Endpoints**

   Use any REST API client (like Postman) or curl to interact with the API endpoints detailed below.

---

## Endpoints and Functionality

### Database Utilities

The script defines several utility functions to interact with MongoDB:

- **get_db()**  
  Connects to the MongoDB using the URI from environment variables and selects the `project_workflow` database.

- **save_to_db(collection_name, data)**  
  Saves a document (`data`) to the specified collection (`collection_name`) and returns the inserted document's ID as a string.
  
  **Parameters:**
  - collection_name (str): Name of the MongoDB collection.
  - data (dict): Dictionary containing the data to be saved.

  **Returns:**  
  - str: Inserted document ID.

- **get_from_db(collection_name, doc_id)**  
  Retrieves a document from the specified collection using its ObjectId.

  **Parameters:**
  - collection_name (str): Name of the MongoDB collection.
  - doc_id (str): Document ID to search for.

  **Returns:**  
  - dict: The document corresponding to the given ID.

- **update_project_state(state_id, updates)**  
  Updates the project state in the `project_states` collection with the provided changes.

  **Parameters:**
  - state_id (str): The ID of the project state to update.
  - updates (dict): A dictionary of fields to update in the project state.

---

### OpenAI GPT Integration

- **query_gpt(prompt, model="gpt-4o-mini", max_tokens=500, temperature=0.7)**  
  This function queries the OpenAI GPT model with a given prompt.

  **Parameters:**
  - prompt (str): The input prompt for the GPT model.
  - model (str, optional): The model to use (default is "gpt-4o-mini").
  - max_tokens (int, optional): Maximum number of tokens for the response (default is 500).
  - temperature (float, optional): The sampling temperature (default is 0.7).

  **Returns:**  
  - str: The generated response from the GPT model.

- **parse_stories(stories_text)**  
  Parses textual user stories generated by GPT into a structured list of stories. Each story includes the keys:
  - STORY_TITLE
  - USER_TYPE
  - USER_NEED
  - ACCEPTANCE_CRITERIA
  - VALUE

  **Parameters:**
  - stories_text (str): The raw text containing multiple stories.

  **Returns:**  
  - list: A list of dictionaries, each representing a parsed user story.

- **extract_tasks(response)**  
  Extracts individual tasks from a GPT response. It splits the response based on common list or key-value formatting.

  **Parameters:**
  - response (str): The raw response text from GPT.

  **Returns:**  
  - list: A list of individual tasks as strings.

---

### API Endpoints

#### 1. Initialize Project State

- **Endpoint:** `/initialize`
- **Method:** POST
- **Description:**  
  Initializes a new project state in the database with default values.
  
- **Response:**
  - JSON containing:
    - `state_id`: The MongoDB ID of the new project state.
  
- **HTTP Status Code:** 201

#### 2. Ask a Question

- **Endpoint:** `/ask_question`
- **Method:** POST
- **Description:**  
  Accepts a question or answer based on the project state�s current progress. It updates the state with user input and queries GPT for clarifying questions if needed.
  
- **Input JSON:**
  - `state_id` (str): The project state identifier.
  - `custom_question` (str, optional): Custom question input.
  - `answer` (str): The user's answer to the question.
  
- **Response:**
  - JSON containing:
    - `state_id`: The updated state ID.
    - `question`: The question that was either generated or provided.
  
- **HTTP Status Code:** 200

#### 3. Generate User Stories

- **Endpoint:** `/generate_stories`
- **Method:** POST
- **Description:**  
  Uses the current project context to generate 5 distinct user stories via GPT, then parses and saves them in the project state.
  
- **Input JSON:**
  - `state_id` (str): The project state identifier.
  
- **Response:**
  - JSON containing:
    - `state_id`: The project state ID.
    - `stories`: A structured list of parsed user stories (each with title, type, need, acceptance criteria, and value).
  
- **HTTP Status Code:** 200

#### 4. Generate Development Plans

- **Endpoint:** `/generate_development_plans`
- **Method:** POST
- **Description:**  
  Queries GPT for development plans tailored for different agent types (frontend, backend, design, product, ai). The responses and extracted tasks are stored in the project state.
  
- **Input JSON:**
  - `state_id` (str): The project state identifier.
  
- **Response:**
  - JSON containing:
    - `state_id`: The project state ID.
    - `agent_responses`: A dictionary mapping agent types to their GPT responses.
    - `tasks`: A dictionary mapping agent types to a list of extracted tasks.
  
- **HTTP Status Code:** 200

---

## Code Walkthrough

1. **Environment Setup**  
   - Load environment variables using `dotenv` to retrieve API keys and MongoDB URI.
   - Set the API key for OpenAI.
   
2. **Flask App Initialization**  
   - Create a Flask application instance.
   
3. **MongoDB Client Initialization**  
   - Define `get_db()` to establish a connection with the MongoDB database named `project_workflow`.
   
4. **Database Helper Functions**  
   - `save_to_db()`: Inserts documents into a designated collection.
   - `get_from_db()`: Retrieves a document by its ID.
   - `update_project_state()`: Updates a project state document.
   
5. **OpenAI GPT Query Function**  
   - `query_gpt()`: Forms a prompt, sends a request to the OpenAI API, and returns the generated response.
   
6. **API Endpoints**  
   - `/initialize`: Creates and saves a default project state.
   - `/ask_question`: Depending on the project state, either asks an initial question, uses a custom question, or generates a clarifying question with GPT. It then updates the context with the question and the user�s answer.
   - `/generate_stories`: Uses the project context to generate user stories via GPT, then parses and updates the state.
   - `/generate_development_plans`: Iterates over a set of predefined agent types, queries the GPT model for each, extracts tasks, and updates the state.
   
7. **Utility Functions for Parsing**  
   - `parse_stories()`: Converts the GPT raw text for user stories into a structured list.
   - `extract_tasks()`: Extracts task items from GPT responses based on common formatting patterns.

8. **Running the Application**  
   - The Flask application runs in debug mode when the script is executed directly.

---

## Example Output

### Initializing a Project

Request (POST to `/initialize`):

```json
{}
```

Response:

```json
{
  "state_id": "64a1f8f5f8ab3c0012345678"
}
```

### Asking a Question

Request (POST to `/ask_question`):

```json
{
  "state_id": "64a1f8f5f8ab3c0012345678",
  "custom_question": "Could you explain the main functionality of the application?",
  "answer": "The application manages user stories and development plans."
}
```

Response:

```json
{
  "state_id": "64a1f8f5f8ab3c0012345678",
  "question": "Could you explain the main functionality of the application?"
}
```

### Generating User Stories

Request (POST to `/generate_stories`):

```json
{
  "state_id": "64a1f8f5f8ab3c0012345678"
}
```

Response (simplified):

```json
{
  "state_id": "64a1f8f5f8ab3c0012345678",
  "stories": [
    {
      "STORY_TITLE": "User Registration",
      "USER_TYPE": "New User",
      "USER_NEED": "To register for access to the platform.",
      "ACCEPTANCE_CRITERIA": "User can create an account with a valid email.",
      "VALUE": "Improves user engagement."
    },
    ...
  ]
}
```

### Generating Development Plans

Request (POST to `/generate_development_plans`):

```json
{
  "state_id": "64a1f8f5f8ab3c0012345678"
}
```

Response (simplified):

```json
{
  "state_id": "64a1f8f5f8ab3c0012345678",
  "agent_responses": {
    "frontend": "Response from GPT for frontend tasks...",
    "backend": "Response from GPT for backend tasks...",
    "design": "Response from GPT for design tasks...",
    "product": "Response from GPT for product tasks...",
    "ai": "Response from GPT for AI tasks..."
  },
  "tasks": {
    "frontend": [
      "Design and implement UI components",
      "Integrate API endpoints"
    ],
    "backend": [
      "Develop REST APIs",
      "Implement database models"
    ],
    ...
  }
}
```

---

## Error Handling

- The code does not employ extensive try/except blocks for error handling.
- Relying on Flask�s default error handling, failed database connections or invalid ObjectId conversions might result in unhandled exceptions.
- The script assumes that the incoming request JSON contains the necessary keys (`state_id`, `answer`, etc.). Robust production code would include validation and exception handling to manage missing or malformed data.
- The logic in `ask_question()` handles different cases based on the number of questions asked and the presence of a custom question.

---

This documentation should provide a clear understanding of the script, how to set it up, and how to interact with its endpoints. For further customization or error handling improvements, consider adding input validations and try/except blocks around critical operations.