
# %%
# ============================================================
# 셀 1. 라이브러리 가져오기 및 Streamlit 페이지 기본 설정
# ============================================================

# Streamlit 라이브러리를 가져옵니다.
# 이후 streamlit이라는 긴 이름 대신 st라는 짧은 이름으로 사용합니다.
import html
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd
import pymysql
from PIL import Image, ImageDraw, ImageFont, ImageOps
import streamlit as st

from crawling.db_config import ensure_schema, get_db_connection

# 브라우저 탭에 표시되는 제목, 아이콘, 화면 폭을 설정합니다.
#
# 주의:
# st.set_page_config()는 Streamlit 명령 중 가장 먼저 실행되어야 합니다.
# 따라서 함수 내부보다 파일 상단에 두는 편이 이해하기 쉽습니다.
st.set_page_config(
    page_title="성향 검사",
    page_icon="📝",
    layout="wide",
)


# ------------------------------------------------------------
# DB 연결 헬퍼
#   - db_config.get_db_connection()으로 pymysql 커넥션을 얻고,
#   - 쿼리 결과를 pandas DataFrame으로 돌려줘서
#     기존 st.connection(...).query(...) 결과(DataFrame)를 쓰던
#     아래쪽 코드(.iloc, .columns, .empty, .to_dict("records") 등)를
#     그대로 재사용할 수 있게 합니다.
#   - 쿼리 문자열의 파라미터는 SQLAlchemy 스타일(:name) 대신
#     pymysql pyformat 스타일(%(name)s)을 사용합니다.
# ------------------------------------------------------------
@st.cache_resource
def _init_schema():
    """앱이 처음 뜰 때(또는 인스턴스가 새로 뜰 때) 딱 한 번만 스키마를 보장합니다."""
    ensure_schema()
    return True


_init_schema()


def _run_query(sql, params=None):
    """SELECT 쿼리를 실행하고 결과를 pandas DataFrame으로 반환합니다."""
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(sql, params or {})
            rows = cur.fetchall()
    finally:
        conn.close()
    return pd.DataFrame(rows)


# %%
# ============================================================
# 셀 2. 질문 데이터와 결과 데이터 정의
# ============================================================

# QUESTIONS는 검사에서 사용할 전체 질문 목록입니다.
#
# 각 질문은 다음 정보를 가집니다.
# id       : 질문을 구분하는 고유 번호
# text     : 사용자에게 표시할 질문
# choices  : 선택지 목록
#
# 각 선택지는 다음 정보를 가집니다.
# text     : 사용자에게 표시할 선택지 문구
# scores   : 이 선택지를 골랐을 때 증가할 점수

QUESTIONS = [{'id': 1,
  'text': '주말 드라이브를 떠날 때, 내가 생각하는 가장 이상적인 인원은?',
  'choices': [{'text': '친구나 가족들을 가득 태우고 시끌벅적하게 떠나는 여행', 'scores': {'E': 1}},
              {'text': '혼자 조용히 생각에 잠기거나 연인과 단둘이 오붓하게 즐기는 시간', 'scores': {'I': 1}}]},
 {'id': 2,
  'text': '차 안에서 음악을 들을 때 나의 드라이빙 스타일은?',
  'choices': [{'text': '창문을 살짝 열고 베이스를 울리며 내 신나는 흥을 밖으로 분출!', 'scores': {'E': 1}},
              {'text': '방음이 잘된 차 안에서 조용히 나만의 감성 플레이리스트에 몰입', 'scores': {'I': 1}}]},
 {'id': 3,
  'text': '내가 가장 중요하게 생각하는 차량 내부 공간은?',
  'choices': [{'text': '캠핑 매트를 깔거나 큰 짐을 가득 실을 수 있는 넓고 광활한 트렁크 공간', 'scores': {'E': 1}},
              {'text': '앰비언트 라이트와 안락한 가죽 시트가 나를 감싸주는 운전석 콕핏 공간', 'scores': {'I': 1}}]},
 {'id': 4,
  'text': '기다리던 새 차를 드디어 출고받았을 때, 내가 가장 먼저 하고 싶은 일은?',
  'choices': [{'text': '지인들 단톡방에 인증샷을 올리고 친구들을 태워 밤바다 보러 가기', 'scores': {'E': 1}},
              {'text': '인적이 드문 한적한 교외 도로로 나가 차의 고요한 주행감을 혼자 음미하기', 'scores': {'I': 1}}]},
 {'id': 5,
  'text': '꽉 막히는 헬게이트 도로 위 정체에 갇혔을 때, 나의 행동은?',
  'choices': [{'text': '동승자와 쉴 새 없이 수다를 떨거나 전화 통화를 하며 지루함을 달랜다', 'scores': {'E': 1}},
              {'text': '라디오, 팟캐스트를 잔잔하게 틀어놓고 혼자만의 사색 시간을 즐긴다', 'scores': {'I': 1}}]},
 {'id': 6,
  'text': '차를 살 때 내가 가장 먼저 꼼꼼하게 뜯어보는 데이터 지표는?',
  'choices': [{'text': "리터당 연비, 자동차세, 부품값, 중고차 감가상각 등 '유지비 지표'", 'scores': {'S': 1}},
              {'text': "자율주행 등급, OTA(무선 업데이트) 기능, 배터리 플랫폼 등 '최신 테크 지표'", 'scores': {'N': 1}}]},
 {'id': 7,
  'text': '완벽하게 새로운 개념의 신형 전기차가 출시되었다는 뉴스를 보았을 때 내 생각은?',
  'choices': [{'text': '"충전소 인프라나 겨울철 배터리 방전 문제는 해결됐나? 난 검증된 하이브리드가 편해."', 'scores': {'S': 1}},
              {'text': '"와, 엔진이 사라지고 완전히 디지털로 통제되네! 이게 미래지, 당장 타보고 싶다."', 'scores': {'N': 1}}]},
 {'id': 8,
  'text': '내가 생각하는 주유(또는 충전)의 가장 유쾌한 경험은?',
  'choices': [{'text': '오피넷 앱으로 주변에서 가장 기름값이 싼 주유소를 찾아 알뜰하게 채웠을 때', 'scores': {'S': 1}},
              {'text': '충전기를 꽂아두고 차 안에서 대형 스크린으로 OTT를 보며 미래 라이프를 즐길 때', 'scores': {'N': 1}}]},
 {'id': 9,
  'text': '내가 선호하는 차량 계기판(클러스터)의 디자인 스타일은?',
  'choices': [{'text': '속도와 RPM이 직관적으로 팍팍 보이는 클래식하고 선명한 디자인', 'scores': {'S': 1}},
              {'text': '스마트폰 화면처럼 위젯을 맘대로 배치하고 증강현실(AR) 지도가 펼쳐지는 디자인', 'scores': {'N': 1}}]},
 {'id': 10,
  'text': '나에게 자동차란 어떤 존재에 더 가까운가?',
  'choices': [{'text': '기름을 넣고 주기적으로 소모품을 갈아주며 타는 정통 기계공학의 결정체', 'scores': {'S': 1}},
              {'text': '주기적으로 소프트웨어가 업데이트되는 바퀴 달린 스마트 디바이스', 'scores': {'N': 1}}]},
 {'id': 11,
  'text': '친구가 "나 이번에 디자인이 진짜 미친 차 계약했어!"라고 자랑할 때 나의 첫 마디는?',
  'choices': [{'text': '"오 축하해! 근데 그거 배기량이랑 연비는 얼마나 나와? 할인은 좀 해준대?"', 'scores': {'T': 1}},
              {'text': '"우와 대박! 무슨 색상 샀어? 디자인 진짜 예쁘더라, 너랑 찰떡이겠다!"', 'scores': {'F': 1}}]},
 {'id': 12,
  'text': '시승센터에서 차량을 직접 운전해 볼 때, 내가 가장 예민하게 체감하는 부분은?',
  'choices': [{'text': '엑셀을 밟을 때의 마력과 토크, 브레이크 제동력, 코너링 시 서스펜션의 밸런스', 'scores': {'T': 1}},
              {'text': '문을 닫을 때의 묵직한 소리, 가죽 시트의 부드러운 촉감과 실내의 아늑한 분위기', 'scores': {'F': 1}}]},
 {'id': 13,
  'text': '주차장에 세워둔 내 차에 미세한 문콕이나 긁힘 자국을 발견했을 때 나의 반응은?',
  'choices': [{'text': '즉시 블랙박스를 확인해 범인을 찾거나, 컴파운드로 지워질지 견적부터 계산한다', 'scores': {'T': 1}},
              {'text': '가슴이 찢어지는 것처럼 속상하고, 내 소중한 차에게 미안한 감정이 먼저 몰려온다', 'scores': {'F': 1}}]},
 {'id': 14,
  'text': '차량 옵션을 추가할 때, 돈이 아깝지 않다고 느끼는 기준은?',
  'choices': [{'text': 'HUD(헤드업 디스플레이), 통풍 시트 등 운전의 편의성을 높여주는 실용적인 옵션', 'scores': {'T': 1}},
              {'text': '파노라마 선루프, 실내 고급 내장재 등 차의 멋과 감성을 극대화해 주는 옵션', 'scores': {'F': 1}}]},
 {'id': 15,
  'text': '도로 위에서 내 차를 바라보는 사람들의 시선(하차감)에 대해 나는?',
  'choices': [{'text': '타인의 시선은 전혀 신경 쓰지 않는다. 내가 만족하고 고장 안 나면 그만이다', 'scores': {'T': 1}},
              {'text': '브랜딩이 주는 이미지도 중요하다. 내 가치관이나 취향을 대변해 주는 느낌이 좋다', 'scores': {'F': 1}}]},
 {'id': 16,
  'text': '드라이브를 떠나기 전, 내비게이션을 조작하는 나의 타이밍은?',
  'choices': [{'text': '출발 전 미리 최적 경로, 예상 통행료, 목적지 주차장 위치까지 완벽하게 확인 후 시동을 건다', 'scores': {'J': 1}},
              {'text': '일단 시동을 걸고 목적지만 대충 찍고 출발한 뒤, 가면서 경로를 수정한다', 'scores': {'P': 1}}]},
 {'id': 17,
  'text': "자동차 모델을 최종 결정할 때, 매달 집계되는 '국내 판매량 순위'를 보는 나의 태도는?",
  'choices': [{'text': '"사람들이 많이 사는 데는 다 이유가 있지." 판매량 상위권의 실패 없는 대중적인 차를 고른다', 'scores': {'J': 1}},
              {'text': '"도로에 흔해 빠진 클론 차는 싫어." 판매량이 낮더라도 나만의 개성을 보여줄 희소성 있는 차를 고른다',
               'scores': {'P': 1}}]},
 {'id': 18,
  'text': '내 차의 세차 및 엔진오일 등 소모품을 관리하는 스타일은?',
  'choices': [{'text': '매월 정기 세차 날짜를 정해두거나, 주행거리 달력을 만들어 주기적으로 정비소에 간다', 'scores': {'J': 1}},
              {'text': '차가 눈에 띄게 더러워지면 번개 세차를 하고, 계기판에 경고등이 뜨면 그제야 정비소에 간다', 'scores': {'P': 1}}]},
 {'id': 19,
  'text': '수천만 원짜리 자동차의 계약서에 도장을 찍기까지 나의 의사결정 과정은?',
  'choices': [{'text': '몇 달 전부터 예산을 철저히 짜고, 경쟁 모델 시승 예약을 다 돌며 계획대로 구매한다', 'scores': {'J': 1}},
              {'text': '평소 마음에 두던 모델의 기습 프로모션 할인이나 파격 조건이 뜨면 "이건 기회다" 하고 지른다',
               'scores': {'P': 1}}]},
 {'id': 20,
  'text': '조수석에 탄 친구가 갑자기 "우리 원래 가려던 곳 말고, 바다 보러 핸들 꺾을까?"라고 한다면?',
  'choices': [{'text': '원래 계획했던 맛집 예약이나 일정이 꼬여서 속으로 살짝 스트레스를 받거나 당황한다', 'scores': {'J': 1}},
              {'text': '"오 완전 대박! 콜!"을 외치며 신나게 경로를 변경해 새로운 드라이브를 즐긴다', 'scores': {'P': 1}}]}]




