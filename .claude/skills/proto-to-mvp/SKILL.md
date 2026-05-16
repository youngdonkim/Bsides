---
name: proto-to-mvp
description: MVP 사이클 (prototype → PMF 검증 MVP, 15단계, PSF 진입·PMF retro 게이트)
disable-model-invocation: true
---

이 스킬은 한 번 호출되면 **현재 사이클의 현재 단계**를 판별하고 해당 단계 references를 읽어 사용자와 인터랙티브하게 진행한다. 15단계를 한 번에 다 진행하지 않는다 — 단계별 호출, 또는 빌드 단계처럼 자동 실행 명시 시에만 연속 실행.

## 1. 진입 흐름

### 1.0 사이클 위치 — MVP 단계

이 스킬은 **MVP 단계** 전용. **prototype 사이클 retro의 PSF(Problem-Solution Fit) ✅ 판정이 진입 전제**. 빈 캔버스 시작 X — 직전 prototype 산출물을 base로 진화. 15단계(13 + Launch + PR/Marketing) → retro에서 **PMF(Product-Market Fit) 판정**으로 사이클 종료. PMF ✅ → `mvp-to-production`로 production 진입. PMF ❌ → MVP 재실행(산출물 추가 진화) 또는 종료.

### 1.1 현재 MVP 사이클 판별

- **진입 조건 검증** — 직전 prototype 사이클(`v*-prototype` 폴더)의 `retro.md`에 PSF 판정 결과 확인. 미판정·❌면 사용자에게 알리고 `zero-to-proto`로 회귀 안내 (피봇 또는 retro 마무리).
- `v*-mvp` 폴더 있으면 그 폴더 사용 (가장 큰 vN).
- 없으면 → `references/cycle-triggers.md`의 "직전 사이클 산출물 base로 복사" 절차로 새 `v{N+1}-mvp/` 폴더 생성. **빈 파일에서 시작 금지** — 직전 prototype 산출물을 모두 복사 후 단계별로 diff 업데이트.
- 사용자가 특정 단계를 콕 집어 지시하면 그 단계로 점프 (§1.2 게이트는 "사용자 명시 점프" 사유로 통과).
- `v*-prototype` 또는 `v*-prod` 폴더는 **이 스킬 영역 X** (`v*-prototype`은 진입 검증용 read만).

### 1.2 현재 단계 판별

- 현재 사이클 폴더에서 §2 표 산출물의 존재·완성도를 단계 순으로 검사.
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

## 2. 15단계 구성

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
| 8 | Automation Setup | `automation-setup.md` — 스택 기반 dev env 자동 셋업 (빌드 도구·환경변수·테스트·CI/CD) | `8-automation-setup.md` |
| 9 | Phase 빌드 | 코드 + `build/phase{N}-output.json` | `9-phase-run.md` |
| 10 | 통합 테스트 | `qa-report.md`, `tests/integration/` | `10-integration-test.md` |
| 11 | 문서화 | `docs/README.md` 등 | `11-documentation.md` |
| 12 | 배포 | `deploy-checklist.md` | `12-deploy.md` |
| 13 | **출시 (Launch)** | `launch-checklist.md`·`first-users.md` | `13-launch.md` |
| 14 | **홍보·마케팅** | `marketing-plan.md`·`channel-experiments.md` | `14-pr-marketing.md` |
| 15 | 회고 | `retro.md` | `15-retro.md` |

각 단계의 플랫폼·stage 분기·skip 조건은 해당 references 참조. **5번 Design은 UI 플랫폼(web/mobile/desktop) 전용** — 비 UI(cli/library/api-server)는 4번 PRD 후 6번 Architecture로 직행.

### 2.1 SoT 매트릭스 — 영역별 진실의 원천

산출물 간 중복·충돌을 피하기 위해 영역별 SoT(Source of Truth) 분리. 각 references는 이 매트릭스를 input/output 경계로 작동.

