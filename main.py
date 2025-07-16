import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq

load_dotenv()

# Configuration
PERSIST_DIR = "./perfect_chroma_db"


def setup_vectorstore():
    """Setup or load vector store"""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(PERSIST_DIR):
        return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    
    # Process document if vector store doesn't exist
    loader = PyPDFLoader("Get_Started_With_Smallpdf.pdf")
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

def run_llm(query: str):
    """Main function to run queries"""
    # Setup components
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192", temperature=0)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template("""
Context: {context}
Question: {input}
Answer based on the context provided:
if the context does not provide enough information, use general knowledge to answer".
if the context provides enough information, answer the question.

""")
    
    # Create chains
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    qa = create_retrieval_chain(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        combine_docs_chain=stuff_documents_chain
    )
    
    result = qa.invoke({"input": query})
    return result

if __name__ == "__main__":
    # Setup vector store (run once)
    setup_vectorstore()
    
    # Use it
    result = run_llm("butter chicken?")
    print(result)