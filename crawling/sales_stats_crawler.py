from db_config import get_db_connection

# ── 판매실적 데이터 ──────────────────────────────
sales_records = [
    # ── 기아 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "기아", "vehicle_name": "쏘렌토", "sales_year": 2026, "sales_month": 6, "sales_count": 8561, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "셀토스", "sales_year": 2026, "sales_month": 6, "sales_count": 6685, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "카니발", "sales_year": 2026, "sales_month": 6, "sales_count": 6267, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "스포티지", "sales_year": 2026, "sales_month": 6, "sales_count": 6176, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "EV5", "sales_year": 2026, "sales_month": 6, "sales_count": 3192, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "K5", "sales_year": 2026, "sales_month": 6, "sales_count": 3150, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "레이", "sales_year": 2026, "sales_month": 6, "sales_count": 2954, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "EV3", "sales_year": 2026, "sales_month": 6, "sales_count": 2838, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "K8", "sales_year": 2026, "sales_month": 6, "sales_count": 1981, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "모닝", "sales_year": 2026, "sales_month": 6, "sales_count": 1919, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "니로", "sales_year": 2026, "sales_month": 6, "sales_count": 1880, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "EV6", "sales_year": 2026, "sales_month": 6, "sales_count": 820, "sales_avg_price": None},
    {"manufacturer_name": "기아", "vehicle_name": "EV9", "sales_year": 2026, "sales_month": 6, "sales_count": 392, "sales_avg_price": None},

    # ── 다음 브랜드부터는 여기 아래에 이어서 추가 ──────────────────────────────

    # ── 현대자동차 (2026년 6월) ──────────────────────────────
    # 전기차 트림은 vehicle_seed.py 원래 방침대로 같은 모델에 합산함
    {"manufacturer_name": "현대자동차", "vehicle_name": "그랜저", "sales_year": 2026, "sales_month": 6, "sales_count": 10062, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "쏘나타", "sales_year": 2026, "sales_month": 6, "sales_count": 5102, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "팰리세이드", "sales_year": 2026, "sales_month": 6, "sales_count": 4211, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "아반떼", "sales_year": 2026, "sales_month": 6, "sales_count": 4201 + 115, "sales_avg_price": None},  # 아반떼 4,201 + 아반떼 N 115
    {"manufacturer_name": "현대자동차", "vehicle_name": "싼타페", "sales_year": 2026, "sales_month": 6, "sales_count": 4068, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "투싼", "sales_year": 2026, "sales_month": 6, "sales_count": 3285, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "스타리아", "sales_year": 2026, "sales_month": 6, "sales_count": 2579 + 456, "sales_avg_price": None},  # 더 뉴 스타리아 2,579 + 스타리아 일렉트릭 456
    {"manufacturer_name": "현대자동차", "vehicle_name": "코나", "sales_year": 2026, "sales_month": 6, "sales_count": 2558 + 519, "sales_avg_price": None},  # 코나 2,558 + 코나 일렉트릭 519
    {"manufacturer_name": "현대자동차", "vehicle_name": "아이오닉5", "sales_year": 2026, "sales_month": 6, "sales_count": 1693 + 1, "sales_avg_price": None},  # 아이오닉 5 1,693 + 아이오닉 5 N 1
    {"manufacturer_name": "현대자동차", "vehicle_name": "아이오닉9", "sales_year": 2026, "sales_month": 6, "sales_count": 1318, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "베뉴", "sales_year": 2026, "sales_month": 6, "sales_count": 1123, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "아이오닉6", "sales_year": 2026, "sales_month": 6, "sales_count": 773, "sales_avg_price": None},
    {"manufacturer_name": "현대자동차", "vehicle_name": "캐스퍼", "sales_year": 2026, "sales_month": 6, "sales_count": 711 + 774, "sales_avg_price": None},  # 캐스퍼 711 + 캐스퍼 일렉트릭 774
    {"manufacturer_name": "현대자동차", "vehicle_name": "넥쏘", "sales_year": 2026, "sales_month": 6, "sales_count": 459, "sales_avg_price": None},
    # 매칭 제외(우리 vehicle 테이블에 없음): 포터2 3,270 / 버스·트럭(현대) 2,375 / 포터2 일렉트릭 558 / ST1 85

    # ── 제네시스 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "제네시스", "vehicle_name": "G80", "sales_year": 2026, "sales_month": 6, "sales_count": 2757 + 187, "sales_avg_price": None},  # G80 2,757 + Electrified G80 187
    {"manufacturer_name": "제네시스", "vehicle_name": "GV70", "sales_year": 2026, "sales_month": 6, "sales_count": 2294 + 134, "sales_avg_price": None},  # GV70 2,294 + Electrified GV70 134
    {"manufacturer_name": "제네시스", "vehicle_name": "GV80", "sales_year": 2026, "sales_month": 6, "sales_count": 1840, "sales_avg_price": None},
    {"manufacturer_name": "제네시스", "vehicle_name": "G90", "sales_year": 2026, "sales_month": 6, "sales_count": 361, "sales_avg_price": None},
    {"manufacturer_name": "제네시스", "vehicle_name": "G70", "sales_year": 2026, "sales_month": 6, "sales_count": 228, "sales_avg_price": None},
    {"manufacturer_name": "제네시스", "vehicle_name": "GV60", "sales_year": 2026, "sales_month": 6, "sales_count": 125 + 10, "sales_avg_price": None},  # GV60 125 + GV60 MAGMA 10
    # GV80 쿠페는 이번 달 목록에 없음(집계 제외 또는 판매 0으로 추정) -> 스킵

    # ── KG모빌리티 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "무쏘 스포츠 & 무쏘 칸", "sales_year": 2026, "sales_month": 6, "sales_count": 1333, "sales_avg_price": None},  # 원자료 표기: "무쏘"
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "토레스", "sales_year": 2026, "sales_month": 6, "sales_count": 624, "sales_avg_price": None},  # 원자료 표기: "뉴 토레스"
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "무쏘 EV", "sales_year": 2026, "sales_month": 6, "sales_count": 578, "sales_avg_price": None},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "액티언", "sales_year": 2026, "sales_month": 6, "sales_count": 528, "sales_avg_price": None},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "티볼리", "sales_year": 2026, "sales_month": 6, "sales_count": 372, "sales_avg_price": None},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "렉스턴", "sales_year": 2026, "sales_month": 6, "sales_count": 111, "sales_avg_price": None},  # 원자료 표기: "렉스턴 뉴 아레나"
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "토레스 EVX", "sales_year": 2026, "sales_month": 6, "sales_count": 91, "sales_avg_price": None},
    # 코란도는 이번 달 목록에 없음 -> 스킵

    # ── 르노코리아 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "르노코리아", "vehicle_name": "그랑 콜레오스", "sales_year": 2026, "sales_month": 6, "sales_count": 1313, "sales_avg_price": None},
    {"manufacturer_name": "르노코리아", "vehicle_name": "아르카나", "sales_year": 2026, "sales_month": 6, "sales_count": 763, "sales_avg_price": None},
    # "필랑트"는 우리 vehicle 테이블에 없는 모델(신차) -> 스킵

    # ── 쉐보레 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "쉐보레", "vehicle_name": "트랙스 크로스오버", "sales_year": 2026, "sales_month": 6, "sales_count": 842, "sales_avg_price": None},
    {"manufacturer_name": "쉐보레", "vehicle_name": "트레일블레이저", "sales_year": 2026, "sales_month": 6, "sales_count": 174, "sales_avg_price": None},
    # "단종차량"은 특정 모델이 아니라 집계 카테고리 -> 스킵

    # ── 테슬라 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "테슬라", "vehicle_name": "Model Y", "sales_year": 2026, "sales_month": 6, "sales_count": 9188, "sales_avg_price": None},
    {"manufacturer_name": "테슬라", "vehicle_name": "Model X", "sales_year": 2026, "sales_month": 6, "sales_count": 1027, "sales_avg_price": None},
    {"manufacturer_name": "테슬라", "vehicle_name": "Model 3", "sales_year": 2026, "sales_month": 6, "sales_count": 414, "sales_avg_price": None},
    {"manufacturer_name": "테슬라", "vehicle_name": "Model S", "sales_year": 2026, "sales_month": 6, "sales_count": 394, "sales_avg_price": None},
    # Cybertruck은 우리 vehicle 테이블에 없는 모델 -> 스킵

    # ── BMW (2026년 6월) ──────────────────────────────
    # i/M 등 전동화·고성능 트림은 vehicle_seed.py 방침대로 같은 베이스 모델에 합산 (i4는 원본에서도 별도 라인이라 유지)
    {"manufacturer_name": "BMW", "vehicle_name": "5시리즈", "sales_year": 2026, "sales_month": 6, "sales_count": 2266 + 300 + 74, "sales_avg_price": None},  # 5 Series 2,266 + i5 300 + M5 74
    {"manufacturer_name": "BMW", "vehicle_name": "X3", "sales_year": 2026, "sales_month": 6, "sales_count": 619 + 58, "sales_avg_price": None},  # X3 619 + The New iX3 58
    {"manufacturer_name": "BMW", "vehicle_name": "X5", "sales_year": 2026, "sales_month": 6, "sales_count": 495 + 2, "sales_avg_price": None},  # X5 495 + X5 M 2
    {"manufacturer_name": "BMW", "vehicle_name": "3시리즈", "sales_year": 2026, "sales_month": 6, "sales_count": 448 + 2, "sales_avg_price": None},  # 3 Series 448 + M3 2
    {"manufacturer_name": "BMW", "vehicle_name": "7시리즈", "sales_year": 2026, "sales_month": 6, "sales_count": 427 + 60, "sales_avg_price": None},  # 7 Series 427 + i7 60
    {"manufacturer_name": "BMW", "vehicle_name": "X7", "sales_year": 2026, "sales_month": 6, "sales_count": 305, "sales_avg_price": None},
    {"manufacturer_name": "BMW", "vehicle_name": "X6", "sales_year": 2026, "sales_month": 6, "sales_count": 221 + 4, "sales_avg_price": None},  # X6 221 + X6 M 4
    {"manufacturer_name": "BMW", "vehicle_name": "X1", "sales_year": 2026, "sales_month": 6, "sales_count": 176 + 85, "sales_avg_price": None},  # X1 176 + iX1 85
    {"manufacturer_name": "BMW", "vehicle_name": "4시리즈", "sales_year": 2026, "sales_month": 6, "sales_count": 154 + 3, "sales_avg_price": None},  # 4 Series 154 + M4 3
    {"manufacturer_name": "BMW", "vehicle_name": "X4", "sales_year": 2026, "sales_month": 6, "sales_count": 110, "sales_avg_price": None},
    {"manufacturer_name": "BMW", "vehicle_name": "1시리즈", "sales_year": 2026, "sales_month": 6, "sales_count": 110, "sales_avg_price": None},
    {"manufacturer_name": "BMW", "vehicle_name": "2시리즈", "sales_year": 2026, "sales_month": 6, "sales_count": 3 + 87 + 75 + 63, "sales_avg_price": None},  # 2 Series 3 + Active Tourer 87 + Gran Coupe 75 + M2 63
    {"manufacturer_name": "BMW", "vehicle_name": "i4", "sales_year": 2026, "sales_month": 6, "sales_count": 80, "sales_avg_price": None},
    {"manufacturer_name": "BMW", "vehicle_name": "X2", "sales_year": 2026, "sales_month": 6, "sales_count": 63 + 58, "sales_avg_price": None},  # X2 63 + iX2 58
    # 매칭 제외(우리 vehicle 테이블에 없음): iX 111 / Z4 46 / 8 Series 43 / XM 20 / M8 1

    # ── 메르세데스-벤츠 (2026년 6월) ──────────────────────────────
    # Maybach/전동화 트림은 vehicle_seed.py 방침대로 같은 베이스 모델에 합산
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "E클래스", "sales_year": 2026, "sales_month": 6, "sales_count": 2114, "sales_avg_price": None},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLC", "sales_year": 2026, "sales_month": 6, "sales_count": 1221, "sales_avg_price": None},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLE", "sales_year": 2026, "sales_month": 6, "sales_count": 634, "sales_avg_price": None},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "G클래스", "sales_year": 2026, "sales_month": 6, "sales_count": 327 + 9, "sales_avg_price": None},  # G-Class 327 + Electric G-Class 9
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "S클래스", "sales_year": 2026, "sales_month": 6, "sales_count": 292 + 28, "sales_avg_price": None},  # S-Class 292 + Maybach S-Class 28
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "C클래스", "sales_year": 2026, "sales_month": 6, "sales_count": 206, "sales_avg_price": None},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLS", "sales_year": 2026, "sales_month": 6, "sales_count": 145 + 29, "sales_avg_price": None},  # GLS-Class 145 + Maybach GLS 29
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "EQE", "sales_year": 2026, "sales_month": 6, "sales_count": 26 + 43, "sales_avg_price": None},  # EQE 26 + EQE SUV 43
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLB", "sales_year": 2026, "sales_month": 6, "sales_count": 34, "sales_avg_price": None},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "AMG GT", "sales_year": 2026, "sales_month": 6, "sales_count": 10 + 6, "sales_avg_price": None},  # AMG GT 10 + The New AMG GT 6
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "CLA", "sales_year": 2026, "sales_month": 6, "sales_count": 18, "sales_avg_price": None},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLA", "sales_year": 2026, "sales_month": 6, "sales_count": 18, "sales_avg_price": None},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "EQS", "sales_year": 2026, "sales_month": 6, "sales_count": 7 + 8, "sales_avg_price": None},  # EQS SUV 7 + Maybach EQS SUV 8
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "A클래스", "sales_year": 2026, "sales_month": 6, "sales_count": 12, "sales_avg_price": None},
    # 매칭 제외(우리 vehicle 테이블에 없음): CLE 242 / EQB 111 / SL-Class 20 / EQA 4 / Maybach SL 1

    # ── 아우디 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "아우디", "vehicle_name": "A6", "sales_year": 2026, "sales_month": 6, "sales_count": 455 + 10 + 20, "sales_avg_price": None},  # The new A6 455 + A6 10 + A6 e-tron 20
    {"manufacturer_name": "아우디", "vehicle_name": "Q4 e-tron", "sales_year": 2026, "sales_month": 6, "sales_count": 438, "sales_avg_price": None},
    {"manufacturer_name": "아우디", "vehicle_name": "Q5", "sales_year": 2026, "sales_month": 6, "sales_count": 427, "sales_avg_price": None},  # 원자료 표기: "The new Q5"
    {"manufacturer_name": "아우디", "vehicle_name": "Q3", "sales_year": 2026, "sales_month": 6, "sales_count": 97 + 2, "sales_avg_price": None},  # The new Q3 97 + Q3 2
    {"manufacturer_name": "아우디", "vehicle_name": "A3", "sales_year": 2026, "sales_month": 6, "sales_count": 84, "sales_avg_price": None},
    {"manufacturer_name": "아우디", "vehicle_name": "Q8", "sales_year": 2026, "sales_month": 6, "sales_count": 54 + 4, "sales_avg_price": None},  # Q8 54 + Q8 e-tron 4
    {"manufacturer_name": "아우디", "vehicle_name": "Q7", "sales_year": 2026, "sales_month": 6, "sales_count": 54, "sales_avg_price": None},
    {"manufacturer_name": "아우디", "vehicle_name": "A8", "sales_year": 2026, "sales_month": 6, "sales_count": 21, "sales_avg_price": None},
    {"manufacturer_name": "아우디", "vehicle_name": "A4", "sales_year": 2026, "sales_month": 6, "sales_count": 3, "sales_avg_price": None},
    {"manufacturer_name": "아우디", "vehicle_name": "e-tron GT", "sales_year": 2026, "sales_month": 6, "sales_count": 2, "sales_avg_price": None},  # 원자료 표기: "The new e-tron GT"
    {"manufacturer_name": "아우디", "vehicle_name": "A7", "sales_year": 2026, "sales_month": 6, "sales_count": 1, "sales_avg_price": None},
    # 매칭 제외(우리 vehicle 테이블에 없음): The new A5+A5 64 / Q6 e-tron 36

    # ── 렉서스 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "렉서스", "vehicle_name": "ES", "sales_year": 2026, "sales_month": 6, "sales_count": 545, "sales_avg_price": None},
    {"manufacturer_name": "렉서스", "vehicle_name": "NX", "sales_year": 2026, "sales_month": 6, "sales_count": 530, "sales_avg_price": None},
    {"manufacturer_name": "렉서스", "vehicle_name": "RX", "sales_year": 2026, "sales_month": 6, "sales_count": 288, "sales_avg_price": None},
    {"manufacturer_name": "렉서스", "vehicle_name": "UX", "sales_year": 2026, "sales_month": 6, "sales_count": 165, "sales_avg_price": None},
    {"manufacturer_name": "렉서스", "vehicle_name": "LX", "sales_year": 2026, "sales_month": 6, "sales_count": 32, "sales_avg_price": None},
    {"manufacturer_name": "렉서스", "vehicle_name": "LS", "sales_year": 2026, "sales_month": 6, "sales_count": 12, "sales_avg_price": None},
    # 매칭 제외(우리 vehicle 테이블에 없음): LM 122 / IS는 이번 달 목록에 없음

    # ── 볼보 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "볼보", "vehicle_name": "EX30", "sales_year": 2026, "sales_month": 6, "sales_count": 624 + 322, "sales_avg_price": None},  # EX30 624 + EX30 CC 322
    {"manufacturer_name": "볼보", "vehicle_name": "XC60", "sales_year": 2026, "sales_month": 6, "sales_count": 366, "sales_avg_price": None},
    {"manufacturer_name": "볼보", "vehicle_name": "S90", "sales_year": 2026, "sales_month": 6, "sales_count": 117, "sales_avg_price": None},
    {"manufacturer_name": "볼보", "vehicle_name": "XC40", "sales_year": 2026, "sales_month": 6, "sales_count": 115, "sales_avg_price": None},
    {"manufacturer_name": "볼보", "vehicle_name": "XC90", "sales_year": 2026, "sales_month": 6, "sales_count": 111, "sales_avg_price": None},
    {"manufacturer_name": "볼보", "vehicle_name": "V60", "sales_year": 2026, "sales_month": 6, "sales_count": 24, "sales_avg_price": None},  # 원자료 표기: "V60 Cross Country"
    # S60, EX90은 이번 달 목록에 없음 -> 스킵

    # ── 토요타 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "토요타", "vehicle_name": "RAV4", "sales_year": 2026, "sales_month": 6, "sales_count": 674, "sales_avg_price": None},  # 원자료 표기: "All New RAV4"
    {"manufacturer_name": "토요타", "vehicle_name": "캠리", "sales_year": 2026, "sales_month": 6, "sales_count": 214, "sales_avg_price": None},
    {"manufacturer_name": "토요타", "vehicle_name": "프리우스", "sales_year": 2026, "sales_month": 6, "sales_count": 112, "sales_avg_price": None},
    {"manufacturer_name": "토요타", "vehicle_name": "시에나", "sales_year": 2026, "sales_month": 6, "sales_count": 71, "sales_avg_price": None},
    {"manufacturer_name": "토요타", "vehicle_name": "하이랜더", "sales_year": 2026, "sales_month": 6, "sales_count": 24, "sales_avg_price": None},
    {"manufacturer_name": "토요타", "vehicle_name": "GR86", "sales_year": 2026, "sales_month": 6, "sales_count": 24, "sales_avg_price": None},
    # 매칭 제외(우리 vehicle 테이블에 없음): Alphard 186 / Crown 96 (코롤라·코롤라 크로스는 이번 달 목록에 없음)

    # ── 미니 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "미니", "vehicle_name": "쿠퍼", "sales_year": 2026, "sales_month": 6, "sales_count": 389, "sales_avg_price": None},  # 원자료 표기: "Cooper"
    {"manufacturer_name": "미니", "vehicle_name": "쿠퍼 SE", "sales_year": 2026, "sales_month": 6, "sales_count": 134, "sales_avg_price": None},  # 원자료 표기: "Mini Electric"
    {"manufacturer_name": "미니", "vehicle_name": "컨트리맨", "sales_year": 2026, "sales_month": 6, "sales_count": 157 + 2, "sales_avg_price": None},  # Countryman 157 + Countryman Electric 2
    # 매칭 제외(우리 vehicle 테이블에 없음): Aceman 80 / Convertible 74 (쿠퍼 S는 이번 자료에 별도 표기 없음)

    # ── 포르쉐 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "포르쉐", "vehicle_name": "타이칸", "sales_year": 2026, "sales_month": 6, "sales_count": 196, "sales_avg_price": None},  # 원자료 표기: "Taycan"
    {"manufacturer_name": "포르쉐", "vehicle_name": "카이엔", "sales_year": 2026, "sales_month": 6, "sales_count": 158, "sales_avg_price": None},  # 원자료 표기: "Cayenne"
    {"manufacturer_name": "포르쉐", "vehicle_name": "파나메라", "sales_year": 2026, "sales_month": 6, "sales_count": 137, "sales_avg_price": None},  # 원자료 표기: "Panamera"
    {"manufacturer_name": "포르쉐", "vehicle_name": "마칸", "sales_year": 2026, "sales_month": 6, "sales_count": 123, "sales_avg_price": None},  # 원자료 표기: "Macan Electric"
    {"manufacturer_name": "포르쉐", "vehicle_name": "911", "sales_year": 2026, "sales_month": 6, "sales_count": 102, "sales_avg_price": None},  # 원자료 표기: "The New 911"
    # 카이맨은 이번 달 목록에 없음 -> 스킵

    # ── 폭스바겐 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "폭스바겐", "vehicle_name": "ID.4", "sales_year": 2026, "sales_month": 6, "sales_count": 249, "sales_avg_price": None},
    {"manufacturer_name": "폭스바겐", "vehicle_name": "골프", "sales_year": 2026, "sales_month": 6, "sales_count": 198, "sales_avg_price": None},  # 원자료 표기: "Golf"
    {"manufacturer_name": "폭스바겐", "vehicle_name": "아틀라스", "sales_year": 2026, "sales_month": 6, "sales_count": 31, "sales_avg_price": None},  # 원자료 표기: "Atlas"
    # 매칭 제외(우리 vehicle 테이블에 없음): Touareg 91 / ID.5 33 (티구안·파사트·아테온·ID.7은 이번 달 목록에 없음)

    # ── 혼다 (2026년 6월) ──────────────────────────────
    {"manufacturer_name": "혼다", "vehicle_name": "파일럿", "sales_year": 2026, "sales_month": 6, "sales_count": 24, "sales_avg_price": None},  # 원자료 표기: "New Pilot"
    {"manufacturer_name": "혼다", "vehicle_name": "CR-V", "sales_year": 2026, "sales_month": 6, "sales_count": 15, "sales_avg_price": None},
    {"manufacturer_name": "혼다", "vehicle_name": "어코드", "sales_year": 2026, "sales_month": 6, "sales_count": 7, "sales_avg_price": None},  # 원자료 표기: "Accord"
    # 매칭 제외(우리 vehicle 테이블에 없음): Odyssey 1 (시빅·HR-V는 이번 달 목록에 없음)
]


