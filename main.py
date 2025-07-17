import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
import glob
load_dotenv()

# Configuration
PERSIST_DIR = "./perfect_chroma_db"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create embeddings instance once and reuse
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def setup_vectorstore():
    """Setup or load vector store"""
    if os.path.exists(PERSIST_DIR):
        return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    
    # Process document if vector store doesn't exist
  # Load all PDF files from upload_files/ directory
    pdf_files = glob.glob("./upload_files/*.pdf")

    all_documents = []
    for file_path in pdf_files:
        print(f"Loading: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        all_documents.extend(documents)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    chunks = text_splitter.split_documents(all_documents)
    
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

def run_llm(query, chat_history):
    
    setup_vectorstore()
    """Main function to run queries"""
    # Setup components
    vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192", temperature=0)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. 

Context from documents:
{context}
Chat History:
{chat_history}
Instructions:
- If the user is asking about previous questions, conversations, or what they asked earlier, use the chat history 
to answer and generate a suggested question that he should ask about the context.                                          
- For all other questions, use only the information provided in the document context above.
- If the document context does not contain enough information to answer (and it's not about chat history), reply:
"This question is beyond my knowledge as it is not covered in the provided context."

Current question: {input}

Answer:
""")
    # Create chains
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    qa = create_retrieval_chain(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
        combine_docs_chain=stuff_documents_chain
    ) 
    result = qa.invoke({"input": query, "chat_history": chat_history})
    if not result["context"]:
        print("No context found. Falling back to general LLM answer.")
        response = llm.invoke(query)
        new_result = {
            "query": query,
            "result": response.content,
            "source_documents": []
        }
    else:
        new_result = {
            "query": result["input"],
            "result": result["answer"],
            "source_documents": result["context"]
        }
    return new_result

if __name__ == "__main__":
    result = run_llm("Butter chicken recipe")
    