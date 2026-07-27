"""
db_config.py
- 모든 crawler / Streamlit 앱이 공통으로 사용하는 DB 연결 + 스키마 자동 생성 모듈
- .env 파일의 HOST / PORT / USERNAME / PASSWORD / DB 값을 사용
- host에 'tidbcloud.com'이 포함되어 있으면 자동으로 SSL을 켬 (TiDB Cloud 대응)
- 테이블 정의는 이 파일에 중복해서 넣지 않고, db/carbti_schema.sql을 그대로 읽어서 실행함
  (스키마를 고칠 땐 carbti_schema.sql 한 곳만 고치면 됨)

.env 예시 (TiDB Cloud):
    HOST=gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    PORT=4000
    USERNAME=xxxxxxxx.root
    PASSWORD=your_password
    DB=carbti

.env 예시 (로컬 MySQL):
    HOST=localhost
    PORT=3306
    USERNAME=root
    PASSWORD=1234
    DB=carbti

Streamlit 앱에서 쓰는 법 (앱 진입점 맨 위에 한 번):
    import streamlit as st
    from db_config import ensure_schema, get_db_connection

    @st.cache_resource
    def _init():
        ensure_schema()
        return True

    _init()   # 앱이 처음 뜰 때(또는 인스턴스가 새로 뜰 때) 딱 한 번만 실행됨
"""

import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_DATABASE", "carbti")


# ------------------------------------------------------------
# 1. 연결
# ------------------------------------------------------------
def _base_config(with_database: bool):
    host = os.getenv("DB_HOST", "localhost")
    config = {
        "host": host,
        "user": os.getenv("DB_USERNAME", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "port": int(os.getenv("DB_PORT", 3306)),
        "charset": "utf8mb4",
    }
    if with_database:
        config["database"] = DB_NAME

    # TiDB Cloud는 SSL 연결이 필수라 자동으로 감지해서 켜줌
    if "tidbcloud.com" in host:
        try:
            import certifi
            config["ssl_ca"] = certifi.where()
        except ImportError:
            config["ssl"] = {"ssl": {}}
        config["ssl_verify_cert"] = True

    return config


def get_db_connection(**extra):
    """
    앱/crawler에서 실제 쿼리할 때 쓰는 커넥션.
    client_flag 등 추가 옵션이 필요하면 get_db_connection(client_flag=...)처럼 넘기면 됨.
    """
    config = _base_config(with_database=True)
    config.update(extra)
    return pymysql.connect(**config)


def _get_server_connection():
    """DB 지정 없이 서버에만 접속 (DB_NAME이 아직 없을 수 있으므로)"""
    return pymysql.connect(**_base_config(with_database=False))


# ------------------------------------------------------------
# 2. 스키마 (테이블이 없으면 생성)
#    - db/carbti_schema.sql 파일을 찾아서 그대로 읽어 실행함 (내용 중복 X)
#    - 이 파일이 crawling/ 안에 있든 프로젝트 루트에 있든 상관없이 찾도록
#      상위 폴더로 올라가면서 db/carbti_schema.sql을 탐색함
# ------------------------------------------------------------
def _find_schema_file():
    here = os.path.dirname(os.path.abspath(__file__))
    for base in [here, os.path.dirname(here), os.path.dirname(os.path.dirname(here))]:
        candidate = os.path.join(base, "db", "carbti_schema.sql")
        if os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(
        "db/carbti_schema.sql을 찾지 못했습니다. "
        "db_config.py 기준 상위 폴더들에 db/carbti_schema.sql이 있는지 확인해주세요."
    )


_schema_ready = False  # 같은 프로세스 안에서 여러 번 호출돼도 한 번만 실제로 실행하기 위한 플래그


def ensure_schema():
    """
    carbti DB와 모든 테이블이 없으면 만듦. 이미 있으면 아무것도 안 하고 넘어감.
    db/carbti_schema.sql 파일을 읽어서 그대로 실행하는 방식이라
    스키마를 고칠 땐 그 .sql 파일 하나만 고치면 됨.
    Streamlit 앱 시작 시 한 번 호출하도록 설계됨 (idempotent - 여러 번 호출해도 안전).
    """
    global _schema_ready
    if _schema_ready:
        return

    schema_path = _find_schema_file()
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_text = f.read()

    statements = [s.strip() for s in sql_text.split(";") if s.strip()]

    # DB 지정 없이 접속 (carbti가 아직 없을 수 있으므로) -> 스크립트 안의 CREATE DATABASE / USE부터 실행
    conn = _get_server_connection()
    cur = conn.cursor()

    for stmt in statements:
        try:
            cur.execute(stmt)
        except pymysql.err.OperationalError as e:
            # 이미 존재하는 테이블(1050) 등은 무시하고 계속 진행 -> 여러 번 실행해도 안전
            if e.args and e.args[0] in (1050,):  # 1050: Table already exists
                continue
            raise

    conn.commit()
    cur.close()
    conn.close()

    _schema_ready = True