# RESULT_PROFILES는 점수 계산 결과와 car_mbti의 기본키를 연결합니다.
#
# mbti_id는 car_mbti.mbti_id와 반드시 같아야 합니다.
# PDF의 4개 기준에서 계산되는 16개 MBTI 코드를 사용합니다.
# car_mbti.mbti_id에도 같은 4글자 코드가 저장되어 있어야 합니다.
RESULT_PROFILES = [{'mbti_id': 'ISTJ'},
 {'mbti_id': 'ISFJ'},
 {'mbti_id': 'INFJ'},
 {'mbti_id': 'INTJ'},
 {'mbti_id': 'ISTP'},
 {'mbti_id': 'ISFP'},
 {'mbti_id': 'INFP'},
 {'mbti_id': 'INTP'},
 {'mbti_id': 'ESTP'},
 {'mbti_id': 'ESFP'},
 {'mbti_id': 'ENFP'},
 {'mbti_id': 'ENTP'},
 {'mbti_id': 'ESTJ'},
 {'mbti_id': 'ESFJ'},
 {'mbti_id': 'ENFJ'},
 {'mbti_id': 'ENTJ'}]




CAR_MBTI_QUERY = """
SELECT
    mbti_id,
    mbti_name,
    mbti_description,
    mbti_tags
FROM car_mbti
WHERE mbti_id = %(mbti_id)s
"""

CAR_MBTI_BASE_QUERY = """
SELECT
    mbti_id,
    mbti_name,
    mbti_description
FROM car_mbti
WHERE mbti_id = %(mbti_id)s
"""

CAR_RECOMMEND_QUERY = """
SELECT
    cr.recom_car_rank,
    cr.recom_reason,
    v.vehicle_id,
    v.vehicle_name,
    v.body_type,
    v.car_img,
    v.car_description,
    v.vec_purpose,
    m.manufacturer_name
FROM car_recommend AS cr
JOIN vehicle AS v
    ON v.vehicle_id = cr.vehicle_id
LEFT JOIN manufacturer AS m
    ON m.manufacturer_id = v.manufacturer_id
WHERE cr.mbti_id = %(mbti_id)s
ORDER BY cr.recom_car_rank
"""

CAR_RECOMMEND_VEHICLE_ID_QUERY = """
SELECT
    cr.vehicle_id
FROM car_recommend AS cr
WHERE cr.mbti_id = %(mbti_id)s
  AND cr.recom_car_rank = %(vehicle_rank)s
ORDER BY cr.recom_id DESC
LIMIT 1
"""

# Project_carbti_design.pptx 8~23페이지의 MBTI별 1~3위 차량 명세입니다.
# DB의 오래된 추천 행이나 중복 행이 있더라도 이 순서로 결과를 정렬합니다.
PPT_RESULT_VEHICLES = {
    "ISTJ": (
        (1, "현대자동차", "아반떼"),
        (2, "렉서스", "ES"),
        (3, "현대자동차", "그랜저"),
    ),
    "ISFJ": (
        (1, "메르세데스-벤츠", "E클래스"),
        (2, "제네시스", "G80"),
        (3, "BMW", "5시리즈"),
    ),
    "INFJ": (
        (1, "제네시스", "G80"),
        (2, "메르세데스-벤츠", "E클래스"),
        (3, "현대자동차", "그랜저"),
    ),
    "INTJ": (
        (1, "볼보", "XC60"),
        (2, "폭스바겐", "티구안"),
        (3, "제네시스", "GV70"),
    ),
    "ISTP": (
        (1, "포르쉐", "카이엔"),
        (2, "BMW", "5시리즈"),
        (3, "제네시스", "GV70"),
    ),
    "ISFP": (
        (1, "렉서스", "ES"),
        (2, "제네시스", "G80"),
        (3, "현대자동차", "아반떼"),
    ),
    "INFP": (
        (1, "폭스바겐", "티구안"),
        (2, "볼보", "XC60"),
        (3, "기아", "쏘렌토"),
    ),
    "INTP": (
        (1, "현대자동차", "아이오닉5"),
        (2, "테슬라", "Model Y"),
        (3, "기아", "레이"),
    ),
    "ESTP": (
        (1, "제네시스", "GV70"),
        (2, "포르쉐", "카이엔"),
        (3, "BMW", "5시리즈"),
    ),
    "ESFP": (
        (1, "미니", "쿠퍼"),
        (2, "기아", "레이"),
        (3, "테슬라", "Model Y"),
    ),
    "ENFP": (
        (1, "기아", "레이"),
        (2, "현대자동차", "아이오닉5"),
        (3, "미니", "쿠퍼"),
    ),
    "ENTP": (
        (1, "테슬라", "Model Y"),
        (2, "현대자동차", "아이오닉5"),
        (3, "제네시스", "GV70"),
    ),
    "ESTJ": (
        (1, "현대자동차", "그랜저"),
        (2, "제네시스", "G80"),
        (3, "기아", "쏘렌토"),
    ),
    "ESFJ": (
        (1, "기아", "쏘렌토"),
        (2, "기아", "카니발"),
        (3, "현대자동차", "그랜저"),
    ),
    "ENFJ": (
        (1, "기아", "카니발"),
        (2, "기아", "쏘렌토"),
        (3, "볼보", "XC60"),
    ),
    "ENTJ": (
        (1, "BMW", "5시리즈"),
        (2, "메르세데스-벤츠", "E클래스"),
        (3, "포르쉐", "카이엔"),
    ),
}

