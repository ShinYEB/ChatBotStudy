import os
from time import time, strftime, gmtime
from glob import glob
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm
from dotenv import load_dotenv

from .preprocessor import preprocessing

load_dotenv()

pdf_folder_path = "./database"
qdrant_url = "http://localhost:6333" # 1단계에서 띄운 서버 주소
collection_name = "azure_docs"

def build_index():

    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    print("--- Qdrant에 데이터 저장을 시작합니다. (1회성 작업) ---")

    pdf_files = glob(os.path.join(pdf_folder_path, "*.pdf"))

    if not pdf_files:
        print(f"'{pdf_folder_path}' 폴더에 PDF 파일이 없습니다.")
        return None
    print(f"--- 총 {len(pdf_files)}개의 PDF 파일을 찾았습니다. 순차적으로 처리합니다. ---")

    vectorstore = None
    total_splits = 0
    start_time = time()
    batch_size = 100

    for i, pdf_path in enumerate(pdf_files):
        try:
            print(f"\n[{i + 1}/{len(pdf_files)}] 파일 로드 중: {pdf_path}")

            loader = PyMuPDFLoader(pdf_path)
            docs = loader.load()

            if not docs:
                print("    -> 경고: 파일에서 문서를 로드하지 못했습니다. 건너뜁니다.")
                continue

            for doc in docs:
                doc.page_content = preprocessing(doc.page_content)

            splits = text_splitter.split_documents(docs)
            total_splits += len(splits)

            total_batches = (len(splits) - 1) // batch_size + 1

            for batch_num, j in tqdm(
                    enumerate(range(0, len(splits), batch_size)),
                    total=(len(splits) - 1) // batch_size + 1,  # 전체 배치 수
                    desc=f"파일 {i + 1}/{len(pdf_files)} 처리 중",
                    ncols=100
            ):

                batch_splits = splits[j: j + batch_size]

                try:
                    if vectorstore is None:
                        vectorstore = Qdrant.from_documents(
                                            batch_splits,
                                            embeddings,
                                            url=qdrant_url,
                                            collection_name=collection_name,
                                        )
                    else:
                        vectorstore.add_documents(batch_splits)

                except Exception as e:
                    print(f"    !! 배치 처리 오류 발생: {e}")

            print(f"    -> {pdf_path} 파일의 모든 배치 처리 완료.")
            total_splits += len(splits)  # 총 조각 수 누적

        except Exception as e:
            print(f"!! 오류 발생: {pdf_path} 처리 중 문제 발생 ({e}). 이 파일을 건너뜁니다.")

    print(f"\n--- 총 {len(pdf_files)}개의 파일, {total_splits}개의 조각을 Qdrant 서버에 저장 완료! ---")

    end_time = time()
    total_seconds = end_time - start_time
    formatted_time = strftime("%H:%M:%S", gmtime(total_seconds))
    print(f"총 소요시간: {formatted_time}")
