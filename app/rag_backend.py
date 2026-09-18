import os

from databricks.ai_search.client import AISearchClient
from databricks.sdk import WorkspaceClient
from databricks.sql import connect


# --------------------------------------------------
# AI SEARCH CONNECTION
# --------------------------------------------------

client_id = os.getenv("DATABRICKS_CLIENT_ID")
client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
workspace_url = os.getenv("DATABRICKS_HOST")

if workspace_url and not workspace_url.startswith("http"):
    workspace_url = "https://" + workspace_url

vsc = AISearchClient(
    workspace_url=workspace_url,
    service_principal_client_id=client_id,
    service_principal_client_secret=client_secret
)

index = vsc.get_index(
    index_name="workspace.finance_genai.finance_document_chunks_index"
)


# --------------------------------------------------
# RETRIEVE RELEVANT POLICY CONTEXT
# --------------------------------------------------

def retrieve_finance_context(question, num_results=3):

    results = index.similarity_search(
        query_text=question,
        columns=["chunk", "document_name"],
        num_results=num_results,
        query_type="hybrid"
    )

    rows = results["result"]["data_array"]

    context = "\n\n".join(
        [
            f"Source: {row[1]}\nContent: {row[0]}"
            for row in rows
        ]
    )

    sources = [row[1] for row in rows]

    return context, sources


# --------------------------------------------------
# GENERATE ANSWER USING DATABRICKS LLM
# --------------------------------------------------

def generate_finance_answer(question, context):

    warehouse_id = os.getenv("DATABRICKS_WAREHOUSE_ID")

    cfg = WorkspaceClient().config

    connection = connect(
        server_hostname=cfg.host.replace("https://", ""),
        http_path=f"/sql/1.0/warehouses/{warehouse_id}",
        credentials_provider=lambda: cfg.authenticate
    )

    prompt = f"""
You are a finance policy assistant.

Answer the user's question ONLY using the provided finance policy context.

If the context does not contain enough information to answer the question, say:

"I could not find enough information in the provided finance policies."

Do not invent, assume, or use outside knowledge.

User question:
{question}

Finance policy context:
{context}

Provide a concise answer and mention the relevant policy document(s).
"""

    escaped_prompt = prompt.replace("'", "''")

    query = f"""
    SELECT ai_query(
        'databricks-meta-llama-3-3-70b-instruct',
        '{escaped_prompt}'
    ) AS answer
    """

    try:
        with connection.cursor() as cursor:

            cursor.execute(query)

            result = cursor.fetchone()

            return result[0]

    finally:
        connection.close()