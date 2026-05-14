---
name: mvp-to-production
description: Run a **production-phase** development cycle from a PMF-validated MVP to production (scale·ops·sustainable business). Guides through 15 stages — the 13 prototype stages (Intent · Brand Guide · Sketch · PRD · Design · Architecture · Build plan · Automation setup · Phase build · Integration test · Documentation · Deploy) + Launch + PR & Marketing + Retrospective — each scoped for production: scale, monitoring·SLA, multi-channel marketing, ops procedures, cost·SLA budget. Inherits from MVP retro. **Scope: production only.** For prototype phase use `zero-to-prototype`; for MVP phase use `prototype-to-mvp`. Each skill is self-contained — content may overlap but each diverges per scope.
---

이 스킬은 한 번 호출되면 **현재 사이클의 현재 단계**를 판별하고 해당 단계 references를 읽어 사용자와 인터랙티브하게 진행한다. 13단계를 한 번에 다 진행하지 않는다 — 단계별 호출, 또는 빌드 단계처럼 자동 실행 명시 시에만 연속 실행.

## 0. 운영 원칙 (Background)

스킬을 진행할 때 다음 3가지를 머리에 심고 출발한다. 각 단계 references는 이 원칙을 전제로 짧게 쓰여있다.

### 0.1 위협 모델 — 외부 도달 가정

이 스킬로 만드는 소프트웨어는 **외부 인터넷 도달 가능**을 기본 가정한다. preview 배포·공유 URL·봇 prefetch·검색엔진·우연한 ID 추측 모두 가능. "내부 베타라 안전"이라는 가정은 위협 모델 불일치. 따라서:
- 인증·권한·민감정보·파일 업로드 룰은 **prototype 1차부터 적용**. v2에서 보강이 아니라 v1부터 baseline.
- preview = prod와 동일 노출 환경. `NODE_ENV === 'development'`는 로컬에서만 true.
- 플랫폼·스택별 룰은 `.claude/rules/`에 박혀있고 매칭 파일 read 시 자동 로드. 단계별 결정은 그 룰을 입력으로 받음.

### 0.2 LLM 한계 — 못 보는 것은 사용자가 본다

LLM은 다음을 못 본다:
- **시각·UX**: 화면 렌더링 결과·마이크로 인터랙션 실제 느낌·다크모드 색감·여백 비율
- **실사용 부수 효과**: 사용자가 실제로 클릭했을 때 흐름·로딩 체감·터치 반응
- **현장 dynamics**: 사용자 N=3 베타에서 어떤 카피가 "이상하다" 같은 코멘트

→ 이런 영역은 **디자인·아키텍처 단계 입력으로 표준 baseline을 박아 사전 반영**하고 (예: `.claude/rules/ui-ux-baseline.md`), 그래도 남는 부분은 사용자 발견·retrospective 룰화 판정으로 누적. phase build 중간에 visual walkthrough 강제는 폐쇄루프 사상에 반함 — 표준은 **단계 입력으로**, 발견은 **회고로**.

### 0.3 룰 인플레이션 경계 — 추가는 비용

`.claude/rules/`·`CLAUDE.md` 룰은 매 세션 또는 매칭 파일 read 시 LLM context를 먹는다. 추가는 비용:
- 길수록 매 phase에서 다 평가 안 함 (context bandwidth 한계)
- 좁고 정확한 트리거 매핑(`paths:` frontmatter)이 약해짐
- 사용자가 후에 "이 룰 왜 있지?" 추적 비용 ↑

→ 발견 사항을 즉시 룰화하지 말고, 13단계 retrospective의 **3분류 판정**(룰화 / spot fix / 코멘트)을 통과한 것만 룰화. 자세히는 `references/13-retro.md` §2.3.1.

