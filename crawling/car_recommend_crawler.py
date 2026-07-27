"""
car_recommend_crawler.py
- Project_carbti_design_2.pptx (슬라이드 9~24, 인화님 디자인 시안) 기준
  16개 MBTI 유형별 1·2·3위 추천 차량 조합을 car_recommend 테이블에 저장
- vehicle_id는 (manufacturer_name, vehicle_name)으로 vehicle 테이블에서 조회해서 채움
"""

from db_config import get_db_connection

# ------------------------------------------------------------
# 1. 인화님 PPT 'Project_carbti_design_2' 슬라이드 9~24 기준 1/2/3위 조합
#    key: mbti_id, value: [(rank, manufacturer_name, vehicle_name), ...]
# ------------------------------------------------------------
car_recommend_seed = {
    "ISTJ": [(1, "현대자동차", "아반떼"), (2, "렉서스", "ES"), (3, "현대자동차", "그랜저")],
    "ISFJ": [(1, "메르세데스-벤츠", "E클래스"), (2, "제네시스", "G80"), (3, "BMW", "5시리즈")],
    "INFJ": [(1, "제네시스", "G80"), (2, "메르세데스-벤츠", "E클래스"), (3, "현대자동차", "그랜저")],
    "INTJ": [(1, "볼보", "XC60"), (2, "폭스바겐", "티구안"), (3, "제네시스", "GV70")],
    "ISTP": [(1, "포르쉐", "카이엔"), (2, "BMW", "5시리즈"), (3, "제네시스", "GV70")],
    "ISFP": [(1, "렉서스", "ES"), (2, "제네시스", "G80"), (3, "현대자동차", "아반떼")],
    "INFP": [(1, "폭스바겐", "티구안"), (2, "볼보", "XC60"), (3, "기아", "쏘렌토")],
    "INTP": [(1, "현대자동차", "아이오닉5"), (2, "테슬라", "Model Y"), (3, "기아", "레이")],
    "ESTP": [(1, "제네시스", "GV70"), (2, "포르쉐", "카이엔"), (3, "BMW", "5시리즈")],
    "ESFP": [(1, "미니", "쿠퍼"), (2, "기아", "레이"), (3, "테슬라", "Model Y")],
    "ENFP": [(1, "기아", "레이"), (2, "현대자동차", "아이오닉5"), (3, "미니", "쿠퍼")],
    "ENTP": [(1, "테슬라", "Model Y"), (2, "현대자동차", "아이오닉5"), (3, "제네시스", "GV70")],
    "ESTJ": [(1, "현대자동차", "그랜저"), (2, "제네시스", "G80"), (3, "기아", "쏘렌토")],
    "ESFJ": [(1, "기아", "쏘렌토"), (2, "기아", "카니발"), (3, "현대자동차", "그랜저")],
    "ENFJ": [(1, "기아", "카니발"), (2, "기아", "쏘렌토"), (3, "볼보", "XC60")],
    "ENTJ": [(1, "BMW", "5시리즈"), (2, "메르세데스-벤츠", "E클래스"), (3, "포르쉐", "카이엔")],
}


# ------------------------------------------------------------
# 2. 조회 헬퍼
# ------------------------------------------------------------
def get_vehicle_map():
    """(manufacturer_name, vehicle_name) -> {vehicle_id, car_description} 매핑 반환"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT v.vehicle_id, v.vehicle_name, m.manufacturer_name, v.car_description
        FROM vehicle v
        JOIN manufacturer m ON v.manufacturer_id = m.manufacturer_id
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {
        (mname, vname): {"vehicle_id": vid, "car_description": desc}
        for vid, vname, mname, desc in rows
    }


def get_mbti_description_map():
    """mbti_id -> mbti_description 매핑 반환 (1위 추천 이유로 재사용)"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT mbti_id, mbti_description FROM car_mbti")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return dict(rows)


# ------------------------------------------------------------
# 3. 삽입 함수
# ------------------------------------------------------------
def insert_car_recommend(seed):
    vehicle_map = get_vehicle_map()
    mbti_desc_map = get_mbti_description_map()

    conn = get_db_connection()
    cur = conn.cursor()

    # 이미 들어가있는 (mbti_id, recom_car_rank) 조합 조회 -> 중복 방지
    cur.execute("SELECT mbti_id, recom_car_rank FROM car_recommend")
    existing = set(cur.fetchall())

    sql = """
        INSERT INTO car_recommend (recom_reason, recom_car_rank, vehicle_id, mbti_id)
        VALUES (%s, %s, %s, %s)
    """

    saved, skipped, no_match = 0, 0, []
    for mbti_id, combo in seed.items():
        for rank, manufacturer_name, vehicle_name in combo:
            if (mbti_id, rank) in existing:
                print(f"[이미 있음, 스킵] {mbti_id} {rank}위")
                skipped += 1
                continue

            vehicle_info = vehicle_map.get((manufacturer_name, vehicle_name))
            if vehicle_info is None:
                no_match.append(f"{mbti_id} {rank}위: {manufacturer_name} {vehicle_name}")
                skipped += 1
                continue

            if rank == 1:
                # 1위는 pptx 결과 슬라이드와 동일하게 car_mbti 캐릭터 설명을 그대로 사용
                reason = mbti_desc_map.get(mbti_id)
            else:
                # 2,3위는 ppt에 별도 추천 이유 문구가 없어서 우선 해당 차량의 car_description으로 임시 채워두었습니다.
                # 나중에 별도 문구를 정하면 이 부분만 교체하면 됩니다!
                reason = vehicle_info["car_description"]

            cur.execute(sql, (reason, rank, vehicle_info["vehicle_id"], mbti_id))
            existing.add((mbti_id, rank))
            saved += 1
            print(f"저장: {mbti_id} {rank}위 -> {manufacturer_name} {vehicle_name}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n총 {saved}개 저장 완료 / {skipped}개 스킵")
    if no_match:
        print("\nvehicle 테이블에서 매칭 안 된 조합 (이름 확인 필요):")
        for n in no_match:
            print(f"  - {n}")


if __name__ == "__main__":
    insert_car_recommend(car_recommend_seed)
