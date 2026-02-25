# Study Room Booking API 명세

스터디룸 예약 API 문서입니다. 인증이 필요한 엔드포인트는 `Authorization: Bearer <access_token>` 헤더를 사용합니다.

---

## 목차

1. [공통](#공통)
2. [인증 (Auth)](#인증-auth)
3. [사용자 (Users)](#사용자-users)
4. [시설 (Facilities)](#시설-facilities)
5. [스터디룸 (Studyroom)](#스터디룸-studyroom)
6. [예약 (Reservations)](#예약-reservations)
7. [리뷰 (Reviews)](#리뷰-reviews)

---

## 공통

### 인증

- **OAuth2 Password Bearer**: 로그인 시 발급된 `access_token`을 `Authorization: Bearer <access_token>` 형식으로 전달합니다.
- 토큰 발급 엔드포인트: `POST /auth/login`

### 에러 응답

- `401 Unauthorized`: 토큰 없음/만료/잘못된 토큰
- `404 Not Found`: 리소스 없음
- `422 Unprocessable Entity`: 요청 바디/쿼리 검증 실패

---

## 인증 (Auth)

### 회원가입

**POST** `/auth/signup`

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| student_number | string | O | 학번 (최대 20자) |
| password | string | O | 비밀번호 (최소 4자) |
| name | string | O | 사용자 이름 (최대 50자) |

**Response** `201 Created`

```json
{
  "id": 1,
  "student_number": "20241234",
  "name": "홍길동"
}
```

---

### 로그인

**POST** `/auth/login`

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| student_number | string | O | 학번 |
| password | string | O | 비밀번호 |

**Response** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 사용자 (Users)

### 내 정보 조회

**GET** `/me`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Response** `200 OK`

```json
{
  "id": 1,
  "student_number": "20241234",
  "name": "홍길동"
}
```

---

## 시설 (Facilities)

### 시설 목록 조회

**GET** `/facilities`

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "name": "화이트보드"
  },
  {
    "id": 2,
    "name": "프로젝터"
  }
]
```

---

## 스터디룸 (Studyroom)

### 스터디룸 목록 조회

**GET** `/studyroom`

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| floor | int | X | 층 필터 |
| min_capacity | int | X | 최소 수용 인원 |

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "name": "스터디룸 A",
    "floor": 2,
    "location": "2층 동쪽",
    "capacity": 6,
    "facilities": [
      { "id": 1, "name": "화이트보드" }
    ]
  }
]
```

---

## 예약 (Reservations)

### 예약 생성

**POST** `/reservations`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| studyroom_id | int | O | 스터디룸 ID |
| start_datetime | datetime (ISO 8601) | O | 예약 시작 시각 |
| end_datetime | datetime (ISO 8601) | O | 예약 종료 시각 |

**Response** `201 Created`

```json
{
  "id": 1,
  "user_id": 1,
  "studyroom": {
    "name": "스터디룸 A",
    "floor": 2
  },
  "start_datetime": "2025-02-26T09:00:00",
  "end_datetime": "2025-02-26T12:00:00",
  "status": "RESERVED",
  "created_at": "2025-02-25T10:00:00"
}
```

**status**: `RESERVED` | `CANCELED` | `COMPLETED`

---

### 내 예약 목록 조회

**GET** `/reservations/mine`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "user_id": 1,
    "studyroom": { "name": "스터디룸 A", "floor": 2 },
    "start_datetime": "2025-02-26T09:00:00",
    "end_datetime": "2025-02-26T12:00:00",
    "status": "RESERVED",
    "created_at": "2025-02-25T10:00:00"
  }
]
```

---

### 예약 취소

**PATCH** `/reservations/{reservation_id}/cancel`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| reservation_id | int | 예약 ID |

**Response** `200 OK`

취소된 예약 객체 (동일한 구조, `status`: `CANCELED`)

---

## 리뷰 (Reviews)

### 리뷰 작성 (예약 단위)

**POST** `/reviews/reservation/{reservation_id}`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| reservation_id | int | 예약 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| rating | float | O | 평점 (0~5) |
| comment | string | X | 리뷰 내용 (최대 500자) |

**Response** `201 Created`

```json
{
  "id": 1,
  "reservation_id": 1,
  "user_id": 1,
  "rating": 4.5,
  "comment": "좋았습니다.",
  "created_at": "2025-02-25T14:00:00",
  "updated_at": "2025-02-25T14:00:00"
}
```

---

### 리뷰 조회 (예약 단위)

**GET** `/reviews/reservation/{reservation_id}`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| reservation_id | int | 예약 ID |

**Response** `200 OK`

해당 예약의 리뷰 객체 (위와 동일 구조). 본인 예약이 아니거나 리뷰가 없으면 404.

---

### 리뷰 수정 (예약 단위)

**PUT** `/reviews/reservation/{reservation_id}`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| reservation_id | int | 예약 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| rating | float | X | 평점 (1~5) |
| comment | string | X | 리뷰 내용 (최대 500자) |

**Response** `200 OK`

수정된 리뷰 객체.

---

### 리뷰 삭제 (예약 단위)

**DELETE** `/reviews/reservation/{reservation_id}`

**Headers**: `Authorization: Bearer <access_token>` (필수)

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| reservation_id | int | 예약 ID |

**Response** `204 No Content`

---

### 스터디룸별 리뷰 목록 조회

**GET** `/reviews/studyroom/{room_id}`

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| room_id | int | 스터디룸 ID |

**Query Parameters**

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| limit | int | 20 | 조회 개수 |
| offset | int | 0 | 건너뛸 개수 |
| sort | string | "recent" | 정렬 (recent: 최신순) |

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "reservation_id": 1,
    "user_id": 1,
    "rating": 4.5,
    "comment": "좋았습니다.",
    "created_at": "2025-02-25T14:00:00",
    "updated_at": "2025-02-25T14:00:00"
  }
]
```

---

### 예약 완료 처리 - 개발자용

**PATCH** `/reviews/reservations/{reservation_id}/complete`

**Path Parameters**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| reservation_id | int | 예약 ID |

**Response** `200 OK`

- 성공: 완료 처리된 예약 객체 (`status`: `COMPLETED`)
- 이미 완료된 경우: `{"detail": "이미 완료된 예약입니다."}`

---

## 기타

### 헬스 체크

**GET** `/`

**Response** `200 OK`

```json
{
  "Hello": "World"
}
```

---

*문서 생성일: 2025-02-25*
