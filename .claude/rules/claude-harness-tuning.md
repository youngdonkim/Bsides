---
name: claude-harness-tuning
description: Bsides Claude Code 하네스 튜닝 표준 — CLAUDE.md·.claude/rules/·.claude/skills/·.claude/agents/ 어느 파일에 무엇을 어떻게 넣을지 결정 기준. Anthropic 공식 docs + context engineering 원칙 흡수.
paths:
  - "CLAUDE.md"
  - "CLAUDE.local.md"
  - ".claude/CLAUDE.md"
  - ".claude/rules/**/*.md"
  - ".claude/skills/**/*.md"
  - ".claude/skills/**/SKILL.md"
  - ".claude/agents/**/*.md"
  - ".claude/settings.json"
---

# Claude Code 하네스 튜닝 표준

## 0. 결정 표 — 어디에 넣을지

| 종류                                 | 위치          | 로드 시점                                                    | 적합한 내용                                                                                               | 부적합한 내용                                            |
| ------------------------------------ | ------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **CLAUDE.md**                        | 프로젝트 루트 | 매 세션 시작 시 **전체 로드**                                | 매 세션 필수 — 빌드 명령·핵심 컨벤션·금지 사항·"항상 X" 룰                                                | 특정 영역에서만 쓰는 룰·긴 절차·도메인 디테일            |
| **`.claude/rules/<topic>.md`**       | 프로젝트      | `paths` 매칭 파일 read 시 (lazy) 또는 매 세션 (paths 없으면) | 특정 영역(스택·테스트·보안 등) 룰 — 해당 파일 작업 시에만 필요                                            | 매 세션 필요한 룰 → CLAUDE.md / 다단계 절차 → skill      |
| **`.claude/skills/<name>/SKILL.md`** | 프로젝트      | invoke 시점 (Claude 자동 또는 `/<name>`)                     | 다단계 절차·작업·체크리스트·invoke 가능한 task                                                            | 매 세션 적용 룰 → CLAUDE.md                              |
| **`.claude/agents/<name>.md`**       | 프로젝트      | delegate 매칭 또는 명시 호출 시점 (별도 컨텍스트 윈도우)     | 단일 책임 task를 별도 컨텍스트에서 처리 — 검색·리뷰·디버그 등 main 대화를 floods 안 시키고 summary만 받기 | 매 세션 적용 룰 → CLAUDE.md / 다단계 사용자 절차 → skill |

**원칙**: 컨텍스트는 자원 — 자주 안 쓰는 내용은 lazy-load 위치에. CLAUDE.md는 **최후 수단**.

## 1. 공통 — context engineering 원칙

네 위치 모두 공통:

| 원칙                            | 의미                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| **High-signal tokens**          | 빼도 모르는 줄은 즉시 삭제. 토큰당 의사결정 영향력 최대화.   |
| **Lazy > Eager**                | 매 세션 vs 매칭 read vs invoke — 가능한 한 늦은 단계로 미룸. |
| **Specificity**                 | "코드 깨끗히" X / "API handler는 `src/api/` 아래" O          |
| **Single SoT**                  | 같은 룰이 두 파일에 있으면 충돌 위험 — 한 곳에서만.          |
| **No redundancy with LLM 상식** | LLM이 아는 표준 패턴은 박지 마.                              |

### 1.1 Codify 가치 판단 — 박을지 말지

LLM은 표준 지식 다 학습돼 있지만 **매번 결정 동일 X** (sampling·context 의존). codify 가치 = adherence + spec lock + grounding + audit trail. 다만 *redundancy with LLM 상식*은 noise.

**✅ codify 하는 케이스**:

