
import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore

load_dotenv()

def generate_crafted_response(email_scenario: str) -> str:
    # Setup clients
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

    # Style description
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

    # Query company rules from Pinecone (namespace: companyrules2)
    vector_store_rules = PineconeVectorStore(pinecone_index=pinecone_index, namespace='companyrules2')
    index_rules = VectorStoreIndex.from_vector_store(vector_store=vector_store_rules, embed_model=embed_model)
    query_engine_rules = index_rules.as_query_engine(similarity_top_k=3)
    rule_context = query_engine_rules.query(email_scenario)

    # Query past user emails (namespace: user4)
    query_vector = embed_model._get_text_embeddings([email_scenario])
    top_k_results = pinecone_index.query(
        namespace="user4",
        top_k=5,
        include_metadata=True,
        vector=query_vector[0]
    )

    # Build examples text from previous emails
    examples_text = ""
    for match in top_k_results["matches"]:
        email_text = match['metadata']['text']
        examples_text += f"Email:\n{email_text}\n\n"

    # Final prompt for Gemini
    final_prompt = f"""
Below are some past email examples:

{examples_text}
Now generate a suitable response to the following email:

{email_scenario}

Based on the following company rules or guidelines:

{rule_context}

User style preferences:
{user_style_instruction}

Write a professional email response following all applicable company policies. Only give me email text and nothing else.
Response:
"""

    response = llm.complete(final_prompt)
    return response.text.strip()

# import os
# import json
# from dotenv import load_dotenv
# from pinecone import Pinecone
# from llama_index.core import Settings, VectorStoreIndex
# from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
# from llama_index.llms.google_genai import GoogleGenAI
# from llama_index.vector_stores.pinecone import PineconeVectorStore

# load_dotenv()

# def generate_crafted_response(email_scenario: str, user_prompt = None) -> str:
#     # Setup clients
#     pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
#     pinecone_index = pinecone_client.Index("first")

#     embed_model = GoogleGenAIEmbedding(model_name='models/embedding-001')
#     llm = GoogleGenAI(
#         model="gemini-2.0-flash",
#         api_key=os.environ["GOOGLE_API_KEY"]
#     )

#     Settings.embed_model = embed_model
#     Settings.llm = llm

#     # Load user profile
#     with open("userProfile.json", "r") as f:
#         user_data = json.load(f)

#     user_profile = user_data["user1"]
#     top_tone = max(user_profile["tone_profile"], key=user_profile["tone_profile"].get)
#     top_category = max(user_profile["category_profile"], key=user_profile["category_profile"].get)
#     conciseness_score = user_profile["avg_conciseness"]

#     # Style description
#     if conciseness_score > 0.75:
#         concise_note = "The response should be concise and to the point."
#     elif conciseness_score > 0.5:
#         concise_note = "The response should maintain moderate detail and clarity."
#     else:
#         concise_note = "The response can be more descriptive and elaborate if necessary."

#     user_style_instruction = f"""
# Please write the email in a **{top_tone.lower()}** tone, suitable for a **{top_category.lower()}** communication scenario.
# {concise_note}
# """

#     # Query company rules from Pinecone (namespace: companyrules2)
#     vector_store_rules = PineconeVectorStore(pinecone_index=pinecone_index, namespace='companyrules2')
#     index_rules = VectorStoreIndex.from_vector_store(vector_store=vector_store_rules, embed_model=embed_model)
#     query_engine_rules = index_rules.as_query_engine(similarity_top_k=3)
#     rule_context = query_engine_rules.query(email_scenario)

#     # Query past user emails (namespace: user4)
#     query_vector = embed_model._get_text_embeddings([email_scenario])
#     top_k_results = pinecone_index.query(
#         namespace="user4",
#         top_k=5,
#         include_metadata=True,
#         vector=query_vector[0]
#     )

#     # Build examples text from previous emails
#     examples_text = ""
#     for match in top_k_results["matches"]:
#         email_text = match['metadata']['text']
#         examples_text += f"Email:\n{email_text}\n\n"


#     if user_prompt is not None:
#     # Final prompt for Gemini
#         final_prompt = f"""
#         Below are some past email examples:

#         {examples_text}
#         Now generate a suitable response to the following email:

#         {email_scenario}

#         Based on the following company rules or guidelines:

#         {rule_context}

#         User style preferences:
#         {user_style_instruction}

#         User conditions to take into consideration:
#         {user_prompt}
#         Write a professional email response following all applicable company policies. Only give me email text and nothing else.
#         Response:
#         """

#         response = llm.complete(final_prompt)
#         return response.text.strip()
#     else:
#         final_prompt = f"""
#         Below are some past email examples:

#         {examples_text}
#         Now generate a suitable response to the following email:

#         {email_scenario}

#         Based on the following company rules or guidelines:

#         {rule_context}

#         User style preferences:
#         {user_style_instruction}

#         Write a professional email response following all applicable company policies. Only give me email text and nothing else.
#         Response:
#         """

#         response = llm.complete(final_prompt)
#         return response.text.strip()
