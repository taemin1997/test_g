import pymysql

from db_config import get_db_connection

vehicle_seed = [
    # ── 현대자동차 (14) ──────────────────────────────
    {"manufacturer_name": "현대자동차", "vehicle_name": "캐스퍼", "body_type": "경차", "car_description": "가성비 좋은 경형 SUV, 짧은 출퇴근에 적합", "vec_purpose": "출퇴근", "car_img": "https://m.casper.hyundai.com/wcontents/attach-1/2021/08/016/movie/main.png", "new_car_url": "https://casper.hyundai.com/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BA%90%EC%8A%A4%ED%8D%BC"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "아반떼", "body_type": "준중형세단", "car_description": "현대차 베스트셀링 준중형 세단", "vec_purpose": "출퇴근", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/avante-26my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/avante/intro", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Page=1&Order=8&Brand=303&Series=2710&Model="},
    {"manufacturer_name": "현대자동차", "vehicle_name": "쏘나타", "body_type": "중형세단", "car_description": "안정적인 승차감의 중형 세단", "vec_purpose": "출퇴근", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/sonata-the-edge-26my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/sonata-the-edge/intro", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%8F%98%EB%82%98%ED%83%80"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "그랜저", "body_type": "준대형세단", "car_description": "국민 준대형 세단, 품격 있는 비즈니스카", "vec_purpose": "비즈니스", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/grandeur-27fl-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/grandeur/intro", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Page=1&Order=8&Brand=303&Series=2718&Model="},
    {"manufacturer_name": "현대자동차", "vehicle_name": "베뉴", "body_type": "SUV", "car_description": "현대차 엔트리 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/venue-27my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/venue/intro", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%B2%A0%EB%89%B4"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "코나", "body_type": "SUV", "car_description": "개성있는 디자인의 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/kona-27my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/kona/intro", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BD%94%EB%82%98"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "투싼", "body_type": "SUV", "car_description": "실용적인 준중형 SUV", "vec_purpose": "가족", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/tucson-26my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/tucson/intro/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%88%AC%EC%8B%BC"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "싼타페", "body_type": "SUV", "car_description": "넉넉한 공간의 중형 SUV, 가족 나들이용", "vec_purpose": "가족", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/santafe-26my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/santafe/intro", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%8B%BC%ED%83%80%ED%8E%98"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "팰리세이드", "body_type": "대형SUV", "car_description": "3열까지 여유로운 대형 SUV", "vec_purpose": "가족", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/meta-palisade-25fc-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/the-all-new-palisade/intro", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%8C%B0%EB%A6%AC%EC%84%B8%EC%9D%B4%EB%93%9C"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "스타리아", "body_type": "MPV", "car_description": "다인승 미니밴, 캠핑·가족 여행에 적합", "vec_purpose": "캠핑", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/staria-26pe-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/staria/intro", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%8A%A4%ED%83%80%EB%A6%AC%EC%95%84"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "아이오닉5", "body_type": "SUV", "car_description": "현대차 전용 전기 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/ioniq5-27my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/ioniq5/intro/", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Page=1&Order=8&Brand=303&Series=4200&Model="},
    {"manufacturer_name": "현대자동차", "vehicle_name": "아이오닉6", "body_type": "세단", "car_description": "공기역학적 디자인의 전기 세단", "vec_purpose": "출퇴근", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/ioniq6-25fl-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/the-new-ioniq6/intro/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%95%84%EC%9D%B4%EC%98%A4%EB%8B%896"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "아이오닉9", "body_type": "대형SUV", "car_description": "3열 대형 전기 SUV", "vec_purpose": "가족", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/ioniq9-27my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/ioniq9/intro/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%95%84%EC%9D%B4%EC%98%A4%EB%8B%899"},
    {"manufacturer_name": "현대자동차", "vehicle_name": "넥쏘", "body_type": "SUV", "car_description": "수소전기 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.hyundai.com/contents/repn-car/side-45/nexo-27my-45side.png", "new_car_url": "https://www.hyundai.com/kr/ko/e/vehicles/nexo/intro", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%84%A5%EC%8F%98"},

    # ── 기아 (14) ──────────────────────────────
    {"manufacturer_name": "기아", "vehicle_name": "모닝", "body_type": "경차", "car_description": "기아 엔트리 경차", "vec_purpose": "출퇴근", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krja305/morning_s_a2g.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/morning/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%AA%A8%EB%8B%9D"},
    {"manufacturer_name": "기아", "vehicle_name": "레이", "body_type": "경차", "car_description": "박스형 경차, 넓은 실내가 장점", "vec_purpose": "출퇴근", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krtm311/ray_s_ud.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/ray/features", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=307&Series=3162&Model="},
    {"manufacturer_name": "기아", "vehicle_name": "K5", "body_type": "중형세단", "car_description": "스포티한 디자인의 중형 세단", "vec_purpose": "출퇴근", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krdl243/k5_s_c7s.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/k5/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+K5"},
    {"manufacturer_name": "기아", "vehicle_name": "K8", "body_type": "준대형세단", "car_description": "그랜저급 준대형 세단", "vec_purpose": "비즈니스", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krgl301/k8_s_byg.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/k8/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+K8"},
    {"manufacturer_name": "기아", "vehicle_name": "셀토스", "body_type": "SUV", "car_description": "소형 SUV 베스트셀러", "vec_purpose": "출퇴근", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krst290/seltos_s_swp.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/seltos/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%85%80%ED%86%A0%EC%8A%A4"},
    {"manufacturer_name": "기아", "vehicle_name": "니로", "body_type": "SUV", "car_description": "하이브리드/전기 대표 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krsg300/niro-hybrid_s_cge.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/niro/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%8B%88%EB%A1%9C"},
    {"manufacturer_name": "기아", "vehicle_name": "스포티지", "body_type": "SUV", "car_description": "글로벌 판매 1위 준중형 SUV", "vec_purpose": "가족", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krnq259/sportage_nqjj5ab36_a_c7a.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/sportage/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%8A%A4%ED%8F%AC%ED%8B%B0%EC%A7%80"},
    {"manufacturer_name": "기아", "vehicle_name": "쏘렌토", "body_type": "SUV", "car_description": "패밀리형 중형 SUV", "vec_purpose": "가족", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krmq255/sorento_s_bn4.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/sorento/features", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=307&Series=2740&Model="},
    {"manufacturer_name": "기아", "vehicle_name": "모하비", "body_type": "대형SUV", "car_description": "프레임 바디의 대형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSX9DMjtYl5roLC1IsVmsatSSqzqwOxiJ7Ig-GHnjjg5w&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%AA%A8%ED%95%98%EB%B9%84"},
    {"manufacturer_name": "기아", "vehicle_name": "카니발", "body_type": "MPV", "car_description": "국내 미니밴 시장 1위, 캠핑·다인승에 최적", "vec_purpose": "캠핑", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krkp214/carnival_s_isg.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/carnival/features", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=307&Series=2743&Model="},
    {"manufacturer_name": "기아", "vehicle_name": "EV3", "body_type": "SUV", "car_description": "준중형 전기 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krsv292/ev3_s_ag3.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/ev3/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EV3"},
    {"manufacturer_name": "기아", "vehicle_name": "EV5", "body_type": "SUV", "car_description": "중형 전기 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrIXtenVCaGwGw83iB2ILDUXw8Gl8nnrpr1RFpGOooAA&s", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EV5"},
    {"manufacturer_name": "기아", "vehicle_name": "EV6", "body_type": "SUV", "car_description": "기아 전용 전기 SUV/크로스오버", "vec_purpose": "출퇴근", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krcv253/ev6_s_swp.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/ev6/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EV6"},
    {"manufacturer_name": "기아", "vehicle_name": "EV9", "body_type": "대형SUV", "car_description": "3열 대형 전기 SUV", "vec_purpose": "가족", "car_img": "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krmv297/ev9_s_ism.png?imwidth=800", "new_car_url": "https://www.kia.com/kr/vehicles/ev9/features", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EV9"},

    # ── 제네시스 (7) ──────────────────────────────
    {"manufacturer_name": "제네시스", "vehicle_name": "G70", "body_type": "세단", "car_description": "제네시스 엔트리 럭셔리 세단", "vec_purpose": "출퇴근", "car_img": "https://dams.hyundai-autoever.com/v1/openapi/hmg-presigned-url/50534b313031303030303030303030303130333833/models/g70/2026/key-visual/genesis-g70-2026-key-visual-large.jpg", "new_car_url": "https://www.genesis.com/kr/ko/models/luxury-sedan-genesis/g70/highlights.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+G70"},
    {"manufacturer_name": "제네시스", "vehicle_name": "G80", "body_type": "세단", "car_description": "준대형 럭셔리 세단", "vec_purpose": "비즈니스", "car_img": "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/G80/list-thumbnail/2026-01-06/16-22-33/genesis-kr-admin-model-list-thumbnail-g80-27my-pc-630x240-ko.png", "new_car_url": "https://www.genesis.com/kr/ko/models/luxury-sedan-genesis/g80/highlights.html", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=304&Series=3558&Model="},
    {"manufacturer_name": "제네시스", "vehicle_name": "G90", "body_type": "세단", "car_description": "제네시스 플래그십 세단", "vec_purpose": "비즈니스", "car_img": "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/G90/list-thumbnail/2025-02-27/15-21-43/genesis-kr-admin-model-list-thumbnail-g90-desktop-630x240-ko.png", "new_car_url": "https://www.genesis.com/kr/ko/models/luxury-sedan-genesis/g90/highlights.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+G90"},
    {"manufacturer_name": "제네시스", "vehicle_name": "GV60", "body_type": "SUV", "car_description": "제네시스 전용 전기 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV60/list-thumbnail/2026-03-17/13-33-39/genesis-kr-admin-model-list-thumbnail-gv60-27my-desktop-630x240.png", "new_car_url": "https://www.genesis.com/kr/ko/models/luxury-suv-genesis/gv60/highlights.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GV60"},
    {"manufacturer_name": "제네시스", "vehicle_name": "GV70", "body_type": "SUV", "car_description": "스포티한 중형 SUV", "vec_purpose": "가족", "car_img": "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV70/list-thumbnail/2025-10-10/11-18-12/genesis-kr-admin-model-list-thumbnail-gv70-desktop-630x240-ko.png", "new_car_url": "https://www.genesis.com/kr/ko/models/luxury-suv-genesis/gv70/highlights.html", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=304&Series=4161&Model="},
    {"manufacturer_name": "제네시스", "vehicle_name": "GV80", "body_type": "SUV", "car_description": "제네시스 대표 대형 SUV", "vec_purpose": "가족", "car_img": "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV80/list-thumbnail/2026-02-11/15-51-00/genesis-kr-admin-model-list-thumbnail-gv80-desktop-630x240-ko.png", "new_car_url": "https://www.genesis.com/kr/ko/models/luxury-suv-genesis/gv80/highlights.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GV80"},
    {"manufacturer_name": "제네시스", "vehicle_name": "GV80 쿠페", "body_type": "SUV", "car_description": "GV80의 쿠페형 파생 모델", "vec_purpose": "가족", "car_img": "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV80%20Coupe/list-thumbnail/2025-09-05/16-47-57/genesis-kr-admin-model-list-thumbnail-gv80-coupe-desktop-630x240-ko.png", "new_car_url": "https://www.genesis.com/kr/ko/models/luxury-suv-genesis/gv80-coupe/highlights.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GV80+%EC%BF%A0%ED%8E%98"},

    # ── KG모빌리티 (8) ──────────────────────────────
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "티볼리", "body_type": "SUV", "car_description": "KGM 엔트리 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://cdn.aictimg.com/newcar/model/202306/44285.jpg", "new_car_url": "https://www.kg-mobility.com/pr/model/show-room/200000100010007", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%8B%B0%EB%B3%BC%EB%A6%AC"},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "코란도", "body_type": "SUV", "car_description": "준중형 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRW2dlfN_ZJx0shK1y8FuB0v6ccEXcT3dKq-FMM1NIhew&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BD%94%EB%9E%80%EB%8F%84"},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "액티언", "body_type": "SUV", "car_description": "쿠페형 중형 SUV", "vec_purpose": "출퇴근", "car_img": "https://cdn.aictimg.com/newcar/model/202408/128939.jpg", "new_car_url": "https://www.kg-mobility.com/pr/model/show-room/200000100010016", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%95%A1%ED%8B%B0%EC%96%B8"},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "토레스", "body_type": "SUV", "car_description": "정통 SUV 스타일의 중형 SUV", "vec_purpose": "캠핑", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7zV7hu4ceWj2bekD0RPMKmX8yd_qEvZfhg67Z1bmsiA&s=10", "new_car_url": "https://www.kg-mobility.com/pr/model/show-room/200000100010001", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%86%A0%EB%A0%88%EC%8A%A4"},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "토레스 EVX", "body_type": "SUV", "car_description": "토레스 기반 전기 SUV", "vec_purpose": "캠핑", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7zV7hu4ceWj2bekD0RPMKmX8yd_qEvZfhg67Z1bmsiA&s=10", "new_car_url": "https://www.kg-mobility.com/kr/showroom/torresevx/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%86%A0%EB%A0%88%EC%8A%A4+EVX"},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "무쏘 스포츠 & 무쏘 칸", "body_type": "픽업트럭", "car_description": "국내 픽업트럭 대표 모델(구 렉스턴 스포츠&칸, 2025년 개명)", "vec_purpose": "캠핑", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqBqpa2ZGkgrkAxfeIzgxJwsXgfuV7xozMDlCxoElWmQ&s=10", "new_car_url": "https://www.kg-mobility.com/pr/model/show-room/200000100030004", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%AC%B4%EC%8F%98+%EC%8A%A4%ED%8F%AC%EC%B8%A0+%26+%EB%AC%B4%EC%8F%98+%EC%B9%B8"},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "무쏘 EV", "body_type": "픽업트럭", "car_description": "전기 픽업트럭", "vec_purpose": "캠핑", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSIKKe4rtMmVKJGP87kT0NYeZ6wjIM9NBQlKZiVLHI0Q&s=10", "new_car_url": "https://www.kg-mobility.com/pr/model/show-room/200000100030003", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%AC%B4%EC%8F%98+EV"},
    {"manufacturer_name": "KG모빌리티", "vehicle_name": "렉스턴", "body_type": "대형SUV", "car_description": "프레임 바디의 대형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJb2iDvyF1Swm-yn3WSz45id2YFT8PQBu5Q4RPKe0jYQ&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%A0%89%EC%8A%A4%ED%84%B4"},

    # ── 르노코리아 (2, SM6·QM6 단종으로 실제 라인업이 이 정도임) ──────────────────────────────
    {"manufacturer_name": "르노코리아", "vehicle_name": "그랑 콜레오스", "body_type": "SUV", "car_description": "하이브리드 인기의 중형 SUV, 르노코리아 판매 대부분 차지", "vec_purpose": "가족", "car_img": "https://cdn.renault.co.kr/ko/resource/img/upload/asset/koleos/carousel/img_carousel01_01.webp", "new_car_url": "https://www.renault.co.kr/ko/model/koleos_overview.jsp", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EA%B7%B8%EB%9E%91+%EC%BD%9C%EB%A0%88%EC%98%A4%EC%8A%A4"},
    {"manufacturer_name": "르노코리아", "vehicle_name": "아르카나", "body_type": "SUV", "car_description": "쿠페형 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbH51smUbX8R2oBG1xXKAeka1Aflm30nRKZV5ENXMz7g&s=10", "new_car_url": "https://www.renault.co.kr/ko/model/arkana_overview.jsp", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%95%84%EB%A5%B4%EC%B9%B4%EB%82%98"},

    # ── 쉐보레 (2, 수입모델 전량 단종으로 국내생산 2종만 판매중) ──────────────────────────────
    {"manufacturer_name": "쉐보레", "vehicle_name": "트랙스 크로스오버", "body_type": "SUV", "car_description": "국내 생산 소형 SUV, 쉐보레코리아 판매의 대부분 차지", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPrjZPKxGvfJh4A8IYzertj9fpIS-h7T2gtvUkd9Atbw&s", "new_car_url": "https://www.chevrolet.co.kr/cuvs/trax-crossover", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%8A%B8%EB%9E%99%EC%8A%A4+%ED%81%AC%EB%A1%9C%EC%8A%A4%EC%98%A4%EB%B2%84"},
    {"manufacturer_name": "쉐보레", "vehicle_name": "트레일블레이저", "body_type": "SUV", "car_description": "국내 생산 소형 SUV, 수출 비중이 높음", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHrC37iGWcgtuzk2ZoKqSy-k_5bPEB3iT1Gw01_odDdA&s=10", "new_car_url": "https://www.chevrolet.co.kr/suvs/trailblazer", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%8A%B8%EB%A0%88%EC%9D%BC%EB%B8%94%EB%A0%88%EC%9D%B4%EC%A0%80"},

    # ── BMW (14) ──────────────────────────────
    {"manufacturer_name": "BMW", "vehicle_name": "1시리즈", "body_type": "해치백", "car_description": "BMW 엔트리 해치백", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1Gb7xSHq2p7sAsK7QJ9tiAWm4s3Az0LC-iiBM9DJECg&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/1-series/bmw-1-series/bmw-1-series.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+1%EC%8B%9C%EB%A6%AC%EC%A6%88"},
    {"manufacturer_name": "BMW", "vehicle_name": "2시리즈", "body_type": "쿠페", "car_description": "컴팩트 쿠페/그란쿠페", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0FTity3vmHV-LmC4qMLW-2lWtvhKO0j-ibA-KSf2a3Q&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/2-series/gran-coupe/bmw-2-series-gran-coupe.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+2%EC%8B%9C%EB%A6%AC%EC%A6%88"},
    {"manufacturer_name": "BMW", "vehicle_name": "3시리즈", "body_type": "세단", "car_description": "BMW 대표 스포츠 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR_JL9Iq83qW-53h__nO_xvXKrKc0DYDGKya-cBAyfpw&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/3-series/bmw-3-series-sedan/bmw-3-series-sedan.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+3%EC%8B%9C%EB%A6%AC%EC%A6%88"},
    {"manufacturer_name": "BMW", "vehicle_name": "4시리즈", "body_type": "쿠페", "car_description": "3시리즈 기반 쿠페/컨버터블", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQs0rND00Z-g4C5J7D4hTxTRfdKTt181pWL1O-e-nQZeA&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/4-series/4-series-coupe/bmw-4-series-coupe.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+4%EC%8B%9C%EB%A6%AC%EC%A6%88"},
    {"manufacturer_name": "BMW", "vehicle_name": "5시리즈", "body_type": "세단", "car_description": "비즈니스 세단의 기준", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8VgvJTtQ6fa5X7fXF8SvEwm9bMXaXdDILZIbpnSislA&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/5-series/sedan/bmw-5-series-sedan-overview.html", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=362&Series=2792&Model="},
    {"manufacturer_name": "BMW", "vehicle_name": "7시리즈", "body_type": "세단", "car_description": "BMW 플래그십 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4HWLfCmBkCWf_lDt9BhNmPNsiuKe_FTvxaJzjhfsMA&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/7-series/7-series-sedan/bmw-7-series-sedan.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+7%EC%8B%9C%EB%A6%AC%EC%A6%88"},
    {"manufacturer_name": "BMW", "vehicle_name": "X1", "body_type": "SUV", "car_description": "BMW 엔트리 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4_nMUkC9Wl1i-ishIA3GNQgKlzkdjQ0oyxTcsfnK07A&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/x-series/x1/bmw-x1.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+X1"},
    {"manufacturer_name": "BMW", "vehicle_name": "X2", "body_type": "SUV", "car_description": "쿠페형 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ55L14StNen_cAPQCC-YsPgxHXeoJxT2vxDuqBwY0T5Q&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/x-series/x2/bmw-x2-overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+X2"},
    {"manufacturer_name": "BMW", "vehicle_name": "X3", "body_type": "SUV", "car_description": "준중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThi7fvhMU9pepW8zXlTSQ4805PE0IMgokD2EzENY7DxQ&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/x-series/x3/bmw-x3.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+X3"},
    {"manufacturer_name": "BMW", "vehicle_name": "X4", "body_type": "SUV", "car_description": "쿠페형 준중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-fkDQtBGkHS_EFZyoM6V6pQCSlOP36SojFpyMtT9YzQ&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+X4"},
    {"manufacturer_name": "BMW", "vehicle_name": "X5", "body_type": "SUV", "car_description": "BMW 대표 중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPh_wqXxyKKiW38_Lv9BvK9WpfwQGYkp9UT-HA7HF9Ew&s", "new_car_url": "https://www.bmw.co.kr/ko/all-models/x-series/x5/bmw-x5.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+X5"},
    {"manufacturer_name": "BMW", "vehicle_name": "X6", "body_type": "SUV", "car_description": "쿠페형 중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR41iDBLji5gN4HBpzlDPS3i3gNvGfBVAUGSsIQytV_gg&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/x-series/x6/bmw-x6.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+X6"},
    {"manufacturer_name": "BMW", "vehicle_name": "X7", "body_type": "대형SUV", "car_description": "BMW 최상위 대형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbNwpGdx7BYpdBFZWUhgD7srBVsc0FMqR0lmh2J7NS4w&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/x-series/x7/bmw-x7.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+X7"},
    {"manufacturer_name": "BMW", "vehicle_name": "i4", "body_type": "세단", "car_description": "3시리즈 기반 전기 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfmdrKKbJxleLXQYFnhMQuJFgc4uH2Kj2q7z3eqqqwwQ&s=10", "new_car_url": "https://www.bmw.co.kr/ko/all-models/bmw-i/i4/bmw-i4-gran-coupe.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+i4"},

    # ── 메르세데스-벤츠 (14) ──────────────────────────────
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "A클래스", "body_type": "세단", "car_description": "벤츠 엔트리 세단/해치백", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUC2amOxYjMxtZAzIWkTWZGEgsip9bCYVsMkQVuBEIFA&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/hatchback/a-class/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+A%ED%81%B4%EB%9E%98%EC%8A%A4"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "C클래스", "body_type": "세단", "car_description": "준중형 럭셔리 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS654Uj2hQxmJhJrH1dArCE-jAMEMwyFF9--gnS83_-zw&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/saloon/c-class/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+C%ED%81%B4%EB%9E%98%EC%8A%A4"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "E클래스", "body_type": "세단", "car_description": "국내 수입차 판매 1위권, 비즈니스 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXmqvQSAfO2ifwv4hPjCLftM1L2uhf1sTVzOxY-aYqbw&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/saloon/e-class/overview.html", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=349&Series=2822&Model="},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "S클래스", "body_type": "세단", "car_description": "벤츠 플래그십 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4yuR1tEKNmFz1b0kEqWROsW-c3x_ivb9SBPi61kqM-w&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/saloon/s-class/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+S%ED%81%B4%EB%9E%98%EC%8A%A4"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "CLA", "body_type": "세단", "car_description": "쿠페형 컴팩트 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPDpLbq-MnMjqE3T0aFQxi_SPsiPxohPJOIeGG1o1_Lw&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/coupe/cla/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+CLA"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLA", "body_type": "SUV", "car_description": "벤츠 엔트리 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhLJ-uZrr1oWNRo76K95FxF1wM6WY25tVNiRznYBgiFw&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/suv/gla/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GLA"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLB", "body_type": "SUV", "car_description": "7인승 옵션의 준중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtAeZrPpZr-DuU8XWpl4mjH47vOU57YaAj6-8R4wHCAg&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/suv/glb/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GLB"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLC", "body_type": "SUV", "car_description": "준중형 럭셔리 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTas67lM7qtO7ghnTnoPDrvZ4ncrf9DnaBD9Mhq_pQE-g&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/suv/glc/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GLC"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLE", "body_type": "SUV", "car_description": "중형 럭셔리 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQstfxFuEYk_t7OFflqMEGLBBDm0jBhZblHftBwMaJVfg&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/suv/gle/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GLE"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "GLS", "body_type": "대형SUV", "car_description": "벤츠 최상위 대형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxmwT-mrzsRMyuKvSgCvPlPzxn6vwlR2pC8GMRglVONw&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/suv/gls/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GLS"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "G클래스", "body_type": "SUV", "car_description": "정통 오프로더 SUV", "vec_purpose": "캠핑", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLb8ToI6Hlz_GNh59WLqxlr6poSBC-p5NR-Kdc4KfQEA&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/suv/g-class/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+G%ED%81%B4%EB%9E%98%EC%8A%A4"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "EQE", "body_type": "세단", "car_description": "E클래스급 순수 전기 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsKxN66iSnrAiyCcSjuiypcbcb6LkfSsDKugo0eufGew&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/suv/eqe/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EQE"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "EQS", "body_type": "세단", "car_description": "S클래스급 순수 전기 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUXAYbIzL_2yhxHrBZd5ZKCPunGgR1qh9jAsz9v8p2nw&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/saloon/eqs/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EQS"},
    {"manufacturer_name": "메르세데스-벤츠", "vehicle_name": "AMG GT", "body_type": "쿠페", "car_description": "벤츠 고성능 스포츠카", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvuWbISjmhkL0jmT3cDVv0VYyEOQU5WROvt0J7NKAlFQ&s=10", "new_car_url": "https://www.mercedes-benz.co.kr/passengercars/models/coupe/amg-gt-2-door/overview.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+AMG+GT"},

    # ── 아우디 (11) ──────────────────────────────
    {"manufacturer_name": "아우디", "vehicle_name": "A3", "body_type": "세단", "car_description": "아우디 엔트리 세단/해치백", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBcJzCwlXC5WMnOEgXzENntV56WrEkbBJMHrD258RG7Q&s", "new_car_url": "https://www.audi.co.kr/ko/models/a3/a3-saloon-2025/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+A3"},
    {"manufacturer_name": "아우디", "vehicle_name": "A4", "body_type": "세단", "car_description": "아우디 준중형 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7eLN45oeSvKi6iivKKmIUcr3TGWYgeG4BHOFZfTguhg&s=10", "new_car_url": "https://www.audi.co.kr/ko/models/a4/a4-saloon_2021/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+A4"},
    {"manufacturer_name": "아우디", "vehicle_name": "A6", "body_type": "세단", "car_description": "아우디 중형 비즈니스 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQnVDNtWJqaSzNK9kYEkXEG5wj99b4zccspMd8687fxQ&s", "new_car_url": "https://www.audi.co.kr/ko/models/a6/a6-sedan-2026/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+A6"},
    {"manufacturer_name": "아우디", "vehicle_name": "A7", "body_type": "세단", "car_description": "쿠페형 대형 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc6d85CQ89qa26sYj7thB8d_PDTDQAgd6MmXEMpG2m2Q&s=10", "new_car_url": "https://www.audi.co.kr/ko/models/a7/a7-sportback-2024/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+A7"},
    {"manufacturer_name": "아우디", "vehicle_name": "A8", "body_type": "세단", "car_description": "아우디 플래그십 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS72dR7xGRUhwPQ4QzSGD5yRT00mgWtps6XvZgbXC_hng&s=10", "new_car_url": "https://www.audi.co.kr/ko/models/a8/a8_2023/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+A8"},
    {"manufacturer_name": "아우디", "vehicle_name": "Q3", "body_type": "SUV", "car_description": "아우디 엔트리 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyUW51eUqw4WuK34zv8bm0WY_Os1UlYi4jv70fk-4VLA&s=10", "new_car_url": "https://www.audi.co.kr/ko/models/q3/q3_2022/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Q3"},
    {"manufacturer_name": "아우디", "vehicle_name": "Q5", "body_type": "SUV", "car_description": "콰트로 4륜구동 준중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCqtHhtJxM1oFbsiHLsnL6AJJrnRflSWMPvJSeomlfoQ&s=10", "new_car_url": "https://www.audi.co.kr/ko/models/q5/q5-suv-2025/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Q5"},
    {"manufacturer_name": "아우디", "vehicle_name": "Q7", "body_type": "SUV", "car_description": "7인승 대형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4zHD4zS9Jhcrf_wUIjp_jNm__znmYgGn_hrkvalZA_g&s=10", "new_car_url": "https://www.audi.co.kr/ko/models/q7/q7-suv-2025/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Q7"},
    {"manufacturer_name": "아우디", "vehicle_name": "Q8", "body_type": "SUV", "car_description": "쿠페형 대형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRivR3SY5KvXnQX_5PuNlD0yaOJjYLm-jD5Y2OtS5Xeow&s=10", "new_car_url": "https://www.audi.co.kr/ko/models/q8/q8-suv-2025/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Q8"},
    {"manufacturer_name": "아우디", "vehicle_name": "Q4 e-tron", "body_type": "SUV", "car_description": "준중형 전기 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0-MW_BADShVvzONjRgL8FJT9l8OdGNAXCBjZCtC5NUw&s", "new_car_url": "https://www.audi.co.kr/ko/models/q4-e-tron/q4etron_2022/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Q4+e-tron"},
    {"manufacturer_name": "아우디", "vehicle_name": "e-tron GT", "body_type": "세단", "car_description": "아우디 고성능 전기 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZskdU8ysyw8PNVsZfwqwQJqCTGDMxWMcZT1eJ2xpPgA&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+e-tron+GT"},

    # ── 폭스바겐 (7) ──────────────────────────────
    {"manufacturer_name": "폭스바겐", "vehicle_name": "골프", "body_type": "해치백", "car_description": "폭스바겐 스테디셀러 해치백", "vec_purpose": "출퇴근", "car_img": "https://www.volkswagen.co.kr/etc.clientlibs/clientlibs/vwa-ngw18/ngw18-frontend/apps/resources/statics/img/vw-logo-2x.png", "new_car_url": "https://www.volkswagen.co.kr/ko/models/golf.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EA%B3%A8%ED%94%84"},
    {"manufacturer_name": "폭스바겐", "vehicle_name": "티구안", "body_type": "SUV", "car_description": "국내 수입 SUV 판매 1위권 준중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ07ud1ygS4dQXyhI5-XpsG9U8gNZ8hiVNSkOg19B9bSQ&s=10", "new_car_url": None, "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=376&Series=3369&Model="},
    {"manufacturer_name": "폭스바겐", "vehicle_name": "파사트", "body_type": "세단", "car_description": "중형 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDdmKwh9dk5l0nKS9FMX4b9hYJGSxg9_9oh5vahGF3Rw&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%8C%8C%EC%82%AC%ED%8A%B8"},
    {"manufacturer_name": "폭스바겐", "vehicle_name": "아테온", "body_type": "세단", "car_description": "쿠페형 준대형 세단", "vec_purpose": "비즈니스", "car_img": "https://www.volkswagen.co.kr/etc.clientlibs/clientlibs/vwa-ngw18/ngw18-frontend/apps/resources/statics/img/vw-logo-2x.png", "new_car_url": "https://www.volkswagen.co.kr/ko/models/suggest_design.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%95%84%ED%85%8C%EC%98%A8"},
    {"manufacturer_name": "폭스바겐", "vehicle_name": "아틀라스", "body_type": "대형SUV", "car_description": "7인승 대형 SUV", "vec_purpose": "가족", "car_img": "https://www.volkswagen.co.kr/etc.clientlibs/clientlibs/vwa-ngw18/ngw18-frontend/apps/resources/statics/img/vw-logo-2x.png", "new_car_url": "https://www.volkswagen.co.kr/ko/models/atlas.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%95%84%ED%8B%80%EB%9D%BC%EC%8A%A4"},
    {"manufacturer_name": "폭스바겐", "vehicle_name": "ID.4", "body_type": "SUV", "car_description": "폭스바겐 순수 전기 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.volkswagen.co.kr/etc.clientlibs/clientlibs/vwa-ngw18/ngw18-frontend/apps/resources/statics/img/vw-logo-2x.png", "new_car_url": "https://www.volkswagen.co.kr/ko/models/id4.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+ID.4"},
    {"manufacturer_name": "폭스바겐", "vehicle_name": "ID.7", "body_type": "세단", "car_description": "폭스바겐 순수 전기 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRshF5xqnzG8N7eQ2j1gOKT6MWDtirNkEushVKgUbWapw&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+ID.7"},

    # ── 볼보 (8) ──────────────────────────────
    {"manufacturer_name": "볼보", "vehicle_name": "XC40", "body_type": "SUV", "car_description": "안전성 강조한 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSag_ndK_Cnwe7YpZMxIOFwL5fwy16qcL4dgVr1Au9ehQ&s=10", "new_car_url": "https://www.volvocars.com/kr/cars/xc40/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+XC40"},
    {"manufacturer_name": "볼보", "vehicle_name": "XC60", "body_type": "SUV", "car_description": "볼보 베스트셀러 중형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc71DmAJMKp7p2LclMt1sGNo6OL7WuUaEM8F5wRhsStw&s=10", "new_car_url": "https://www.volvocars.com/kr/cars/xc60/", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=459&Series=3527&Model="},
    {"manufacturer_name": "볼보", "vehicle_name": "XC90", "body_type": "대형SUV", "car_description": "7인승 플래그십 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoIONiR_ssGPzbMqAbmPGErLG3YGKnkkabzcN1LyqAUg&s=10", "new_car_url": "https://www.volvocars.com/kr/cars/xc90/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+XC90"},
    {"manufacturer_name": "볼보", "vehicle_name": "S60", "body_type": "세단", "car_description": "준중형 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkWkwxy7sbEfM331rggEXJaXFizmYHND-0s4jlA22ecg&s=10", "new_car_url": "https://ivy.volvocars.co.kr/v/cars/s60.asp", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+S60"},
    {"manufacturer_name": "볼보", "vehicle_name": "S90", "body_type": "세단", "car_description": "볼보 플래그십 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSJ9aGYRyZ6N3coTmuPVE5ouyhUbaKWZsBbnXeB-3WWg&s=10", "new_car_url": "https://www.volvocars.com/kr/cars/s90/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+S90"},
    {"manufacturer_name": "볼보", "vehicle_name": "V60", "body_type": "왜건", "car_description": "왜건형 준중형 모델", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnulMN-lAL4B4DipZjdpOUCDa7U5z8VWGXsLWNaepyVA&s=10", "new_car_url": "https://www.volvocars.com/kr/cars/v60-cross-country/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+V60"},
    {"manufacturer_name": "볼보", "vehicle_name": "EX30", "body_type": "SUV", "car_description": "볼보 엔트리 전기 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjyLP1RQwdEyXcHPOz_kJaFctvbsM_71BTEkxCUccCsw&s=10", "new_car_url": "https://www.volvocars.com/kr/cars/ex30-electric/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EX30"},
    {"manufacturer_name": "볼보", "vehicle_name": "EX90", "body_type": "대형SUV", "car_description": "볼보 플래그십 전기 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR6QOdmJM6HevrfRcONbAWHpoF_X8-2u2s1yXjpBi-EQ&s=10", "new_car_url": "https://www.volvocars.com/kr/cars/ex90-electric/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+EX90"},

    # ── 토요타 (8) ──────────────────────────────
    {"manufacturer_name": "토요타", "vehicle_name": "캠리", "body_type": "세단", "car_description": "토요타 대표 중형 세단", "vec_purpose": "출퇴근", "car_img": "https://www.toyota.co.kr/image/toyota_cover_camry.jpg", "new_car_url": "https://www.toyota.co.kr/models/camry/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BA%A0%EB%A6%AC"},
    {"manufacturer_name": "토요타", "vehicle_name": "코롤라", "body_type": "세단", "car_description": "준중형 세단, 뛰어난 연비", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRj_dEWE1BiI2bDdh8_vHLQPEfDJw2cmEZWC5zof_iEaw&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BD%94%EB%A1%A4%EB%9D%BC"},
    {"manufacturer_name": "토요타", "vehicle_name": "코롤라 크로스", "body_type": "SUV", "car_description": "코롤라 기반 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTl38ZJmpaqDNV_5xYzrViP4F37v0s1j3Mqaq9eKNSryQ&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BD%94%EB%A1%A4%EB%9D%BC+%ED%81%AC%EB%A1%9C%EC%8A%A4"},
    {"manufacturer_name": "토요타", "vehicle_name": "RAV4", "body_type": "SUV", "car_description": "글로벌 베스트셀링 SUV", "vec_purpose": "가족", "car_img": "https://www.toyota.co.kr/image/toyota_cover_rav4phev.jpg?v=2", "new_car_url": "https://www.toyota.co.kr/models/rav4phev/?detail_model=rav4phev_gr", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+RAV4"},
    {"manufacturer_name": "토요타", "vehicle_name": "하이랜더", "body_type": "대형SUV", "car_description": "3열 대형 SUV", "vec_purpose": "가족", "car_img": "https://www.toyota.co.kr/image/toyota_cover_highlander.jpg?v=3", "new_car_url": "https://www.toyota.co.kr/models/highlander/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%95%98%EC%9D%B4%EB%9E%9C%EB%8D%94"},
    {"manufacturer_name": "토요타", "vehicle_name": "프리우스", "body_type": "세단", "car_description": "하이브리드 대명사", "vec_purpose": "출퇴근", "car_img": "https://www.toyota.co.kr/image/toyota_cover_priusphev.jpg", "new_car_url": "https://www.toyota.co.kr/models/priusphev/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%94%84%EB%A6%AC%EC%9A%B0%EC%8A%A4"},
    {"manufacturer_name": "토요타", "vehicle_name": "시에나", "body_type": "MPV", "car_description": "하이브리드 미니밴", "vec_purpose": "캠핑", "car_img": "https://www.toyota.co.kr/image/toyota_cover_sienna.jpg?v=2", "new_car_url": "https://www.toyota.co.kr/models/sienna/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%8B%9C%EC%97%90%EB%82%98"},
    {"manufacturer_name": "토요타", "vehicle_name": "GR86", "body_type": "쿠페", "car_description": "후륜구동 스포츠 쿠페", "vec_purpose": "출퇴근", "car_img": "https://www.toyota.co.kr/image/toyota_cover_gr86.jpg", "new_car_url": "https://www.toyota.co.kr/models/gr86/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+GR86"},

    # ── 렉서스 (7) ──────────────────────────────
    {"manufacturer_name": "렉서스", "vehicle_name": "ES", "body_type": "세단", "car_description": "렉서스 베스트셀러 세단", "vec_purpose": "비즈니스", "car_img": "https://www.lexus.co.kr/source/sitemap/1200x630_28.jpg", "new_car_url": "https://www.lexus.co.kr/models/ES-300h/#/highlight", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=486&Series=2905&Model="},
    {"manufacturer_name": "렉서스", "vehicle_name": "IS", "body_type": "세단", "car_description": "후륜구동 스포츠 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7IPnDb50beWZPBhLVvB6A9GInrM9QDcziyVH_4XqUhw&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+IS"},
    {"manufacturer_name": "렉서스", "vehicle_name": "RX", "body_type": "SUV", "car_description": "렉서스 대표 SUV", "vec_purpose": "가족", "car_img": "https://www.lexus.co.kr/source/sitemap/1200x630_29.jpg", "new_car_url": "https://www.lexus.co.kr/models/RX-350h/#/highlight", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+RX"},
    {"manufacturer_name": "렉서스", "vehicle_name": "NX", "body_type": "SUV", "car_description": "준중형 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.lexus.co.kr/source/sitemap/1200x630_32.jpg", "new_car_url": "https://www.lexus.co.kr/models/NX-350h/#/highlight", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+NX"},
    {"manufacturer_name": "렉서스", "vehicle_name": "UX", "body_type": "SUV", "car_description": "렉서스 엔트리 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://www.lexus.co.kr/source/sitemap/2WD_thumb_A@x2_1_1.jpg", "new_car_url": "https://www.lexus.co.kr/models/UX-300h-2WD/#/highlight", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+UX"},
    {"manufacturer_name": "렉서스", "vehicle_name": "LS", "body_type": "세단", "car_description": "렉서스 플래그십 세단", "vec_purpose": "비즈니스", "car_img": "https://www.lexus.co.kr/source/sitemap/1200x630_26.jpg", "new_car_url": "https://www.lexus.co.kr/models/LS-500/#/highlight", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+LS"},
    {"manufacturer_name": "렉서스", "vehicle_name": "LX", "body_type": "대형SUV", "car_description": "프레임 바디 대형 SUV", "vec_purpose": "가족", "car_img": "https://www.lexus.co.kr/source/sitemap/VIP_share_thumb_B.jpg", "new_car_url": "https://www.lexus.co.kr/models/LX-700h-VIP/#/highlight", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+LX"},

    # ── 혼다 (5) ──────────────────────────────
    {"manufacturer_name": "혼다", "vehicle_name": "어코드", "body_type": "세단", "car_description": "혼다 중형 세단", "vec_purpose": "출퇴근", "car_img": "https://auto.hondakorea.co.kr/static/images/main/m1-car1.png", "new_car_url": "https://auto.hondakorea.co.kr/purchase/selectOption?carSeq=6&csnTrim=Hybrid&carCd=A0010004&year=2026", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%96%B4%EC%BD%94%EB%93%9C"},
    {"manufacturer_name": "혼다", "vehicle_name": "시빅", "body_type": "세단", "car_description": "준중형 세단/해치백", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUoMVySolB8df29RzlNkiE986x8L4OAK6A-RbMy69ejw&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%8B%9C%EB%B9%85"},
    {"manufacturer_name": "혼다", "vehicle_name": "CR-V", "body_type": "SUV", "car_description": "혼다 베스트셀러 SUV", "vec_purpose": "가족", "car_img": "https://auto.hondakorea.co.kr/static/images/main/m1-car1.png", "new_car_url": "https://auto.hondakorea.co.kr/purchase/selectTrim?carCd=A0010002&carNm=CR-V%20Hybrid&carSeq=3&year=2026", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+CR-V"},
    {"manufacturer_name": "혼다", "vehicle_name": "HR-V", "body_type": "SUV", "car_description": "혼다 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://auto.hondakorea.co.kr/static/images/main/m1-car1.png", "new_car_url": "https://auto.hondakorea.co.kr/purchase/selectOption?carSeq=5&csnTrim=Black%20Edition&carCd=A0010006&year=2026", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+HR-V"},
    {"manufacturer_name": "혼다", "vehicle_name": "파일럿", "body_type": "대형SUV", "car_description": "3열 대형 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcx1PhlwQjD4T_SNUhM4bIEZa7n2dcJ69MI60nsBK82g&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%8C%8C%EC%9D%BC%EB%9F%BF"},

    # ── 포르쉐 (6) ──────────────────────────────
    {"manufacturer_name": "포르쉐", "vehicle_name": "911", "body_type": "쿠페", "car_description": "포르쉐 아이코닉 스포츠카", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRDG5EN_Ovlc7bvfAnJNWVYmR8tvvMQHrlfUbaJ-RO0g&s=10", "new_car_url": "https://www.porsche.com/korea/ko/models/911/#modelRangeId=911", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+911"},
    {"manufacturer_name": "포르쉐", "vehicle_name": "카이맨", "body_type": "쿠페", "car_description": "미드십 스포츠카", "vec_purpose": "출퇴근", "car_img": "https://a.storyblok.com/f/322327/2400x2400/760d23203d/cm21n3kox0004-718-cayman-gts-40-twitter.jpg/m/2400x2400/smart/filters:format(avif)?dpl=dpl_Hz59koRSnHTVcc2uzfyWHR7dTtVN", "new_car_url": "https://www.porsche.com/korea/ko/models/718/718-models/718-cayman-gts-4/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%B9%B4%EC%9D%B4%EB%A7%A8"},
    {"manufacturer_name": "포르쉐", "vehicle_name": "카이엔", "body_type": "SUV", "car_description": "포르쉐 베스트셀러 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQscSoA4TJ-sUqt54VPLBiU4O8ScPfS9Sccem9d5FlyvA&s=10", "new_car_url": "https://www.porsche.com/korea/ko/models/cayenne/cayenne-models/cayenne/", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Page=1&Order=8&Brand=381&Series=3047&Model="},
    {"manufacturer_name": "포르쉐", "vehicle_name": "마칸", "body_type": "SUV", "car_description": "포르쉐 엔트리 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyF5dt9sKskxA1WRM1mt5OOPz5KjBkCVvYVOWWY40_jA&s=10", "new_car_url": "https://www.porsche.com/korea/ko/models/macan/#modelRangeId=macan", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EB%A7%88%EC%B9%B8"},
    {"manufacturer_name": "포르쉐", "vehicle_name": "파나메라", "body_type": "세단", "car_description": "4도어 그란투리스모", "vec_purpose": "비즈니스", "car_img": "https://a.storyblok.com/f/322327/1200x1200/958e6b2a37/000-twitter-card-panamera-4.jpg/m/1200x1200/smart/filters:format(avif)?dpl=dpl_Hz59koRSnHTVcc2uzfyWHR7dTtVN", "new_car_url": "https://www.porsche.com/korea/ko/models/panamera/panamera-models/panamera-4/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%8C%8C%EB%82%98%EB%A9%94%EB%9D%BC"},
    {"manufacturer_name": "포르쉐", "vehicle_name": "타이칸", "body_type": "세단", "car_description": "포르쉐 순수 전기 세단", "vec_purpose": "출퇴근", "car_img": "https://a.storyblok.com/f/322327/1200x1200/5aa52c184a/ta24q3eox0007-taycan-turbo-s-pko.jpg/m/1200x1200/smart/filters:format(avif)?dpl=dpl_Hz59koRSnHTVcc2uzfyWHR7dTtVN", "new_car_url": "https://www.porsche.com/korea/ko/models/taycan/taycan-models/taycan/", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%ED%83%80%EC%9D%B4%EC%B9%B8"},

    # ── 미니 (4) ──────────────────────────────
    {"manufacturer_name": "미니", "vehicle_name": "쿠퍼", "body_type": "해치백", "car_description": "미니 대표 소형 해치백", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrVTj2e23umwHTTUn6AyptmABKZeByXuqFTK7tMFB4yw&s=10", "new_car_url": "https://www.mini.co.kr/ko_KR/home/range/mini-cooper-3-door.html", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=367&Series=2886&Model="},
    {"manufacturer_name": "미니", "vehicle_name": "쿠퍼 S", "body_type": "해치백", "car_description": "쿠퍼의 고성능 버전", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfONgXzu4d915SVTya9ma0SbLz1VhBQvlFfVyvLyR2MA&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BF%A0%ED%8D%BC+S"},
    {"manufacturer_name": "미니", "vehicle_name": "쿠퍼 SE", "body_type": "해치백", "car_description": "미니 순수 전기 모델", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtcC-EUgDv_pwhX47gVvVttg4imzxMyKyVB73vZKvcUw&s=10", "new_car_url": "https://www.mini.co.kr/ko_KR/home/range/all-electric-mini-cooper.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BF%A0%ED%8D%BC+SE"},
    {"manufacturer_name": "미니", "vehicle_name": "컨트리맨", "body_type": "SUV", "car_description": "미니 소형 SUV", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSsvRPAS_nGm5MXHgENBiMCN8iM1Uu_8Kmj-j0vXQ6DJA&s=10", "new_car_url": "https://www.mini.co.kr/ko_KR/home/range/mini-countryman.html", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+%EC%BB%A8%ED%8A%B8%EB%A6%AC%EB%A7%A8"},

    # ── 테슬라 (4) ──────────────────────────────
    {"manufacturer_name": "테슬라", "vehicle_name": "Model 3", "body_type": "세단", "car_description": "테슬라 보급형 세단", "vec_purpose": "출퇴근", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQD4d4W3j6jRW8jSGY3Lc9mwsXvSyRE6U_LjsSeBChSxg&s=10", "new_car_url": "https://www.tesla.com/ko_kr/model3", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Model+3"},
    {"manufacturer_name": "테슬라", "vehicle_name": "Model Y", "body_type": "SUV", "car_description": "국내 테슬라 판매 대부분 차지하는 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjt8XvJ9m66MLVtKiWDjhTll-lILm8Zp8EmfiJFKW8sg&s=10", "new_car_url": "https://www.tesla.com/ko_kr/modely", "used_car_url": "https://auto.danawa.com/usedcar/?Work=list&Tab=list&Brand=611&Series=4333&Model="},
    {"manufacturer_name": "테슬라", "vehicle_name": "Model S", "body_type": "세단", "car_description": "테슬라 플래그십 세단", "vec_purpose": "비즈니스", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5ZJ-P_n86UxhvLQhWIAjIOC1wi9Amk4wLt6nnInOcJg&s=10", "new_car_url": None, "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Model+S"},
    {"manufacturer_name": "테슬라", "vehicle_name": "Model X", "body_type": "SUV", "car_description": "팰컨윙 도어의 플래그십 SUV", "vec_purpose": "가족", "car_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf3ok23MUroWhE7FBppi6FSzQV1KnGTEJHEVALgd-G3g&s=10", "new_car_url": "https://www.tesla.com/ko_kr/modelx", "used_car_url": "https://www.google.com/search?q=site%3Aauto.danawa.com%2Fusedcar+Model+X"},
]


def get_manufacturer_map():
    """manufacturer 테이블을 조회해 {"현대자동차": 1, ...} 형태로 매핑 반환"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT manufacturer_id, manufacturer_name FROM manufacturer")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {name: mid for mid, name in rows}


def insert_vehicles(data):
    manufacturer_map = get_manufacturer_map()

    conn = get_db_connection()
    cur = conn.cursor()

    # 이미 DB에 있는 (vehicle_name, manufacturer_id) 조합을 미리 조회해서 중복 방지
    cur.execute("SELECT vehicle_name, manufacturer_id FROM vehicle")
    existing = set(cur.fetchall())

    sql = """
        INSERT INTO vehicle
            (vehicle_name, body_type, car_img, car_description, vec_purpose,
             manufacturer_id, new_car_url, used_car_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    saved, skipped, duplicated = 0, 0, 0
    for v in data:
        manufacturer_id = manufacturer_map.get(v["manufacturer_name"])
        if manufacturer_id is None:
            print(f"매핑 실패(manufacturer 없음): {v['manufacturer_name']} {v['vehicle_name']}")
            skipped += 1
            continue

        if (v["vehicle_name"], manufacturer_id) in existing:
            duplicated += 1
            continue

        cur.execute(
            sql,
            (
                v["vehicle_name"],
                v["body_type"],
                v.get("car_img"),
                v["car_description"],
                v["vec_purpose"],
                manufacturer_id,
                v.get("new_car_url"),
                v.get("used_car_url"),
            ),
        )
        existing.add((v["vehicle_name"], manufacturer_id))
        saved += 1
        print(f"저장 완료: {v['manufacturer_name']} {v['vehicle_name']}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n총 {saved}개 저장 완료 / {duplicated}개 이미 존재(스킵) / {skipped}개 매핑 실패(스킵)")


def update_vehicle_urls(data):
    """
    vehicle_seed 리스트에서 car_img / new_car_url / used_car_url이 채워진 항목을 골라
    (vehicle_name, manufacturer_id) 기준으로 UPDATE함 (INSERT 아님, 중복 안 생김)
    -> None으로 남아있던 값을 직접 URL로 채운 뒤 이 함수로 실행하면 됨
    """
    manufacturer_map = get_manufacturer_map()

    # UPDATE 시 rowcount가 "변경된 행"이 아니라 "매칭된 행"을 반환하도록 함
    conn = get_db_connection(client_flag=pymysql.constants.CLIENT.FOUND_ROWS)
    cur = conn.cursor()

    sql = """
        UPDATE vehicle
        SET car_img = %s, new_car_url = %s, used_car_url = %s
        WHERE vehicle_name = %s AND manufacturer_id = %s
    """

    updated, skipped = 0, 0
    for v in data:
        img_url = v.get("car_img")
        new_url = v.get("new_car_url")
        used_url = v.get("used_car_url")
        if not img_url and not new_url and not used_url:  # 셋 다 없으면 건너뜀
            continue

        manufacturer_id = manufacturer_map.get(v["manufacturer_name"])
        if manufacturer_id is None:
            print(f"매핑 실패(manufacturer 없음): {v['manufacturer_name']} {v['vehicle_name']}")
            skipped += 1
            continue

        cur.execute(sql, (img_url, new_url, used_url, v["vehicle_name"], manufacturer_id))
        if cur.rowcount == 0:
            print(f"매칭되는 vehicle 없음(이름 확인 필요): {v['manufacturer_name']} {v['vehicle_name']}")
            skipped += 1
        else:
            print(f"업데이트: {v['manufacturer_name']} {v['vehicle_name']} -> img={img_url}, new={new_url}, used={used_url}")
            updated += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n총 {updated}개 업데이트 완료 / {skipped}개 스킵")


def auto_fill_car_img(data, overwrite_placeholder_only=True, sleep_sec=0.5, timeout=15):
    """
    new_car_url이 있는 항목에 대해 해당 페이지의 <meta property="og:image">를 읽어와
    car_img를 자동으로 채워주는 함수.
    - overwrite_placeholder_only=True면 현재 car_img가 placehold.co 인 것만 덮어씀
      (이미 실제 이미지가 들어간 항목은 건드리지 않음)
    - new_car_url이 None인 항목은 건너뜀 (placehold.co 그대로 유지)
    - requests, beautifulsoup4 필요: pip install requests beautifulsoup4

    사용법:
        from vehicle_seed import vehicle_seed, auto_fill_car_img
        auto_fill_car_img(vehicle_seed)
        # 이후 vehicle_seed 리스트가 메모리상 업데이트됨.
        # DB에 반영하려면 update_vehicle_urls(vehicle_seed) 호출
        # 이 파일에 직접 반영하고 싶다면 print(vehicle_seed) 등으로 값을 확인 후
        # 코드에 수동으로 옮겨 적거나, json으로 덤프해서 diff 확인 권장
    """
    import time
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    }

    updated, skipped, failed = 0, 0, []

    for v in data:
        url = v.get("new_car_url")
        if not url:
            skipped += 1
            continue

        if overwrite_placeholder_only:
            current = v.get("car_img") or ""
            if "placehold.co" not in current:
                skipped += 1
                continue

        try:
            try:
                res = requests.get(url, headers=headers, timeout=timeout)
            except requests.exceptions.Timeout:
                print(f"[재시도] {v['manufacturer_name']} {v['vehicle_name']} (1차 타임아웃, 20초로 재시도)")
                res = requests.get(url, headers=headers, timeout=20)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            og_image = soup.find("meta", property="og:image")
            if not og_image or not og_image.get("content"):
                og_image = soup.find("meta", attrs={"name": "twitter:image"})

            if og_image and og_image.get("content"):
                img_url = og_image["content"].strip()
                if img_url.startswith("http"):
                    v["car_img"] = img_url
                    updated += 1
                    print(f"[og:image 추출 성공] {v['manufacturer_name']} {v['vehicle_name']} -> {img_url}")
                else:
                    # og:image 내용이 URL이 아닌 이상한 문자열(사이트 자체 버그 등)인 경우 -> 스킵
                    failed.append((v["manufacturer_name"], v["vehicle_name"], url))
                    print(f"[og:image 값이 URL 아님, 스킵] {v['manufacturer_name']} {v['vehicle_name']} -> '{img_url}' ({url})")
            else:
                failed.append((v["manufacturer_name"], v["vehicle_name"], url))
                print(f"[og:image 없음] {v['manufacturer_name']} {v['vehicle_name']} ({url})")

        except Exception as e:
            failed.append((v["manufacturer_name"], v["vehicle_name"], url))
            print(f"[요청 실패] {v['manufacturer_name']} {v['vehicle_name']} ({url}) - {e}")

        time.sleep(sleep_sec)  # 상대 서버에 과도한 부하를 주지 않기 위한 딜레이

    print(f"\n총 {updated}개 이미지 자동 채움 / {skipped}개 스킵(이미 채워짐 또는 URL 없음) / {len(failed)}개 실패")
    if failed:
        print("실패 목록 (수동 확인 필요):")
        for m, n, u in failed:
            print(f"  - {m} {n}: {u}")

    return data


def check_vehicle_data():
    """
    DB에 반영된 상태를 조회만 하는 함수 (아무것도 바꾸지 않음).
    - 전체 vehicle 개수
    - car_img가 아직 placehold.co인 개수
    - 샘플 몇 개(니로, 쏘렌토, G70, GR86, ES)의 car_img 값
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM vehicle")
    total = cur.fetchone()[0]
    print(f"전체 vehicle 개수: {total}")

    cur.execute("SELECT COUNT(*) FROM vehicle WHERE car_img LIKE '%placehold.co%'")
    placeholder_count = cur.fetchone()[0]
    print(f"아직 placehold.co인 개수: {placeholder_count}")

    cur.execute(
        "SELECT vehicle_name, car_img FROM vehicle "
        "WHERE vehicle_name IN ('니로', '쏘렌토', 'G70', 'GR86', 'ES')"
    )
    print("\n샘플 확인:")
    for name, img in cur.fetchall():
        print(f"  - {name}: {img}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # 아무것도 바꾸지 않고 DB 상태만 조회함
        #   uv run crawler/vehicle_crawler.py check
        check_vehicle_data()
    elif len(sys.argv) > 1 and sys.argv[1] == "fill-images":

        import json
        auto_fill_car_img(vehicle_seed)
        with open("vehicle_seed_filled.json", "w", encoding="utf-8") as f:
            json.dump(vehicle_seed, f, ensure_ascii=False, indent=2)
        print("\nvehicle_seed_filled.json 으로 저장 완료")
        print("\nDB에도 바로 반영합니다...")
        update_vehicle_urls(vehicle_seed)
    elif len(sys.argv) > 1 and sys.argv[1] == "update":
        # 처음 넣을 땐: uv run crawler/vehicle_seed.py
        # None -> URL로 채운 뒤 다시 돌릴 땐: uv run crawler/vehicle_seed.py update
        update_vehicle_urls(vehicle_seed)
    else:
        insert_vehicles(vehicle_seed)