**룰 작성 시 — Anthropic 공식 가이드**: 원칙·heuristics 먼저, 코드 예시는 default로 깔지 말 것. *"Find the smallest set of high-signal tokens"* (Anthropic context engineering). 표준 컨벤션·LLM이 이미 아는 패턴은 박지 말 것. 예시는 (a) specific value(magic byte hex·timing 등 외울 수 없는 정량), (b) non-standard 패턴(LLM 직관과 어긋나는 흐름), (c) 1~2줄 ❌/✅ 대조 — 이 3가지에만 사용. 매 줄 "이걸 빼도 LLM이 실수할까?" 질문 통과해야 유지.

### 0.3.1 룰 검증 강도 분류 — codify 시점 결정

룰이 "어디서 검증됐나"에 따라 codify 시점 다름. AI 시대 비용은 개발 공수 X, **검증 안 된 룰의 부정확성 + context token + 신뢰 erosion**이 진짜 비용.

| 검증 강도 | 출처 | codify 시점 |
|---|---|---|
| **산업 표준** | Google web.dev·OWASP·WCAG 등 공식 | 즉시 references / `.claude/rules/`에 박음 |
| **공식 docs 권장** | 스택 공식 문서 (Next.js·Vue·Flutter 등) | 6단계에서 stack rule로 자동 생성 |
| **cycle 경험** | 우리 cycle에서 발견 | 13-retro 3분류 판정 통과 후 codify |

**4 Layer 분리 원칙**:
1. **Universal** (플랫폼·스택 무관) → 스킬 references
2. **Platform별** (web/mobile/cli 등) → 스킬 references 플랫폼 분기
3. **Stack별** (Next.js·Flutter 등) → **6단계 Architecture 후 `.claude/rules/{kind}-{stack}.md` 자동 생성** (LLM이 공식 docs 조사·정리)
4. **Project별** → 13-retro 누적

스킬은 1·2만 박고, 3·4는 프로젝트 안에 분리. 스킬을 다른 프로젝트에 빌릴 때 1·2는 그대로 통하고 3·4는 그 프로젝트 환경에 맞게 새로 생성.

## 1. 진입 흐름

### 1.1 현재 사이클 판별

- `planning/cycles/` 없으면 → 자동으로 `cycles/v1-prototype/` 생성 후 Intent부터 시작.
- 있으면 → vN 접두사가 가장 큰 폴더가 진행 중 사이클(별도 포인터 파일 없음).
- 사용자 입력에 새 사이클 시작 의도가 있으면 `references/cycle-triggers.md` 절차. 의도 모호하면(예: "이제 MVP 만들고 싶어") 같은 파일의 확인 질문 템플릿 사용.

### 1.2 현재 단계 판별

- 현재 사이클 폴더에서 §3 표 산출물의 존재·완성도를 단계 순으로 검사.
- 비거나 미완성인 가장 빠른 단계 = 진행 대상.
- 사용자가 특정 단계를 콕 집어 지시하면 그 단계로 점프 (게이트는 "사용자 명시 점프" 사유로 통과).

### 1.3 단계 references 라우팅 + 응대 톤

- `references/{N}-{name}.md`를 읽고 그 가이드대로 진행. 각 references는 (a) 사용자 질문 셋, (b) 산출물 스펙, (c) 완료 체크리스트, (d) 좋은/나쁜 예시를 가짐.
- **사용자 응대 톤**: 반말·친구처럼 친근·짧지만 핵심 담음·유쾌. 표·헤더·긴 설명 디폴트로 깔지 않음. 결론부터. 자세히 풀어 말하는 건 사용자가 그 핵심을 구체적으로 물을 때만.

### 1.4 인터뷰 코칭 원칙

각 references의 인터뷰는 **사용자가 처음부터 좋은 답을 만들지 못한다**는 가정으로 작동한다. PRD·User Story·기능 명세 같은 산출물은 사람이 처음 써보면 누락·추상·일반론이 섞이는 게 정상이다. AI가 가공·되물음으로 좋은 예 형식까지 끌고 간다.

