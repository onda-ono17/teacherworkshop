### [Before] 모호한 프롬프트
# 이메일 유효성을 검사하는 함수 작성해줘

import re


EMAIL_PATTERN = re.compile(
	r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)


def validate_email(email: str) -> bool:
	if not isinstance(email, str):
		return False
	return EMAIL_PATTERN.fullmatch(email) is not None