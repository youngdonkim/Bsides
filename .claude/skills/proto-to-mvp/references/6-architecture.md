---
name: 6-architecture
description: Architecture 단계 가이드. PRD + (UI 플랫폼이면) Design 코드를 받아 기술 스택·시스템 구조·데이터 모델·API 명세·디렉토리 구조 + 마이그레이션 계획을 결정. Design 코드를 진실의 원천으로 받음. SKILL.md §3의 6번 단계.
---

Architecture는 PRD + (UI 플랫폼이면) **Design 코드를 진실의 원천으로 받아** "어떻게 만들 것인가"의 구체적 결정을 내리는 단계다. 디자인 코드의 컴포넌트 트리·mock 데이터·API 호출 패턴이 data-model·API 명세 도출에 직접 입력되어 추측이 거의 없음. Claude Design 출력 스택(React+Babel CDN)과 타겟 스택이 다르면 마이그레이션 계획도 함께 수립.

## 1. 단계 목표

- **기술 스택**: 언어·프레임워크·DB·인프라·외부 서비스. 메인 플랫폼 + (있으면) 추가 platforms 모두 cover.
- **시스템 구조**: 모듈 경계·레이어·데이터 흐름.
- **데이터 모델**: 엔티티·관계·스키마. 별도 산출물(`data-model.md`)로 분리.
- **API 명세**: 외부 노출 인터페이스의 시그니처와 계약. 플랫폼 분기.
- **디렉토리 구조**: 코드를 어디에 둘 것인가의 골격.
- **마이그레이션 계획** (UI 플랫폼이고 디자인 스택 ≠ 타겟 스택): Design 코드를 타겟 스택으로 옮기는 전략. `migration-analysis.md` + `migration-plan.md`.

## 2. 진행 절차

### 2.1 사이클 분기

- 첫 사이클이고 `architecture.md` 비어있음: PRD + Design 코드(있으면) 다시 보여주고 인터뷰.
- 첫 사이클인데 이미 있음: 내용 읽고 §3 체크리스트 검증, 부족분만 보완.
- 두 번째 이상 사이클: 직전 architecture + retro 기반 업데이트. **§5 사이클 업데이트 모드**.

### 2.2 Design 코드 분석 (UI 플랫폼) — 진실의 원천 추출

Design 단계 통과한 UI 플랫폼이면 **먼저 디자인 코드부터 분석**. AI가 자동 추출:

- **컴포넌트 트리** → 모듈 경계·시스템 구조 추론
- **props·state·mock 데이터** → 엔티티·필드·관계 추출 (data-model 초안)
- **API 호출 패턴** (`fetch(...)`·`axios.get(...)`) → 엔드포인트 시그니처·요청/응답 형태 (API 명세 초안)
- **디자인 시스템 (컬러·타이포·간격)** → 디자인 토큰 코드 상수 후보
- **사용된 라이브러리/패턴** → 스택 결정 힌트 (React·SWR·Zustand 등)

추출 결과를 사용자에게 초안으로 보여주고 검토:

```
디자인 코드에서 자동 추출:
- 엔티티 [N]개: User, Contract, Clause, ...
- 관계: User 1─< Contract 1─< Clause
- 핵심 필드: User.email, Contract.text, Clause.severity, ...
- API 엔드포인트 [M]개: POST /api/contracts/check, GET /api/checklist, ...
- 디자인 토큰: 컬러 [k]개, 타이포 스케일 5단, 간격 8단

이거 base로 §2.3 스택 결정·§2.4 시스템 구조·§2.5 data-model 채울게. 빠진 거 있으면 알려줘.
```

비UI 플랫폼(cli·library·api-server)은 이 단계 skip — PRD만 base로 진행.

### 2.3 기술 스택 결정

PRD 외부 의존성 + (UI면) 디자인 코드의 패턴/라이브러리 힌트 base.

```
PRD 의존성 [목록] + 디자인 코드에서 [라이브러리·패턴]. 풀 스택 결정:

- 언어: 메인 플랫폼·platforms이 다 가능한 거?
- 프레임워크: 디자인 코드 그대로 갈래? 다른 거로?
- DB: 데이터 모델 복잡도·트랜잭션·검색 요구.
- 인프라/호스팅: 예산·규제·사용자 지역.
- 외부 서비스: 인증·결제·이메일·알림·관측성.
```

