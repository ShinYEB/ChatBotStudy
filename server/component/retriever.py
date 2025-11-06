from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv

load_dotenv()

def getRetriever():

    # 'database' 폴더 안에 있는 '.pdf' 파일 불러옴.
    pdf_folder_path = "./database"
    loader = DirectoryLoader(
        pdf_folder_path,
        glob="*.pdf",
        loader_cls=PyMuPDFLoader,
    )
    docs = loader.load()

    if not docs:
        print(f"'{pdf_folder_path}' 폴더에 PDF 파일이 없습니다.")
        return None

    print(f"--- {len(docs)}개의 PDF 문서를 로드했습니다. ---")

    # PDF 문서들은 내용이 길기 때문에 잘게 쪼갠다.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 쪼갠 문서 조각들을 FAISS에 저장한다.
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)

    print(f"--- {len(splits)}개의 문서 조각으로 나누어 Vector DB에 저장 완료! ---")

    retriever = vectorstore.as_retriever()

    return retriever
