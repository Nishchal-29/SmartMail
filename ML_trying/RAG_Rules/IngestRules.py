from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from pinecone import Pinecone
from llama_index.core.ingestion import IngestionPipeline #There are many splitters, check which works best
from llama_index.core.node_parser import SentenceSplitter #There are many parsers, check which works best
from llama_index.vector_stores.pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv
load_dotenv()
llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

embed_model = GoogleGenAIEmbedding(model_name="models/embedding-001")
llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)
Settings.llm = llm
Settings.embed_model = embed_model
docs = SimpleDirectoryReader("./hackfest/company_guide").load_data()


pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pinecone_client.Index("testhackfest")
# print(f"Before updating: \n{pinecone_index.describe_index_stats()}")

vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace="companyrules")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    docs,
    storage_context=storage_context
)

# print("Done")
# print(f"After updating: \n{pinecone_index.describe_index_stats()}")
