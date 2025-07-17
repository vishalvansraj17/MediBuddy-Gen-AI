from flask import Flask, request, jsonify, render_template
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import logging
from helper import some_function
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    docsearch = PineconeVectorStore(index_name="medibuddy-bot", embedding=embeddings)
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
except Exception as e:
    logger.error(f"Failed to initialize embeddings or vector store: {str(e)}")
    raise

try:
    chatModel = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.4)
except Exception as e:
    logger.error(f"Failed to initialize chat model: {str(e)}")
    raise

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

try:
    question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
except Exception as e:
    logger.error(f"Failed to initialize RAG chain: {str(e)}")
    raise

@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg")
        if not msg:
            logger.warning("No message provided in request")
            return jsonify({"error": "No message provided"}), 400
        logger.info(f"Received query: {msg}")
        response = rag_chain.invoke({"input": msg})
        logger.info(f"Generated response: {response['answer']}")
        return jsonify({"response": response["answer"]})
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)