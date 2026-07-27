"""
manufacturer_crawler.py
- manufacturer 테이블에 들어갈 데이터를 정리하고 MySQL DB에 저장하는 스크립트
"""

from db_config import get_db_connection

manufacturers_seed = [
    {
        "manufacturer_name": "현대자동차",
        "country": "대한민국",
        "official_url": "https://www.hyundai.com/kr/ko/e",
        "logo_url": "https://www.hyundai.com/static/images/hyu_logo_og_image.jpg",
    },
    {
        "manufacturer_name": "기아",
        "country": "대한민국",
        "official_url": "https://www.kia.com/kr/main.html",
        "logo_url": "https://www.kia.com/content/dam/kwp/kr/ko/common/kia_logo_og.jpg",
    },
    {
        "manufacturer_name": "제네시스",
        "country": "대한민국",
        "official_url": "https://www.genesis.com/kr/ko.html",
        "logo_url": "https://cms-static.genesis.com/cci/20260722050641/assets/logo_footer-BybBGRkJ.svg",
    },
    {
        "manufacturer_name": "KG모빌리티",
        "country": "대한민국",
        "official_url": "https://www.kg-mobility.com/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "르노코리아",
        "country": "대한민국",
        "official_url": "https://www.renaultkorea.com/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "쉐보레",
        "country": "미국",
        "official_url": "https://www.chevrolet.co.kr/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "BMW",
        "country": "독일",
        "official_url": "https://www.bmw.co.kr/",
        "logo_url": "https://iconape.com/wp-content/files/yb/374344/png/374344.png",
    },
    {
        "manufacturer_name": "메르세데스-벤츠",
        "country": "독일",
        "official_url": "https://www.mercedes-benz.co.kr/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "아우디",
        "country": "독일",
        "official_url": "https://www.audi.co.kr/",
        "logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFGLJBroBQL9A7J4GSc1_5wF44W4YWJpgj0Qn3z5nAorZbEK1CBetHnDQ&s=10",
    },
    {
        "manufacturer_name": "폭스바겐",
        "country": "독일",
        "official_url": "https://www.volkswagen.co.kr/ko.html",
        "logo_url": None,
    },
    {
        "manufacturer_name": "볼보",
        "country": "스웨덴",
        "official_url": "https://www.volvocars.com/kr/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "토요타",
        "country": "일본",
        "official_url": "https://www.toyota.co.kr/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "렉서스",
        "country": "일본",
        "official_url": "https://www.lexus.co.kr/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "혼다",
        "country": "일본",
        "official_url": "https://www.hondakorea.co.kr/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "포르쉐",
        "country": "독일",
        "official_url": "https://www.porsche.com/korea/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "미니",
        "country": "영국",
        "official_url": "https://www.mini.co.kr/",
        "logo_url": None,
    },
    {
        "manufacturer_name": "테슬라",
        "country": "미국",
        "official_url": "https://www.tesla.com/ko_kr",
        "logo_url": None,
    },
]


def insert_manufacturers(data):
    conn = get_db_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO manufacturer (manufacturer_name, country, logo_url, official_url)
        VALUES (%s, %s, %s, %s)
    """

    for m in data:
        cur.execute(
            sql,
            (
                m["manufacturer_name"],
                m["country"],
                m["logo_url"],
                m["official_url"],
            ),
        )
        print(f"저장 완료: {m['manufacturer_name']}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n총 {len(data)}개 제조사 저장 완료")


if __name__ == "__main__":
    insert_manufacturers(manufacturers_seed)
