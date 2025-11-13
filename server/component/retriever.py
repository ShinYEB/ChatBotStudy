from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

def getRetriever():
    qdrant_url = "http://localhost:6333"
    collection_name = "azure_docs"
    embeddings = OpenAIEmbeddings()

    print("--- Qdrant 서버에 연결 중... ---")

    client = QdrantClient(url=qdrant_url)

    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings
    )

    print("--- Qdrant 연결 완료! FastAPI 서버 시작 준비 끝. ---")

    retriever = vectorstore.as_retriever(search_type="similarity", k=5)

    return retriever