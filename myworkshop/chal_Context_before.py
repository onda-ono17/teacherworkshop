### [Before] 맥락이 없는 프롬프트
# 사용 정보를 데이터베이스에 저장하는 코드 작성

import sqlite3
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
	name: str
	email: str
	created_at: str | None = None


def initialize_db(db_path: str = "users.db") -> None:
	with sqlite3.connect(db_path) as conn:
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				email TEXT NOT NULL UNIQUE,
				created_at TEXT NOT NULL
			)
			"""
		)
		conn.commit()


def save_user(user: User, db_path: str = "users.db") -> int:
	created_at = user.created_at or datetime.utcnow().isoformat()

	with sqlite3.connect(db_path) as conn:
		cursor = conn.execute(
			"INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
			(user.name, user.email, created_at),
		)
		conn.commit()
		return int(cursor.lastrowid)


if __name__ == "__main__":
	initialize_db()
	new_user_id = save_user(User(name="Alice", email="alice@example.org"))
	print(f"saved user id: {new_user_id}")
	
    ###
	# User 데이터 클래스 정의
    # SQLite 테이블 생성 함수 initialize_db
    # 사용자 저장 함수 save_user
    # 파일 직접 실행 시 샘플 사용자 1건 저장하는 예시 코드
    
    # 현재 파일 기준 문법 오류도 없습니다.
    # 원하시면 다음으로 조회, 수정, 삭제 함수까지 이어서 확장해드릴 수 있습니다.
    # ###