---
num: "11"
en: "Documentation"
ko: "문서화"
group: build-ship
read_time: "약 6분 읽기"
h1_lead: "문서화 — 미래의 본인이 읽는 자기 메모."
lead: "README + 운영 가이드 + 의사결정 기록(ADR). 코드 옆 1줄 README가 멀리 떨어진 wiki 100줄보다 자주 읽혀요."
italic: "\"문서는 미래의 본인이 가장 자주 읽는 자기 메모예요.\" — 운영 노트"
workshop_text: "Documentation은 워크샵에서 운영자가 \"지금 작성한 README, 1년 후 본인이 읽을 때 충분해?\" 질문 던지는 시간이에요."
---
문서는 다른 사람을 위해 쓰는 게 아니라 미래의 본인을 위해 써요. 6개월 후 "왜 이렇게 했지?" 물을 때 답이 있는 한 줄이 가치예요.

### README 구조

**무엇**·**왜**·**어떻게 실행**·**어디에 컨트리뷰트** 네 영역. 각 영역 한 단락. 그 이상은 별도 문서로 link.

### 운영 가이드 + ADR

사이트 콘텐츠 추가 흐름·배포 절차·롤백 방법 같은 운영 일상. 굵직한 결정(스택 교체·DB 스키마 변경)은 ADR로 따로 기록.

<div style="margin: 12px 0px; padding: 20px 22px; background: var(--b-note-mint); border-radius: 12px; transform: rotate(-1deg); box-shadow: var(--b-shadow-note);"><div style="font-family: var(--b-font-hand); font-size: 22px; color: var(--b-ink); margin-bottom: 6px;">한 스푼 메모</div><div style="font-family: var(--b-font-sans); font-size: 14.5px; line-height: 1.55; color: var(--b-ink);">코드 옆 1줄 README가 멀리 떨어진 wiki 100줄보다 자주 읽혀요. 짧고 정확한 게 미덕.</div></div>

### 다음 단계로

문서가 박히면 **12 Deploy**에서 진짜 외부 사용자가 만날 수 있는 상태로. 사이클이 진짜 사용되는 순간.
