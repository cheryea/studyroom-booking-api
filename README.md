# Study Room Booking API

스터디룸 예약을 위한 REST API 서버입니다. FastAPI 기반으로 인증, 시설/스터디룸 조회, 예약, 리뷰 기능을 제공합니다.

## 주요 기능

- **인증**: 회원가입, 로그인 (JWT)
- **시설·스터디룸**: 시설 목록, 스터디룸 목록(층/수용인원 필터)
- **예약**: 예약 생성, 내 예약 조회, 예약 취소
- **리뷰**: 예약 단위 리뷰 CRUD, 스터디룸별 리뷰 목록, 예약 완료 처리

## 기술 스택

- **Python** 3.12
- **FastAPI** – API 프레임워크
- **SQLAlchemy** 2.x – ORM
- **PostgreSQL** – 데이터베이스
- **JWT** – 인증
- **bcrypt** – 비밀번호 해싱
- **uv** – 패키지/가상환경 관리

## 사전 요구사항

- Python 3.12+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) (권장) 또는 pip

## 설치 및 실행

### 1. 저장소 클론 및 이동

```bash
cd studyroom-booking-api
```

### 2. 가상환경 및 의존성 설치 (uv)

```bash
uv sync
```

또는 pip 사용 시:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
```

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 만들고 PostgreSQL 연결 정보를 넣습니다.

```env
DATABASE_URL=postgresql://사용자:비밀번호@호스트:포트/DB이름
```

예시:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/studyroom_db
```

### 4. 서버 실행

```bash
uvicorn main:app --reload
```

기본 주소: **http://127.0.0.1:8000**

- API 문서 (Swagger): http://127.0.0.1:8000/docs  
- ReDoc: http://127.0.0.1:8000/redoc  

## API 문서

- **상세 명세**: [docs/api-spec.md](docs/api-spec.md)  
- 실행 중인 서버의 대화형 문서: `/docs`, `/redoc`

## 프로젝트 구조

```
studyroom-booking-api/
├── app/
│   ├── api-spec.md      # API 명세 문서
│   ├── models/          # SQLAlchemy 모델
│   ├── routers/         # API 라우터 (auth, user, facility, studyroom, reservation, review)
│   ├── schemas/         # Pydantic 요청/응답 스키마
│   ├── services/        # 비즈니스 로직
│   └── repositories/    # 데이터 접근
├── main.py              # FastAPI 앱 진입점
├── database.py          # DB 엔진·세션 설정
├── dependencies.py      # 인증 등 공통 의존성
├── pyproject.toml       # 프로젝트 설정·의존성
└── README.md
```

## 라이선스

이 프로젝트는 교육/포트폴리오 목적으로 작성되었습니다.
