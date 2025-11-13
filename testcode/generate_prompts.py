import random

core_intents = [
    # 배송
    "배송비", "무료배송 기준", "총알배송", "아침배송", "배송 지연", "배송 조회",
    # 포인트/결제
    "포인트", "YES포인트", "적립금", "예치금", "YES머니", "할인카드", "신한카드", "KB국민카드",
    # 회원/계정
    "회원가입 혜택", "신규 쿠폰", "비밀번호 찾기", "회원 탈퇴", "크레마클럽",
    # 상품/주문
    "품절 보상", "재고", "eBook", "중고도서", "주문 취소", "반품", "환불", "매장 픽업",
    # CS
    "고객센터", "상담원 연결", "전화번호", "채팅 상담"
]

actions = [
    "알려줘", "궁금해", "어떻게 해?", "뭐야?", "기준이 뭐야?",
    "정책 알려줘", "유효기간", "얼마야?", "언제까지야?", "가능해?",
    "신청 방법", "관련해서 질문", "좀 보자", "확인해 줘"
]

off_topic = [
    "오늘 날씨 어때?", "지금 몇 시야?", "가까운 편의점 어디 있어?",
    "짜장면 맛있게 만드는 법", "너는 누구야?", "예스24 주가 알려줘",
    "세종대왕님은 어떤 책을 읽으셨어?", "배가 너무 아파", "오늘 저녁 뭐 먹지?",
    "로또 1등 당첨 번호", "가장 빠른 동물은?", "서울에서 부산까지 얼마나 걸려?",
    "BTS 신곡 제목", "인생의 의미는 뭘까?", "파이썬으로 웹사이트 만드는 법",
    "주말에 볼만한 영화 추천", "AI가 세상을 지배할까?", "사랑이 뭘까?",
    "가장 감명 깊게 읽은 책은?", "우주의 끝은 어디?"
]

new_topics = [
    "해외 배송도 가능해?", "캐나다로 책 보낼 수 있어?", "군부대로 배송할 때 주소",
    "대량 주문 할인", "학교 도서관에서 책 100권 살 건데",
    "결제 영수증", "현금영수증 발급", "법인카드로 결제", "신용카드 무이자 할부",
    "eBook은 어떻게 다운로드해?", "내 크레마 기기 등록", "eBook 환불 규정",
    "중고도서 매입 신청", "내 책 팔기", "중고 매입 가격",
    "리뷰 작성하면 포인트 줘?", "포토 리뷰 혜택", "이달의 리뷰 혜택",
    "개인정보 변경", "휴대폰 번호 바꾸기", "마케팅 수신 동의 철회"
]

def getPrompts(target_count = 1000):
    final_prompt_list = []

    for _ in range(int(target_count * 0.6)):
        intent = random.choice(core_intents)
        action = random.choice(actions)

        if random.random() > 0.5:
            prompt = f"{intent} {action}"
        else:
            # 가끔 순서도 바꾸기
            prompt = f"{action} {intent}"

        final_prompt_list.append(prompt)

    for _ in range(int(target_count * 0.2)):
        prompt = random.choice(new_topics)

        # 가끔 변형 어구도 붙이기
        if random.random() > 0.3:
            prompt += f" {random.choice(actions)}"

        final_prompt_list.append(prompt)

    for _ in range(int(target_count * 0.2)):
        prompt = random.choice(off_topic)
        final_prompt_list.append(prompt)

    random.shuffle(final_prompt_list)

    final_prompt_list = final_prompt_list[:target_count]

    return final_prompt_list