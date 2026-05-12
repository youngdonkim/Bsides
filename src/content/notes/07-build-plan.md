---
num: "07"
en: "Build Plan"
ko: "빌드 계획"
group: design-architect
read_time: "약 6분 읽기"
h1_lead: "빌드 계획 — phase는 검증 단위."
lead: "큰 빌드를 phase N개로 분할. 각 phase는 끝나는 시점에 검증 가능한 산출물."
italic: "\"phase는 commit 단위가 아니라 검증 단위예요.\" — 운영 노트"
workshop_text: "Build plan은 워크샵에서 운영자가 phase 그래프를 보여주고 \"여기서 막히면 어떻게 할래?\" 시나리오 연습하는 시간이에요."
---
한 phase가 너무 크면 검증이 죽어요. 한 phase 4~6시간 안에 끝나서 산출물 자체로 "이게 됐다/안 됐다" 판정할 수 있어야 해요.

### 의존성·자동 실행 단위

phase 간 의존성을 그래프로. 의존성 없는 phase들끼리는 병렬, 의존성 있는 건 순차. 자동화 셋업이 잘 박혀있으면 사람이 자리 비워도 phase 여러 개가 도는 상태로.

### needs_review 게이트

보안·시크릿·DB 스키마·외부 호출·권한 상승은 사용자 승인 필수. 자동으로 진행 안 됨. needs_review 진입 조건을 명시해두면 자동화가 안전해요.

<div style="margin: 12px 0px; padding: 20px 22px; background: var(--b-note-mint); border-radius: 12px; transform: rotate(-1deg); box-shadow: var(--b-shadow-note);"><div style="font-family: var(--b-font-hand); font-size: 22px; color: var(--b-ink); margin-bottom: 6px;">한 스푼 메모</div><div style="font-family: var(--b-font-sans); font-size: 14.5px; line-height: 1.55; color: var(--b-ink);">phase가 너무 크면 절반 자르기. 4~6시간 안에 끝나야 검증이 살아있어요.</div></div>

### 다음 단계로

Build plan이 박히면 **08 Automation Setup**에서 .claude/ skills·hooks·permissions를 만들어요. 매 phase가 자동 돌아가게.
