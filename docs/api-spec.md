## User API
### 회원 생성
POST /users
#### Request
```json
{
  "student_number": "20240001",
  "password": "1234",
  "name": "홍길동"
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
### 회원 조회
GET /users/{user_id}
#### Response (200 OK)
```json
{
  "id": 1,
  "student_number": "20240001",
  "name": "홍길동"
}
```
### 로그인
POST /users/login
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
  "user": {
    "id": 1,
    "student_number": "20240001",
    "name": "홍길동"
  }
}
```


## StudyRoom API
### 스터디룸 목록
GET /studyroom
#### Response (200 OK)
```json
{
  "id": 1,
  "name": "스터디룸 A",
  "floor": 4,
  "capacity": 4,
  "location": "중앙도서관"
}