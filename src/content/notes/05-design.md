---
num: "05"
en: "Design"
ko: "디자인"
group: design-architect
read_time: "약 10분 읽기"
h1_lead: "디자인 — 결정의 시각화."
lead: "Brand · Sketch · PRD를 받아 전 화면 hi-fi + 디자인 시스템. Claude Design 핸드오프 패턴으로 운영자 한 명이 한 사이클을 끌고 가요."
italic: "\"디자인은 결정의 시각화지 장식이 아니에요.\" — 운영 노트"
workshop_text: "Design 단계는 워크샵에서 Claude Design 핸드오프 → \"사람 한 스푼\" 추가하는 패턴을 같이 연습해요. AI 출력을 그대로 쓰지 않고 다듬는 감을 익히는 시간."
---
Design 단계가 박혀야 Architecture가 추측 없이 진행돼요. 화면 컴포넌트 트리·mock 데이터·디자인 토큰이 다 잡힌 상태에서 스택을 결정하면 마이그레이션 비용이 거의 없어요.

### 디자인 토큰을 코드 상수로

컬러·타입·spacing·radii·shadow를 한 곳에 박음. CSS variables이든 Tailwind config든 같은 토큰을 코드 전체가 참조해요. 다음 사이클에 토큰만 바꾸면 전체 톤이 한 번에 바뀌어요.

### 전 화면 + 엣지 상태

빈·로딩·에러·404를 design 단계에서 다 그림. 빌드에서 누락 X. Bsides는 이번 사이클에 site/ 안에 404·진행상황 0개·사이 회차·잘못된 slug 4가지 엣지 화면을 다 박았어요.

<div class="b-note-card"><div class="b-note-card-title">AI 슬롭 회피</div><div class="b-note-card-body">그라데이션 글로우·중앙 정렬 hero stack·"Powered by AI" 뱃지·매끈한 stock 사진 — 이 네 가지만 빼도 한국 brand 톤에 훨씬 가까워요.</div></div>

### 다음 단계로

디자인 코드가 frozen되면 **06 Architecture**가 그 코드를 진실의 원천으로 받아 스택·data model·API를 결정해요.