| 케이스                              | 예                                                        |
| ----------------------------------- | --------------------------------------------------------- |
| 우리 프로젝트의 _수준_ 선택         | WCAG AA vs AAA, P95 응답 ≤ 1s                             |
| 표준 _수치_ lock                    | LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1                      |
| 표준끼리 충돌 시 우선순위·trade-off | a11y vs perf 충돌 시 a11y 우선                            |
| 비명백한 함정·gotcha                | preview = prod 노출, `git checkout <SHA>`는 detached HEAD |
| 우리 프로젝트만의 컨벤션            | branch 네이밍 `harness-md/<topic>`, squash merge 전용     |
| stage·환경별 강도 차이              | prototype 측정·기록만 / mvp 경고 / prod 강제 차단         |

**❌ codify 안 하는 케이스** (LLM 자율에 맡김):

| 케이스                                                         | 이유                          |
| -------------------------------------------------------------- | ----------------------------- |
| 표준 그대로 따르는 일반 룰 (HTTPS·UTF-8·HTML 시맨틱·camelCase) | LLM 100% 동일 적용. noise.    |
| 자명한 모범 사례 ("clean code 작성", "이름 의미 있게")         | 토큰 낭비                     |
| 자주 바뀌는 정보 (의존성 버전·날짜·인물명)                     | 룰 stale 위험 → ADR·README로  |
| 표준을 *그대로 적용*하고 세부는 LLM 해석 OK                    | 한 줄로 충분 ("WCAG AA 적용") |

**Frame shift**: codify = *수동적 기록*이 아니라 _프로젝트의 능동적 spec_. "LLM은 자격증 있는 의사, codify는 _우리 병원 진료 매뉴얼_" — 자명한 의학 지식은 매뉴얼에 안 적고, 우리 결정만 적는다.

### 1.2 LLM sampling 경계 — 반복 가능성

LLM은 _같은 입력에 다른 출력_ 가능 (temperature·sampling). 룰로 *결정의 경계*를 잡아 일관성 보장.

| 기법                      | 적용                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------- |
| **Output schema 명시**    | "JSON 응답: `{status: 'ok' \| 'fail', reason: string}`" 같이 구조 박기              |
| **Verification step**     | LLM이 만든 결과를 *다른 단계*에서 schema·테스트로 검증 (예: build·lint·typecheck)   |
| **Temperature/seed**      | 자동화 스크립트·재현 필요한 곳은 temperature 0 권장 (대화는 그대로 OK)              |
| **Idempotent operations** | 같은 작업 두 번 실행해도 결과 동일 (재시도 안전)                                    |
| **결정 명시**             | "후보 X·Y·Z 중 X 선택, 이유" 같이 _선택과 이유_ 함께 출력 → 다음 invoke가 같은 결정 |

### 1.3 외부 의존성 fallback

agent·skill이 외부 서비스(MCP·API·플러그인)에 의존할 때 fail 처리 명시:

- **Graceful degradation** — 외부 down 시 기본 동작은? (예: WebFetch 실패 시 사용자에게 알리고 캐시 결과 또는 수동 입력 요청)
- **Timeout·retry** — 명시. 무한 대기 금지.
- **명확한 에러 메시지** — "외부 서비스 X 도달 실패. fallback: Y" 식
- **사이드이펙트 없는 retry** — POST·결제 등은 idempotency key

### 1.4 비유·예시 정책 — LLM 룰엔 비유 기본 X

비유는 *사람*에게 정착되지만 LLM 추론엔 보통 추가 신호 X (학습된 패턴 매칭 우선). Anthropic prompt engineering 실험: **few-shot examples > 추상 비유**.

| 위치                                                 | 비유 정책                                 |
| ---------------------------------------------------- | ----------------------------------------- |
| `.claude/rules/`·`.claude/skills/` (LLM이 매번 읽음) | 기본 X. *frame shift 필요*한 경우만 한 줄 |
| `CLAUDE.md` voice·대화 톤                            | OK (사람도 읽음)                          |
| `planning/docs/`·`README.md` (사람용)                | 자유                                      |

**예시 선택 원칙**:

1. specific value — magic byte·timing·외울 수 없는 정량
2. non-standard pattern — LLM 직관과 어긋나는 흐름
3. 1~2줄 ❌/✅ 대조 — 흔한 함정과 정답

