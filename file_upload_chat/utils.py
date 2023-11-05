import os
import pinecone
import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings

def get_pinecone_index():
    pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENVIRONMENT'))
    print("Active Index", pinecone.list_indexes())
    index = pinecone.Index("chatwithdocs")
    return index


def split_docs(document, chunk_size=200, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_documents = text_splitter.split_documents(document)
    return split_documents


def get_embeddings_document(document):
    text = document.page_content   
    model = OpenAIEmbeddings()
    response = model.embed_documents(text)
    return response


def get_embeddings(text):
    model = OpenAIEmbeddings()
    response = model.embed_query(text)
    return response


def embed_documents(documents, file_key):
    embeddings = []
    for doc in documents:
        metadata = {
            "text": doc.page_content.replace('\n', '').strip(),
            "file_key": file_key
        }
        doc = Document(
            page_content=doc.page_content.replace('\n', '').strip(),
            metadata=metadata
        )
        embedding = get_embeddings_document(doc)
        hash = hashlib.md5(doc.page_content.encode()).hexdigest()
        
        data = {
            "id": hash,
            "values": embedding[0],
            "metadata": doc.metadata
        }
        embeddings.append(data)
        
    return embeddings

# query pinecone db to retrieve matching embeddings
def get_matches_from_embeddings(embeddings, file_key):
    index = get_pinecone_index()
    query_result = index.query(
            vector=embeddings, 
            filter={
                "file_key": {"$eq": file_key}
            }, 
            top_k=5, 
            include_metadata=True
            )
    return query_result
    
    
def get_context(query, file_key):
    query_embeddings = get_embeddings(query.replace('\n', '').strip())
    matches = get_matches_from_embeddings(query_embeddings, file_key)
    qualifying_docs = [match for match in matches.get('matches', []) if match.get('score', 0) > 0.7]
    docs = [match["metadata"]["text"] for match in qualifying_docs if "metadata" in match]
    result = "\n".join(docs)[:3000]
    return result

    
    
        
        
        
    
    

    

