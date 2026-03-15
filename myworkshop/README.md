능개원 Copilot chat1 fair dev 1일차 실습

# myworkshop

FastAPI + async SQLAlchemy 예제 프로젝트입니다.

## 구성

- 사용자 생성: POST /users
- 사용자 목록 조회: GET /users
- 사용자 단건 조회: GET /users/{user_id}
- 사용자 부분 수정: PATCH /users/{user_id}
- 사용자 삭제(하드 삭제): DELETE /users/{user_id}
- SQLite(async) 연동: sqlalchemy + aiosqlite

## 사용자 스키마

- id: int
- email: string (unique)
- username: string (unique)
- created_at: datetime (UTC)

## 상태 코드

- 201: 생성 성공
- 200: 조회/수정 성공
- 204: 삭제 성공
- 404: 사용자 없음
- 409: email 또는 username 중복
- 422: 요청 검증 실패

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
uvicorn test_api:app --reload
```

## 테스트

```bash
pytest -q
```

## 예시 요청

```bash
curl -X POST http://127.0.0.1:8000/users \
	-H "Content-Type: application/json" \
	-d '{"email":"newuser@example.com","username":"new_user"}'
```
