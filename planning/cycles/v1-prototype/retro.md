---
cycle: v1-prototype
created_at: 2026-05-14
status: confirmed
---

# 핵심 발견 (한두 줄)

1. **prototype 정의를 "출시(deploy)까지" 한정으로 재정의 — operational 검증(워크샵·멤버쉽)은 MVP 영역으로 분리.** 이 재정의 기준에선 v1-prototype은 **출시 완료**. 이전 정의(operational 메트릭 검증)에선 미달이지만, 재정의 후엔 적합.
2. **첫 prototype 사이클은 메타로 진행 중 — 운영자(현지) 자신의 도토리룸이 첫 멤버 사이드 프로젝트. Bsides 자체도 메타-prototype.** 정식 모집·외부 멤버는 v2-mvp부터.
3. **개발 워크플로우 자체에서 발견이 다수 — Bsides는 "method를 검증·실증하는 곳"이라 워크플로우 정리(rules·hooks·skills)도 v1의 정당한 산출물.** 즉흥 결정보다 codify가 future-self·미래 멤버에게 신뢰 자료.

# 가설 검증 결과

prototype 재정의 (출시까지) 기준으로 평가.

| 가설 | 상태 | 비고 |
|---|---|---|
| **H1 (릴레이 자생)**: 객원 → 정식 멤버 → 다음 사이클 주인공 전환 | **메타 실험 진행 중** | 운영자(현지)가 정식 멤버 + 첫 주인공. 현재 객원 디자이너 1명이 다음 사이클 주인공 후보로 진행 중. **외부 멤버 대상 본격 검증은 v2-mvp**. |
| **H2 (organic 유입 충분성)** | **v1 검증 대상 아님** (재정의 후 MVP 영역) | prototype 재정의로 operational 메트릭은 MVP 사이클로 이관. v2-mvp에서 본격 평가. |
| **H3 (사이클 → 출시)**: 사이클 내 멤버 사이드 프로젝트 출시 도달 | **✅ 진행 중·달성 경로 위** | 도토리룸이 첫 prototype 사이클로 진행. Bsides 자체도 메타-prototype 출시 완료. 운영자·디자이너 객원 협업으로 사이클 모델 작동 확인. |
| **새 가설 H4 (스킬 분리 가치)**: prototype·MVP·production을 각각 별 스킬로 분리하면 통합 스킬보다 단계별 코칭 정확도·context 효율 ↑ | **신규** | v2-mvp 사이클 진입 시 검증 |
| **새 가설 H5 (PM agent 멤버 가치)**: product-manager agent 멤버 전용 제공이 정식 멤버쉽 incentive로 작동 | **신규** | v2-mvp 사이클 RBAC + 멤버 모집 시 검증 |

# 성공 기준 vs 실제

prototype 재정의 (출시까지) 기준으로 평가. operational 메트릭은 MVP 영역으로 이관.

| 기준 | 상태 | 비고 |
|---|---|---|
| **사이트 빌드·deploy 완료** (prototype 핵심 산출물) | ✅ 완료 | bsides-one.vercel.app 운영 중 |
| **첫 prototype 사이클 실행** (메타) | ✅ 진행 중 | 도토리룸 + Bsides 자체 메타-prototype |
| **객원·정식 멤버 협업 모델 작동 검증** | ✅ 작동 중 | 운영자·디자이너 객원 1명 협업 진행 중 |
| **method (zero-to-prototype skill) 자기 적용** | ✅ 적용·정교화 중 | 도토리룸 진행하며 스킬 개선 누적 |
| 워크샵 6회 진행 / 멤버쉽 2명 확보 / 강의 콘텐츠 누적 | v2-mvp 영역 (이관) | operational 메트릭, prototype scope 외 |

→ **목표 이상 달성**. 4가지 prototype-scope 기준 모두 ✅. operational 메트릭은 정의 재조정으로 v2 이관.

# 잘된 점

