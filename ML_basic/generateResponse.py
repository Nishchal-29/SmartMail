#currently uses only company rules to write responses

import os
from dotenv import load_dotenv
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.google_genai import GoogleGenAI
from pinecone import Pinecone

load_dotenv()

# Pinecone setup
pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pinecone_client.Index("first")

# Embedding & LLM
embed_model = GoogleGenAIEmbedding(
    model="models/embedding-001"
)
llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)
Settings.llm = llm
Settings.embed_model = embed_model
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
# Rebuild the index from Pinecone
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=embed_model
)

# Define your email situation
email_scenario = """
Hi, I’d like to take a leave from April 2nd to April 4th due to health reasons.
Please let me know if that’s okay.
"""

# Get context from rules via similarity search
query_engine = index.as_query_engine(similarity_top_k=3)
rule_context = query_engine.query(email_scenario)

# Compose a response using the LLM and rule context
prompt = f"""
Given the following request from an employee:

"{email_scenario}"

And based on the following company rules or guidelines:

"{rule_context}"

Write a professional email response from the manager's side. Be polite and follow all applicable company policies. Only give me email text and nothing else.
"""

response = llm.complete(prompt)
print("\nResponse Email:\n")
print(response)
