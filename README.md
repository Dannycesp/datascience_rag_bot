# Data Science RAG Bot

Understanding data science concepts can be challenging, especially for beginners. With the vast amount of information available, finding clear and concise explanations can be overwhelming.

The **Data Science Assistant** provides a conversational AI that helps users understand various data science concepts and terms, making learning more accessible and engaging.

This project was implemented as part of **LLM Zoomcamp**.

## Project Overview

The Data Science Assistant is a Retrieval-Augmented Generation (RAG) application designed to assist users with understanding data science concepts.

**Main use cases include:**

- **Concept Explanation:** Providing clear explanations of data science terms and concepts.
- **Instructional Support:** Offering guidance on how to perform specific data science tasks or techniques.
- **Conversational Interaction:** Enabling users to interact naturally and ask questions without searching through dense textbooks or online resources.

## Dataset

The dataset used in this project contains over 1,000 data science concepts, including questions, instructions, and responses about various data science terms.

- **Source:** [1000+ Data Science Concepts](https://www.kaggle.com/datasets/hserdaraltan/1000-data-science-concepts) on Kaggle.
- **Contents:** Questions, instructions, and detailed explanations of data science concepts and terms.

The dataset serves as the foundation for the Data Science Assistant's ability to provide accurate and helpful responses.

**You can find the data prepared for use in the RAG application in `data/data.csv`.**

## Technologies

- **Python 3.12**
- **Docker and Docker Compose** for containerization
- **Minsearch** for full-text search
- **Flask** as the API interface
- **Grafana** for monitoring and **PostgreSQL** as the backend
- **OpenAI** as an LLM

## Preparation

Since we use OpenAI, you need to provide your API key.

### Setting Up Environment Variables

Ensure that your `.env` file is not committed to version control by adding it to `.gitignore`.

### Creating and Activating a Virtual Environment

We use `venv` to manage the virtual environment.

- **Create the virtual environment:**

  ```bash
  python -m venv venv
  ```

- **Activate the virtual environment:**

  On Unix or macOS:
  ```bash
  source venv/bin/activate
  ```

  On Windows:
  ```cmd
  venv\Scripts\activate
  ```

### Install Dependencies

Install the application dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the Application

### Database Configuration

Before starting the application for the first time, the database needs to be initialized.

- **Run PostgreSQL:**

  ```bash
  docker-compose up -d postgres
  ```

  The `-d` flag runs the service in detached mode.

- **Initialize the Database:**

  Ensure your virtual environment is activated.

- **Run the `db_prep.py` script:**

  ```bash
  python db_prep.py
  ```

- **Check the Database Content (Optional):**

  Install `pgcli` if you haven't:

  ```bash
  pip install pgcli
  ```

  Connect to the database:

  ```bash
  pgcli -h localhost -U your_db_user -d your_db_name -W
  ```

  View the schema:

  ```sql
  \d conversations;
  ```

  Select data:

  ```sql
  SELECT * FROM conversations;
  ```

## Running with Docker Compose

The easiest way to run the application is with Docker Compose:

```bash
docker-compose up
```

## Running Locally

If you want to run the application locally:

- **Start PostgreSQL and Grafana:**

  ```bash
  docker-compose up -d postgres grafana
  ```

- **Stop the Dockerized App (if it's running):**

  ```bash
  docker-compose stop app
  ```

- **Run the App on Your Host Machine:**

  ```bash
  source venv/bin/activate
  export POSTGRES_HOST=localhost
  python app.py
  ```

## Running with Docker (Without Compose)

To run the application in Docker without Docker Compose:

- **Build the Docker Image:**

  ```bash
  docker build -t data-science-rag-bot .
  ```

- **Run the Docker Container:**

  ```bash
  docker run -it --rm \
      --network="data-science-rag-bot_default" \
      --env-file=".env" \
      -e OPENAI_API_KEY=${OPENAI_API_KEY} \
      -e DATA_PATH="data/data.csv" \
      -p 5000:5000 \
      data-science-rag-bot
  ```

## Using the Application

### CLI

We built an interactive CLI application using `questionary`.

- **Start the CLI:**

  ```bash
  python cli.py
  ```

- **Use a Random Question from the Dataset:**

  ```bash
  python cli.py --random
  ```

### Using Requests

You can use `test.py` to send questions to the app:

```bash
python test.py
```

It will pick a random question from the dataset and send it to the app.

### CURL

You can also use `curl` to interact with the API:

```bash
URL=http://localhost:5000
QUESTION="What is the difference between supervised and unsupervised learning?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

Example response:

```json
{
  "answer": "Supervised learning involves training a model on labeled data, where the correct output is known, to make predictions. Unsupervised learning, on the other hand, deals with unlabeled data and seeks to find hidden patterns or intrinsic structures within the data without prior knowledge of the correct output.",
  "conversation_id": "some-unique-id",
  "question": "What is the difference between supervised and unsupervised learning?"
}
```

### Sending Feedback

```bash
ID="137"
URL=http://localhost:5000
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback
```

After sending it, you'll receive the acknowledgement:

```json
{
    "message": "Feedback received for conversation 137: 1"
}
```

## Code

The code for the application is in the `/apps` folder:

- `app.py` - the Flask API, the main entry point to the application
- `rag.py` - the main RAG logic for retrieving data and building prompts
- `ingest.py` - loading the data into the knowledge base
- `minsearch.py` - an in-memory search engine
- `db.py` - logic for logging requests and responses to PostgreSQL
- `db_prep.py` - script for initializing the database

We also have some code in the project root directory:

- `test.py` - selects a random question for testing
- `cli.py` - interactive CLI for the app

## Interface

We use Flask to serve the application as an API. Refer to the **Using the Application** section for examples of how to interact with the application.

## Ingestion

The ingestion script is in `ingest.py`.

Since we use an in-memory database (`minsearch`) as our knowledge base, we run the ingestion script at the startup of the application. It is executed inside `rag.py` when it is imported.

## Experiments

For experiments, we use Jupyter notebooks located in the `notebooks` folder.

The following notebooks are included:

- **`rag-test.ipynb`**: Evaluates the RAG flow and overall system performance.
- **`evaluation-data-generation.ipynb`**: Generates the ground truth dataset for retrieval evaluation.

The data generation involved creating a set of questions similar to those in the original dataset. One of the biggest challenges was managing to parse the outputs from the language models. Small open-source language models struggled to provide reliably formatted outputs even with detailed prompts to guide them, so it was necessary to create an ad hoc parsing function that handled various edge cases.

Among the several open-source models tested, the chosen one was **llama3.1:8b** for its reliability and consistent output quality for this use case. For using the LLM as a judge to evaluate the relevance of the answers, **llama3.1:8b** and **gpt-4o-mini** from OpenAI were used. For generating the answers to be evaluated, the mentioned llama model was also used.

In the role of judges or evaluators, both models performed similarly, providing comparable results:

**Retrieval Evaluation**

  **LLM-as-a-Judge metric** to evaluate the quality of our RAG flow.
  
  - **Model: LLama 3.1 8b** (sample: 200)
    - RELEVANT: 0.79
    - PARTLY_RELEVANT: 0.20
    - NON_RELEVANT: 0.01
  
  - **Model: gpt-4o-mini** (sample: 200)
    - RELEVANT: 0.75
    - PARTLY_RELEVANT: 0.24
    - NON_RELEVANT: 0.01

From the results, the llama model could very well be used for this use case, especially for local deployment. The decision to use OpenAI's gpt-4o-mini was for convenience, as it is faster than running a model locally, more reliable in formatting outputs, and cost-effective for the scope of this project.

**Basic Approach Metrics (using Minsearch without any boosting):**

- Hit Rate: 95%
- MRR: 80%

**Improved Version Metrics (with tuned boosting):**

- Hit Rate: 99%
- MRR: 91%

**Best Boosting Parameters:**

```python
boost = {
    'Question': 0.56,
    'Answer': 1.46
}
```

## Monitoring

We use Grafana for monitoring the application.

- **Access Grafana at:** [http://localhost:3000](http://localhost:3000)
  - **Login:** admin
  - **Password:** admin

### Dashboards

The monitoring dashboard contains several panels:

- **Last 5 Conversations (Table):** Displays recent conversations with details.
- **+1/-1 (Pie Chart):** Visualizes user feedback.
- **Relevancy (Gauge):** Represents the relevance of responses.
- **OpenAI Cost (Time Series):** Depicts OpenAI usage costs over time.
- **Tokens (Time Series):** Tracks the number of tokens used.
- **Model Used (Bar Chart):** Shows the count of conversations by model.
- **Response Time (Time Series):** Displays response times over time.

### Setting Up Grafana

All Grafana configurations are in the `grafana` folder:

- `init.py` - for initializing the data source and the dashboard
- `dashboard.json` - the actual dashboard configuration

**Initialize the Dashboard:**

- **Ensure Grafana is running:**

  ```bash
  docker-compose up -d grafana
  ```

- **Run the Initialization Script:**

  ```bash
  source venv/bin/activate
  cd grafana

  # Ensure POSTGRES_HOST is set correctly
  env | grep POSTGRES_HOST

  python init.py
  ```

- **Access Grafana:**
  - **URL:** [http://localhost:3000](http://localhost:3000)
  - **Login:** admin
  - **Password:** admin

  When prompted, you can keep "admin" as the new password or set a new one.

## Background

Here we provide background on some technologies not covered in detail and links for further reading.

### Flask

We use Flask to create the API interface for our application. It is a lightweight web application framework for Python, allowing us to easily create endpoints for asking questions and interacting with the app via web clients like `curl` or `requests`.

For more information, visit the [official Flask documentation](https://flask.palletsprojects.com/en/latest/).

## Acknowledgements

I would like to thank Alexey Grigorev and the course organizers and participants for their great energy and effort in making this course available freely to the commnunity. 
This project is based on the project shared by Alexey Grigorev during the course: https://github.com/alexeygrigorev/fitness-assistant/tree/main Thanks again for all the materials shared with such a varety and great quality.