- **빠진 부분을 일일이 짚어 되묻기.** references의 "좋은 예" 패턴(구체성·검증 가능성·필수 항목 충족)에 사용자 답이 못 미치면 그대로 두지 말고 모자란 항목 체크. 한 번에 다 짚지 말고 핵심 1~2개부터 → 답 받으면 다음 → 반복.
- **"잘 모르겠어"는 정상 답.** 사용자가 답을 못하면 AI가 후보 2~3개 제시 → 사용자가 골라서 다듬는 형태로. 빈 칸 채우라고 압박하지 말기.
- **AI가 좋은 예 형식으로 정리해 보여주고 확인 받기.** "이거 맞아? 고칠 데 있어?" — 사용자가 처음부터 형식 갖춰 답할 필요 없음.
- **본질 보존 + 형식만 가공.** 사용자가 답한 의미는 절대 변경 금지. 임의 정보 추가도 금지 — 모르는 부분은 산출물에 `TBD: [무엇을 다시 확인할지]`로 명시 후 다음 단계 진입 시 사용자에게 재확인.
- **진행 중 이전 결정 변경 처리.** 단계 진행 중 이전 산출물의 결정이 바뀌어야 함을 감지하면(예: Sketch 그리다 플랫폼이 web → mobile로), AI가 자연어로 영향 범위 짚고 사용자 의향 확인. **영향 작으면**(frontmatter 한 줄 또는 와이어프레임 일부) 자연스럽게 부분 업데이트해 진행. **영향 크면**(여러 단계 산출물 영향) 두 옵션 제시: (a) 영향 부분만 손봐서 이어가기, (b) 새 사이클로 시작해 직전 산출물을 base로 보존. 전체 단계 재방문 강제 금지.

## 2. 플랫폼 분기 패턴

소프트웨어 전반(웹·앱·CLI·라이브러리·데스크톱·API서버) 포괄. 플랫폼이 다르면 묻는 질문도 다름.

- Intent 단계 첫 질문 = **"어떤 형태의 소프트웨어인가요?"**. 답을 `intent.md` frontmatter `platform` 필드에 기록 (`web`, `mobile`, `cli`, `library`, `desktop`, `api-server`, `other` 중 하나). **메인 플랫폼 하나만**(UX 우선순위 가장 높은 플랫폼).
- **Cross-platform 케이스**(Flutter·RN·Tauri·Electron 등): 메인 플랫폼 + `platforms` 추가 필드(예: `[web, mobile-ios, mobile-android]`) + `cross_platform_framework` 필드. 추가 platforms가 있으면 PRD·Architecture 단계에서 각 플랫폼 분기 질문 셋을 모두 적용 — 한 코드베이스라도 각 플랫폼 UX는 native하게.
- 이후 단계 references는 플랫폼별 분기 질문 셋을 가짐. `other`/미결정이면 범용으로 진행.

## 3. 15단계 구성

MVP 사이클은 prototype의 13단계를 이어받고 **출시·홍보·마케팅을 추가**해 retro 앞에 끼움. retro는 15번으로 밀림.

| # | 단계 | 산출물 (현재 사이클 폴더 기준) | references |
|---|------|---|---|
| 1 | Intent | `intent.md` | `1-intent.md` |
| 2 | Brand Guide | `brand-guide.md` | `2-brand-guide.md` |
| 3 | Sketch | `sketch.md` 또는 `sketch/` | `3-sketch.md` |
| 4 | PRD | `prd.md` | `4-prd.md` |
| 5 | Design | `design/` (Claude Design 산출물 + 정합성 점검 결과) | `5-design.md` |
| 6 | Architecture | `architecture.md`, `data-model.md`, `migration-analysis.md`, `migration-plan.md` | `6-architecture.md` |
| 7 | Build plan | `build/index.json` + `build/phase{N}.md` | `7-build-plan.md` |
| 8 | Automation Setup | `.claude/`(skills·hooks·permissions) | `8-automation-setup.md` |
| 9 | Phase 빌드 | 코드 + `build/phase{N}-output.json` | `9-phase-run.md` |
| 10 | 통합 테스트 | `qa-report.md`, `tests/integration/` | `10-integration-test.md` |
| 11 | 문서화 | `docs/README.md` 등 | `11-documentation.md` |
| 12 | 배포 | `deploy-checklist.md` | `12-deploy.md` |
| 13 | **출시 (Launch)** | `launch-checklist.md`·`first-users.md` | `13-launch.md` |
| 14 | **홍보·마케팅** | `marketing-plan.md`·`channel-experiments.md` | `14-pr-marketing.md` |
| 15 | 회고 | `retro.md` | `15-retro.md` |