1. **빌드 단계 자동화의 효율 — 9 phase 약 1시간 wall-clock.** 모든 phase 성공. needs_review 2회(분석 도구·인프라) 사용자 명시 승인. error·blocked·external 장애 0.
2. **사이트 콘텐츠와 운영 모델의 빠른 정합.** 초기 카피("LLM이 만든..."·"수업"·"객원→정식 멤버")가 사용자 친화 톤으로 다듬어짐 — v1 안에서 PR #7·#8로 빠르게 iterate.
3. **개발 워크플로우 자체의 codify** — CLAUDE.md slim, rules 분리, hooks(no-auto-deploy + auto-wip-commit), skill(next-task), claude-config-authoring 표준. 이건 단순 잡일이 아니라 **method를 자기 자신에 일관 적용**한 결과.
4. **사이클 중간 "사이클 자체"를 메타로 인식 (이 retro 작성 자체)** — 즉흥 결정 누적이 아니라 **공식 회고·다음 사이클 전환**으로 정리해 신뢰 결을 쌓음.

# 아쉬운 점

1. **prototype·MVP·production 경계 모호** — 13단계 노트에 출시·홍보를 끼우려다 "이건 MVP 영역" 발견. 처음부터 zero-to-prototype 스킬 범위가 prototype 한정임을 명시했어야. (이 발견은 v2 진입의 자연 트리거가 됨)
2. **needs_review 게이트 항목 중 "배포"가 훅 enforcement와 중복 — 한참 지나서 발견·제거.** CLAUDE.md slim 원칙을 룰 자체에 더 일찍 적용했어야.
3. **squash merge policy vs 스킬 detection 불일치** — `git branch --merged`가 squash 못 잡는 gap을 first invoke 시점에야 발견. 스킬 설계 시 GitHub merge style 가정 명시했어야.
4. **auto-wip-commit 메시지 multi-byte 컷 이슈** — `cut -c1-60`이 UTF-8 경계에서 글자 깨짐. 기능 자체엔 무영향이나 가독성 ↓.
5. **첫 PM agent 사용 시점이 v1 후반에야 명확화** — Notes index 페이지에서 "어떤 도구로 가나" 질문이 첫 표면화. 초기 intent부터 PM agent 노출 모델 정해두었으면 카피·구조가 한 번에 잡혔을 것.

# 발견 사항 — 룰화 판정 (§2.3.1 분류)

| # | 내용 | 분류 | 처리 |
|---|---|---|---|
| 1 | Vercel auto-deploy + 명령어 차단 필요 | 룰화 (완료) | `no-auto-deploy.sh` hook + `.claude/rules/deploy.md` 정책. PR #3·#4 |
| 2 | 작업 손실 방지 자동 wip 커밋 패턴 | 룰화 (완료) | `auto-wip-commit.sh` hook. PR #4 |
| 3 | PR 직전 wip 흡수 표준 | 룰화 (완료) | `.claude/rules/deploy.md` PR 워크플로 섹션 + 메모리 `feedback_pr_cleanup_wip.md`. PR #6 |
| 4 | CLAUDE.md·rules·skills 작성 표준 부재 | 룰화 (완료) | `.claude/rules/claude-config-authoring.md` 신규. Anthropic context engineering 흡수. PR #4 |
| 5 | next-task 자동화 (post-merge 브랜치 전환) | 룰화 (완료) | `.claude/skills/next-task/` 신규. PR #5 |
| 6 | 머지 정책(squash) ↔ 스킬 detection 정합 | 룰화 (완료) | `next-task` SKILL.md PR status 기반 detection로 수정. PR #6 |
| 7 | rules는 LLM context — 인간 가독성보다 토큰·신호 효율 | 룰화 (완료) | 메모리 `feedback_rules_llm_context.md` |
| 8 | needs_review 항목 중 hook enforcement된 것 제거 | 룰화 (완료) | CLAUDE.md "배포" 항목 제거. PR #4 |
| 9 | Brand essence "LLM" 표현이 일반 사용자엔 너무 tech | spot fix | "AI"로 일괄 수정. PR #7 |
| 10 | "수업"이라는 카드 제목이 워크샵 모델로 오해 | spot fix | "사이드 프로젝트 진행"으로 수정. PR #7 |
| 11 | "다음 워크샵 일정 안내"가 사이클 모델과 불일치 | spot fix | "다음 사이클 일정 안내". PR #7 |
| 12 | Notes index에 method overview 부재 (도구·티어·범위 첫 스캔에 안 보임) | spot fix | Method 섹션 추가. PR #8 |
| 13 | 13단계 노트에 출시·홍보 끼우려다 MVP 영역 발견 | 코멘트 | retro 아쉬운 점 §1·§5 → 다음 사이클 입력으로 흡수 (스킬 분리) |
| 14 | auto-wip-commit 메시지 multi-byte 컷 깨짐 | spot fix | UTF-8 안전 컷으로 수정 (v2 작업) |
| 15 | LCP 측정 환경 한계(Rosetta) — prod PSI 재측정 보류 | 코멘트 | phase 7 review_summary에 기록됨. v2-mvp에서 prod 환경 PSI 재측정 |

