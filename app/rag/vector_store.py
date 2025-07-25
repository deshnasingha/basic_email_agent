from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from app.core.config import OPENAI_API_KEY

def create_doc_vector_store(file_path: str):
    # getting the data
    try:
        loader = TextLoader(file_path)
        doc = loader.load()

    # now splitting the data to smaller chunks
    #configuring the text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
    #splitting the document
        split_doc = text_splitter.split_documents(doc)

    # now making the embeddings
    #default embedding model in OpenAIEmbeddings
        embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # now making the embeddings
        vector_store = DocArrayInMemorySearch.from_documents(split_doc, embedding_model)

    except Exception as e:
        return f"failed to make the vectorstore, error: {e}"

    return vector_store