→ "Use examples, not analogies" — 명시적 ❌/✅ 짝이 비유보다 강한 신호.

### 1.5 Codify 시점 — 4 Layer × 사이클 단계

언제·어디서 codify할지 4 Layer로 매핑. 사이클 진행 중 또는 코드·디자인 작업 중 LLM이 자동 trigger 인지하도록.

| Layer            | 무엇                                          | codify 시점·위치                                                          | 절차                                    |
| ---------------- | --------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------- |
| **1. Universal** | 플랫폼·스택 무관 baseline (위협 모델·UX·a11y) | 스킬 작성 시점 — 스킬 references                                          | (사이클 전 박힘)                        |
| **2. Platform**  | web/mobile/cli 분기                           | 스킬 references 플랫폼 분기 질문 셋                                       | (스킬 안)                               |
| **3. Stack**     | Astro·Next·Flutter 등 stack 특화              | **6단계 Architecture 직후** — `.claude/rules/{kind}-{stack}.md` 자동 생성 | LLM이 공식 docs 조사·정리               |
| **4. Project**   | 우리 사이클에서 발견한 패턴                   | **retro 3분류 판정 통과 후** codify (또는 즉시 spot fix)                  | retro에서 룰화 / spot fix / 코멘트 분류 |

스킬은 Layer 1·2만 박고, 3·4는 프로젝트 안에 분리 — 스킬을 다른 프로젝트에 빌릴 때 1·2는 그대로 통하고 3·4는 그 프로젝트 환경에 맞게 새로 생성.

## 2. CLAUDE.md 작성 기준

### 2.1 핵심 룰 (공식 docs 직역)

- **분량 < 200줄 목표.** 길수록 어드히어런스(adherence) ↓. 안 따르기 시작하면 "파일이 비대해서 룰이 묻혔다"는 신호.
- **삭제 테스트**: 매 줄에 _"이 줄을 빼면 Claude가 실수할까?"_ — No면 즉시 삭제. (공식 best-practices)
- **구체 > 추상**: "코드 잘 작성" ❌ / "`npm test` 커밋 전 실행" ✅
- **충돌 룰 회피**. 두 룰 충돌 시 Claude가 임의 선택.

### 2.2 ✅ 넣을 것 vs ❌ 빼야 할 것

CLAUDE.md 한정 항목 (공통 codify ✅/❌는 §1.1 참조):

| ✅ Include                                     | ❌ Exclude                |
| ---------------------------------------------- | ------------------------- |
| Claude가 못 추론하는 Bash 명령 (커스텀 script) | 상세 API 문서 (링크만)    |
| 테스트 명령·선호 runner                        | 긴 설명·튜토리얼          |
| Repo 매너 (브랜치 네이밍·PR 컨벤션)            | 파일별 코드베이스 설명    |
| 개발 환경 quirk (필요 env var 등)              | 코드 읽으면 알 수 있는 것 |

### 2.3 강조 패턴

- `IMPORTANT` / `YOU MUST` emphasis → 어드히어런스 ↑. **남용 금지** (모든 게 IMPORTANT면 아무것도 IMPORTANT 아님).
- "Claude가 자꾸 룰 위배" = CLAUDE.md가 너무 길어 룰이 묻힘 → 가지 치기.

### 2.4 위치·hierarchy 핵심

- CLAUDE.md는 4 위치 (사용자 전역 / 프로젝트 / 프로젝트 개인 / 모노레포 서브) 모두 **concatenate** — 덮어쓰기 X.
- 영역별 다른 룰은 **nested CLAUDE.md 대신 path-scoped `.claude/rules/`** (의도 명확).
- `@path` import는 _조직화 목적만_ — launch 시 풀 로드라 컨텍스트 절약 X. 진짜 lazy는 `.claude/rules/` paths.
- 로드 순서·`CLAUDE.local.md` worktree 동작·conflict 처리 상세 → `docs/claude-config-hierarchy.md`.

