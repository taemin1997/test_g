# SKN35-1st-3Team

Python 3.12와 Streamlit 1.59.2 기반 자동차 MBTI 검사 애플리케이션입니다.
질문과 점수 계산은 애플리케이션에서 관리하고, 결과 이름과 설명은
`car_mbti` 테이블에서 조회합니다.

## 재현 가능한 실행 환경

이 프로젝트는 `uv`와 `uv.lock`으로 Python 및 패키지 버전을 관리합니다.
`.venv`는 PC별로 새로 생성해야 하며 Git이나 압축 파일로 공유하지 않습니다.

필요한 도구:

- Git
- uv

`uv`는 `.python-version`과 `pyproject.toml`을 읽어 Python 3.12 환경을
자동으로 준비합니다.

## 처음 clone한 경우

```powershell
git clone <저장소-주소>
cd SKN35-1st-3Team
uv sync --frozen
uv run python scripts/check_environment.py
uv run python -m unittest discover -s tests -v
uv run streamlit run app.py
```

macOS와 Linux에서도 같은 `uv` 명령을 사용합니다.

## DB 종류에 따른 설치

팀에서 사용하는 DB 종류에 맞춰 한 가지 extra를 선택합니다.

MySQL 또는 MariaDB:

```powershell
uv sync --frozen --extra mysql
```

PostgreSQL:

```powershell
uv sync --frozen --extra postgres
```

SQLite는 별도 드라이버 없이 기본 동기화만 사용합니다.

```powershell
uv sync --frozen
```

다른 DB를 사용한다면 팀에서 동일한 SQLAlchemy 드라이버를 정해
`pyproject.toml`에 추가한 뒤 `uv.lock`도 함께 갱신해야 합니다.

## DB 접속 설정

예시 파일을 복사해 개인 설정 파일을 만듭니다.

Windows PowerShell:

```powershell
Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
```

macOS 또는 Linux:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml`의 URL을 실제 환경에 맞게 수정합니다.

```toml
[connections.car_mbti]
url = "mysql+pymysql://username:password@host:3306/database"
```

다른 URL 예시:

```text
postgresql+psycopg://username:password@host:5432/database
sqlite:///car_mbti.db
```

실제 비밀번호가 포함된 `.streamlit/secrets.toml`은 Git에 커밋하지 않습니다.

앱은 다음 컬럼을 조회합니다.

```sql
SELECT mbti_id, mbti_name, mbti_description
FROM car_mbti;
```

`app.py`의 `RESULT_PROFILES`에 있는 `mbti_id`는 실제
`car_mbti.mbti_id`와 동일해야 합니다.

## 기존 작업자가 pull한 경우

```powershell
git pull
uv sync --frozen
uv run python scripts/check_environment.py
uv run streamlit run app.py
```

MySQL/MariaDB 또는 PostgreSQL 사용자는 처음 설치할 때와 동일한
`--extra mysql` 또는 `--extra postgres` 옵션을 사용합니다.

## 노트북 작업 방식

`streamlit_set.ipynb`는 앱 코드를 관리하는 단일 코드 셀입니다. 셀 첫 줄의
`%%writefile app.py`가 실행 파일을 생성합니다.

노트북을 수정한 경우:

1. 단일 셀을 실행해 `app.py`를 갱신합니다.
2. 환경 점검과 테스트를 실행합니다.
3. `streamlit_set.ipynb`와 `app.py`를 함께 커밋합니다.

## 공유해야 하는 파일

```text
.python-version
.gitignore
.streamlit/secrets.toml.example
app.py
pyproject.toml
README.md
scripts/check_environment.py
streamlit_set.ipynb
tests/test_app_structure.py
uv.lock
```

공유하지 않는 파일:

```text
.venv/
.streamlit/secrets.toml
.env
__pycache__/
```

서비스명
기술 스택
팀원
프로젝트 개요
Project Structure

핵심기술
ERD

특이사항

구현 화면

관련 이슈, 개선내역 dddd