
# 스터디룸 예약 API 문서
## User API
### 회원 생성
```bash
POST /users
```
#### Request
```json
{
  "student_number": "201602042",  // max 20자
  "password": "1234",             // min 4자
  "name": "홍길동"                 // max 50자
}
```
#### Response (201 Created)
```json
{
  "id": 1,
  "student_number": "20240001",
  "name": "홍길동"
}
```
### 회원 가입
```bash
GET /auth/signup
```
#### Request
```json
{
  "student_number": "20240001",
  "password": "1234",
  "name": "홍길동"
}
```
#### Response (200 OK)
```json
{
    "id": 1,
    "student_number": "20240001",
    "name": "홍길동"
}
```
#### Error Responses
- 409_CONFLICT
```json
{"detail": "이미 등록된 이메일입니다."}
```

### 로그인
```bash
POST /auth/login
```
#### Request
```json
{
  "student_number": "20240001",
  "password": "1234"
}
```
#### Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer",
}
```
#### Error Responses
- 401_UNAUTHORIZED
```json
{"detail": "이메일 또는 비밀번호가 올바르지 않습니다."}
```

## Facility API
### 시설 목록 조회
```bash
GET /studyrooms/{studyroom_id}/facilities
```
#### Response (200 OK)
```json
[
  {"id": 1, "name": "화이트보드"},
  {"id": 2, "name": "빔프로젝터"}
]
```


## StudyRoom API
### 스티디룸 목록 + 쿼리 파라미터
```bash
GET /studyrooms?floor=4&min_capacity=4
```
#### Response (200 OK)
```json
[
  {
    "id": 1,
    "name": "스터디룸 A",
    "floor": 4,
    "location": "중앙도서관",
    "capacity": 4,
    "facilities": [
        {"id": 1, "name": "화이트보드"},
        {"id": 2, "name": "빔프로젝터"}
    ]
  }
]
```



## Reservation API
#### Headers
- Authorization: Bearer <access_token>
- Content-Type: application/json

#### Error Responses
- 401_Unauthorized
```json
{"detail": "Not authenticated"}
```
### 예약하기
```bash
POST /reservations
```
#### Request
```json
{
  "studyroom_id": 1,
  "start_datetime": "2026-02-20T09:00:00",
  "end_datetime": "2026-02-20T11:00:00"
}
```
#### Response (201 Created)
```json
{
    "id": 2,
    "user_id": 2,
    "studyroom": {
        "name": "스터디룸 B",
        "floor": 4
    },
    "start_datetime": "2026-02-21T16:00:00",
    "end_datetime": "2026-02-21T17:00:00",
    "status": "RESERVED",
    "created_at": "2026-02-23T09:34:14.585875"
}
```
#### Error Responses
- 400_BAD_REQUEST
```json
{"detail": "종료시간은 시작시간보다 이후여야 합니다."},
{"detail":"이미 해당 시간에 예약이 존재합니다."}
```
- 404_NOT_FOUND
```json
{"detail": "해당 스터디룸이 존재하지 않습니다."}
```

### 내 예약 목록
```bash
GET /reservations/mine
```

#### Response
```json
[
  {
    "id": 1,
    "user_id": 1,
    "studyroom": {
      "name": "스터디룸 A",
      "floor": 4
    },
    "start_datetime": "2026-02-20T09:00:00",
    "end_datetime": "2026-02-20T10:00:00",
    "status": "RESERVED",
    "created_at": "2026-02-23T09:34:14.585875"
  },
  {
    "id": 2,
    "user_id": 2,
    "studyroom": {
      "name": "스터디룸 B",
      "floor": 3
    },
    "start_datetime": "2026-02-18T14:00:00",
    "end_datetime": "2026-02-18T15:00:00",
    "status": "COMPLETED",
    "created_at": "2026-02-23T09:34:14.585875"
  }
]
```
#### Error Responses
- 404_NOT_FOUND
```json
{"detail": "예약을 찾을 수 없습니다."}
```
### 내 예약 취소
```bash
PATCH /reservations/{reservation_id}/cancel
```
#### Response (200 OK)
```json
{
    "id": 2,
    "user_id": 2,
    "studyroom": {
        "name": "스터디룸 B",
        "floor": 4
    },
    "start_datetime": "2026-02-21T16:00:00",
    "end_datetime": "2026-02-21T17:00:00",
    "status": "CANCELED",
    "created_at": "2026-02-23T09:34:14.585875"
}
```
#### Error Responses
- 404_NOT_FOUND
```json
{"detail": "예약을 찾을 수 없습니다."}
```
- 403_Forbidden
```json
{"detail": "본인의 예약만 취소할 수 있습니다."}
```
- 409_CONFLICT
```json
{"detail": "이미 취소된 예약입니다."}
```

## Review API
#### Headers
- Authorization: Bearer <access_token>
- Content-Type: application/json
#### Error Responses
- 401 Unauthorized
```json
{"detail": "Not authenticated"}
```
- 403 Forbidden
```json
{ "detail": "Cannot write review before the service is completed" }
```

### 리뷰 작성
```bash
POST /reservations/{id}/reviews
```
#### Request
```json
{
  "reservation_id": 2,
  "rating": 5,
  "comment": "깨끗하고 넓어요!"
}
```
#### Response (201 Created)
```json
{
  "id": 1,
  "reservation_id": 2,
  "rating": 5,
  "comment": "깨끗하고 넓어요!",
  "created_at": "2026-02-20T12:00:00"
}