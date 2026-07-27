"""
load_vehicle_detail.py
- data/raw/vehicle_detail.json 을 읽어서
- vehicle 테이블에서 이름으로 vehicle_id를 찾은 뒤
- vehicle_detail 테이블에 INSERT
"""

import json
import re
import os

from db_config import get_db_connection


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_vehicle_id_map(cur):
    cur.execute("SELECT vehicle_id, vehicle_name FROM vehicle")
    return {name: vid for vid, name in cur.fetchall()}


def parse_int(value):
    if value is None:
        return None
    match = re.search(r"[\d,]+", str(value))
    return int(match.group().replace(",", "")) if match else None


def parse_float(value):
    if value is None:
        return None
    match = re.search(r"[\d.]+", str(value))
    return float(match.group()) if match else None


def normalize_transmission(value):
    if value is None:
        return None
    if "CVT" in value:
        return "CVT"
    if "DCT" in value:
        return "DCT"
    if "수동" in value:
        return "manual"
    return "auto"


def insert_vehicle_detail(cur, vehicle_id, item):
    sql = """
        INSERT INTO vehicle_detail
        (detail_trim_name, detail_fuel_type, detail_displacement,
         detail_horsepower, detail_transmission, detail_base_price,
         detail_fuel_efficiency, vehicle_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, (
        item.get("trim_name"),
        item.get("fuel_type"),
        parse_int(item.get("displacement")),
        parse_int(item.get("horsepower")),
        normalize_transmission(item.get("transmission")),
        item.get("base_price"),
        parse_float(item.get("fuel_efficiency")),
        vehicle_id,
    ))


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "..", "data", "raw", "vehicle_detail.json")
    data = load_json(json_path)

    conn = get_db_connection()
    cur = conn.cursor()

    vehicle_id_map = get_vehicle_id_map(cur)

    success, skipped = 0, []
    for item in data:
        vehicle_id = vehicle_id_map.get(item["vehicle_name"])
        if vehicle_id is None:
            skipped.append(item["vehicle_name"])
            continue
        try:
            insert_vehicle_detail(cur, vehicle_id, item)
            success += 1
        except Exception as e:
            print(f"[실패] {item['vehicle_name']}: {e}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n저장 완료: {success}건")
    if skipped:
        print(f"매칭 실패(vehicle 테이블에 이름 없음): {skipped}")