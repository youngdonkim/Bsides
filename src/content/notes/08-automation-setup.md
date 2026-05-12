---
num: "08"
en: "Automation Setup"
ko: "자동화 셋업"
group: design-architect
read_time: "약 6분 읽기"
h1_lead: "자동화 셋업 — 미래의 본인에게 편지."
lead: ".claude/ 디렉토리 — skills, hooks, permissions. 매 phase가 자동 동작하게 한 번 박아두는 단계."
italic: "\"자동화는 미래의 본인에게 보내는 편지예요.\" — 운영 노트"
workshop_text: "Automation Setup은 워크샵에서 운영자가 hook 한두 개 같이 만들면서 \"왜 이걸 자동화하나\" 감을 익히는 시간이에요."
---
한 번 잘 박아두면 사이클이 도는 동안 손이 거의 안 가요. 단, 위험한 명령은 항상 사람 게이트.

### hooks — 자동 검증·로깅

매 행동 후 자동으로 type check·lint·test 등을 트리거. 사용자가 알기 전에 발견하는 게 핵심. 실패하면 사용자에게 보고.

### permissions — 위험 게이트

파일 삭제·rm -rf·force push·DB drop 같은 비가역 작업은 사용자 승인 필수. 자동화가 똑똑할수록 권한은 보수적으로.

<div style="margin: 12px 0px; padding: 20px 22px; background: var(--b-note-mint); border-radius: 12px; transform: rotate(-1deg); box-shadow: var(--b-shadow-note);"><div style="font-family: var(--b-font-hand); font-size: 22px; color: var(--b-ink); margin-bottom: 6px;">한 스푼 메모</div><div style="font-family: var(--b-font-sans); font-size: 14.5px; line-height: 1.55; color: var(--b-ink);">사람 손 거치는 단계 줄이기. 단, 위험은 항상 사람 게이트. 두 원칙이 충돌하면 위험 쪽이 우선.</div></div>

### 다음 단계로

Automation Setup이 박히면 **09 Phase Build**에서 실제 코딩이 시작돼요. 자동화 위에서 코드가 흐르는 단계.