**플랫폼별 표준 후보** (모르겠다 답에 후보 제시용):
- **web**: Next.js·Remix·SvelteKit·Vite+React / Postgres·Supabase / Vercel·Netlify·AWS
- **mobile**: Swift+SwiftUI / Kotlin+Compose / Flutter / React Native — `cross_platform_framework` 우선
- **cli**: Go·Rust·Python / 패키징(Homebrew·npm·brew·apt)
- **library**: 호스트 언어 native 빌드 시스템 / SemVer 정책
- **desktop**: Tauri·Electron·네이티브(Swift/Kotlin/.NET)
- **api-server**: Node+Fastify / Python+FastAPI / Go+Echo / Postgres+Redis

**Cross-platform 케이스**: 메인 + 추가 platforms 모두 cover하는 스택 단일/조합 결정. 트레이드오프(코드 공유율·플랫폼별 native 느낌·개발 속도) 짚어주기.

각 결정에 **선택 이유**와 **대안** 한 줄 메모 강제.

### 2.4 마이그레이션 분석·계획 (UI 플랫폼 한정)

Claude Design 출력은 **React + Babel CDN inline**(빌드 도구 없이 동작). §2.3에서 결정한 타겟 스택과 비교 후 `design/migration-analysis.md` 작성.

- **타겟 스택이 React 계열** (Next.js·Vite+React·CRA): 컴포넌트 거의 그대로. 빌드 환경 도입(Vite/Next)만 필요. 마이그 공수 작음.
- **다른 JS 프레임워크** (Vue·Svelte·Solid): JSX → SFC 변환. 디자인 시스템(컬러·타이포·간격)은 그대로 이식. 공수 중간.
- **Flutter·React Native·native**: JSX 컴포넌트 트리 → 해당 플랫폼 위젯 매핑. 디자인 토큰만 직접 이식. 공수 큼.
- **백엔드 연동 부재**: Claude Design은 mock 데이터로 동작. 실제 API 연동은 빌드 단계의 별도 phase.

마이그레이션 필요 시 `design/migration-plan.md` 작성 — 4 항목:

1. **디자인 토큰 추출**: 컬러·타이포·간격을 스택 무관 코드 상수로.
2. **컴포넌트 매핑 표**: Claude Design 컴포넌트 → 타겟 스택 컴포넌트.
3. **화면 단위 우선순위**: 핵심 시나리오의 화면부터.
4. **백엔드 연동 분리**: mock → 실제 API 교체는 별도 phase.

이게 7단계 Build plan의 phase 0(셋업·마이그레이션)의 1차 입력이 됨.

### 2.5 시스템 구조

```
- 레이어: presentation / domain / data 같은 분리. 또는 단순 단층(소형 프로젝트).
- 모듈 경계: 어디서 어디까지 한 모듈? (기능 단위 / 플랫폼 단위 / 레이어 단위)
- 데이터 흐름: 사용자 입력 → 처리 → 저장 → 응답까지 핵심 경로 1~2개.
- Cross-platform이면: 공통 코어 vs 플랫폼별 어댑터 경계.
```

UI 플랫폼이면 디자인 코드 컴포넌트 트리 base로 추출. 소형 프로토타입은 과한 레이어링 금지.

### 2.6 데이터 모델

별도 산출물 `data-model.md`. UI 플랫폼이면 §2.2 추출 결과 base + 보완. 비UI는 PRD base로.

```
- 엔티티: 핵심 객체들 (디자인 mock 데이터에서 자동 추출 또는 PRD base)
- 관계: 1:1·1:N·N:M.
- 스키마: 각 엔티티의 필드·타입·제약(NOT NULL·UNIQUE·FK).
- 인덱스: 자주 검색·조인되는 필드.
- 파생 데이터·집계: 캐시 vs 즉시 계산.
```

DB 없는 케이스(library·일부 cli)는 메모리 데이터 구조(클래스·dataclass·struct)로 대체.

### 2.7 API 명세 — 플랫폼 분기

API 형태가 플랫폼마다 다름. UI 플랫폼이면 §2.2 추출 결과 base.

- **api-server**: HTTP 엔드포인트 시그니처. 메서드·경로·요청·응답·에러 코드·인증.
- **library**: 외부 노출 함수·클래스 시그니처. 파라미터·반환·예외·SemVer 영향.
- **cli**: 명령어·서브커맨드·플래그·인자·종료 코드.
- **web/mobile/desktop**: 백엔드와 통신하는 API + 내부 컴포넌트 인터페이스.
- **Cross-platform**: 공통 코어가 노출하는 인터페이스.