def get_vehicle_map():
    """(manufacturer_name, vehicle_name) -> vehicle_id 매핑 반환"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT v.vehicle_id, v.vehicle_name, m.manufacturer_name
        FROM vehicle v
        JOIN manufacturer m ON v.manufacturer_id = m.manufacturer_id
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {(mname, vname): vid for vid, vname, mname in rows}


def get_estimated_price_map():
    """
    vehicle_id -> 추정 평균가 매핑 반환.
    vehicle_detail에 등록된 트림들의 detail_base_price 평균을 사용함.
    (실거래가 공식 통계가 없어서 카탈로그 가격 기준 추정치로 대신함)
    트림 정보가 하나도 없는 vehicle_id는 매핑에서 빠짐(그 경우 sales_avg_price는 NULL로 남음).
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT vehicle_id, AVG(detail_base_price)
        FROM vehicle_detail
        WHERE detail_base_price IS NOT NULL
        GROUP BY vehicle_id
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {vid: round(avg_price) for vid, avg_price in rows}


def insert_sales_stats(records):
    vehicle_map = get_vehicle_map()
    price_map = get_estimated_price_map()

    conn = get_db_connection()
    cur = conn.cursor()

    # 이미 들어가있는 (vehicle_id, year, month) 조합 조회 -> 중복 방지
    cur.execute("SELECT vehicle_id, sales_year, sales_month FROM sales_stat")
    existing = set(cur.fetchall())

    sql = """
        INSERT INTO sales_stat (sales_year, sales_month, sales_count, sales_avg_price, vehicle_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    saved, skipped, no_match, no_price = 0, 0, [], []
    for r in records:
        if r.get("sales_year") is None or r.get("sales_month") is None:
            print(f"[연/월 미입력, 스킵] {r['manufacturer_name']} {r['vehicle_name']}")
            skipped += 1
            continue

        key = (r["manufacturer_name"], r["vehicle_name"])
        vehicle_id = vehicle_map.get(key)
        if vehicle_id is None:
            no_match.append(f"{r['manufacturer_name']} {r['vehicle_name']}")
            skipped += 1
            continue

        if (vehicle_id, r["sales_year"], r["sales_month"]) in existing:
            print(f"[이미 있음, 스킵] {r['manufacturer_name']} {r['vehicle_name']} {r['sales_year']}-{r['sales_month']}")
            skipped += 1
            continue

        # sales_avg_price가 명시적으로 채워져 있으면 그 값을 쓰고,
        # 없으면(None) vehicle_detail 트림 평균가로 추정치를 채움
        avg_price = r.get("sales_avg_price")
        if avg_price is None:
            avg_price = price_map.get(vehicle_id)
            if avg_price is None:
                no_price.append(f"{r['manufacturer_name']} {r['vehicle_name']}")

        cur.execute(
            sql,
            (
                r["sales_year"],
                r["sales_month"],
                r.get("sales_count"),
                avg_price,
                vehicle_id,
            ),
        )
        existing.add((vehicle_id, r["sales_year"], r["sales_month"]))
        saved += 1
        price_note = f", 추정가={avg_price:,}원" if avg_price else ""
        print(f"저장: {r['manufacturer_name']} {r['vehicle_name']} {r['sales_year']}-{r['sales_month']} -> {r['sales_count']}대{price_note}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n총 {saved}개 저장 완료 / {skipped}개 스킵")
    if no_match:
        print("\nvehicle 테이블에서 매칭 안 된 모델 (이름 확인 필요):")
        for n in no_match:
            print(f"  - {n}")
    if no_price:
        print("\nvehicle_detail에 트림 가격이 없어서 sales_avg_price가 NULL로 들어간 모델:")
        for n in no_price:
            print(f"  - {n}")


if __name__ == "__main__":
    insert_sales_stats(sales_records)