# 최신 car_mbti_crawler.py와 동일한 화면 안전용 기본 정보입니다.
# DB 조회가 실패해도 테이블·컬럼명이 사용자 화면에 노출되지 않게 합니다.
CAR_MBTI_FALLBACKS = {'ISTJ': {'mbti_name': '갓생 정비요정',
          'mbti_description': '첫 도전에 실패란 없다! 기본기에 충실한 갓생 살기 정석 정비요정입니다.',
          'mbti_tags': '#부동의 기본,#가성비 첫차,#첫차의 정석'},
 'ISFJ': {'mbti_name': '젠틀 배려왕',
          'mbti_description': '내 울타리 안에선 모두가 편안하게. 클래식하고 부드러운 젠틀 배려왕입니다.',
          'mbti_tags': '#세련된 프리미엄,#안락함의 표준,#클래식의 품격'},
 'INFJ': {'mbti_name': '묵직한 신사',
          'mbti_description': '조용하지만 뿜어져 나오는 아우라! 내면이 깊고 우아한 묵직한 신사입니다.',
          'mbti_tags': '#Quiet Luxury,#우아한 품격,#내면의 품격'},
 'INTJ': {'mbti_name': '철벽 파수꾼',
          'mbti_description': '과장된 껍데기는 가라, 오직 본질만! 나와 내 가족을 지키는 철벽 파수꾼입니다.',
          'mbti_tags': '#스마트 드라이빙,#이성적 안전,#완벽한 보호'},
 'ISTP': {'mbti_name': '속도 매니아',
          'mbti_description': '도로를 질주하는 속도 매니아입니다.',
          'mbti_tags': '#성공의 맛,#끝판왕 퍼포먼스,#과묵한 실력파'},
 'ISFP': {'mbti_name': '정숙 힐러',
          'mbti_description': '내 인생에 스트레스 제로, 잔고장도 제로! 평화와 정숙을 사랑하는 힐러입니다.',
          'mbti_tags': '#하이브리드 정숙,#고장 제로,#마이웨이 힐링'},
 'INFP': {'mbti_name': '낭만 여행자',
          'mbti_description': '화려하지 않아도 꽉 찬 알맹이, 소박하고 따뜻한 일상을 걷는 낭만 여행자입니다.',
          'mbti_tags': '#탄탄한 기본기,#소박한 낭만,#일상의 여유'},
 'INTP': {'mbti_name': '얼리어답터 공대장',
          'mbti_description': '이게 바로 바퀴 달린 미래 컴퓨터? 기계와 테크에 진심인 얼리어답터 공대장입니다.',
          'mbti_tags': '#미래지향테크,#바퀴달린 컴퓨터,#얼리어답터 픽'},
 'ESTP': {'mbti_name': '트렌디 승부사',
          'mbti_description': '지루한 일상은 거부한다! 어디서나 시선을 싹 쓸어 담는 트렌디한 승부사입니다.',
          'mbti_tags': '#스포티 디자인,#트렌디 아이콘,#화려한 승부사'},
 'ESFP': {'mbti_name': '러블리 파티피플',
          'mbti_description': '오늘 밤 주인공은 나야 나! 톡톡 튀는 독보적 개성의 러블리 파티피플입니다.',
          'mbti_tags': '#독보적 개성,#톡톡튀는 매력,#파티 무드'},
 'ENFP': {'mbti_name': '에너자이저 탐험가',
          'mbti_description': '작다고 무시 마, 무한 변신 가능! 언제든 차박 떠날 준비 완료된 에너자이저 탐험가입니다.',
          'mbti_tags': '#공간활용 끝판왕,#차박캠핑 마스터,#무한변신매력'},
 'ENTP': {'mbti_name': '바퀴 달린 혁신가',
          'mbti_description': '상상 그 이상을 현실로! 기존의 모든 틀을 깨부수며 달리는 바퀴 달린 혁신가입니다.',
          'mbti_tags': '#테크이노베이터,#미니멀리즘,#틀을깨는혁신'},
 'ESTJ': {'mbti_name': '비즈니스 캡틴',
          'mbti_description': '내 사전에 대충이란 없다! 성공 가도를 달리는 철두철미한 비즈니스 캡틴입니다.',
          'mbti_tags': '#성공의 상징,#정통 비즈니스,#철두철미관리'},
 'ESFJ': {'mbti_name': '다둥이 아빠',
          'mbti_description': '우리가족 너무 사랑해~ 다둥이 아빠입니다.',
          'mbti_tags': '#국민 SUV,#가족사랑 1위,#든든한 패밀리카'},
 'ENFJ': {'mbti_name': '마당발 반장님',
          'mbti_description': '혼자 가면 외롭잖아, 다 같이 타! 사교 모임을 책임지는 든든한 마당발 반장님입니다.',
          'mbti_tags': '#하이브리드 대세,#사교의 중심,#마당발 반장'},
 'ENTJ': {'mbti_name': '리드하는 야망가',
          'mbti_description': '앞만 보고 달린다! 열정과 주행의 재미로 세상을 리드하는 야망가입니다.',
          'mbti_tags': '#주행의 즐거움,#열정적 리더,#거침없는 질주'}}

VEHICLE_BY_NAME_QUERY = """
SELECT
    v.vehicle_id,
    v.vehicle_name,
    v.body_type,
    v.car_img,
    v.car_description,
    v.vec_purpose,
    m.manufacturer_name
FROM vehicle AS v
JOIN manufacturer AS m
    ON m.manufacturer_id = v.manufacturer_id
WHERE m.manufacturer_name = %(manufacturer_name)s
  AND v.vehicle_name = %(vehicle_name)s
"""

VEHICLE_QUERY = """
SELECT
    v.vehicle_id,
    v.vehicle_name,
    v.body_type,
    v.car_img,
    v.car_description,
    v.vec_purpose,
    v.new_car_url,
    v.used_car_url,
    m.manufacturer_id,
    m.manufacturer_name,
    m.country,
    m.logo_url,
    m.official_url
FROM vehicle AS v
JOIN manufacturer AS m
    ON m.manufacturer_id = v.manufacturer_id
WHERE v.vehicle_id = %(vehicle_id)s
"""

VEHICLE_DETAIL_QUERY = """
SELECT
    detail_id,
    detail_trim_name,
    detail_fuel_type,
    detail_displacement,
    detail_horsepower,
    detail_transmission,
    detail_drive_type,
    detail_seat_count,
    detail_base_price,
    detail_fuel_efficiency
FROM vehicle_detail
WHERE vehicle_id = %(vehicle_id)s
ORDER BY detail_base_price, detail_id
"""

VEHICLE_OPTION_QUERY = """
SELECT
    vd.detail_id,
    vd.detail_trim_name,
    o.option_category,
    o.option_name
FROM vehicle_detail AS vd
JOIN vehicle_option AS vo
    ON vo.detail_id = vd.detail_id
JOIN `option` AS o
    ON o.option_id = vo.option_id
WHERE vd.vehicle_id = %(vehicle_id)s
ORDER BY vd.detail_id, o.option_category, o.option_name
"""

VEHICLE_SALES_QUERY = """
SELECT
    sales_year,
    sales_month,
    sales_count,
    sales_avg_price
FROM sales_stat
WHERE vehicle_id = %(vehicle_id)s
ORDER BY sales_year, sales_month
"""

VEHICLE_NEWS_QUERY = """
SELECT
    news_id,
    title,
    summary,
    news_url,
    news_img,
    news_category,
    publish_date
FROM news
WHERE vehicle_id = %(vehicle_id)s
ORDER BY publish_date DESC, news_id DESC
"""

VEHICLE_RECOMMEND_REASON_QUERY = """
SELECT
    recom_reason
FROM car_recommend
WHERE vehicle_id = %(vehicle_id)s
  AND (%(mbti_id)s IS NULL OR mbti_id = %(mbti_id)s)
ORDER BY
    CASE WHEN mbti_id = %(mbti_id)s THEN 0 ELSE 1 END,
    recom_car_rank
LIMIT 1
"""



class MbtiDataError(RuntimeError):
    """car_mbti 조회 또는 데이터 검증 실패."""


class VehicleDataError(RuntimeError):
    """차량 상세 정보 조회 또는 데이터 검증 실패."""


