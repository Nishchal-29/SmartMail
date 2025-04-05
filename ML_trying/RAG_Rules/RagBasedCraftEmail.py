from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import os
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore

llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

embed_model = GoogleGenAIEmbedding(model_name="models/embedding-001")

Settings.llm = llm
Settings.embed_model = embed_model

pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pinecone_client.Index("testhackfest")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace="companyrules")

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context,
)
data_prompt = input("Enter the prompt:\n")
query_engine = index.as_query_engine(similarity_top_k=3)
rule_context = query_engine.query(data_prompt)

prompt = f"""
Use the following rules while writing the email: 
{rule_context}

Now, generate a well-structured email using the user-provided parameters:
{data_prompt}

The email should strictly follow any provided rules or formats.
Just return the email body, no extra text.
"""
response1 = llm.complete(prompt)
def extract_email_components(raw_email: str) -> tuple:
    lines = raw_email.strip().splitlines()

    # Find the subject line
    subject = ""
    body_lines = []
    subject_found = False
    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line[len("Subject:"):].strip()
            subject_found = True
        elif subject_found:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    return (subject, body)

pair = extract_email_components(response1.text.strip())
print(pair)
