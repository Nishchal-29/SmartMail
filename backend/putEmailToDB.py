from pinecone import Pinecone
import os
from dotenv import load_dotenv
import json
from llama_index.core import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
load_dotenv()

pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pinecone_client.Index("first")

embed_model = GoogleGenAIEmbedding(model_name='models/embedding-001')
Settings.embed_model = embed_model

with open("hackfest/new.json", "r") as f:
    data = json.load(f)

email_texts = []
id_list = []
metadata_list = []

email_texts = [item["email"] for item in data]
ids = [str(item["id"]) for item in data]
embeddings = embed_model._get_text_embeddings(email_texts)
vectors = []
for i, (id, email_text, embedding) in enumerate(zip(ids, email_texts, embeddings)):
    vector = {
        "id": id,  # Random UUID for now
        "values": embedding,
        "metadata": {
            "text": email_text,
            "source": "email",         # optional, could help later
        }
    }
    vectors.append(vector)


index.upsert(
    namespace="user4",
    vectors=vectors
)
#Takes in the address of the json database of email response pairs, then takes in only the emails. convert emails to embeddings, then add those vector emails with appropriate metadata to the vector db. Metadata should be "text": email_text1,"source": "email","formality". Formality not in intial phase




#Calculation: findout formality score OF THE EMAIL and not the response. Then classify as formal or informal. Not to do in initial phase