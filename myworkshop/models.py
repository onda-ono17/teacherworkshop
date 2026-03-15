# `models.py` > `User` 클래스 정의(id, email, username, created_at 필드)

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class User:
	id: int
	email: str
	username: str
	created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