| 영역 | SoT | 다른 산출물 |
|---|---|---|
| Brand essence · voice · 시각·언어 톤 · 금지 사항 · **Tokens**(컬러·타입·spacing·motion) | **brand-guide.md** | sketch·prd·design은 참조만 |
| 화면 layout · 컴포넌트 stacking · 시나리오 · 플로우 · 화면별 엣지 케이스 (빈·로딩·에러 등) | **sketch.md** | prd에선 sketch 참조로 redirect |
| 기능 동작 (트리거·동작·결과) · 비기능 요구사항 · 외부 의존성 · 제약조건 | **prd.md** | 시각·카피 정보는 sketch/brand 참조로 redirect |
| 모든 화면 + 엣지 + 인터랙션 상태 + 디자인 시스템 (hi-fi) | **design/** | brand·sketch·prd가 input, design이 frozen output → Architecture로 인계 |

각 references는 자기 영역만 SoT, 다른 영역은 참조만. PRD에 시각 layout 정보가 들어가면 sketch와 중복 — sketch SoT 기준으로 PRD에서 redirect.

해당 references가 아직 없으면 사용자에게 알리고 작성 후 진행하거나 사용자가 직접 진행하도록 안내.

### 2.2 Retro 게이트 — 사이클 졸업·다음 단계 진입

15번 Retro에서 **PMF(Product-Market Fit) 판정**: real users(10s~100s) retention·organic 시그널·NPS·사용 빈도 기반. 판정 결과로 다음 단계 분기:

- **PMF ✅** → `mvp-to-production` 스킬로 production 사이클 진입 (MVP 산출물을 base로 진화, scale·운영·다채널 마케팅 깊이)
- **PMF ❌** → MVP 재실행 (산출물 추가 진화, 새 MVP 사이클 `v{N+1}-mvp` 또는 동일 폴더 deepening) 또는 종료

Retro 작성 절차: `references/15-retro.md`.

## 3. 사이클 관리

산출물 위치: `planning/cycles/v{N}-{label}/`. 디렉토리 구조·새 사이클 시작 절차·라벨 컨벤션·엣지 케이스(수동 폴더, vN 점프, 라벨 충돌)는 모두 `references/cycle-triggers.md` 참조.

핵심 원칙: **새 사이클은 직전 산출물 base로 복사 후 diff 업데이트**. 빈 파일에서 시작 금지.

### 3.1 영구 의사결정 (ADR)

사이클을 가로지르는 결정은 **`planning/adr.md` 단일 파일**에 한 섹션씩 누적. 사이클 산출물(`planning/cycles/`)은 시점 frozen 스냅샷이라, 결정의 *이유*와 *변경 이력*을 따로 보존. **사안마다 개별 파일 금지**.

**ADR 트리거** — 다음 감지 시 AI가 한 줄로 확인 ("이건 ADR감인 것 같아 — 기록할까?"):
- 외부 인프라 선택·교체 (DB·Auth·Storage·Hosting·LLM provider 등)
- 보안·인증·권한 모델 변경
- 스택 주요 컴포넌트 추가·제거 (Redis·GraphQL·queue 등)
- 비용 구조에 큰 영향을 주는 결정
- 이전 cycle artifact의 결정을 뒤집는 변경

**ADR 아닌 것**: 사이클 안 임시 결정 → cycle artifact 인라인 / 코드 컨벤션 → `.claude/rules/`·`CLAUDE.md` / 일반 버그 수정·리팩터링.

**작성 형식** — `planning/adr.md` 안 한 섹션:

```markdown
## ADR-NNNN: <제목> (YYYY-MM-DD)
- **상태**: Accepted | Superseded by ADR-XXXX | Deprecated
- **변경**: 무엇이 어떻게 바뀌었나
- **이유**: 왜 (제약·트레이드오프·대안 검토)
```

뒤집힐 때 옛 섹션 삭제·수정 금지 — *새 ADR-NNNN으로 supersede*. 파일이 너무 커지면 사용자가 분리.

## 4. 단계 게이트와 건너뛰기

각 단계 진입 전 이전 산출물의 **존재**와 **완성도**(해당 references 체크리스트)를 검사. *게이트* = "이전 단계 산출물이 갖춰졌는지 확인하는 잠금장치". 미통과 시 3 옵션:

- (a) 이전 단계 보완 — 안전한 디폴트
- (b) 강행 — 빈 placeholder 산출물 자동 생성 후 진행, 회고에서 재점검
- (c) 산출물 없이 진행 + 회고에서 재점검

선택 사유는 해당 단계 산출물 또는 `retro.md`에 기록.

### 4.1 MVP 사이클 게이트 강도 — **경고 + 사용자 선택**

이 사이클은 *real users 10s~100s 노출·PMF 검증*. 게이트 미달 시 **사용자에게 확인** — 통과 결정하면 사유를 retro에 기록. (a)(b)(c) 옵션 모두 가능하되, (b)·(c) 선택 시 retro 기록 필수.

각 단계 references의 정량 체크리스트(비기능 임계값·성능 budget·보안 룰)는 mvp 강도 하위에서 평가. (다른 사이클 강도: Prototype = 측정·기록만. Production = 강제 차단. 해당 SKILL.md 참조.)

## 5. Phase 빌드(9단계) 실행

빌드 단계는 `scripts/run-phases.py` 자동화로 동작. 핵심 절차:

1. `build/` 디렉토리 확인 (생성 가이드 = `references/7-build-plan.md`).
2. 사용자에게 실행 방식(foreground/background) 확인. 복잡도 기반 추천하되 결정은 사용자.
3. 스크립트 실행: `python3 .claude/skills/proto-to-mvp/scripts/run-phases.py <cycle-label>` (예: `v2-mvp`).
4. 종료 후 `build/index.json`의 모든 phase status 검사. **종료 코드만 보고 성공 판단 금지.**
5. error/blocked/needs_review 발견 시 구체적 액션과 함께 보고. 사용자 자연어 재개 지시 시 status 자동 리셋 후 재실행.

자세한 절차·진행 보고·재시작 처리·외부 장애 구분은 `references/9-phase-run.md`. 상태 머신은 `references/states.md`.
