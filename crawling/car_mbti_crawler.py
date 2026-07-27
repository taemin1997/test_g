"""
car_mbti_crawler.py
- car_mbti 테이블(16가지 Carbti 유형)을 정리하고 MySQL DB에 저장하는 스크립트
"""

from db_config import get_db_connection

# ------------------------------------------------------------
# 1. Carbti 16유형 데이터
# ------------------------------------------------------------
car_mbti_seed = [
    {"mbti_id": "ISTJ", "mbti_name": "갓생 정비요정",
     "mbti_description": "첫 도전에 실패란 없다! 기본기에 충실한 갓생 살기 정석 정비요정입니다.",
     "mbti_tags": "#부동의 기본,#가성비 첫차,#첫차의 정석"},

    {"mbti_id": "ISFJ", "mbti_name": "젠틀 배려왕",
     "mbti_description": "내 울타리 안에선 모두가 편안하게. 클래식하고 부드러운 젠틀 배려왕입니다.",
     "mbti_tags": "#세련된 프리미엄,#안락함의 표준,#클래식의 품격"},

    {"mbti_id": "INFJ", "mbti_name": "묵직한 신사",
     "mbti_description": "조용하지만 뿜어져 나오는 아우라! 내면이 깊고 우아한 묵직한 신사입니다.",
     "mbti_tags": "#Quiet Luxury,#우아한 품격,#내면의 품격"},

    {"mbti_id": "INTJ", "mbti_name": "철벽 파수꾼",
     "mbti_description": "과장된 껍데기는 가라, 오직 본질만! 나와 내 가족을 지키는 철벽 파수꾼입니다.",
     "mbti_tags": "#스마트 드라이빙,#이성적 안전,#완벽한 보호"},

    {"mbti_id": "ISTP", "mbti_name": "속도 매니아",
     "mbti_description": "도로를 질주하는 속도 매니아입니다.",
     "mbti_tags": "#성공의 맛,#끝판왕 퍼포먼스,#과묵한 실력파"},

    {"mbti_id": "ISFP", "mbti_name": "정숙 힐러",
     "mbti_description": "내 인생에 스트레스 제로, 잔고장도 제로! 평화와 정숙을 사랑하는 힐러입니다.",
     "mbti_tags": "#하이브리드 정숙,#고장 제로,#마이웨이 힐링"},

    {"mbti_id": "INFP", "mbti_name": "낭만 여행자",
     "mbti_description": "화려하지 않아도 꽉 찬 알맹이, 소박하고 따뜻한 일상을 걷는 낭만 여행자입니다.",
     "mbti_tags": "#탄탄한 기본기,#소박한 낭만,#일상의 여유"},

    {"mbti_id": "INTP", "mbti_name": "얼리어답터 공대장",
     "mbti_description": "이게 바로 바퀴 달린 미래 컴퓨터? 기계와 테크에 진심인 얼리어답터 공대장입니다.",
     "mbti_tags": "#미래지향테크,#바퀴달린 컴퓨터,#얼리어답터 픽"},

    {"mbti_id": "ESTP", "mbti_name": "트렌디 승부사",
     "mbti_description": "지루한 일상은 거부한다! 어디서나 시선을 싹 쓸어 담는 트렌디한 승부사입니다.",
     "mbti_tags": "#스포티 디자인,#트렌디 아이콘,#화려한 승부사"},

    {"mbti_id": "ESFP", "mbti_name": "러블리 파티피플",
     "mbti_description": "오늘 밤 주인공은 나야 나! 톡톡 튀는 독보적 개성의 러블리 파티피플입니다.",
     "mbti_tags": "#독보적 개성,#톡톡튀는 매력,#파티 무드"},

    {"mbti_id": "ENFP", "mbti_name": "에너자이저 탐험가",
     "mbti_description": "작다고 무시 마, 무한 변신 가능! 언제든 차박 떠날 준비 완료된 에너자이저 탐험가입니다.",
     "mbti_tags": "#공간활용 끝판왕,#차박캠핑 마스터,#무한변신매력"},

    {"mbti_id": "ENTP", "mbti_name": "바퀴 달린 혁신가",
     "mbti_description": "상상 그 이상을 현실로! 기존의 모든 틀을 깨부수며 달리는 바퀴 달린 혁신가입니다.",
     "mbti_tags": "#테크이노베이터,#미니멀리즘,#틀을깨는혁신"},

    {"mbti_id": "ESTJ", "mbti_name": "비즈니스 캡틴",
     "mbti_description": "내 사전에 대충이란 없다! 성공 가도를 달리는 철두철미한 비즈니스 캡틴입니다.",
     "mbti_tags": "#성공의 상징,#정통 비즈니스,#철두철미관리"},

    {"mbti_id": "ESFJ", "mbti_name": "다둥이 아빠",
     "mbti_description": "우리가족 너무 사랑해~ 다둥이 아빠입니다.",
     "mbti_tags": "#국민 SUV,#가족사랑 1위,#든든한 패밀리카"},

    {"mbti_id": "ENFJ", "mbti_name": "마당발 반장님",
     "mbti_description": "혼자 가면 외롭잖아, 다 같이 타! 사교 모임을 책임지는 든든한 마당발 반장님입니다.",
     "mbti_tags": "#하이브리드 대세,#사교의 중심,#마당발 반장"},

    {"mbti_id": "ENTJ", "mbti_name": "리드하는 야망가",
     "mbti_description": "앞만 보고 달린다! 열정과 주행의 재미로 세상을 리드하는 야망가입니다.",
     "mbti_tags": "#주행의 즐거움,#열정적 리더,#거침없는 질주"},
]


def insert_car_mbti(data):

    conn = get_db_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO car_mbti (mbti_id, mbti_name, mbti_description, mbti_tags)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            mbti_name = VALUES(mbti_name),
            mbti_description = VALUES(mbti_description),
            mbti_tags = VALUES(mbti_tags)
    """

    for c in data:
        cur.execute(
            sql,
            (c["mbti_id"], c["mbti_name"], c["mbti_description"], c["mbti_tags"]),
        )
        print(f"저장 완료: {c['mbti_id']} - {c['mbti_name']} ({c['mbti_tags']})")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n총 {len(data)}개 Carbti 유형 저장 완료")


if __name__ == "__main__":
    insert_car_mbti(car_mbti_seed)