### 2.5 변경 시 점검 ✅

- [ ] < 200줄?
- [ ] 매 줄 "빼도 Claude 실수할까?" 통과?
- [ ] 다른 곳(rules·skill)으로 옮길 수 있는 절차·도메인 정보 없나?
- [ ] 충돌·중복 없나? (특히 nested CLAUDE.md vs 상위 CLAUDE.md)
- [ ] 새 항목이 진짜 "매 세션 필요"한가? (No면 rules로)
- [ ] 개인용·로컬용이면 `CLAUDE.local.md`에 넣고 `.gitignore` 체크?

## 3. `.claude/rules/<topic>.md` 작성 기준

### 3.1 Frontmatter — 필수

```yaml
---
name: <topic>
description: <한 줄 — 룰의 범위와 적용 시점. 다른 세션에서 관련성 판단 근거가 됨>
paths:
  - "glob/pattern/**/*.ext"
  - "specific/file.json"
---
```

- **`name`**: 파일명과 동일(확장자 제외).
- **`description`**: 1~2줄. 룰이 다루는 것 + 언제 적용 명시. 짧고 구체적.
- **`paths`**: glob 패턴 list. **반드시 넣어라** — 없으면 매 세션 자동 로드 → 컨텍스트 낭비.

### 3.2 path-scoped vs 무조건 로드

| paths 필드 | 로드 시점                          | 권장                                               |
| ---------- | ---------------------------------- | -------------------------------------------------- |
| 있음       | 매칭 파일 read 시 (lazy)           | ✅ 기본                                            |
| 없음       | 매 세션 launch 시 (CLAUDE.md 동급) | ⚠️ 신중히 — "CLAUDE.md에 박는 게 낫지 않은가" 자문 |

### 3.3 Glob 패턴 가이드 (공식)

| 패턴                    | 매칭                    |
| ----------------------- | ----------------------- |
| `**/*.ts`               | 모든 디렉토리의 TS 파일 |
| `src/**/*`              | src/ 아래 전체          |
| `*.md`                  | 루트 markdown만         |
| `src/api/**/*.{ts,tsx}` | 확장자 alternation      |

**작성 균형**: 너무 좁으면 룰 매칭 놓침 / 너무 넓으면 노이즈. 의심되면 좁게 시작 → 사용하며 넓힘.

### 3.4 내용 작성

§1 (공통 원칙)과 §1.4 (비유·예시 정책) 그대로 적용. 핵심:

- 원칙·heuristics 먼저, 코드 예시는 default로 깔지 마.
- 표준 컨벤션·LLM이 이미 아는 패턴은 박지 마.
- 예시는 §1.4의 3 케이스 (specific value · non-standard pattern · ❌/✅ 대조)에만.

### 3.5 변경 시 점검 ✅

- [ ] frontmatter `name`·`description`·`paths` 셋 다 있나?
- [ ] `paths`가 충분히 좁아서 lazy load 효과 있나?
- [ ] description이 다른 세션에서 관련성 판단에 충분히 구체적?
- [ ] CLAUDE.md에 박는 게 더 맞는 내용 아닌가? (매 세션 필요 → CLAUDE.md)
- [ ] 다단계 절차 아닌가? (절차면 skill)

## 4. `.claude/skills/<name>/SKILL.md` 작성 기준

### 4.1 Frontmatter — 필수·선택

```yaml
---
name: <skill-name> # 소문자·숫자·하이픈, 64자 이하 (생략 시 디렉토리명)
description: <key use case 먼저, 그다음 트리거 단서>
when_to_use: <부가 트리거 문구> # 선택
disable-model-invocation: true # Claude 자동 호출 차단 (deploy·commit 등 부수효과)
user-invocable: false # `/` 메뉴 숨김 (백그라운드 지식)
allowed-tools: Read Grep Bash # invoke 시 권한 부여
paths: ["glob"] # 매칭 파일 작업 시에만 활성화
---
```

