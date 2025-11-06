import redis
from redis.commands.search.field import (
    TextField,
    VectorField
)
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)

# --- 상수 정의 ---
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_INDEX_NAME = "faq_cache_index"
VECTOR_DIMENSION = 384  # 사용할 모델의 차원 (예: all-MiniLM-L6-v2)
VECTOR_FIELD_NAME = "question_vector"
METRIC = "COSINE"  # 유사도 측정 기준 (코사인 유사도)

# --- Redis 연결 ---
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()
    print("Redis에 성공적으로 연결되었습니다.")
except Exception as e:
    print(f"Redis 연결 실패: {e}")
    exit(1)

# --- 인덱스 스키마 정의 ---
schema = (
    # 1. 질문 텍스트 (참고용)
    TextField("question_text"),

    # 2. 캐시된 답변 텍스트
    TextField("answer_text"),

    # 3. 질문 임베딩 벡터 (핵심!)
    VectorField(
        VECTOR_FIELD_NAME,
        "FLAT",  # 간단한 브루트포스 검색 (데이터가 적을 때 좋음)
        {
            "TYPE": "FLOAT32",
            "DIM": VECTOR_DIMENSION,
            "DISTANCE_METRIC": METRIC,
        },
    ),
)


# --- 인덱스 생성 (및 기존 인덱스 삭제) ---
def create_index():
    try:
        # 기존 인덱스가 있다면 삭제 (개발 시 유용)
        print(f"기존 인덱스 '{REDIS_INDEX_NAME}' 삭제 시도...")
        r.ft(REDIS_INDEX_NAME).dropindex(delete_documents=True)
        print("기존 인덱스 삭제 완료.")
    except redis.exceptions.ResponseError:
        print("삭제할 기존 인덱스가 없습니다. 새로 생성합니다.")

    # 새 인덱스 생성
    definition = IndexDefinition(
        prefix=["faq:"],  # 이 prefix를 가진 key만 인덱싱
        index_type=IndexType.HASH
    )
    r.ft(REDIS_INDEX_NAME).create_index(
        fields=schema, definition=definition
    )
    print(f"'{REDIS_INDEX_NAME}' 인덱스 생성 완료.")


# --- 메인 실행 ---
if __name__ == "__main__":
    create_index()