2번 Brand Guide는 UI 플랫폼에서 8개 항목 전부, 비 UI 플랫폼(cli/library/api-server)에서는 essence·voice·카피·금지 4개만 적용. Brand Guide의 §1~5·§8은 Intent만 있어도 박을 수 있고, §6·7(차별 시각 시그널·카피 패턴)은 다음 단계인 Sketch가 진행되면서 보강된다 — Sketch가 brand-guide를 input으로 받아 카피·시각 placeholder가 처음부터 정합하게 박히는 것이 이 순서의 목적. 5번 Design은 **UI 플랫폼(web/mobile/desktop) 전용**. CLI·library·api-server는 게이트 정책으로 skip — 그 경우 PRD(4번) 통과 후 바로 6번 Architecture로. 6번 Architecture는 모든 플랫폼 적용 (UI 플랫폼은 Design 코드를 진실의 원천으로 받아 스택·data-model·API 명세·마이그레이션 계획 결정).

### 3.1 SoT 매트릭스 — 영역별 진실의 원천

산출물 간 중복·충돌을 피하기 위해 영역별 SoT(Source of Truth) 분리. 각 references는 이 매트릭스를 input/output 경계로 작동.

| 영역 | SoT | 다른 산출물 |
|---|---|---|
| Brand essence · voice · 시각·언어 톤 · 금지 사항 · **Tokens**(컬러·타입·spacing·motion) | **brand-guide.md** | sketch·prd·design은 참조만 |
| 화면 layout · 컴포넌트 stacking · 시나리오 · 플로우 · 화면별 엣지 케이스 (빈·로딩·에러 등) | **sketch.md** | prd에선 sketch 참조로 redirect |
| 기능 동작 (트리거·동작·결과) · 비기능 요구사항 · 외부 의존성 · 제약조건 | **prd.md** | 시각·카피 정보는 sketch/brand 참조로 redirect |
| 모든 화면 + 엣지 + 인터랙션 상태 + 디자인 시스템 (hi-fi) | **design/** | brand·sketch·prd가 input, design이 frozen output → Architecture로 인계 |

각 references는 자기 영역만 SoT, 다른 영역은 참조만. PRD에 시각 layout 정보가 들어가면 sketch와 중복 — sketch SoT 기준으로 PRD에서 redirect.

해당 references가 아직 없으면 사용자에게 알리고 작성 후 진행하거나 사용자가 직접 진행하도록 안내.

## 4. 사이클 관리

산출물 위치: `planning/cycles/v{N}-{label}/`. 디렉토리 구조·새 사이클 시작 절차·라벨 컨벤션·엣지 케이스(수동 폴더, vN 점프, 라벨 충돌)는 모두 `references/cycle-triggers.md` 참조.

핵심 원칙: **새 사이클은 직전 산출물 base로 복사 후 diff 업데이트**. 빈 파일에서 시작 금지.

### 4.1 영구 의사결정 (ADR)

사이클을 가로지르는 결정은 **`planning/docs/adr/NNNN-<제목>.md`** 에 기록한다. 사이클 산출물(`planning/cycles/`)은 시점 frozen 스냅샷이라, 결정의 *이유*와 *변경 이력*을 따로 보존해야 한다.

**ADR 작성 트리거 — 다음을 감지하면 AI가 사용자에게 작성 제안**:
- 외부 인프라 선택·교체 (DB, Auth, Storage, Hosting, LLM provider 등)
- 보안·인증 모델 변경 (예: 인증 provider 추가·제거)
- 권한 모델·데이터 격리 전략 변경
- 스택 주요 컴포넌트 추가·제거 (Redis, GraphQL, queue 등)
- 비용 구조에 큰 영향을 주는 결정
- 이전 cycle artifact의 결정을 뒤집는 변경 (architecture.md DB row 갈아엎기 등)
- 코드 리뷰·incident에서 발견된 보안 결정

**ADR 안 쓰는 것**:
- 사이클 안에서만 유효한 임시 결정 → cycle artifact에 인라인
- 코드 컨벤션·스타일 → `.claude/rules/` 또는 `CLAUDE.md`
- 일반 버그 수정·리팩터링

**작성 절차**:
1. AI가 트리거를 감지하면 한 줄로 "이건 ADR감인 것 같아 — 기록할까?" 확인
2. 승인 시 `planning/docs/adr/README.md`의 포맷(Michael Nygard 1-page) 따라 작성
3. 번호는 기존 ADR 다음 번호 (zero-padded 4자리, 영구·재사용 금지)
4. 관련 cycle artifact·CLAUDE.md·`.claude/rules/`도 함께 갱신 (인라인 표기는 ADR 링크로 대체 가능)
5. `planning/docs/adr/README.md` 색인 표에 한 줄 추가

**Status 규칙**: `Proposed → Accepted → Superseded by ADR-XXXX | Deprecated`. 결정 뒤집힐 때 옛 ADR을 삭제·수정하지 않고 **새 ADR로 supersede**.

## 5. 단계 게이트와 건너뛰기

각 단계 진입 전 이전 산출물의 **존재**와 **완성도**(해당 references 체크리스트)를 검사. 미통과 시 강제로 막지 않고 선택지 제시:

- (a) 이전 단계 보완 — 안전한 디폴트
- (b) 강행 — 빈 placeholder 산출물 자동 생성 후 진행, 회고에서 재점검
- (c) 산출물 없이 진행 + 회고에서 재점검

선택 사유는 해당 단계 산출물 또는 `retro.md`에 기록.

### 5.1 Stage별 게이트 강도 — 사이클 라벨 base

같은 게이트라도 사이클 stage에 따라 강도 다름. shift-left 점진 적용 패턴:

| 사이클 라벨 | 게이트 강도 | 적용 |
|---|---|---|
| `v*-prototype` | **측정·기록만** | 미달이면 retro에 기록, 강제 차단 X. 디자인·기능 빠른 변경 우선. |
| `v*-mvp` | **경고 + 사용자 선택** | 미달이면 사용자에게 확인. 통과 결정 시 사유 retro에 기록. |
| `v*-prod` | **강제 차단** | 미달 시 다음 단계 진입 불가. 게이트 통과 의무. |

각 단계 references의 정량 체크리스트(예: 비기능 임계값·성능 budget·보안 룰)는 stage 강도 메타룰 하위에서 평가. 미달 시 게이트 정책(§5)의 (a/b/c) 선택지 적용은 그대로.

## 6. Phase 빌드(9단계) 실행

빌드 단계는 `scripts/run-phases.py` 자동화로 동작. 핵심 절차:

1. `build/` 디렉토리 확인 (생성 가이드 = `references/7-build-plan.md`).
2. 사용자에게 실행 방식(foreground/background) 확인. 복잡도 기반 추천하되 결정은 사용자.
3. 스크립트 실행: `python3 .claude/skills/zero-to-prototype/scripts/run-phases.py <cycle-label>` (예: `v1-prototype`).
4. 종료 후 `build/index.json`의 모든 phase status 검사. **종료 코드만 보고 성공 판단 금지.**
5. error/blocked/needs_review 발견 시 구체적 액션과 함께 보고. 사용자 자연어 재개 지시 시 status 자동 리셋 후 재실행.

자세한 절차·진행 보고·재시작 처리·외부 장애 구분은 `references/9-phase-run.md`. 상태 머신은 `references/states.md`.

## 7. 상태 관리

빌드 phase 상태는 `references/states.md`의 6상태 머신(`pending`/`in_progress`/`needs_review`/`blocked`/`error`/`completed`)을 따른다. `needs_review`는 보안·시크릿·DB 스키마·외부 호출·비결정성·권한 상승 변경 시 자동 진입, 사용자 승인 없이 `completed`로 못 감.