- **`description` 이 핵심** — Claude가 이 텍스트만 보고 자동 invoke 여부 결정.
- **`description` + `when_to_use` 합쳐 1,536자 cap** (공식). 초과 시 잘림 → key use case 먼저 박아라.
- 다른 필드는 선택.

### 4.2 분량 — SKILL.md < 500줄 (공식 권장)

- skill 본체는 invoke 후 **세션 끝까지 컨텍스트에 남음** (auto-compaction에서도 부분 유지: 최근 invoke 기준 5,000 tokens).
- 500줄 넘으면 supporting file (`references/*.md`) 로 분리.

### 4.3 Progressive disclosure (공식)

SKILL.md는 진입점·navigation. 상세 절차·예시는 `references/*.md`로 분리해서 lazy read. 실행 스크립트는 `scripts/` (Bash 호출).

### 4.4 invoke 패턴 결정 표

| 케이스                                                            | 설정                             |
| ----------------------------------------------------------------- | -------------------------------- |
| Claude 자동 + 사용자 수동 둘 다                                   | (default — 둘 다 가능)           |
| 부수효과 있는 워크플로 (deploy·send-message 등) — 사용자만 invoke | `disable-model-invocation: true` |
| 백그라운드 지식 (legacy system 설명 등) — Claude만 자동 사용      | `user-invocable: false`          |

### 4.5 동적 컨텍스트 주입 (공식)

