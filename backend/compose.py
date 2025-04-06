

#This will composes emails based on the company policy. Yet to integrate the user parameters

import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

# Initialize Pinecone and LLM
pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pinecone_client.Index("first")
embed_model = GoogleGenAIEmbedding(model_name='models/embedding-001')
llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

Settings.embed_model = embed_model
Settings.llm = llm

# Load user profile
with open("userProfile.json", "r") as f:
    user_data = json.load(f)

user_profile = user_data["user1"]
top_tone = max(user_profile["tone_profile"], key=user_profile["tone_profile"].get)
top_category = max(user_profile["category_profile"], key=user_profile["category_profile"].get)
conciseness_score = user_profile["avg_conciseness"]

# Style description based on user profile
if conciseness_score > 0.75:
    concise_note = "The response should be concise and to the point."
elif conciseness_score > 0.5:
    concise_note = "The response should maintain moderate detail and clarity."
else:
    concise_note = "The response can be more descriptive and elaborate if necessary."

user_style_instruction = f"""
Please write the email in a **{top_tone.lower()}** tone, suitable for a **{top_category.lower()}** communication scenario.
{concise_note}
"""

# Load company rules vector store
vector_store1 = PineconeVectorStore(pinecone_index=pinecone_index, namespace='companyrules2')
index1 = VectorStoreIndex.from_vector_store(
    vector_store=vector_store1,
    embed_model=embed_model
)
query_engine1 = index1.as_query_engine(similarity_top_k=3)

# ✅ Function to call from app.py
def generate_email_from_prompt(original_email_body: str) -> str:
    email_scenario = f"""
You are an assistant that helps users craft professional replies to emails.

Below is the email the user received. Write a professional, thoughtful reply to it.
Respond in a way that aligns with company policy and etiquette.

Email to reply to:
\"\"\"
{original_email_body}
\"\"\"
"""

    rule_context = query_engine1.query(email_scenario)
    
    final_prompt = f"""
Generate a suitable email based on the following condition:

{email_scenario}

And based on the following company rules or guidelines:

{rule_context}

User style preferences:
{user_style_instruction}
Write a professional email response following all applicable company policies. Only give me email text and nothing else.
Email:
"""
    response = llm.complete(final_prompt)
    return response.text.strip()
