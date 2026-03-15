
`markdown
# 프로젝트 컨텍스트
- 본 프로젝트는 Python 3.11과 FastAPI를 사용하는 핀테크 API 서버입니다.
- ORM은 SQLAlchemy 2.0 비동기(Async) 모드를 사용합니다.

# 코딩 스타일 가이드
- 모든 함수 선언부에는 Python Type Hint를 의무적으로 작성하세요.
- 함수와 클래스에 대한 Docstring은 반드시 Google Style 포맷의 '한국어'로 작성하세요.
- Pydantic 모델을 사용할 때 필드 길이나 정규식 등 유효성 검사 코드를 의도적으로 많이 포함하세요.

# 보안 제약 사항
- 하드코딩된 비밀번호나 토큰을 절대 코드에 포함하지 마세요. 환경변수(os.getenv)를 사용하세요.
`



###
# Hands on Lab: Custom Instructions (컨벤션 강제)

이 실습에서는 앞서 배운 기능 중 가장 강력한 기능인 **팀 규칙의 자동 적용** (.github/copilot-instructions.md)을 경험합니다. 개발자가 일일이 "이 스타일로 짜줘"라고 프롬프트를 작성하지 않아도, 프로젝트 전역의 암묵적 규칙(Implicit Rule)이 자동으로 주입됨을 확인합니다.

---

## 1. 개요 (Context)
* **목적:** .github/copilot-instructions.md 파일에 정의된 규칙이 Chat 응답과 자동완성 제안에 어떻게 영향을 미치는지 실험합니다.
* **시나리오 (Problem Statement):** 팀의 기본 에러 핸들링은 항상 \Exception\ 객체를 로그로 남기는 것이고, 언어는 한국어로 주석을 달아야 하며, 변수명은 snake_case를 사용해야 합니다. 
* **해결 (Solution Method):** Global Prompt 파일을 워크스페이스에 생성하고, 지시를 따르는지 검증합니다.

---

## 2. 실습 세팅 (Setting up)

1. 활성화 되어있는 현재 VS Code 탐색기 워크스페이스의 루트 경로(현재 githubcopilot 폴더 제일 상단)에 다음 폴더를 만듭니다.: \.github\ (이미 있다면 건너뛰기)
2. 해당 폴더 안에 \copilot-instructions.md\ 라는 이름의 텍스트 파일을 만듭니다.
3. 생성된 파일 안에 아래의 **지시사항(Instructions)** 을 복사하여 붙여넣고 저장합니다.

`markdown
# 프로젝트 규칙
- 언어: 주석, 변수명 설명, Chat 설명 등은 모두 '한국어(Korean)'로 작성하세요.
- 네이밍 규칙: 모든 Python 변수 및 함수 이름은 'snake_case' 방식을 사용하세요. 
- 예외 처리 강제 규정: 함수 내에 try-except 구문을 사용할 때, 에러 발생 시 항상 \logging.error("에러 메시지", exc_info=True)\ 방식으로 로그를 남겨야 합니다. Print 문을 쓰지 마세요.
- 타입 힌트: Python 코딩 시 모든 인자와 리턴 타입에 Type Hint를 명시하세요.
`

---

## 3. 실습 진행 (Action)

1. 이제 빈 Python 파일 \	est_lab_custom.py\ 를 엽니다.
2. Copilot Chat(측면 패널)을 열고, **평소처럼 단순하게** 다음 프롬프트를 입력하세요:
   > "리스트(numbers)를 받아서 평균을 계산하고 반환하는 파이썬 함수를 만들어줘. 아무 요소도 없으면 에러를 리턴해"
   - 위 프롬프트에는 한국어 주석, snake_case, 예외처리 로깅 등에 대한 구체적인 패러다임이 전혀 포함되지 않은 Zero-shot 형태의 명령어입니다.
3. **결과 확인:** 생성된 코드가 \copilot-instructions.md\ 에 적힌 4가지 룰(한국어, snake_case, logging.error, Type Hint)을 완벽하게 따르고 있는지 코드를 삽입하여 확인합니다.

---

## 4. 실무 활용 팁 (Best Practices)
* **결과 예측:** 지시사항 파일이 없을 때 똑같은 프롬프트를 실행해보면, 영문 주석, print() 에러, 카멜케이스 등 일반적인 답변이 나옴을 알 수 있습니다.
* **버전 관리:** 이 마크다운 파일을 Git에 커밋(.gitignore에 넣지 마세요!)하여 팀원 전체가 pull을 통해 동일한 Copilot 지능을 갖도록 구성하세요.

* **팀 협업:** 팀원들과 함께 규칙을 논의하여 가장 중요한 코딩 스타일과 보안 규칙을 포함시키세요. 프로젝트마다 다른 지시사항 파일을 만들어도 됩니다.

