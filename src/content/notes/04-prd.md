---
num: "04"
en: "PRD"
ko: "기능 명세"
group: discover-plan
read_time: "약 9분 읽기"
h1_lead: "기능 명세 — 빼는 결정이 80%."
lead: "기능을 Must/Should/Could/Won't로 줄세우는 단계. 가설 검증에 진짜 필요한 것만 남기기."
italic: "\"v1은 빼는 결정이 80%, 더하는 결정이 20%.\" — 운영 노트"
workshop_text: "PRD는 워크샵에서 운영자가 \"이거 정말 v1에 필요해요?\" 질문을 반복하는 시간이에요. 멤버가 \"음 그건 v2네요\" 답하면 Won't로 옮김."
---
PRD 1차 초안은 늘 너무 길어요. 의도 단계의 가설 검증에 정말 필요한 기능만 Must로 두고, 나머지는 Should·Could로 미루거나 Won't로 명시해서 비목표를 손에 잡히게.

### MoSCoW 줄세우기

**Must** = 가설 검증 불가하면 못 빠짐. **Should** = 있으면 좋지만 가설 검증 자체엔 not blocking. **Could** = 시간 남으면. **Won't** = intent 비목표 명시. Won't 명시가 미래 토론 비용을 가장 많이 줄여줘요.

### 비기능 요구사항

성능·보안·접근성·호환성·SEO. prototype 단계엔 산업 표준 인용 (Google Core Web Vitals · WCAG 2.2 AA 등). 정량 임계값은 mvp에서 측정 후 lock.

<div class="b-note-card"><div class="b-note-card-title">한 스푼 메모</div><div class="b-note-card-body">두 번째 패스에서 절반 잘라내기. 잘려도 좋은 게 진짜 Must.</div></div>

### 다음 단계로

PRD가 박히면 **05 Design**에서 Must 기능을 전 화면 hi-fi로 시각화해요. Sketch에서 미뤘던 엣지·인터랙션 상태도 다 그려요.
