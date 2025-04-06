# ingest_rules.py
import os
from pinecone import Pinecone
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.storage.storage_context import StorageContext

load_dotenv()

# Optional: Choose OpenAI or Gemini embedding depending on what you're using
embed_model = GoogleGenAIEmbedding(model_name='models/embedding-001')
Settings.embed_model = embed_model
# Load and split rules
docs = SimpleDirectoryReader(input_dir="hackfest/new/Rules").load_data()
if docs is not None:
    parser = SentenceSplitter(chunk_size=512)
    nodes = parser.get_nodes_from_documents(docs)

    pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    pinecone_index = pinecone_client.Index("first")

    vector_store = PineconeVectorStore(pinecone_index=pinecone_index,namespace="companyrules2")

    # Build index
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embed_model)