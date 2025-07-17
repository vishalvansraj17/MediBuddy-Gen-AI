from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from langchain_core.documents import Document
import os

def load_pdf_file(data: str) -> List[Document]:
    """
    Load PDF files from a specified directory and return a list of Document objects.
    
    Args:
        data (str): Path to the directory containing PDF files.
    
    Returns:
        List[Document]: List of Document objects extracted from PDFs.
    
    Raises:
        FileNotFoundError: If the specified directory does not exist.
        ValueError: If no PDF files are found in the directory.
    """
    if not os.path.exists(data):
        raise FileNotFoundError(f"Directory '{data}' does not exist.")
    
    loader = DirectoryLoader(
        path=data,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )

    try:
        documents = loader.load()
        if not documents:
            raise ValueError(f"No PDF files found in directory '{data}'.")
        return documents
    except Exception as e:
        raise Exception(f"Failed to load PDF files: {str(e)}")

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Filter Document objects to retain only 'source' in metadata and original page_content.
    
    Args:
        docs (List[Document]): List of Document objects to filter.
    
    Returns:
        List[Document]: List of Document objects with minimal metadata.
    
    Raises:
        ValueError: If input list is empty or contains invalid documents.
    """
    if not docs:
        raise ValueError("Input document list is empty.")
    
    minimal_docs: List[Document] = []
    for doc in docs:
        if not hasattr(doc, 'page_content') or not hasattr(doc, 'metadata'):
            continue
        src = doc.metadata.get("source", "unknown")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    if not minimal_docs:
        raise ValueError("No valid documents found after filtering.")
    return minimal_docs

def text_split(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks for vector store processing.
    
    Args:
        documents (List[Document]): List of Document objects to split.
    
    Returns:
        List[Document]: List of chunked Document objects.
    
    Raises:
        ValueError: If input list is empty.
    """
    if not documents:
        raise ValueError("Input document list is empty.")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
        length_function=len
    )
    try:
        text_chunks = text_splitter.split_documents(documents)
        if not text_chunks:
            raise ValueError("No chunks created from documents.")
        return text_chunks
    except Exception as e:
        raise Exception(f"Failed to split documents: {str(e)}")

def get_gemini_embeddings() -> GoogleGenerativeAIEmbeddings:
    """
    Initialize and return Google Generative AI embeddings.
    
    Returns:
        GoogleGenerativeAIEmbeddings: Configured embeddings object.
    
    Raises:
        Exception: If embedding initialization fails.
    """
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        return embeddings
    except Exception as e:
        raise Exception(f"Failed to initialize embeddings: {str(e)}")