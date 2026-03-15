### [After] 개선된 프롬프트 (Specificity 적용)
# 다음 조건을 만족하는 이메일 유효성 검사 함수를 작성하십시오:
# 1. 정규표현식을 사용하여 이메일 형식을 확인합니다.
# 2. 이메일 호스트가 'example.com'인 경우 허용하지 않습니다.
# 3. 유효하지 않은 형식일 경우 'InvalidEmailError' 커스텀 예외를 발생시킵니다.
# 4. 유효할 경우 True를 반환합니다.

import re


class InvalidEmailError(ValueError):
	"""이메일 형식이 유효하지 않을 때 발생하는 커스텀 예외."""


EMAIL_PATTERN = re.compile(
	r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)


def validate_email(email: str) -> bool:
	if not isinstance(email, str) or not EMAIL_PATTERN.fullmatch(email):
		raise InvalidEmailError("유효하지 않은 이메일 형식입니다.")

	host = email.rsplit("@", 1)[1].lower()
	if host == "example.com":
		raise InvalidEmailError("example.com 도메인은 허용되지 않습니다.")

	return True

