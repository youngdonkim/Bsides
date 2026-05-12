---
num: "10"
en: "Integration Test"
ko: "통합 테스트"
group: build-ship
read_time: "약 6분 읽기"
h1_lead: "통합 테스트 — 시나리오 안전망."
lead: "phase 빌드 종료 후 시나리오 단위 통합 테스트. Sketch 시나리오를 그대로 테스트 case로."
italic: "\"E2E는 빌드 끝의 안전망이지 검증의 본질이 아니에요.\" — 운영 노트"
workshop_text: "Integration Test는 워크샵에서 멤버가 직접 시나리오 5개를 손으로 클릭해보는 시간이에요. 자동 테스트 외에도 직접 만져보는 게 중요."
---
통합 테스트는 안심망 역할. 본질적 검증은 시나리오·사람 사용 흐름이지만, 회귀를 잡아주는 자동 안전망이 같이 있어야 사이클을 닫을 수 있어요.

### 시나리오 우선

Sketch 단계에서 박은 핵심 시나리오 N개를 그대로 E2E case로. Bsides는 5개 시나리오 (S1~S5) 모두 자동 테스트가 있으면 사이클 닫기 가능 판정.

### 회귀 잡기

새 기능이 옛 기능을 깨뜨리지 않는지. 너무 정밀한 테스트는 깨지기 쉬워서 유지 비용 ↑. 핵심 흐름 N개만 단단하게.

<div style="margin: 12px 0px; padding: 20px 22px; background: var(--b-note-mint); border-radius: 12px; transform: rotate(-1deg); box-shadow: var(--b-shadow-note);"><div style="font-family: var(--b-font-hand); font-size: 22px; color: var(--b-ink); margin-bottom: 6px;">한 스푼 메모</div><div style="font-family: var(--b-font-sans); font-size: 14.5px; line-height: 1.55; color: var(--b-ink);">테스트가 너무 정밀하면 깨지기 쉬워요. 핵심 흐름 5개만 단단하게.</div></div>

### 다음 단계로

통합 테스트 통과하면 **11 Documentation**에서 운영 가이드를 정리해요. 미래의 본인이 가장 자주 읽는 자기 메모.
