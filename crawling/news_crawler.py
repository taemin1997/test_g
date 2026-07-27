"""
news_crawler.py
- 네이버 뉴스 검색 API로 16대 차량 관련 뉴스를 1건씩 크롤링
- JSON 백업 저장 + MySQL news 테이블에 바로 INSERT

사전 준비:
1. https://developers.naver.com/apps/#/register 에서 애플리케이션 등록
   - 사용 API: "검색" 체크
2. .env 파일에 NAVER_CLIENT_ID, NAVER_CLIENT_SECRET 입력
"""

import requests
import json
import time
import re
import os
from email.utils import parsedate_to_datetime
from dotenv import load_dotenv

from db_config import get_db_connection

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

VEHICLE_LIST = {
    "ISTJ": "아반떼",
    "ISFJ": "벤츠 E클래스",
    "INFJ": "제네시스 G80",
    "INTJ": "볼보 XC60",
    "ISTP": "포르쉐 카이엔",
    "ISFP": "렉서스 ES",
    "INFP": "폭스바겐 티구안",
    "INTP": "아이오닉5",
    "ESTP": "제네시스 GV70",
    "ESFP": "미니 쿠퍼",
    "ENFP": "기아 레이",
    "ENTP": "테슬라 Model Y",
    "ESTJ": "현대 그랜저",
    "ESFJ": "기아 쏘렌토",
    "ENFJ": "기아 카니발",
    "ENTJ": "BMW 5시리즈",
}


def clean_html(text):
    """네이버 API가 <b>태그로 감싸서 주는 하이라이트/HTML 엔티티 제거"""
    text = re.sub(r"<.*?>", "", text)
    text = text.replace("&quot;", '"').replace("&amp;", "&").replace("&#39;", "'")
    return text.strip()


def get_press_name(url):
    """URL 도메인에서 언론사 이름을 대략 추정 (참고용, 완벽하지 않음)"""
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    return match.group(1) if match else ""


def search_news(query):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {
        "query": query,
        "display": 5,   # 상위 5개 받아서 그중 1개 선택
        "start": 1,
        "sort": "sim",  # sim: 정확도순, date: 최신순
    }
    res = requests.get(url, headers=headers, params=params, timeout=10)
    res.raise_for_status()
    return res.json()


def crawl_one(persona_code, vehicle_name):
    data = search_news(f"{vehicle_name} 신차")
    items = data.get("items", [])
    if not items:
        return None

    item = items[0]  # 가장 관련도 높은 뉴스 1건만 사용
    news_url = item.get("originallink") or item.get("link")

    return {
        "persona_code": persona_code,
        "vehicle_name": vehicle_name,
        "news_title": clean_html(item["title"]),
        "news_url": news_url,
        "press": get_press_name(news_url),
        "publish_date": item["pubDate"],
        "summary": clean_html(item["description"]),
    }


# ---------------- DB 저장 관련 ----------------

def get_vehicle_id_map(cur):
    cur.execute("SELECT vehicle_id, vehicle_name FROM vehicle")
    return {name: vid for vid, name in cur.fetchall()}


def find_vehicle_id(vehicle_id_map, news_vehicle_name):
    """정확히 일치하면 바로 매칭, 아니면 news_vehicle_name 안에
    vehicle 테이블 이름이 포함되어 있는지로 매칭 (예: 'E클래스' in '벤츠 E클래스')"""
    if news_vehicle_name in vehicle_id_map:
        return vehicle_id_map[news_vehicle_name]
    for table_name, vid in vehicle_id_map.items():
        if table_name in news_vehicle_name:
            return vid
    return None


def parse_date(value):
    """네이버 API의 'Mon, 26 Jun 2026 09:00:00 +0900' 형식을 DATE로 변환"""
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).date()
    except Exception:
        return None


def truncate(value, max_len=255):
    if value is None:
        return None
    return str(value)[:max_len]


def insert_news(cur, vehicle_id_map, item):
    """news 테이블 스키마(news_id, title, summary, news_url, news_img,
    news_category, publish_date, vehicle_id)에 맞춰 INSERT.
    news_img, news_category는 크롤링 데이터에 없어서 NULL로 저장됨."""

    vehicle_id = find_vehicle_id(vehicle_id_map, item["vehicle_name"])
    if vehicle_id is None:
        print(f"   [건너뜀] '{item['vehicle_name']}' -> vehicle 테이블에서 매칭 안 됨")
        return False

    sql = """
        INSERT INTO news
        (title, summary, news_url, publish_date, vehicle_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(sql, (
        truncate(item.get("news_title")),
        truncate(item.get("summary")),
        truncate(item.get("news_url")),
        parse_date(item.get("publish_date")),
        vehicle_id,
    ))
    return True


if __name__ == "__main__":
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        print("먼저 .env에 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET을 채워주세요!")
        exit()

    results = []

    for persona_code, vehicle_name in VEHICLE_LIST.items():
        print(f"검색 중: {vehicle_name} ({persona_code})")
        try:
            data = crawl_one(persona_code, vehicle_name)
            if data:
                print(" ->", data["news_title"])
                results.append(data)
            else:
                print(" -> 검색 결과 없음")
        except Exception as e:
            print(f"[실패] {vehicle_name}: {e}")

        time.sleep(0.5)

    # JSON 백업 저장
    with open("data/raw/vehicle_news.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nJSON 백업 완료 -> ../data/raw/vehicle_news.json")

    # MySQL 저장
    conn = get_db_connection()
    cur = conn.cursor()
    vehicle_id_map = get_vehicle_id_map(cur)

    success = 0
    for item in results:
        try:
            if insert_news(cur, vehicle_id_map, item):
                success += 1
        except Exception as e:
            print(f"[DB 저장 실패] {item['vehicle_name']}: {e}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"DB 저장 완료: {success}건 / 전체 {len(results)}건")