PRD §2.4 Must 기능과 1:1 매핑이 이상적.

### 2.8 디렉토리 구조

플랫폼·프레임워크별 표준 패턴 + 모듈 경계 + (UI면) 디자인 컴포넌트 트리 반영.

```
- 표준 패턴 우선 (Next.js app router, Flutter lib/features/, FastAPI routers/).
- 모듈 경계 features/ 또는 modules/ 그룹.
- Cross-platform: shared/ + platforms/{ios,android,web}/.
- 테스트 디렉토리: 코드 옆 또는 tests/ 분리.
```

2~3 depth까지만. 빌드 단계에서 더 구체화.

### 2.9 횡단 룰·표준 입력 — 매 cycle 적용

기술 스택·시스템 구조 결정 시, 프로젝트의 **횡단 룰**(`.claude/rules/`)을 입력으로 받아 처음부터 반영. Claude Code가 매칭 파일 read 시 자동 로드되는 룰들이지만 architecture 단계에선 명시적으로 짚고 결정에 반영:

- **인증·OAuth 패턴** → `.claude/rules/kakao-auth-share.md` (provider 결정·session 전략·adapter wrap 필요성·게이트 위치 등)
- **민감정보·환경 분기** → `.claude/rules/sensitive-data-exposure.md` (dev/preview/prod 분기 전략·로깅 정책)
- **페이지 인증 가드** → `.claude/rules/page-auth-pattern.md` (App Router server component 4단계 표준)
- **파일 업로드** → `.claude/rules/file-upload-security.md` (적용 시)
- **UI/UX baseline** → `.claude/rules/ui-ux-baseline.md` (UI 플랫폼이면 5-design.md에서 이미 입력됨)

architecture.md에서 위 룰들이 **어느 결정에 어떻게 반영됐는지** 한 줄씩 명시. cycle 진행 중 룰에 위배되는 결정이 필요하면 사유 + ADR 작성.

### 2.10 스택별 perf baseline 룰 자동 생성

스택 결정(§2.3) 직후 AI 자동 절차. SKILL.md §0.3.1 Layer 3 — 스택별 가이드는 스킬에 박지 않고 프로젝트 안에 stack-specific 룰로 분리.

**절차**:
1. AI가 결정된 스택(예: "Next.js 14 + Vercel + Supabase")의 공식 docs를 WebSearch + context7로 조사.
2. **`.claude/rules/perf-{stack}.md` 자동 생성** — 스택 공식 권장 + 플랫폼 표준 임계값(4-prd.md §2.5) 인용.
   - frontmatter `paths:`로 매칭 파일에서만 자동 로드 (예: web 스택 → `'src/**/*.{ts,tsx}'`).
   - 내용: `next/font` subset / `<Image>` 컴포넌트 / ISR `revalidate` / 번들 사이즈 가이드 등 스택별 high-signal 항목만.
3. 사용자에게 diff 보여주고 confirm. SKILL.md §0.3 "추가는 비용" 원칙 — 매 줄 "이걸 빼도 LLM이 실수할까?" 통과한 것만 유지.
4. 사이클 진행하며 retro로 보강 (Layer 4 — 프로젝트 특수 항목은 12-retro 누적).

**경계**:
- 스택 공식 docs 권장은 "공식 docs 권장" 검증 강도 (산업 표준 < 공식 docs < cycle 경험). 즉시 codify OK.
- 임계값 정량 한도(예: "First Load JS ≤ 200KB")는 cycle 측정 없이 박지 말 것 — 검증 안 된 임계값. retro 거쳐 codify.

### 2.11 누락 점검

PRD §2.2 패턴:

1. **핵심 결정 누락**: PRD Must 기능이 동작하려면 필요한데 안 결정된 기술/구조. 예: F1 "실시간 알림"인데 메시지큐·웹소켓·polling 안 결정.
2. **공통 누락**: 인증 흐름·로깅·에러 핸들링·환경변수·CI/CD·관측성·시크릿.

## 3. 완료 체크리스트

