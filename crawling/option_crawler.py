"""
option_crawler.py
- option 테이블에 들어갈 옵션 마스터 데이터를 정리하고 MySQL DB에 저장하는 스크립트
"""

from db_config import get_db_connection

# ------------------------------------------------------------
# 1. 옵션 데이터 (카테고리별로 표준화해서 직접 정리)
#    - 실제 차량마다 세부 명칭은 다르지만, 대표적인 옵션명으로 통일
# ------------------------------------------------------------
options_seed = [
    # 안전
    {"option_category": "안전", "option_name": "스마트크루즈컨트롤"},
    {"option_category": "안전", "option_name": "차선유지보조"},
    {"option_category": "안전", "option_name": "전방충돌방지보조"},
    {"option_category": "안전", "option_name": "후방카메라"},
    {"option_category": "안전", "option_name": "어라운드뷰모니터"},
    {"option_category": "안전", "option_name": "스마트하이빔"},
    {"option_category": "안전", "option_name": "후측방충돌방지보조"},

    # 편의
    {"option_category": "편의", "option_name": "열선시트"},
    {"option_category": "편의", "option_name": "통풍시트"},
    {"option_category": "편의", "option_name": "전동시트"},
    {"option_category": "편의", "option_name": "스마트키"},
    {"option_category": "편의", "option_name": "무선충전"},
    {"option_category": "편의", "option_name": "통합제어시스템"},
    {"option_category": "편의", "option_name": "하이패스 시스템"},

    # 외관
    {"option_category": "외관", "option_name": "선루프"},
    {"option_category": "외관", "option_name": "LED헤드램프"},
    {"option_category": "외관", "option_name": "알로이휠"},
    {"option_category": "외관", "option_name": "파노라마선루프"},

    # 인포테인먼트
    {"option_category": "인포테인먼트", "option_name": "내비게이션"},
    {"option_category": "인포테인먼트", "option_name": "프리미엄 오디오"},
    {"option_category": "인포테인먼트", "option_name": "무선 애플카플레이"},
    {"option_category": "인포테인먼트", "option_name": "무선 안드로이드오토"},
    {"option_category": "인포테인먼트", "option_name": "헤드업디스플레이"},

    # 공조
    {"option_category": "공조", "option_name": "자동공조시스템"},
    {"option_category": "공조", "option_name": "뒷좌석송풍구"},
    {"option_category": "공조", "option_name": "공기청정모드"},
]


def insert_options(data):
    """option 리스트를 DB에 저장하는 함수"""
    conn = get_db_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO `option` (option_category, option_name)
        VALUES (%s, %s)
    """

    for o in data:
        cur.execute(sql, (o["option_category"], o["option_name"]))
        print(f"저장 완료: [{o['option_category']}] {o['option_name']}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n총 {len(data)}개 옵션 저장 완료")


if __name__ == "__main__":
    insert_options(options_seed)