def load_result_data(mbti_id):
    """MBTI 설명·태그와 PPT 명세에 맞는 추천 차량 1~3위를 조회합니다."""

    params = {"mbti_id": mbti_id}
    try:
        mbti_rows = _run_query(CAR_MBTI_QUERY, params)
    except Exception:
        # 아직 mbti_tags 마이그레이션이 적용되지 않은 DB도 기본 정보는 조회합니다.
        try:
            mbti_rows = _run_query(CAR_MBTI_BASE_QUERY, params).copy()
        except Exception as error:
            raise MbtiDataError(
                "car_mbti 테이블 조회에 실패했습니다."
            ) from error
        mbti_rows["mbti_tags"] = ""

    try:
        recommendation_rows = _run_query(CAR_RECOMMEND_QUERY, params)
    except Exception as error:
        raise MbtiDataError(
            "car_recommend와 차량 연결 테이블 조회에 실패했습니다."
        ) from error

    mbti_columns = {
        "mbti_id",
        "mbti_name",
        "mbti_description",
        "mbti_tags",
    }
    missing_mbti_columns = mbti_columns.difference(mbti_rows.columns)
    if missing_mbti_columns:
        raise MbtiDataError(
            "car_mbti 필수 컬럼이 없습니다: "
            + ", ".join(sorted(missing_mbti_columns))
        )
    if len(mbti_rows) != 1:
        raise MbtiDataError(
            f"car_mbti에서 {mbti_id} 결과를 정확히 1개 찾지 못했습니다."
        )

    recommendation_columns = {
        "recom_car_rank",
        "recom_reason",
        "vehicle_id",
        "vehicle_name",
        "body_type",
        "car_img",
        "car_description",
        "vec_purpose",
        "manufacturer_name",
    }
    missing_recommendation_columns = recommendation_columns.difference(
        recommendation_rows.columns
    )
    if missing_recommendation_columns:
        raise MbtiDataError(
            "추천 차량 조회 필수 컬럼이 없습니다: "
            + ", ".join(sorted(missing_recommendation_columns))
        )

    def clean_text(value):
        if value is None or str(value).lower() == "nan":
            return ""
        return str(value)

    mbti_record = mbti_rows.iloc[0]
    fallback_mbti = CAR_MBTI_FALLBACKS[mbti_id]
    mbti = {
        "mbti_name": (
            clean_text(mbti_record["mbti_name"])
            or fallback_mbti["mbti_name"]
        ),
        "mbti_description": (
            clean_text(mbti_record["mbti_description"])
            or fallback_mbti["mbti_description"]
        ),
        "mbti_tags": (
            clean_text(mbti_record["mbti_tags"])
            or fallback_mbti["mbti_tags"]
        ),
    }

    if len(recommendation_rows) != 3:
        raise MbtiDataError(
            f"car_recommend에서 {mbti_id}의 추천 차량을 "
            f"3개 찾지 못했습니다: {len(recommendation_rows)}개"
        )

    recommendations = []
    seen_ranks = set()
    for recommendation in recommendation_rows.to_dict("records"):
        try:
            rank = int(recommendation["recom_car_rank"])
            vehicle_id = int(recommendation["vehicle_id"])
        except (TypeError, ValueError) as error:
            raise MbtiDataError(
                f"{mbti_id} 추천 차량의 순위 또는 vehicle_id가 올바르지 않습니다."
            ) from error

        if rank not in {1, 2, 3} or rank in seen_ranks:
            raise MbtiDataError(
                f"{mbti_id} 추천 순위는 중복 없이 1~3위여야 합니다."
            )

        seen_ranks.add(rank)
        recommendation["recom_car_rank"] = rank
        recommendation["vehicle_id"] = vehicle_id
        for column_name in recommendation_columns.difference(
            {"recom_car_rank", "vehicle_id"}
        ):
            recommendation[column_name] = clean_text(
                recommendation.get(column_name)
            )
        recommendations.append(recommendation)

    if seen_ranks != {1, 2, 3}:
        raise MbtiDataError(
            f"{mbti_id} 추천 순위 1~3위가 모두 필요합니다: "
            f"{sorted(seen_ranks)}"
        )

    recommendations.sort(key=lambda item: item["recom_car_rank"])

    vehicle_ids = [
        int(recommendation["vehicle_id"])
        for recommendation in recommendations
    ]
    if len(vehicle_ids) != 3 or len(set(vehicle_ids)) != 3:
        raise MbtiDataError(
            f"{mbti_id} 추천 차량 1~3위가 서로 달라야 합니다: "
            f"{vehicle_ids}"
        )

    return mbti, recommendations



def resolve_result_vehicle_id(mbti_id, vehicle_rank):
    """car_recommend의 MBTI·순위 관계로 실제 vehicle_id를 조회합니다."""

    try:
        rank = int(vehicle_rank)
    except (TypeError, ValueError) as error:
        raise VehicleDataError("추천 차량 순위가 올바르지 않습니다.") from error

    if rank not in {1, 2, 3}:
        raise VehicleDataError("추천 차량 순위는 1~3위여야 합니다.")

    try:
        vehicle_rows = _run_query(
            CAR_RECOMMEND_VEHICLE_ID_QUERY,
            {
                "mbti_id": mbti_id,
                "vehicle_rank": rank,
            },
        )
    except Exception as error:
        raise VehicleDataError(
            f"{mbti_id} {rank}위 차량의 DB 관계 조회에 실패했습니다."
        ) from error

    if len(vehicle_rows) != 1:
        raise VehicleDataError(
            f"car_recommend에서 {mbti_id} {rank}위 차량을 찾지 못했습니다."
        )

    try:
        return int(vehicle_rows.iloc[0]["vehicle_id"])
    except (KeyError, TypeError, ValueError) as error:
        raise VehicleDataError(
            f"{mbti_id} {rank}위 차량의 vehicle_id가 올바르지 않습니다."
        ) from error

def load_vehicle_data(vehicle_id):
    """vehicle_id와 연결된 차량·제원·옵션·판매·뉴스 정보를 조회합니다."""

    params = {"vehicle_id": int(vehicle_id)}
    try:
        vehicle_rows = _run_query(VEHICLE_QUERY, params)
        detail_rows = _run_query(VEHICLE_DETAIL_QUERY, params)
        option_rows = _run_query(VEHICLE_OPTION_QUERY, params)
        sales_rows = _run_query(VEHICLE_SALES_QUERY, params)
        news_rows = _run_query(VEHICLE_NEWS_QUERY, params)
        recommendation_rows = _run_query(
            VEHICLE_RECOMMEND_REASON_QUERY,
            {
                "vehicle_id": int(vehicle_id),
                "mbti_id": st.session_state.get("user_mbti") or None,
            },
        )
    except Exception as error:
        raise VehicleDataError(
            "선택한 차량의 상세 정보를 조회하지 못했습니다."
        ) from error

    if len(vehicle_rows) != 1:
        raise VehicleDataError(
            f"vehicle_id={vehicle_id}인 차량을 정확히 1개 찾지 못했습니다."
        )

    vehicle = vehicle_rows.iloc[0].to_dict()
    for key, value in vehicle.items():
        if value is None or str(value).lower() == "nan":
            vehicle[key] = ""

    return {
        "vehicle": vehicle,
        "details": detail_rows,
        "options": option_rows,
        "sales": sales_rows,
        "news": news_rows,
        "recommendation": recommendation_rows,
    }


def has_display_value(value):
    """DB의 NULL·NaN·빈 문자열을 화면에 표시하지 않도록 판별합니다."""

    return (
        value is not None
        and str(value).strip()
        and str(value).lower() not in {"nan", "none", "<na>"}
    )


# %%
# ============================================================
# 셀 3. Streamlit 세션 상태 초기화
# ============================================================

def initialize_session_state():
    """검사 진행에 필요한 세션 상태의 기본값을 설정합니다."""

    if "page" not in st.session_state:
        st.session_state.page = "main"

    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    if "user_scores" not in st.session_state:
        st.session_state.user_scores = {
            "E": 0,
            "I": 0,
            "S": 0,
            "N": 0,
            "T": 0,
            "F": 0,
            "J": 0,
            "P": 0,
        }

    if "user_mbti" not in st.session_state:
        st.session_state.user_mbti = ""

    if "ranked_results" not in st.session_state:
        st.session_state.ranked_results = []

    if "selected_vehicle_id" not in st.session_state:
        st.session_state.selected_vehicle_id = None

    if "selected_vehicle_rank" not in st.session_state:
        st.session_state.selected_vehicle_rank = None



# %%
# ============================================================
# 셀 4. 공통 페이지 이동 및 검사 초기화 함수
# ============================================================

def change_page(page_name):
    """
    현재 화면을 page_name에 해당하는 화면으로 변경합니다.

    page_name 예:
    - "main"
    - "question"
    - "result"
    - "vehicle_detail"
    """

    # 다음에 표시할 페이지 이름을 저장합니다.
    st.session_state.page = page_name

    # Streamlit 파일 전체를 즉시 다시 실행합니다.
    #
    # 다시 실행되면 메인 라우터가 session_state.page를 확인하고
    # 변경된 페이지 함수를 호출합니다.
    st.rerun()


def reset_test():
    """
    현재 검사 진행 상태를 모두 삭제하고 처음 화면으로 돌아갑니다.

    결과 화면에서 '다시 검사' 버튼을 눌렀을 때 사용합니다.
    """

    # 차량 상세 화면에서 사용한 URL 파라미터도 함께 삭제합니다.
    st.query_params.clear()

    # 현재 세션에 저장된 모든 key를 하나씩 삭제합니다.
    #
    # list()로 복사하는 이유:
    # 반복 중인 딕셔너리의 항목을 바로 삭제하면 오류가 발생할 수 있기 때문입니다.
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # 모든 값이 삭제됐으므로 기본 상태를 다시 생성합니다.
    initialize_session_state()

    # 초기화된 상태로 화면을 다시 실행합니다.
    st.rerun()

