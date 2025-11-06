import os
import redis
from sentence_transformers import SentenceTransformer
import numpy as np
from redis.commands.search.query import Query
from dotenv import load_dotenv

load_dotenv()

print("Hugging Face 모델 로드 중...")
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
print("모델 로드 완료.")

try:
    r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True)
    r.ping()
    print("Redis에 성공적으로 연결되었습니다.")
except Exception as e:
    print(f"Redis 연결 실패: {e}")
    exit(1)

VECTOR_FIELD_NAME = "question_vector"
REDIS_INDEX_NAME="faq_cache_index"


def search_cache(user_query: str, similarity_threshold=0.95):
    """
    Redis 캐시에서 유사한 질문을 검색합니다.
    """

    query_vector = model.encode(user_query).astype(np.float32).tobytes()

    q = (
        Query(f"(*)=>[KNN 1 @{VECTOR_FIELD_NAME} $query_vec AS vector_score]")
        .sort_by("vector_score")
        .return_field("vector_score")
        .return_field("question_text")
        .return_field("answer_text")
        .dialect(2)
    )

    query_params = {"query_vec": query_vector}

    try:
        results = r.ft(REDIS_INDEX_NAME).search(q, query_params)
    except redis.exceptions.ResponseError as e:
        print(f"검색 오류 (인덱스가 아직 준비되지 않았을 수 있음): {e}")
        return None

    # 3. 결과 분석
    if results.total == 0:
        print("캐시: 유사한 결과 없음 (Total=0).")
        return None  # 캐시 미스

    doc = results.docs[0]
    score = 1 - float(doc.vector_score)  # 코사인 거리를 유사도(0~1)로 변환

    print(f"캐시: 가장 유사한 질문 찾음 (유사도: {score:.4f})")
    print(f"캐시된 질문: {doc.question_text}")

    # 4. 임계값 비교
    if score >= similarity_threshold:
        print("캐시: 히트! (Hit!)")
        return doc.answer_text  # 캐시된 답변 반환
    else:
        print(f"캐시: 미스! (유사도 {score:.4f} < {similarity_threshold})")
        return None  # 캐시 미스


# --- 캐시에 추가 함수 ---
def add_to_cache(question: str, answer: str):
    """
    새로운 질문과 답변을 캐시에 저장합니다.
    """
    key = f"faq:{r.incr('next_faq_id')}"  # 간단한 고유 ID 생성
    question_vector = model.encode(question).astype(np.float32).tobytes()

    # HASH 자료구조로 저장
    r.hset(
        key,
        mapping={
            "question_text": question,
            "answer_text": answer,
            "question_vector": question_vector,
        },
    )
    print(f"캐시: 저장 완료 (Key: {key})")