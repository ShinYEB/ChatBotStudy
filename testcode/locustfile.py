from locust import HttpUser, task, between, TaskSet, constant_pacing
import random
import time

PROMPT_LIST = [
    "고객센터 전화번호 알려줘",
    "상담원 연결하려면 몇 번이야?",
    "YES포인트 소멸시효 있어?",
    "포인트 유효기간 언제까지야?",
    "포인트 언제 사라져?",
    "무료배송 기준 금액은 얼마?",
    "책 얼마 이상 사면 배송비 안 내?",
    "15,000원 사면 무료배송 맞아?",
    "배송 지연되면 보상해 줘?",
    "총알배송 늦으면 어떻게 돼?",
    "신규 회원 혜택 자세히 알려줘",
    "방금 가입했는데 쿠폰 뭐 줘?",
    "크레마클럽 30일 무료 이용권 어떻게 받아?",
    "앱 다운로드하면 1000원 상품권 줘?",
    "매장 픽업 서비스는 배송비 내야 해?",
    "주문하고 목동점에서 받을 수 있어?",
    "주문한 책이 품절되면 어떻게 되는 거야?",
    "도서 품절 보상으로 몇 포인트 줘?",
    "5천원 미만 책이 품절되면 보상 얼마야?",
    "제휴 할인카드 뭐뭐 있어?",
    "신한카드로 결제하면 혜택 있어?",
    "KB국민카드 포인트 쓸 수 있어?",
    "YES포인트는 얼마부터 현금처럼 사용 가능해?",
    "YES머니로 전환하려면 포인트 몇 개 필요해?",
    "배송지연 보상금액은 얼마인가요?",
    "아침배송 늦으면 2000포인트 주는 거 맞아?",
    "오늘 날씨 어때?",
    "지금 몇 시야?",
    "가까운 편의점 어디 있어?",
    "짜장면 맛있게 만드는 법 알려줘",
    "너는 누구야?",
    "예스24 주가 알려줘",
    "세종대왕님은 어떤 책을 읽으셨어?",
    "배송이 너무 늦는데 환불해줘",
]

class UserBehavior(TaskSet):
    @task
    def get_chat(self):
        data = {
            "prompt": f"{random.choice(PROMPT_LIST)} (test_id: {time.time()})"
        }
        self.client.post("/chat", json=data)

class LocustUser(HttpUser):
    host = "http://127.0.0.1:8000"
    tasks = [UserBehavior]
    wait_time = between(30, 60)