skill 본문에 `` !`<command>` `` (인라인) 또는 fenced ` ```! ` 블록 → invoke 시점에 shell 실행 결과를 본문에 inline. Claude는 명령이 아닌 **결과**를 받음. 라이브 데이터 grounding (예: `!``git diff HEAD```).

### 4.6 변경 시 점검 ✅

- [ ] `description`에 key use case 먼저 박았나? (Claude 자동 invoke 판단 핵심)
- [ ] `description` + `when_to_use` 합쳐 < 1,536자?
- [ ] SKILL.md < 500줄? 초과 시 references/로 분리?
- [ ] 부수효과 있는 workflow면 `disable-model-invocation: true`?
- [ ] references/는 SKILL.md에서 link로 navigate 가능?
- [ ] CLAUDE.md·rules에 박는 게 더 맞는 내용 아닌가? (매 세션·매 파일 필요면 그쪽)

## 5. `.claude/agents/<name>.md` 작성 기준

서브에이전트는 별도 컨텍스트 윈도우에서 단일 책임 task를 처리한다. side task가 main 대화를 검색 결과·로그·파일 내용으로 flood할 때 위임 → **summary만 받음**. 또는 같은 worker를 반복 spawn할 때 정의.

### 5.1 위치·우선순위

| 위치                         | 범위                | git 공유  | 우선순위 |
| ---------------------------- | ------------------- | --------- | -------- |
| `.claude/agents/<name>.md`   | 프로젝트            | ✅ commit | 3 (기본) |
| `~/.claude/agents/<name>.md` | 사용자 전역         | ❌        | 4        |
| 플러그인 `agents/`           | plugin enabled 영역 | (plugin)  | 5        |

재귀 스캔 OK (`agents/review/security.md` 같은 nested 폴더). `name` 중복 금지 — 같은 scope에서 충돌 시 임의 1개 유지·경고 없음.

### 5.2 Frontmatter — 필수·선택

```yaml
---
name: <agent-name> # 필수. kebab-case. 파일명과 달라도 됨.
description: <delegate 트리거> # 필수. Claude가 이걸 보고 delegate 결정.
tools: Read, Grep, Glob # 선택. omit = 부모 conversation 도구 상속.
disallowedTools: Write, Edit # 선택. 상속 list에서 제거.
model: sonnet # 선택. sonnet/opus/haiku/inherit (default inherit).
maxTurns: 10 # 선택. agentic turn 상한 (Bash 등 부수효과 도구 시 권장).
skills: [name1] # 선택. 시작 시 preload (전체 내용 inject).
memory: project # 선택. user/project/local — 세션 간 학습.
isolation: worktree # 선택. 임시 git worktree에서 실행 (격리).
permissionMode: default # 선택. default/acceptEdits/plan 등.
color: blue # 선택. UI 색 (transcript·task list).
---
```

- 필수: `name`·`description`. 나머지 선택.
- 본문 (frontmatter 다음) = **system prompt**. agent는 이 prompt + 환경 메타(cwd 등)만 받음 — Claude Code 전체 시스템 프롬프트 X.

### 5.3 `description` — routing 핵심

Claude가 이 텍스트만 보고 delegate 여부 결정. skill `description`과 같은 원칙 (1,536자 cap, key use case 먼저). 추가:

- **"Use proactively after X" 패턴**이 자동 invoke trigger로 강함 (공식 권장).
- 부수효과·input/output 형태 명시.

### 5.4 도구 + 모델 — 최소 권한·cost 제어

| 케이스              | 설정                                        |
| ------------------- | ------------------------------------------- |
| Read-only 검색·분석 | `tools: Read, Grep, Glob` + `model: haiku`  |
| 코드 리뷰·분석      | `tools: Read, Grep, Glob` + `model: sonnet` |
| Write 강제 차단     | `disallowedTools: Write, Edit`              |
| Bash 등 부수효과    | 명시 allow + `maxTurns` 조이기              |
| 복잡 추론·아키텍처  | `model: opus`                               |

원칙: read-only agent면 Write·Edit 절대 X. 작은 모델 fit이면 _서브 task당_ 비용 큰 절감 (main이 opus여도 sub는 haiku 가능).

### 5.5 본문 + invoke

본문 = system prompt — **짧고 단일 책임**. role + task 절차 + 결과 형식. skill처럼 `references/`·`scripts/` 분리 X (skill 전용 패턴).

invoke 3 케이스:

1. Claude 자동 delegate — `description` 매칭 task 만났을 때
2. 사용자 자연어 — "Use the &lt;name&gt; agent to ..."
3. Agent tool 명시 — `Agent(subagent_type="<name>")`

### 5.6 변경 시 점검 ✅

- [ ] `name`·`description` 둘 다 있나?
- [ ] `description`이 routing trigger·input·output 명시?
- [ ] `tools` 최소 권한? (read-only면 Write·Edit 차단)
- [ ] `model`이 task 복잡도에 맞나? (단순 검색에 opus는 낭비)
- [ ] 본문 system prompt가 짧고 단일 책임?
- [ ] 부수효과 도구 있으면 `maxTurns` 박혔나?
- [ ] CLAUDE.md·rules·skill에 박는 게 더 맞지 않나? (절차 user-invoke = skill, 항시 룰 = rules)

## 6. 변경 트리거 — 이 룰을 다시 보는 시점

- CLAUDE.md / rules / skills / agents **새 파일 추가** 시 → 어디 넣을지 결정
- 기존 파일 **분량이 부풀** 때 → 분리·축약 판단
- "Claude가 자꾸 룰 위배" 신호 → CLAUDE.md 비대 검토
- 룰·skill·**agent**이 **동작 안 함** → description·paths·tools·model 점검
- 사이클 retrospective에서 **새 룰 codify 결정** → 어디에 박을지

## 7. needs_review 게이트와의 관계

이 룰들의 작성·수정 자체는 **needs_review 아님** — 코딩 표준이라 자유롭게 갱신. 단 다음은 게이트 발동:

- CLAUDE.md `needs_review` 항목 추가/제거 (정책 변경)
- skill·**agent**에 외부 명령·시크릿 호출 추가
- agent `permissionMode` 변경 (`bypassPermissions`·`auto` 등 권한 상승)
- 룰·skill·agent이 hooks 동작에 영향 (`.claude/hooks/**` 또는 `.claude/settings.json` 변경)