→ **룰화 8건** (모두 완료) · **spot fix 5건** (모두 완료 또는 다음 사이클 처리) · **코멘트 2건**.

룰 인플레이션 경계 확인: 룰화 8건 모두 **재발 위험 + 횡단 가치** 둘 다 통과. 모두 path-scoped 또는 매 세션 핵심 룰.

# AI 자동화 실패 지점

| 지표 | 측정값 |
|---|---|
| 빌드 phase 수 | 9개 (phase 0~8) |
| 빌드 phase 성공률 | 9/9 (100%) |
| needs_review 발생 phase | 2개 (phase 7 외부 API 신규, phase 8 외부 인프라 첫 연결) |
| error 발생 | 0 |
| blocked 발생 | 0 |
| 외부 장애([external]) | 0 |
| 빌드 wall-clock | 약 56분 (20:58 ~ 21:54) |
| 사용자 명시 승인 (needs_review 해제) | 2회 (모두 승인) |

→ **AI 자동화 측면에서 v1은 매우 견고.** 사이트 자체 빌드는 문제 0. 발견은 빌드 후 **운영·메타 워크플로우 영역**에 집중.

# 다음 사이클 입력 — v2-mvp

## Intent

- **문제 정의**: v1과 **유지** — "솔로 메이커 동료 커뮤니티 부재". 단, scope 변경:
  - v1: 사이트 빌드 (사이트가 객원 모집 funnel 작동 가능 상태)
  - v2-mvp: **실 운영 — 객원 신청·심사·정식 멤버 승격·RBAC·워크샵 진행**
- **타겟 사용자**: **유지** (사이드 프로젝트 지망 직장인·디자이너·개발자·마케터·기획자)
- **성공 기준**: v1 운영 지표를 v2-mvp 본격 검증
  - 워크샵 6회 진행 → v2 내 측정
  - 멤버쉽 2명 확보 → v2 내 측정
  - 멤버 1명 실서비스 출시 도달 (도토리룸) → v2 내 측정 또는 별도 추적
  - 워크샵 6회분 콘텐츠 누적 → v2 내 측정
- **새 핵심 가설** (v2 발견):
  - **H4 (스킬 분리 가치)**: prototype·MVP·production을 각각 별 스킬로 분리하면, 단계별 코칭 정확도·context 효율이 통합 스킬보다 높다.
  - **H5 (PM agent 멤버 가치)**: product-manager agent 멤버 전용 제공이 정식 멤버쉽 신청 incentive로 작동한다.

## PRD

- **새 Must**:
  - 객원 멤버 신청·심사·정식 멤버 승격 프로세스 (현재 카톡 외 자동화 X — v2에 시스템화)
  - RBAC (객원 / 정식 멤버 권한 차이)
  - 정식 멤버 전용 콘텐츠·페이지 (PM agent 안내·다음 단계 가이드)
  - 인증 시스템 (OAuth — 카카오 또는 다른 provider)
  - 멤버 DB (또는 외부 서비스 — Clerk·Supabase 등)
  - 워크샵 진행 산출물 누적 (`/progress/` 트랙은 v1에 있음 — 운영하며 채움)
- **새 비기능**:
  - 인증 보안 (CSRF·세션 관리·토큰 회전)
  - 데이터 보호 (멤버 PII — 가입 시 동의·운영 정책)
  - 분석 강화 (signup funnel·retention·신청 conversion)

## Architecture

- **새 의존성**:
  - 인증 provider — 카카오 OAuth 우선 (브랜드 정합 + 한국 사용자 친화)
  - DB — 마켓플레이스 옵션 (Neon Postgres·Upstash Redis 등) 또는 Supabase 같은 BaaS
  - 미들웨어 — Routing Middleware 또는 Astro server endpoints
