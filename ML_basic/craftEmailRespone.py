#For now, it will not take into account the user parameters

#currently uses only company rules to write responses

# import os
# from dotenv import load_dotenv
# from llama_index.vector_stores.pinecone import PineconeVectorStore
# from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
# from llama_index.core import VectorStoreIndex, Settings
# from llama_index.llms.google_genai import GoogleGenAI
# from pinecone import Pinecone

# load_dotenv()

# # Pinecone setup
# pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# pinecone_index = pinecone_client.Index("first")

# # Embedding & LLM
# embed_model = GoogleGenAIEmbedding(
#     model="models/embedding-001"
# )
# llm = GoogleGenAI(
#     model="gemini-2.0-flash",
#     api_key=os.environ["GOOGLE_API_KEY"]
# )
# Settings.llm = llm
# Settings.embed_model = embed_model
# vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
# # Rebuild the index from Pinecone
# index = VectorStoreIndex.from_vector_store(
#     vector_store=vector_store,
#     embed_model=embed_model
# )

# # Define your email situation
# email_scenario = """
# I am User123 asking my boss to reschedule the meeting to thursday 2pm. My boss is boss123. He was organizing meeting earlier on 3pm wednesday. The tone should be formal and polite. the email should be 75 to 100 words long. My email address is testuser123@gmail.com and my boss email id is testboss123@gmail.com.
# """

# # Get context from rules via similarity search
# query_engine = index.as_query_engine(similarity_top_k=3)
# rule_context = query_engine.query(email_scenario)

# # Compose a response using the LLM and rule context
# prompt = f"""
# Given the following conditions of email:

# "{email_scenario}"

# And based on the following company rules or guidelines:

# "{rule_context}"

# Write a professional email response following all applicable company policies. Only give me email text and nothing else.
# """

# response = llm.complete(prompt)
# print("\nResponse Email:\n")
# print(response)

#Below version also takes into account the past emails along with the company rules:
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import json
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
load_dotenv()

with open("hackfest/new.json", "r") as f:
    data = json.load(f)

id_to_response = {str(item["id"]): item["response"] for item in data}

pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pinecone_client.Index("first")
embed_model = GoogleGenAIEmbedding(model_name='models/embedding-001')
llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)
Settings.embed_model = embed_model
Settings.llm = llm
email_scenario = """
Subject: Request to Reschedule Meeting - Wednesday at 3:00 PM

Dear Boss123,

I am writing to respectfully request you to provide me leaves from April 2 to April 11 because I have to go on outing.
       

I apologize for any inconvenience this may cause and appreciate your understanding and flexibility. Please let me know if this works for you.

Thank you for your time and consideration.

Sincerely,

User123
"""
#User params:
with open("hackfest/new/userProfile.json", "r") as f:
    user_data = json.load(f)

user_profile = user_data["user1"]

# Get top tone
top_tone = max(user_profile["tone_profile"], key=user_profile["tone_profile"].get)
top_category = max(user_profile["category_profile"], key=user_profile["category_profile"].get)
conciseness_score = user_profile["avg_conciseness"]

# Map conciseness score into a description
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


vector_store1 = PineconeVectorStore(pinecone_index=pinecone_index, namespace='companyrules2')
# Rebuild the index from Pinecone
index1 = VectorStoreIndex.from_vector_store(
    vector_store=vector_store1,
    embed_model=embed_model
)
query_engine1 = index1.as_query_engine(similarity_top_k=3)
rule_context = query_engine1.query(email_scenario)
query_vector2 = embed_model._get_text_embeddings([email_scenario])

top_k_results2 = pinecone_index.query(
    namespace="user4",
    top_k=5,
    include_metadata=True,
    vector=query_vector2[0]
)
email_texts = []
ids = []
pairs = []
for match in top_k_results2["matches"]:
    # print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']['text']}")
    matched_id = match['id']
    email_text = match['metadata']['text']
    response = id_to_response.get(matched_id, "No response found")
    email_texts.append(email_text)
    ids.append(matched_id)
    pairs.append((email_text, response))

examples_text = ""
for email, response in pairs:
    examples_text += f"Email:\n{email}\nResponse:\n{response}\n\n"


final_prompt = f"""
Below are some past email-response examples:

{examples_text}
Now generate a suitable response to the following email:

{email_scenario}

And based on the following company rules or guidelines:

{rule_context}
User style preferences:
{user_style_instruction}
Write a professional email response following all applicable company policies. Only give me email text and nothing else.
Response:
"""
print(f"\n\nThe txt in user style instruction was {user_style_instruction}\n\n")
response = llm.complete(final_prompt)
print(response)