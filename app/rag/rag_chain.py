from app.rag.vector_store import create_doc_vector_store
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.ollama import Ollama
from app.core.config import OPENAI_API_KEY

# now to make the RAG mechanism that uses the vector store

def rag_chain(query: str, file_path: str):

    vectorSpace = create_doc_vector_store(file_path)
    if isinstance(vectorSpace, str):
        raise ValueError(f"Failed to create document vector store: {vectorSpace}")
    retriever = vectorSpace.as_retriever()
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs]) 

    # llm = ChatOpenAI(model="gpt-3.5-turbo")
    llm_used = ChatOpenAI(model="gpt-4", openai_api_key= OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_template(
        "Answer the question based only on this context:\n{context}\n\n"
        "Question: {question}"
    )

    prompt_runnable = prompt.format_prompt(context= context, question= query)
    
    response = llm_used.invoke(prompt_runnable.to_messages())


    return response.content