- **스택 결정 변경**:
  - SSG → SSG + 일부 SSR (인증·멤버 콘텐츠 처리)
  - "사용자 데이터 0" 정책 → v2엔 **명시적 정책 변경** (PII·세션 보관 시작)
  - Vercel adapter `output: 'static'` → `'server'` 또는 `'hybrid'` 검토
- **needs_review 트리거** 사전 식별:
  - 인증 코드 신규 (보안)
  - 멤버 DB 스키마 신규 (DB 스키마)
  - 외부 OAuth API 호출 신규 (외부 API)
  - 외부 인프라 변경 (DB·인증 provider 등)

## Design

- v1 디자인 **그대로 유지 + 멤버 콘텐츠 부분 신규 디자인**:
  - 로그인·회원가입 화면
  - 멤버 대시보드 (PM agent 안내·진행 상황·다음 단계)
  - 권한별 콘텐츠 분기 (객원이 멤버 콘텐츠 접근 시 "정식 멤버 되려면 →" CTA)
- brand-guide.md 톤은 유지 — 인증 화면도 sticky note·warm neutral 패턴 정합

## Skill 분리

- `zero-to-prototype` 기존 — 13단계 prototype 한정으로 재정의 (출시·홍보 단계 제거 확정)
- `prototype-to-mvp` **신규** — MVP 단계 (RBAC·인증·실 사용자 onboarding 등 포함)
- `mvp-to-production` **신규** — production 단계 (scale·SLA·인시던트 등)
- 공통 패턴은 shared references 또는 `claude-config-authoring.md` cross-cutting rule

## 작업 우선순위 (v2-mvp 사이클 진입 시)

1. 스킬 분리 (zero-to-prototype 재정의 + prototype-to-mvp 신규)
2. v2-mvp intent.md (이 retro의 "다음 사이클 입력" base)
3. v2-mvp prd.md (RBAC·인증·멤버 시스템 결정)
4. v2-mvp architecture.md (스택 변경·DB·인증 결정)
5. v2-mvp design (신규 멤버 화면)
6. v2-mvp build (실제 구현)

# 워크플로우 개선 제안 — 적용 상태

zero-to-prototype 스킬 자체 피드백 및 현재 적용 상태:

| # | 제안 | 적용 상태 | 처리 |
|---|---|---|---|
| 1 | 사이클 라벨에 prototype/MVP/production 명시화 | **v2-mvp 작업으로 흡수** | 스킬 자체를 3개로 분리 (zero-to-prototype + prototype-to-mvp + mvp-to-production). 분리 자체가 #1의 implement. |
| 2 | needs_review 게이트 항목 중 hook enforcement 중복 점검 | **일회성 정리 완료, 자동 mechanism 미구현** | "배포" 항목 CLAUDE.md에서 제거 (PR #4). 자동 감지 로직은 v2 검토. 현재는 사용자 인지 의존. |
| 3 | squash merge 가정 명시 | ✅ **적용 완료** | `.claude/rules/deploy.md` "Squash and merge" 정책 + 이유·트레이드오프·삭제 force 필요까지 명시. next-task 스킬도 PR status 기반 detection로 정합. |
| 4 | 메타 회고 시점 자동 트리거 | **v2 검토 (보류)** | "scope 외 작업 누적 → 스킬 분리·전환 알림" 자동화 가치 있음. 구현 비용 미평가. v2-mvp Architecture·Automation Setup 단계에서 결정. |

→ 4개 중 1·3 적용, 2·4는 v2 작업으로 이관.

# 사이클 종료 처리

- [x] 사용자 retro 확정 (2026-05-14)
- [ ] git tag `v1-prototype` 생성 (선택)
- [ ] v2-mvp 사이클 폴더 생성 + intent.md 작성 시작

# 운영 상태 메모

- 운영자(현지) = 정식 멤버 + 첫 prototype 사이클 주인공 (도토리룸)
- 디자이너 1명 = 객원 멤버 (현재 진행 중, 다음 사이클 주인공 후보)
- Bsides 자체 = 메타-prototype (도토리룸 진행하며 스킬·룰 정교화 동행)
- v2-mvp 진입 시 외부 객원 모집·RBAC·심사 프로세스 시작
