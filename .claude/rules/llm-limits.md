---
name: llm-limits
description: LLM이 못 보는 영역 — 시각·UX·실사용 부수효과·현장 dynamics. 디자인·컴포넌트 작업 시 baseline + retro로 다룸.
paths:
  - 'src/components/**/*'
  - 'src/pages/**/*'
  - 'src/layouts/**/*'
  - 'planning/cycles/**/design/**'
  - 'planning/cycles/**/sketch*'
---

# LLM 한계 — 못 보는 것은 사용자가 본다

LLM은 다음을 못 본다:

- **시각·UX**: 화면 렌더링 결과·마이크로 인터랙션 실제 느낌·다크모드 색감·여백 비율
- **실사용 부수 효과**: 사용자가 실제로 클릭했을 때 흐름·로딩 체감·터치 반응
- **현장 dynamics**: 사용자 N=3 베타에서 어떤 카피가 "이상하다" 같은 코멘트

## 다루는 방식

1. **디자인·아키텍처 단계 입력으로 표준 baseline을 박아 사전 반영** (예: `.claude/rules/ui-ux-baseline.md`)
2. 그래도 남는 부분은 **사용자 발견·retrospective 룰화 판정**으로 누적

phase build 중간에 visual walkthrough 강제는 폐쇄루프 사상에 반함 — 표준은 **단계 입력으로**, 발견은 **회고로**.