- [ ] **(UI 플랫폼) Design 코드 자동 추출 결과** 사용자 검토 완료.
- [ ] **기술 스택** 5개 카테고리(언어·프레임워크·DB·인프라·외부 서비스) 모두 결정. 각 항목에 대안·이유 한 줄.
- [ ] **(UI 플랫폼, 스택 ≠ React 계열) 마이그레이션 분석·계획** 작성됨.
- [ ] **스택별 perf baseline 룰** (§2.10) — `.claude/rules/perf-{stack}.md` 생성됨 또는 명시적 skip (이유 architecture.md에 한 줄).
- [ ] **시스템 구조** 모듈 경계·레이어·데이터 흐름 1~2개 명시.
- [ ] **데이터 모델** (`data-model.md`) 핵심 엔티티 모두 + 관계·스키마·인덱스.
- [ ] **API 명세** 플랫폼별 형식 + PRD Must 기능과 1:1 추적.
- [ ] **디렉토리 구조** 2~3 depth.
- [ ] **누락 점검 통과**: PRD Must 모두 cover + cross-cutting 인프라 결정.

## 4. 산출물 스펙

위치: `planning/cycles/v{N}-{label}/architecture.md` + `data-model.md` + (UI면) `design/migration-analysis.md`·`design/migration-plan.md`.

### 4.1 architecture.md

```markdown
---
platform: ...
platforms: [...]                    # cross-platform이면
cross_platform_framework: ...       # 사용 시
cycle: v1-prototype
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# 기술 스택
- 언어: TypeScript — 대안: JS, Dart. 이유: 팀 경험·타입 안정성.
- 프레임워크: Next.js 14 (App Router)
- DB: Postgres + Drizzle ORM
- 인프라: Vercel + Supabase
- 외부 서비스: Anthropic Claude API, Sentry

# 시스템 구조
- 레이어: ui / domain (use-cases) / data (repository)
- 모듈 경계: features/ 단위
- 데이터 흐름: [핵심 경로]

# API 명세
## 외부 (HTTP)
- POST /api/contracts/check
  - Body: { text: string }
  - Response 200: { missing_clauses: [...] }

## 내부 (컴포넌트 인터페이스)
- ContractMatcher.match(text, checklist) → MatchResult

# 디렉토리 구조
src/
├── app/
├── features/
└── ...

# 마이그레이션 (UI 플랫폼 + 스택 ≠ React 계열)
- 분석: design/migration-analysis.md
- 계획: design/migration-plan.md
```

### 4.2 data-model.md, migration-analysis.md, migration-plan.md

(이하 구조는 이전 4-architecture.md의 §4.2 + 5-design.md §3.5·§3.6 그대로)

## 5. 사이클 업데이트 모드 (v2 이상)

```
v1 회고 보니 [핵심 발견]였어. v2-mvp architecture 업데이트:

- 기술 스택: 어떤 항목 교체? 새 의존성 추가?
- 시스템 구조: 레이어·모듈 경계 재구성?
- 데이터 모델: 새 엔티티? 스키마 마이그레이션?
- API 명세: 새 엔드포인트? Breaking change?
- 디렉토리 구조: 모듈 분리/통합?
- (UI 플랫폼) 디자인 변경됐으면 마이그레이션 계획 갱신?
```

**원칙**:
- **스택 교체는 사유 명시 필수**. 예: "v1 Vercel → v2 자체 호스팅 (예산)".
- **DB 스키마 변경은 마이그레이션 전략과 묶어 기록**. v1 데이터 보존 전략.
- **Breaking API change는 v1 호환 정책 명시**.

## 6. 좋은 예 vs 나쁜 예

핵심 차이는 **구체 선택 + 대안 + 이유** vs **추상·일반론**.

- **기술 스택** — 좋은: "DB: Postgres 16 + Drizzle. 대안: Prisma. 이유: 타입 안전 + raw SQL escape hatch + 마이그레이션 도구 단순". / 나쁜: "적절한 DB와 ORM".
- **시스템 구조** — 좋은: "3-layer ui/domain/data, feature 단위 모듈, 핵심 흐름 명시". / 나쁜: "MVC 패턴".
- **데이터 모델** — 좋은: "User: id (uuid PK)·email (varchar 255 UNIQUE NOT NULL)·created_at. Index: email". / 나쁜: "사용자 테이블".

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. UI 플랫폼이면 §2.2 디자인 추출 → §2.3 스택 → §2.4 마이그레이션 → §2.5~2.8 차례로. 비UI면 §2.2·2.4 skip.
- **코칭**: SKILL.md §1.4대로. 사용자가 기술 결정 자신 없으면 플랫폼 표준 후보 2~3개 + 트레이드오프. 디자인 코드 추출 결과가 PRD와 충돌하면 5-design.md §3.5 기획 마감 결과 따름. 스택 변경 시 §1.4 마지막 항목으로 영향 범위 짚기. 모르는 부분은 `TBD: ...`.