# %%
# ============================================================
# 셀 5. 최초 진입 화면
# ============================================================

def render_main_page():
    """
    사용자가 애플리케이션에 처음 진입했을 때 표시되는 화면입니다.
    """

    # 페이지의 가장 큰 제목을 출력합니다.
    st.title("성향 검사")

    # 검사에 대한 간단한 설명을 출력합니다.
    st.write(
        "질문에 답하면 사용자의 점수를 계산하고, "
        "가장 가까운 성향 유형을 순서대로 보여줍니다."
    )

    # QUESTIONS 리스트 길이를 이용해 전체 질문 수를 표시합니다.
    st.info(f"전체 질문 수: {len(QUESTIONS)}개")

    # 버튼을 누르면 질문 화면으로 이동합니다.
    if st.button(
        "검사 시작",
        width="stretch",
    ):
        # 첫 번째 질문부터 시작하도록 질문 번호를 0으로 설정합니다.
        st.session_state.question_index = 0

        # 페이지 상태를 question으로 변경합니다.
        change_page("question")

# %%
# ============================================================
# 셀 6. 질문 화면
# ============================================================


def render_sticky_question_progress(
    progress_value,
    start_question,
    end_question,
    total_questions,
):
    """스크롤해도 고정되고 차량이 진행률을 따라가는 진행 바입니다."""

    percentage = max(0.0, min(100.0, progress_value * 100))
    st.html(
        f"""
<style>
div[data-testid="stElementContainer"]:has(.carbti-sticky-progress) {{
  position: sticky;
  top: 3.75rem;
  z-index: 1000;
  overflow: visible;
}}
.carbti-sticky-progress {{
  padding: 0.75rem 1rem 0.65rem;
  border: 1px solid var(--st-border-color, #D1D5DB);
  border-radius: 16px;
  background: var(--st-background-color, #FFFFFF);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.14);
  overflow: visible;
  isolation: isolate;
}}
.carbti-progress-labels {{
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  color: var(--st-text-color);
  font-size: 0.82rem;
  font-weight: 650;
}}
.carbti-progress-rail {{
  position: relative;
  padding-top: 1.75rem;
}}
.carbti-progress-car {{
  position: absolute;
  top: -0.2rem;
  left: clamp(22px, {percentage:.2f}%, calc(100% - 22px));
  width: 44px;
  height: 30px;
  transform: translateX(-50%) scaleX(-1);
  transform-origin: center;
  display: grid;
  place-items: center;
  font-size: 2rem;
  line-height: 1;
  filter: drop-shadow(0 3px 3px rgba(0, 0, 0, 0.2));
  transition: left 420ms cubic-bezier(0.2, 0.8, 0.2, 1);
}}
.carbti-progress-track {{
  width: 100%;
  height: 0.7rem;
  overflow: hidden;
  border-radius: 999px;
  background: var(--st-secondary-background-color, #E5E7EB);
}}
.carbti-progress-fill {{
  width: {percentage:.2f}%;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(
    90deg,
    var(--st-primary-color, #FF4B4B),
    #F59E0B
  );
  transition: width 420ms cubic-bezier(0.2, 0.8, 0.2, 1);
}}
@media (prefers-reduced-motion: reduce) {{
  .carbti-progress-car,
  .carbti-progress-fill {{
    transition: none;
  }}
}}
</style>
<div
  class="carbti-sticky-progress"
  role="progressbar"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuenow="{percentage:.0f}"
>
  <div class="carbti-progress-labels">
    <span>질문 {start_question}~{end_question} / {total_questions}</span>
    <span>{percentage:.0f}%</span>
  </div>
  <div class="carbti-progress-rail">
    <span class="carbti-progress-car" role="img" aria-label="진행 중인 차량">🚙</span>
    <div class="carbti-progress-track">
      <div class="carbti-progress-fill"></div>
    </div>
  </div>
</div>
"""
    )


def render_question_page():
    """질문을 한 페이지에 4개씩 표시합니다."""

    questions_per_page = 4

    # 현재 페이지에서 시작할 질문 위치입니다.
    # 0, 4, 8, 12, 16 순서로 이동합니다.
    current_index = st.session_state.question_index
    total_questions = len(QUESTIONS)

    # 모든 질문에 답했으면 결과 화면으로 이동합니다.
    if current_index >= total_questions:
        calculate_results()
        change_page("result")
        return

    # 현재 페이지에 표시할 질문 범위입니다.
    page_end = min(
        current_index + questions_per_page,
        total_questions,
    )

    page_questions = QUESTIONS[current_index:page_end]

    # 기존 페이지 단위 진행률 계산을 유지합니다.
    progress_value = (current_index + 1) / total_questions
    render_sticky_question_progress(
        progress_value=progress_value,
        start_question=current_index + 1,
        end_question=page_end,
        total_questions=total_questions,
    )

    # 현재 화면에서 선택한 답변을 임시 저장합니다.
    selected_answers = {}

    for question in page_questions:
        st.subheader(question["text"])

        choice_texts = [
            choice["text"]
            for choice in question["choices"]
        ]

        saved_answer_index = st.session_state.answers.get(
            question["id"]
        )

        radio_index = (
            saved_answer_index
            if saved_answer_index is not None
            else None
        )

        selected_text = st.radio(
            label="답변을 선택하세요.",
            options=choice_texts,
            index=radio_index,
            key=f"radio_question_{question['id']}",
            label_visibility="collapsed",
        )

        # 선택한 문구를 선택지 번호로 변환합니다.
        if selected_text is None:
            selected_answers[question["id"]] = None
        else:
            selected_answers[question["id"]] = (
                choice_texts.index(selected_text)
            )

        # 마지막 질문 다음에는 구분선을 표시하지 않습니다.
        if question["id"] != page_questions[-1]["id"]:
            st.divider()

    previous_column, next_column = st.columns(2)

    # 이전 페이지 버튼
    with previous_column:
        if current_index > 0:
            if st.button(
                "이전 페이지",
                width="stretch",
            ):
                st.session_state.question_index = max(
                    0,
                    current_index - questions_per_page,
                )
                st.rerun()

    # 현재 페이지의 네 질문에 모두 답했는지 확인합니다.
    has_unanswered_question = any(
        answer_index is None
        for answer_index in selected_answers.values()
    )

    # 다음 페이지 또는 결과 확인 버튼
    with next_column:
        if page_end >= total_questions:
            next_button_text = "결과 확인"
        else:
            next_button_text = "다음 페이지"

        if st.button(
            next_button_text,
            disabled=has_unanswered_question,
            width="stretch",
        ):
            # 현재 페이지의 답변을 session_state에 저장합니다.
            for question_id, answer_index in selected_answers.items():
                st.session_state.answers[question_id] = (
                    answer_index
                )

            # 다음 네 질문으로 이동합니다.
            st.session_state.question_index = page_end
            st.rerun()

# %%
# ============================================================
# 셀 7. 사용자 답변을 점수로 변환하는 함수
# ============================================================


def calculate_user_scores():
    """저장된 답변으로 E/I, S/N, T/F, J/P 점수를 계산합니다."""

    scores = {
        "E": 0,
        "I": 0,
        "S": 0,
        "N": 0,
        "T": 0,
        "F": 0,
        "J": 0,
        "P": 0,
    }

    for question in QUESTIONS:
        selected_index = st.session_state.answers.get(question["id"])
        if selected_index is None:
            continue

        selected_choice = question["choices"][selected_index]
        for score_name, score_value in selected_choice["scores"].items():
            scores[score_name] += score_value

    return scores



# %%
# ============================================================
# 셀 8. 결과 유형과의 거리 계산 및 순위 생성
# ============================================================


def calculate_mbti(user_scores):
    """각 기준의 5문항 중 3표 이상을 얻은 성향으로 MBTI를 만듭니다."""

    return (
        ("E" if user_scores["E"] >= 3 else "I")
        + ("S" if user_scores["S"] >= 3 else "N")
        + ("T" if user_scores["T"] >= 3 else "F")
        + ("J" if user_scores["J"] >= 3 else "P")
    )




def calculate_results():
    """사용자 점수와 최종 MBTI 코드를 세션 상태에 저장합니다."""

    user_scores = calculate_user_scores()
    user_mbti = calculate_mbti(user_scores)

    st.session_state.user_scores = user_scores
    st.session_state.user_mbti = user_mbti

    # 기존 결과 화면 상태와의 호환을 위해 한 개의 결과로 저장합니다.
    st.session_state.ranked_results = [
        {
            "mbti_id": user_mbti,
            "distance": 0,
        }
    ]



