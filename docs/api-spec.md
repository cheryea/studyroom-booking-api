
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
    "facilities": ["화이트보드"]
  }
]
```



## Reservation API
#### Headers
- Authorization: Bearer <access_token>
- Content-Type: application/json

#### Error Responses
- 401 Unauthorized
```json
{"detail": "Not authenticated"}
```
- 409 Conflict
```json
{ "detail": "Reservation already exists" }
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
  "id": 1,
  "studyroom_id": 1,
  "start_datetime": "2026-02-20T09:00:00",
  "end_datetime": "2026-02-20T10:00:00",
  "status": "RESERVED",
  "created_at": "2026-02-19T12:00:00"
}
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
    "studyroom_id": 1,
    "studyroom_name": "스터디룸 A",
    "floor": 4,
    "location": "중앙도서관",
    "start_datetime": "2026-02-20T09:00:00",
    "end_datetime": "2026-02-20T10:00:00",
    "status": "RESERVED"
  },
  {
    "id": 2,
    "studyroom_id": 2,
    "studyroom_name": "스터디룸 B",
    "floor": 3,
    "location": "중앙도서관",
    "start_datetime": "2026-02-18T14:00:00",
    "end_datetime": "2026-02-18T15:00:00",
    "status": "COMPLETED"
  }
]
```
### 내 예약 취소
```bash
PATCH /reservations/{reservation_id}/cancel
```
#### Response (200 OK)
```json
{
  "id": 1,
  "studyroom_id": 1,
  "start_datetime": "2026-02-20T09:00:00",
  "end_datetime": "2026-02-20T11:00:00",
  "status": "CANCELED",
  "created_at": "2026-02-19T12:00:00"
}
```
#### Error Responses
- 403 Forbidden
```json
{"detail": "Cannot cancel a completed or canceled reservation"}
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