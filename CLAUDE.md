# Bsides

> AI가 만든 그럴듯한 초고 위에, 감성 한 스푼.

혼자가 가능해진 시대지만, 출시까지 같이 가는 **프로젝트 팀 빌딩·재능 품앗이 서비스**.
사이드 프로젝트 출시 의지 있는 직장인·디자이너·개발자·마케터·기획자가 대상. 한 사이클·한 멤버 1명 출시 + 객원 멤버 릴레이로 운영 (객원 참여 → 심사 → 약관 → 정식 멤버 4단계 전환).

## 프로젝트 모델 — 3 사이클

Bsides는 **prototype → MVP → production** 3 사이클로 서비스를 키운다. 각 사이클 = 13~15단계 워크플로우 1 loop (Intent · Brand · Sketch · PRD · Design · Architecture · Build · Test · Doc · Deploy · [Launch · PR/Marketing ·] Retro). 사이클 retro에서 게이트 판정으로 다음 사이클 진입 또는 피봇.

## Commands

```bash
npm run dev        # astro dev — 로컬 개발 서버
npm run build      # astro build — dist/ 정적 출력
npm run preview    # 빌드 결과 로컬 확인
npm run typecheck  # astro check — TS + content schema 검증
```

## AI Coding Discipline

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

    1. [Step] → verify: [check]
    2. [Step] → verify: [check]
    3. [Step] → verify: [check]

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

**Working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## 대화 스타일

- **반말**, 친구처럼 (공통).

### 단순 명령·확인일 때 (예: "ㄱㄱ", "ㅇㅋ", "다음 가자", "수정해줘")

- 결론 먼저, 짧게. 작업 후 한두 줄 보고로 끝. 표·비유 불필요.

### 설명·결정·이해 요청일 때 (예: "왜?", "이게 뭐야?", "이해 안 가", "검토해줘", 새 개념 도입)

**중학생 모드 + 비전공자 친화 — 다음 패턴 모두 적용**:

1. **한 줄 요약**으로 시작.
2. **비유 1~2개** — 일상 사례에 빗대 (검문소·옷가게·회원제 등).
3. **실제 시나리오** — 공격 사례·코드 흐름·실제 출력 등 구체 예시.
4. **기술 용어 첫 등장 시 풀이** — `CSRF(Cross-Site Request Forgery — 위조 요청)` 식 한 번만.
5. **표 비교** — 옵션이 둘 이상일 때 (옵션 / 장단점 / 추천 / 이유).
6. **"왜"를 항상 설명** — 사실 나열 X. 트레이드오프·근거 포함.
7. **결정 요청 → 옵션 + 추천 + 이유 + 다음 액션**으로 마무리.

분량은 사용자가 한 번 읽고 판단 가능한 수준이면 됨. 짧으려고 핵심 빠뜨리지 말 것.

비즈니스 컨텍스트·아키텍처·디자인 결정은 `planning/cycles/<current>/` 하위 문서에 있어. 필요할 때 다음을 읽어:

- @planning/cycles/v1-prototype/intent.md — 제품 의도·타겟·성공 기준
- @planning/cycles/v1-prototype/architecture.md — 스택·시스템 결정·디렉토리
- @planning/cycles/v1-prototype/brand-guide.md — 컬러·voice·금지

토픽별 path-scoped 룰은 `.claude/rules/` 에 분리되어 있어 (해당 파일 작업 시 자동 로드):

- `design-system.md` — CSS 토큰, 클래스 추출, 인라인 정책, Astro Font 매칭
- `content-collections.md` — Markdown collections, Zod schema, frontmatter
- `deploy.md` — Vercel·GitHub·PR 머지·CI 워크플로 + Claude Code 훅 2종(no-auto-deploy·auto-wip-commit)
- `perf-astro.md` — Astro 6 perf baseline (Image·Font·Critical CSS)
- `claude-harness-tuning.md` — CLAUDE.md·rules·skills·agents 하네스 튜닝 표준 (Anthropic context engineering 흡수)
- `llm-limits.md` — LLM이 못 보는 영역(시각·UX·실사용 부수효과). 컴포넌트·페이지·디자인 작업 시 로드
- `threat-model.md` — 외부 도달 위협 모델(preview URL·공유 링크·봇). 인증·민감정보·업로드·API 영역 작업 시 로드

사이클 단계별 스킬 (`.claude/skills/` — invoke 시 lazy load):

- `zero-to-proto` — prototype 단계 (13단계, 아이디어 → 배포된 prototype). 첫 사이클 또는 신규 prototype-phase 사이클.
- `proto-to-mvp` — MVP 단계 (15단계 = 13 + Launch + PR/Marketing + Retro 위치 변경). prototype retro 이후 PMF 검증 단계.
- `mvp-to-production` — production 단계 (15단계, MVP와 같은 구조지만 scope가 scale·ops·multi-channel). MVP PMF 통과 후.

## 코딩 컨벤션

- **TypeScript strict**. Node 24, Astro 6.x.
- **컴포넌트**: 한 화면 = 한 `.astro` 페이지 (`src/pages/`) + 작은 컴포넌트 (`src/components/`).
- **콘텐츠 = Markdown collection** + Zod schema 검증 (`src/content.config.ts`).
- **API 엔드포인트 0개. 사용자 데이터 수집 0** — 카톡 외부 link만. localStorage(Notes 진도) 외 server-side 데이터 없음.

## brand voice

> "LLM이 만든 그럴듯한 초고 위에, 감성 한 스푼."

- 마케팅 클리셰 회피 — "혁신적인", "10x", "AI-powered" 등 (자세히는 brand-guide §10 금지 8가지).
- 친근·반말 OK, 멘토 톤보다 동료 톤.

## needs_review 게이트

다음 변경 시 사용자 승인 필수 — 자동 진행 X:

- 인증·권한·암호화 코드 신규/변경
- 외부 API 키·시크릿 신규 사용
- DB 스키마 변경 (Bsides에선 content collection Zod schema 변경 포함)
- 외부 API 호출 신규 추가 (특히 비용·사용자 데이터 외부 전송)
- 비결정성 의존 (타임존·시스템 시간·무작위 시드)
- sudo·root·OS 권한·파일시스템 외부 접근
- 외부 인프라 변경 (도메인·DNS·Vercel·GitHub secrets)
- **Claude Code 훅 변경 (`.claude/hooks/**`·`.claude/settings.json`)** — 자동 배포 차단·자동 WIP 커밋 동작에 영향. 현재 훅 2종(no-auto-deploy + auto-wip-commit) 상세는 `.claude/rules/deploy.md` §Claude Code 훅 2종.