# %%
# ============================================================
# 셀 9. 결과 화면
# ============================================================

def get_result_font(size, bold=False):
    """운영체제에서 사용할 수 있는 한글 폰트를 찾아 반환합니다."""

    font_candidates = [
        Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
        Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
        Path("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for font_path in font_candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def draw_wrapped_text(draw, text, xy, font, fill, max_width, line_gap=10):
    """한글을 포함한 문자열을 주어진 폭에 맞춰 여러 줄로 그립니다."""

    x, y = xy
    lines = []
    current_line = ""
    for character in str(text):
        if character == "\n":
            lines.append(current_line)
            current_line = ""
            continue
        candidate = current_line + character
        box = draw.textbbox((0, 0), candidate, font=font)
        if current_line and box[2] - box[0] > max_width:
            lines.append(current_line)
            current_line = character
        else:
            current_line = candidate
    if current_line:
        lines.append(current_line)

    line_height = draw.textbbox((0, 0), "가Ag", font=font)[3] + line_gap
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


@st.cache_data(ttl=3600, max_entries=64, show_spinner=False)
def download_vehicle_image(image_url):
    """결과 저장 이미지에 넣을 차량 이미지를 다운로드합니다."""

    if not image_url:
        return None
    try:
        request = Request(
            image_url,
            headers={"User-Agent": "CarBTI-Streamlit/1.0"},
        )
        with urlopen(request, timeout=5) as response:
            return response.read(10 * 1024 * 1024)
    except Exception:
        return None


def build_result_image(user_mbti, mbti, recommendation):
    """CarBTI 결과와 1위 차량을 공유용 PNG 이미지로 만듭니다."""

    canvas = Image.new("RGB", (1200, 1500), "#F7F8FA")
    draw = ImageDraw.Draw(canvas)
    title_font = get_result_font(62, bold=True)
    heading_font = get_result_font(44, bold=True)
    body_font = get_result_font(30)
    caption_font = get_result_font(25)

    draw.rounded_rectangle((60, 55, 1140, 1445), radius=36, fill="white")
    draw.text((110, 105), "나의 CarBTI", font=caption_font, fill="#6B7280")
    draw.text((110, 155), mbti["mbti_name"], font=title_font, fill="#111827")
    draw.text((110, 240), user_mbti, font=heading_font, fill="#E85D35")

    image_box = (110, 330, 1090, 865)
    vehicle_image_bytes = download_vehicle_image(recommendation["car_img"])
    if vehicle_image_bytes:
        try:
            vehicle_image = Image.open(BytesIO(vehicle_image_bytes)).convert("RGB")
            vehicle_image = ImageOps.fit(
                vehicle_image,
                (image_box[2] - image_box[0], image_box[3] - image_box[1]),
            )
            canvas.paste(vehicle_image, image_box[:2])
        except Exception:
            draw.rounded_rectangle(image_box, radius=24, fill="#E5E7EB")
    else:
        draw.rounded_rectangle(image_box, radius=24, fill="#E5E7EB")
        draw.text((500, 565), "test", font=title_font, fill="#9CA3AF")

    vehicle_name = (
        recommendation["manufacturer_name"]
        + " "
        + recommendation["vehicle_name"]
    ).strip()
    draw.text((110, 915), "추천 1위", font=caption_font, fill="#E85D35")
    draw.text((110, 965), vehicle_name, font=heading_font, fill="#111827")
    y = draw_wrapped_text(
        draw,
        mbti["mbti_description"],
        (110, 1040),
        body_font,
        "#374151",
        980,
    )
    draw_wrapped_text(
        draw,
        recommendation["recom_reason"],
        (110, y + 28),
        caption_font,
        "#6B7280",
        980,
    )

    output = BytesIO()
    canvas.save(output, format="PNG", optimize=True)
    return output.getvalue()


TEST_IMAGE_DATA_URI = (
    "data:image/svg+xml,"
    "%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20"
    "viewBox%3D%220%200%201200%20675%22%3E"
    "%3Crect%20width%3D%221200%22%20height%3D%22675%22%20"
    "fill%3D%22%23E5E7EB%22/%3E"
    "%3Ctext%20x%3D%22600%22%20y%3D%22338%22%20"
    "text-anchor%3D%22middle%22%20dominant-baseline%3D%22middle%22%20"
    "font-family%3D%22Arial%2Csans-serif%22%20font-size%3D%22120%22%20"
    "font-weight%3D%22700%22%20fill%3D%22%236B7280%22%3E"
    "test%3C/text%3E%3C/svg%3E"
)


VEHICLE_CARD_STYLE = """
<style>
.carbti-vehicle-card {
  display: block;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  border: 1px solid var(--st-border-color, #D1D5DB);
  border-radius: 18px;
  background: var(--st-background-color, #FFFFFF);
  color: var(--st-text-color);
  text-decoration: none;
  backface-visibility: hidden;
  transform-style: preserve-3d;
  transform-origin: center;
  transition:
    border-color 180ms ease,
    box-shadow 180ms ease,
    transform 240ms cubic-bezier(0.2, 0.8, 0.2, 1);
}
.carbti-vehicle-card:hover,
.carbti-vehicle-card:focus {
  border-color: var(--st-primary-color);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.14);
  transform: perspective(1200px) rotateY(-2deg) translateY(-3px);
  outline: none;
}
.carbti-vehicle-card:active {
  transform: perspective(1200px) rotateY(8deg) scale(0.985);
  transition-duration: 90ms;
}
.carbti-vehicle-card.is-disabled {
  opacity: 0.78;
  pointer-events: none;
}
.carbti-result-header {
  padding: 1.4rem 1.5rem 1.15rem;
  text-align: center;
}
.carbti-result-rank {
  display: inline-block;
  margin-bottom: 0.35rem;
  color: var(--st-primary-color);
  font-size: 0.9rem;
  font-weight: 750;
}
.carbti-result-name {
  margin: 0;
  color: var(--st-heading-color);
  font-size: 2rem;
  line-height: 1.25;
}
.carbti-result-description {
  max-width: 720px;
  margin: 0.65rem auto 0;
  color: var(--st-text-color);
  line-height: 1.65;
}
.carbti-result-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.9rem;
}
.carbti-result-tag {
  display: inline-flex;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  background: color-mix(in srgb, var(--st-primary-color) 16%, transparent);
  color: var(--st-primary-color);
  font-size: 0.85rem;
  font-weight: 700;
}
.carbti-vehicle-image-wrap {
  position: relative;
  display: flex;
  width: 100%;
  height: 220px;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--st-secondary-background-color, #F3F4F6);
}
.carbti-vehicle-card.is-featured .carbti-vehicle-image-wrap {
  height: 390px;
}
.carbti-vehicle-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.carbti-vehicle-rank-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  z-index: 1;
  padding: 0.3rem 0.65rem;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.78);
  color: #FFFFFF;
  font-size: 0.8rem;
  font-weight: 700;
}
.carbti-vehicle-footer {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  padding: 1rem 1.15rem 1.1rem;
}
.carbti-vehicle-identity {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.45rem;
}
.carbti-vehicle-name {
  color: var(--st-heading-color);
  font-size: 1.12rem;
}
.carbti-vehicle-card.is-featured .carbti-vehicle-name {
  font-size: 1.45rem;
}
.carbti-vehicle-divider,
.carbti-manufacturer-name {
  color: var(--st-gray-text-color, #6B7280);
}
.carbti-vehicle-action {
  color: var(--st-primary-color);
  font-size: 0.8rem;
  font-weight: 650;
}
@media (prefers-reduced-motion: reduce) {
  .carbti-vehicle-card {
    transition: none;
  }
  .carbti-vehicle-card:hover,
  .carbti-vehicle-card:focus,
  .carbti-vehicle-card:active {
    transform: none;
  }
}
</style>
"""


def build_result_tags(mbti, user_mbti, recommendation):
    """car_mbti.mbti_tags를 우선 사용해 결과 태그 3개를 만듭니다."""

    mbti = mbti or {}
    tags = []
    for raw_tag in str(mbti.get("mbti_tags") or "").split(","):
        tag = raw_tag.strip()
        if not tag:
            continue
        if not tag.startswith("#"):
            tag = f"#{tag}"
        if tag not in tags:
            tags.append(tag)

    if len(tags) < 3:
        fallback_values = [
            user_mbti,
            recommendation.get("body_type"),
            recommendation.get("vec_purpose"),
        ]
        for value in fallback_values:
            text = str(value or "").strip()
            if not text or "." in text:
                continue
            tag = f"#{text.replace(' ', '')}"
            if tag not in tags:
                tags.append(tag)
            if len(tags) >= 3:
                break

    for fallback in ("#CarBTI", "#추천1위", "#맞춤차량"):
        if len(tags) >= 3:
            break
        if fallback not in tags:
            tags.append(fallback)
    return tags[:3]


def render_vehicle_card(
    recommendation,
    featured=False,
    mbti=None,
    user_mbti="",
):
    """차량 이미지와 명칭 전체를 클릭 가능한 카드로 표시합니다."""

    vehicle_id = recommendation.get("vehicle_id")
    rank = int(recommendation["recom_car_rank"])
    result_mbti = str(
        user_mbti or st.session_state.user_mbti or ""
    ).upper()
    card_is_linkable = bool(
        vehicle_id
        or (
            result_mbti in PPT_RESULT_VEHICLES
            and rank in {1, 2, 3}
        )
    )

    card_classes = ["carbti-vehicle-card"]
    if featured:
        card_classes.append("is-featured")
    if not card_is_linkable:
        card_classes.append("is-disabled")
    card_class = " ".join(card_classes)

    vehicle_name = str(
        recommendation.get("vehicle_name") or "차량명 준비 중"
    )
    manufacturer_name = str(
        recommendation.get("manufacturer_name") or "제조사 준비 중"
    )
    vehicle_label = f"{vehicle_name} | {manufacturer_name}"

    if card_is_linkable:
        score_order = ("E", "I", "S", "N", "T", "F", "J", "P")
        score_text = ",".join(
            str(st.session_state.user_scores.get(score_name, 0))
            for score_name in score_order
        )
        detail_params = {
            "page": "vehicle_detail",
            "vehicle_rank": rank,
            "mbti": result_mbti,
            "scores": score_text,
        }
        if vehicle_id:
            detail_params["vehicle_id"] = int(vehicle_id)
        detail_url = "?" + urlencode(detail_params)
        opening_tag = (
            f'<a class="{card_class}" '
            f'href="{html.escape(detail_url, quote=True)}" target="_self">'
        )
        closing_tag = "</a>"
    else:
        opening_tag = f'<div class="{card_class}">'
        closing_tag = "</div>"

    image_url = str(
        recommendation.get("car_img") or TEST_IMAGE_DATA_URI
    )
    image_html = (
        '<img class="carbti-vehicle-image" '
        f'src="{html.escape(image_url, quote=True)}" '
        f'alt="{html.escape(vehicle_label, quote=True)} 이미지">'
    )

    featured_header = ""
    if featured:
        mbti = mbti or {}
        tags_html = "".join(
            f'<span class="carbti-result-tag">{html.escape(tag)}</span>'
            for tag in build_result_tags(mbti, user_mbti, recommendation)
        )
        featured_header = f"""
  <div class="carbti-result-header">
    <span class="carbti-result-rank">추천 1위 · {html.escape(user_mbti)}</span>
    <h2 class="carbti-result-name">
      {html.escape(str(mbti.get("mbti_name") or ""))}
    </h2>
    <p class="carbti-result-description">
      {html.escape(str(mbti.get("mbti_description") or ""))}
    </p>
    <div class="carbti-result-tags">{tags_html}</div>
  </div>
"""

    card_html = f"""
{opening_tag}
{featured_header}
  <div class="carbti-vehicle-image-wrap">
    <span class="carbti-vehicle-rank-badge">추천 {rank}위</span>
    {image_html}
  </div>
  <div class="carbti-vehicle-footer">
    <div class="carbti-vehicle-identity">
      <strong class="carbti-vehicle-name">
        {html.escape(vehicle_name)}
      </strong>
      <span class="carbti-vehicle-divider">|</span>
      <span class="carbti-manufacturer-name">
        {html.escape(manufacturer_name)}
      </span>
    </div>
    <span class="carbti-vehicle-action">
      카드를 누르면 뒤집히며 차량 상세페이지로 이동합니다 →
    </span>
  </div>
{closing_tag}
"""
    st.html(card_html)


def render_result_page():
    """CarBTI 설명과 추천 점수 결과에 따른 차량 순위를 표시합니다."""

    user_mbti = st.session_state.user_mbti
    if not user_mbti:
        calculate_results()
        user_mbti = st.session_state.user_mbti

    placeholder_error = None
    try:
        mbti, recommendations = load_result_data(user_mbti)
        using_placeholder = False
    except MbtiDataError as error:
        using_placeholder = True
        placeholder_error = str(error)
        mbti = CAR_MBTI_FALLBACKS[user_mbti].copy()
        recommendations = [
            {
                "recom_car_rank": rank,
                "recom_reason": (
                    mbti["mbti_description"]
                    if rank == 1
                    else f"{manufacturer_name} {vehicle_name} 추천 차량"
                ),
                "vehicle_id": None,
                "vehicle_name": vehicle_name,
                "body_type": "",
                "car_img": None,
                "car_description": "",
                "vec_purpose": "",
                "manufacturer_name": manufacturer_name,
            }
            for rank, manufacturer_name, vehicle_name
            in PPT_RESULT_VEHICLES[user_mbti]
        ]
        st.info(
            "DB 일부 데이터를 불러오지 못해 기본 결과 정보를 표시합니다. "
            "카드를 선택하면 해당 차량의 상세 조회를 다시 시도합니다."
        )

    first_recommendation = recommendations[0]

    st.html(VEHICLE_CARD_STYLE)
    render_vehicle_card(
        first_recommendation,
        featured=True,
        mbti=mbti,
        user_mbti=user_mbti,
    )

    lower_recommendations = recommendations[1:3]
    if lower_recommendations:
        st.subheader("2·3위 추천 차량")
        columns = st.columns(len(lower_recommendations))
        for column, recommendation in zip(
            columns,
            lower_recommendations,
        ):
            with column:
                render_vehicle_card(
                    recommendation,
                    user_mbti=user_mbti,
                )

    with st.expander("내 상세 점수 확인", icon=":material/analytics:"):
        st.json(st.session_state.user_scores)
        if using_placeholder:
            st.caption(placeholder_error)

    result_image = build_result_image(
        user_mbti,
        mbti,
        first_recommendation,
    )
    st.divider()
    with st.container(horizontal=True):
        st.download_button(
            "이미지 저장",
            data=result_image,
            file_name=f"carbti-{user_mbti}.png",
            mime="image/png",
            icon=":material/download:",
        )
        if st.button("다시하기", icon=":material/refresh:"):
            reset_test()


def return_to_result_page():
    """차량 상세 URL을 정리하고 기존 결과 화면으로 돌아갑니다."""

    st.query_params.clear()
    st.session_state.selected_vehicle_id = None
    st.session_state.selected_vehicle_rank = None
    change_page("result")


VEHICLE_DETAIL_STYLE = """
<style>
.carbti-detail-image {
  display: block;
  width: 100%;
  max-width: 420px;
  height: 290px;
  margin: 0 auto 1rem;
  object-fit: contain;
}
.carbti-news-list {
  margin-top: .25rem;
  border-top: 1px solid #d9dde5;
}
.carbti-news-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: .75rem;
  min-height: 3rem;
  padding: .65rem .1rem;
  border-bottom: 1px solid #d9dde5;
}
.carbti-news-title {
  overflow: hidden;
  color: #20242c;
  font-size: .95rem;
  font-weight: 650;
  line-height: 1.4;
  text-decoration: none;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.carbti-news-title:hover {
  color: #1769aa;
  text-decoration: underline;
}
.carbti-news-date {
  color: #7a808c;
  font-size: .82rem;
  white-space: nowrap;
}
@media (max-width: 640px) {
  .carbti-detail-image {
    max-width: 330px;
    height: 230px;
  }
  .carbti-news-row {
    grid-template-columns: 1fr;
    gap: .15rem;
  }
}
</style>
"""


def render_vehicle_detail_page():
    """차량 이미지·상세 정보·관련 뉴스 3줄을 2단으로 표시합니다."""

    vehicle_id = st.session_state.selected_vehicle_id
    if not vehicle_id:
        vehicle_rank = st.session_state.selected_vehicle_rank
        result_mbti = st.session_state.user_mbti
        if vehicle_rank and result_mbti:
            try:
                vehicle_id = resolve_result_vehicle_id(
                    result_mbti,
                    vehicle_rank,
                )
            except VehicleDataError as error:
                st.title("차량 상세 정보")
                st.error(str(error))
                if st.button("결과 페이지", icon=":material/arrow_back:"):
                    return_to_result_page()
                return
            st.session_state.selected_vehicle_id = vehicle_id
        else:
            st.warning("선택한 차량이 없습니다.")
            if st.button("결과 페이지", icon=":material/arrow_back:"):
                return_to_result_page()
            return

    try:
        vehicle_data = load_vehicle_data(vehicle_id)
    except VehicleDataError as error:
        st.title("차량 상세 정보")
        st.error(str(error))
        st.caption(
            "vehicle 및 연결 테이블의 데이터와 DB 연결 설정을 확인하세요."
        )
        if st.button("결과 페이지", icon=":material/arrow_back:"):
            return_to_result_page()
        return

    vehicle = vehicle_data["vehicle"]
    details = vehicle_data["details"]
    sales = vehicle_data["sales"]
    news = vehicle_data["news"]
    recommendation_rows = vehicle_data["recommendation"]

    def first_value(rows, column_name):
        if rows.empty or column_name not in rows.columns:
            return ""
        for value in rows[column_name].tolist():
            if has_display_value(value):
                return value
        return ""

    def latest_value(rows, column_name):
        if rows.empty or column_name not in rows.columns:
            return ""
        for value in reversed(rows[column_name].tolist()):
            if has_display_value(value):
                return value
        return ""

    def display_text(value, fallback="정보 없음"):
        return str(value) if has_display_value(value) else fallback

    average_price = latest_value(sales, "sales_avg_price")
    if has_display_value(average_price):
        try:
            average_price_text = f"{int(float(average_price)):,}원"
        except (TypeError, ValueError):
            average_price_text = str(average_price)
    else:
        average_price_text = "정보 없음"

    fuel_type = first_value(details, "detail_fuel_type")
    fuel_efficiency = first_value(details, "detail_fuel_efficiency")
    fuel_parts = []
    if has_display_value(fuel_type):
        fuel_parts.append(str(fuel_type))
    if has_display_value(fuel_efficiency):
        fuel_parts.append(f"{fuel_efficiency} km/L")
    fuel_summary = " / ".join(fuel_parts) or "정보 없음"
    recommendation_reason = first_value(
        recommendation_rows,
        "recom_reason",
    )

    st.html(VEHICLE_DETAIL_STYLE)
    st.title(display_text(vehicle["vehicle_name"], "차량 정보"))

    image_column, info_column = st.columns([0.95, 1.25], gap="large")

    with image_column:
        st.markdown(
            f"#### {display_text(vehicle['vehicle_name'], '차량 이미지')}"
        )
        detail_image_url = str(
            vehicle["car_img"] or TEST_IMAGE_DATA_URI
        )
        st.html(
            '<img class="carbti-detail-image" '
            f'src="{html.escape(detail_image_url, quote=True)}" '
            f'alt="{html.escape(display_text(vehicle["vehicle_name"]))} 이미지">'
        )

        purchase_columns = st.columns(2)
        with purchase_columns[0]:
            if has_display_value(vehicle["new_car_url"]):
                st.link_button(
                    "신차 구매링크",
                    vehicle["new_car_url"],
                    icon=":material/directions_car:",
                    width="stretch",
                )
            else:
                st.button(
                    "신차 구매링크 없음",
                    disabled=True,
                    width="stretch",
                )
        with purchase_columns[1]:
            if has_display_value(vehicle["used_car_url"]):
                st.link_button(
                    "중고차 구매링크",
                    vehicle["used_car_url"],
                    icon=":material/sell:",
                    width="stretch",
                )
            else:
                st.button(
                    "중고차 구매링크 없음",
                    disabled=True,
                    width="stretch",
                )

        if st.button(
            "결과 페이지",
            icon=":material/arrow_back:",
            width="stretch",
        ):
            return_to_result_page()

    with info_column:
        with st.container(border=True):
            st.subheader("차량 정보")
            primary, specification, maker = st.columns(
                [1.15, 0.9, 0.8],
                gap="small",
            )

            with primary:
                st.caption("차량 명칭")
                st.markdown(
                    f"**{display_text(vehicle['vehicle_name'])}**"
                )
                st.caption("국가")
                st.write(display_text(vehicle["country"]))
                st.caption("용도")
                st.write(display_text(vehicle["vec_purpose"]))
                st.caption("평균 가격")
                st.write(average_price_text)

            with specification:
                st.caption("차종")
                st.write(display_text(vehicle["body_type"]))
                st.caption("연료 / 연비")
                st.write(fuel_summary)

            with maker:
                st.caption("제조사")
                st.write(display_text(vehicle["manufacturer_name"]))

            st.divider()
            st.caption("추천 이유")
            st.write(display_text(recommendation_reason))

        with st.container(border=True):
            st.subheader("관련 뉴스")
            if news.empty:
                st.caption("이 차량에 등록된 뉴스가 없습니다.")
            else:
                news_rows = []
                for index, (_, article) in enumerate(
                    news.head(3).iterrows(),
                    start=1,
                ):
                    title = display_text(article["title"], "차량 소식")
                    news_url = (
                        str(article["news_url"])
                        if has_display_value(article["news_url"])
                        else ""
                    )
                    publish_date = article["publish_date"]
                    if has_display_value(publish_date):
                        try:
                            publish_date_text = publish_date.strftime(
                                "%Y-%m-%d"
                            )
                        except (AttributeError, ValueError):
                            publish_date_text = str(publish_date)
                    else:
                        publish_date_text = "게시일 정보 없음"

                    numbered_title = f"{index}. {title}"
                    if news_url:
                        title_html = (
                            '<a class="carbti-news-title" '
                            f'href="{html.escape(news_url, quote=True)}" '
                            f'target="_blank" rel="noopener noreferrer">'
                            f'{html.escape(numbered_title)}</a>'
                        )
                    else:
                        title_html = (
                            '<span class="carbti-news-title">'
                            f'{html.escape(numbered_title)}</span>'
                        )

                    news_rows.append(
                        '<div class="carbti-news-row">'
                        f'{title_html}'
                        '<span class="carbti-news-date">'
                        f'{html.escape(publish_date_text)}</span>'
                        '</div>'
                    )

                st.html(
                    '<div class="carbti-news-list">'
                    + "".join(news_rows)
                    + "</div>"
                )



# %%
# ============================================================
# 셀 10. 메인 실행 함수와 페이지 라우터
# ============================================================


def main():
    """
    애플리케이션의 시작점입니다.

    1. 세션 상태를 초기화합니다.
    2. 현재 page 값에 따라 출력할 화면을 결정합니다.
    3. 해당 화면 함수를 실행합니다.
    """

    # 검사 진행에 필요한 기본 세션 상태를 생성합니다.
    initialize_session_state()

    # HTML 차량 카드가 전달한 vehicle_id를 Python에서 읽습니다.
    query_vehicle_id = st.query_params.get("vehicle_id")
    query_vehicle_rank = st.query_params.get("vehicle_rank")
    query_page = str(st.query_params.get("page", ""))
    if query_vehicle_id or (
        query_page == "vehicle_detail" and query_vehicle_rank
    ):
        query_mbti = str(st.query_params.get("mbti", "")).upper()
        valid_mbti_ids = {
            profile["mbti_id"]
            for profile in RESULT_PROFILES
        }
        if query_mbti in valid_mbti_ids:
            st.session_state.user_mbti = query_mbti
            st.session_state.ranked_results = [
                {"mbti_id": query_mbti, "distance": 0}
            ]

        try:
            selected_vehicle_rank = int(query_vehicle_rank or 0)
            if selected_vehicle_rank not in {1, 2, 3}:
                raise ValueError
        except (TypeError, ValueError):
            selected_vehicle_rank = None
        st.session_state.selected_vehicle_rank = selected_vehicle_rank

        if query_vehicle_id:
            try:
                selected_vehicle_id = int(query_vehicle_id)
                if selected_vehicle_id <= 0:
                    raise ValueError
            except (TypeError, ValueError):
                st.session_state.selected_vehicle_id = None
            else:
                st.session_state.selected_vehicle_id = selected_vehicle_id
        else:
            st.session_state.selected_vehicle_id = None

        query_scores = str(st.query_params.get("scores", ""))
        score_order = ("E", "I", "S", "N", "T", "F", "J", "P")
        try:
            score_values = [
                int(value)
                for value in query_scores.split(",")
            ]
            if len(score_values) != len(score_order):
                raise ValueError
        except ValueError:
            pass
        else:
            st.session_state.user_scores = dict(
                zip(score_order, score_values)
            )
        st.session_state.page = "vehicle_detail"

    # 페이지 이름과 화면 출력 함수를 연결합니다.
    #
    # page가 "main"이면 render_main_page 함수가 실행됩니다.
    # page가 "question"이면 render_question_page 함수가 실행됩니다.
    # page가 "result"이면 render_result_page 함수가 실행됩니다.
    # page가 "vehicle_detail"이면 차량 상세 정보가 표시됩니다.
    page_routes = {
        "main": render_main_page,
        "question": render_question_page,
        "result": render_result_page,
        "vehicle_detail": render_vehicle_detail_page,
    }

    # 현재 세션에 저장된 페이지 이름을 가져옵니다.
    current_page_name = st.session_state.page

    # 현재 페이지 이름에 해당하는 함수를 가져옵니다.
    #
    # 등록되지 않은 페이지 이름일 경우
    # 안전하게 최초 진입 화면을 사용합니다.
    current_page_function = page_routes.get(
        current_page_name,
        render_main_page,
    )

    # 선택된 페이지 함수를 실행해 실제 화면을 출력합니다.
    current_page_function()


# 이 파일을 streamlit run app.py로 직접 실행했을 때만
# main() 함수를 호출합니다.
main()
