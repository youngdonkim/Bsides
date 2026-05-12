---
num: "06"
en: "Architecture"
ko: "아키텍처"
group: design-architect
read_time: "약 10분 읽기"
h1_lead: "아키텍처 — 미래 6개월 그리기."
lead: "기술 스택·시스템 구조·데이터 모델·API·디렉토리. PRD + Design 코드를 입력으로 받아 \"어떻게 만들 것인가\"의 구체적 결정."
italic: "\"스택을 정하는 건 미래 6개월을 그리는 일이에요.\" — 운영 노트"
workshop_text: "Architecture는 워크샵에서 \"이 결정 왜 했지?\" 질문을 다섯 번 던지는 시간이에요. 답이 막히면 그 결정은 다시 깎아야 해요."
---
Architecture가 박힐 때 가장 중요한 건 결정에 **대안**과 **이유**를 한 줄씩 적는 것. 미래에 누군가 "왜 X로 갔지?" 물을 때 1년 후 본인이 답할 수 있어요.

### 5 카테고리 결정

**언어 · 프레임워크 · DB · 인프라 · 외부 서비스** — 다섯 항목 모두 결정. 각 항목에 대안 1개 + 이유 한 줄 강제. 이 한 줄이 미래 토론을 한 번에 끝내요.

### 누락 점검

PRD Must 기능이 동작하려면 결정돼야 하는데 안 결정된 항목 찾기. 인증 흐름·로깅·에러 핸들링·환경 변수·CI/CD·관측성·시크릿 같은 횡단 영역.

<div style="margin: 12px 0px; padding: 20px 22px; background: var(--b-note-mint); border-radius: 12px; transform: rotate(-1deg); box-shadow: var(--b-shadow-note);"><div style="font-family: var(--b-font-hand); font-size: 22px; color: var(--b-ink); margin-bottom: 6px;">한 스푼 메모</div><div style="font-family: var(--b-font-sans); font-size: 14.5px; line-height: 1.55; color: var(--b-ink);">대안 + 이유 한 줄 안 적으면 미래 토론이 끝없이 돌아와요. 적어두면 한 번에 끝.</div></div>

### 다음 단계로

Architecture가 박히면 **07 Build Plan**에서 이 스택을 phase 분할 단위로 나눠요. 각 phase는 검증 가능한 산출물 단위.
