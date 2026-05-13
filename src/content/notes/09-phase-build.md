---
num: "09"
en: "Phase Build"
ko: "빌드 실행"
group: build-ship
read_time: "약 8분 읽기"
h1_lead: "빌드 실행 — 끓는 냄비 옆 30분."
lead: "자동화로 phase 실행. 각 phase 종료 시 status 확인. 사람은 30분씩 자리 비울 수 있는 상태."
italic: "\"phase 실행은 끓는 냄비 옆에서 30분씩 자리 비우는 일이에요.\" — 운영 노트"
workshop_text: "Phase Build는 워크샵에서 운영자가 자동 실행 중인 화면을 같이 보면서 \"needs_review 걸리면 어떻게 답할까\" 연습하는 시간이에요."
---
잘 박아둔 자동화 위에서 phase가 자동 진행되는 단계. 운영자는 status 알림만 보고 needs_review 걸린 phase에 응답해주면 돼요.

### status 머신 6가지

**pending → in_progress → completed** 정상 흐름. 그 외 **needs_review** (사람 승인 대기) · **blocked** (외부 의존성 대기) · **error** (자동 복구 실패). status별로 다음 행동이 달라요.

### 외부 장애 vs 내부 버그

API 일시 오류 vs 로직 버그를 구분. 외부 장애는 재시도, 내부 버그는 코드 수정. 자동화가 이 둘을 헷갈리면 무한 재시도로 시간 날아가요.

<div class="b-note-card"><div class="b-note-card-title">한 스푼 메모</div><div class="b-note-card-body">completed status 보고 안심하지 말기. needs_review는 자동으로 안 풀려요. 사용자가 응답해야 다음 phase가 출발.</div></div>

### 다음 단계로

모든 phase가 completed되면 **10 Integration Test**에서 전체 동작을 시나리오 단위로 검증해요.
