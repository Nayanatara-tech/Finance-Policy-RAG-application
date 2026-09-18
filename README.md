## Application

The RAG pipeline was developed and validated in Databricks notebooks.
The pipeline was then converted into a user-facing Streamlit application
and deployed as a Databricks App.

The application:

1. Accepts a finance policy question through the Streamlit UI.
2. Performs hybrid retrieval using Databricks AI Search.
3. Retrieves the most relevant policy chunks.
4. Passes the retrieved context to Llama using ai_query().
5. Generates a grounded answer.
6. Displays the relevant source documents.

### Application Components

app.py
- Streamlit UI
- Accepts user questions
- Displays answers and source documents

rag_backend.py
- AI Search retrieval
- Context construction
- SQL Warehouse connection
- LLM answer generation

requirements.txt
- Python dependencies

app.yaml
- Application startup configuration
- Resource/environment configuration
