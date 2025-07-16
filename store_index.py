from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not PINECONE_API_KEY or not GOOGLE_API_KEY:
    raise ValueError("Missing API keys. Please check your .env file.")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

try:
    extracted_data = load_pdf_file(data='data/')
    filter_data = filter_to_minimal_docs(extracted_data)
    text_chunks = text_split(filter_data)
except Exception as e:
    raise Exception(f"Failed to process documents: {str(e)}")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
except Exception as e:
    raise Exception(f"Failed to initialize Pinecone: {str(e)}")

index_name = "medibuddy-bot"

try:
    if index_name not in pc.list_indexes().names():
        print(f"Creating new Pinecone index: {index_name}...")
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"Index {index_name} created successfully.")
    else:
        print(f"Connecting to existing Pinecone index: {index_name}")
except Exception as e:
    raise Exception(f"Failed to manage Pinecone index: {str(e)}")

try:
    docsearch = PineconeVectorStore.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        index_name=index_name
    )
    print(f"Pinecone index '{index_name}' is now populated with Gemini embeddings.")
except Exception as e:
    raise Exception(f"Failed to populate Pinecone index: {str(e)}")