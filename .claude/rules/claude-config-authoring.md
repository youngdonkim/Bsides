---
name: claude-config-authoring
description: Bsides Claude Code 설정 작성 표준 — CLAUDE.md·.claude/rules/·.claude/skills/ 어느 파일에 무엇을 어떻게 넣을지 결정 기준. Anthropic 공식 docs + context engineering 원칙 흡수.
paths:
  - 'CLAUDE.md'
  - 'CLAUDE.local.md'
  - '.claude/CLAUDE.md'
  - '.claude/rules/**/*.md'
  - '.claude/skills/**/*.md'
  - '.claude/skills/**/SKILL.md'
  - '.claude/settings.json'
---

# Claude Code 설정 작성 표준

CLAUDE.md·`.claude/rules/`·`.claude/skills/` 는 모두 **매 세션 또는 매칭 파일 read 시 LLM 컨텍스트를 먹는 자원**이다. 어디에 무엇을 어떻게 넣을지 미리 표준을 박아둔다. 출처: Claude Code 공식 docs (code.claude.com/docs/en) + Anthropic context engineering.

## 0. 결정 표 — 어디에 넣을지

| 종류 | 위치 | 로드 시점 | 적합한 내용 | 부적합한 내용 |
|---|---|---|---|---|
| **CLAUDE.md** | 프로젝트 루트 | 매 세션 시작 시 **전체 로드** | 매 세션 필수 — 빌드 명령·핵심 컨벤션·금지 사항·"항상 X" 룰 | 특정 영역에서만 쓰는 룰·긴 절차·도메인 디테일 |
| **`.claude/rules/<topic>.md`** | 프로젝트 | `paths` 매칭 파일 read 시 (lazy) 또는 매 세션 (paths 없으면) | 특정 영역(스택·테스트·보안 등) 룰 — 해당 파일 작업 시에만 필요 | 매 세션 필요한 룰 → CLAUDE.md / 다단계 절차 → skill |
| **`.claude/skills/<name>/SKILL.md`** | 프로젝트 | invoke 시점 (Claude 자동 또는 `/<name>`) | 다단계 절차·작업·체크리스트·invoke 가능한 task | 매 세션 적용 룰 → CLAUDE.md |

**원칙**: 컨텍스트는 자원 — 자주 안 쓰는 내용은 lazy-load 위치에. CLAUDE.md는 **최후 수단**.

## 1. CLAUDE.md 작성 기준

### 1.1 핵심 룰 (공식 docs 직역)

- **분량 < 200줄 목표.** 길수록 어드히어런스(adherence) ↓. 안 따르기 시작하면 "파일이 비대해서 룰이 묻혔다"는 신호.
- **삭제 테스트**: 매 줄에 *"이 줄을 빼면 Claude가 실수할까?"* — No면 즉시 삭제. (공식 best-practices)
- **구체 > 추상**: "코드 잘 작성" ❌ / "`npm test` 커밋 전 실행" ✅
- **markdown 헤더·bullet 사용**. 덩어리 문단 X. Claude는 사람처럼 구조를 스캔함.
- **충돌 룰 회피**. 두 룰 충돌 시 Claude가 임의 선택.
- **표준 컨벤션 박지 마**. LLM이 이미 아는 패턴(예: "변수명은 camelCase") 박지 마. 토큰 낭비 + 진짜 룰 매몰.

### 1.2 ✅ 넣을 것 vs ❌ 빼야 할 것 (공식 표)

| ✅ Include | ❌ Exclude |
|---|---|
| Claude가 못 추론하는 Bash 명령 (커스텀 script) | 코드 읽으면 알 수 있는 것 |
| 기본값과 **다른** 코드 스타일 룰 | LLM이 아는 언어 표준 컨벤션 |
| 테스트 명령·선호 runner | 상세 API 문서 (링크만) |
| Repo 매너 (브랜치 네이밍·PR 컨벤션) | 자주 바뀌는 정보 |
| 프로젝트 특수 아키텍처 결정 | 긴 설명·튜토리얼 |
| 개발 환경 quirk (필요 env var 등) | 파일별 코드베이스 설명 |
| 비명백한 함정·gotcha | 자명한 룰 ("clean code 작성") |

### 1.3 강조 패턴

- `IMPORTANT` / `YOU MUST` emphasis → 어드히어런스 ↑. **남용 금지** (모든 게 IMPORTANT면 아무것도 IMPORTANT 아님).
- "Claude가 자꾸 룰 위배" = CLAUDE.md가 너무 길어 룰이 묻힘 → 가지 치기.

### 1.4 위치·hierarchy — concatenate, **not override**

CLAUDE.md는 여러 위치에 둘 수 있고, **모두 concatenate되어 컨텍스트에 합쳐짐** (덮어쓰기 X). 같은 룰을 두 위치에 다르게 박으면 Claude가 충돌을 임의 선택.

| 위치 | 범위 | 로드 시점 | git 공유 |
|---|---|---|---|
| `~/.claude/CLAUDE.md` | **사용자 전역** — 내 모든 프로젝트 | 매 세션 풀 로드 (가장 먼저) | ❌ 내 머신만 |
| 프로젝트 루트 `./CLAUDE.md` (또는 `./.claude/CLAUDE.md`) | **프로젝트** — 팀 공유 | 매 세션 풀 로드 | ✅ git commit |
| 프로젝트 루트 `./CLAUDE.local.md` | **프로젝트, 개인용** | 매 세션 풀 로드 (`CLAUDE.md` 뒤에 append) | ❌ `.gitignore` 필수 |
| 하위 폴더 `<subdir>/CLAUDE.md` | **모노레포·서브프로젝트** | CWD 위쪽이면 launch 시, CWD 아래면 그 폴더 파일 read 시 on-demand | ✅ git commit |

**로드 순서** (CWD가 `foo/bar/`일 때):
```
1. ~/.claude/CLAUDE.md        ← 사용자 전역, 가장 먼저
2. /CLAUDE.md                  ← root (있다면)
3. foo/CLAUDE.md
4. foo/bar/CLAUDE.md           ← CWD에 가장 가까움, 가장 나중
5. 각 단계에서 같은 폴더의 CLAUDE.local.md (해당 CLAUDE.md 뒤에 append)
```

→ 가장 가까운 위치가 **마지막에** 읽힘. 모순될 경우 Claude가 임의 선택 — 그래서 nested CLAUDE.md는 **상위와 모순되지 않게** 작성.

**`CLAUDE.local.md` 저장 위치 상세**:
- 항상 **프로젝트 루트** (`./CLAUDE.local.md`). subdirectory에 두면 동작하지만 권장 X.
- `.gitignore`에 `CLAUDE.local.md` 추가 필수 — 안 그러면 실수로 commit됨.
- **worktree별 분리**: 같은 repo의 여러 worktree에서 작업해도 `CLAUDE.local.md`는 worktree마다 별개. 공유 안 됨.
- worktree 간 공유 원하면 `~/.claude/<file>.md`에 두고 `CLAUDE.md`에서 `@~/.claude/<file>.md` import (이건 git에 들어가니 import 라인만 공유, 실제 파일은 내 home에).

**영역별 다른 룰을 원할 때** — nested CLAUDE.md 대신 **path-scoped rules**가 더 명확:
```yaml
# .claude/rules/frontend.md
---
paths: ['src/components/**/*']
---
# src/components/ 아래 파일 작업 시에만 자동 로드 — 영역 한정 분명함
```
nested CLAUDE.md는 "추가"되는 거지 "덮어쓰는" 게 아니라서 의도가 모호해짐.

### 1.5 Import (`@path`) 패턴

- `@path/to/file.md` 로 외부 파일 include. **단, import도 launch 시 풀 로드** → 컨텍스트 절약 X. **조직화 목적만**.
- 진짜 컨텍스트 절약은 `.claude/rules/` (path-scoped lazy load).
- worktree 간 개인 설정 공유 시 유용 (`@~/.claude/...`).

### 1.6 변경 시 점검 ✅

- [ ] < 200줄?
- [ ] 매 줄 "빼도 Claude 실수할까?" 통과?
- [ ] 다른 곳(rules·skill)으로 옮길 수 있는 절차·도메인 정보 없나?
- [ ] 충돌·중복 없나? (특히 nested CLAUDE.md vs 상위 CLAUDE.md)
- [ ] 새 항목이 진짜 "매 세션 필요"한가? (No면 rules로)
- [ ] 개인용·로컬용이면 `CLAUDE.local.md`에 넣고 `.gitignore` 체크?

## 2. `.claude/rules/<topic>.md` 작성 기준

### 2.1 Frontmatter — 필수

```yaml
---
name: <topic>
description: <한 줄 — 룰의 범위와 적용 시점. 다른 세션에서 관련성 판단 근거가 됨>
paths:
  - 'glob/pattern/**/*.ext'
  - 'specific/file.json'
---
```

- **`name`**: 파일명과 동일(확장자 제외).
- **`description`**: 1~2줄. 룰이 다루는 것 + 언제 적용 명시. 짧고 구체적.
- **`paths`**: glob 패턴 list. **반드시 넣어라** — 없으면 매 세션 자동 로드 → 컨텍스트 낭비.

### 2.2 path-scoped vs 무조건 로드

| paths 필드 | 로드 시점 | 권장 |
|---|---|---|
| 있음 | 매칭 파일 read 시 (lazy) | ✅ 기본 |
| 없음 | 매 세션 launch 시 (CLAUDE.md 동급) | ⚠️ 신중히 — "CLAUDE.md에 박는 게 낫지 않은가" 자문 |

### 2.3 Glob 패턴 가이드 (공식)

| 패턴 | 매칭 |
|---|---|
| `**/*.ts` | 모든 디렉토리의 TS 파일 |
| `src/**/*` | src/ 아래 전체 |
| `*.md` | 루트 markdown만 |
| `src/api/**/*.{ts,tsx}` | 확장자 alternation |

**작성 균형**: 너무 좁으면 룰 매칭 놓침 / 너무 넓으면 노이즈. 의심되면 좁게 시작 → 사용하며 넓힘.

### 2.4 내용 작성 — context engineering 원칙

Anthropic 공식 + zero-to-prototype skill §0.3 흡수:

- **원칙·heuristics 먼저, 코드 예시는 default로 깔지 마.**
- **"Find the smallest set of high-signal tokens"** — 매 줄 "이걸 빼도 LLM이 실수할까?" 통과해야 유지.
- **표준 컨벤션·LLM이 이미 아는 패턴은 박지 마.**
- **예시는 다음 3 케이스에만 사용**:
  1. **specific value** — magic byte hex, 타이밍, 외울 수 없는 정량
  2. **non-standard 패턴** — LLM 직관과 어긋나는 흐름
  3. **1~2줄 ❌/✅ 대조** — 흔한 함정과 정답

### 2.5 변경 시 점검 ✅

- [ ] frontmatter `name`·`description`·`paths` 셋 다 있나?
- [ ] `paths`가 충분히 좁아서 lazy load 효과 있나?
- [ ] description이 다른 세션에서 관련성 판단에 충분히 구체적?
- [ ] CLAUDE.md에 박는 게 더 맞는 내용 아닌가? (매 세션 필요 → CLAUDE.md)
- [ ] 다단계 절차 아닌가? (절차면 skill)

## 3. `.claude/skills/<name>/SKILL.md` 작성 기준

### 3.1 Frontmatter — 필수·선택

```yaml
---
name: <skill-name>                    # 소문자·숫자·하이픈, 64자 이하 (생략 시 디렉토리명)
description: <key use case 먼저, 그다음 트리거 단서>
when_to_use: <부가 트리거 문구>          # 선택
disable-model-invocation: true        # Claude 자동 호출 차단 (deploy·commit 등 부수효과)
user-invocable: false                 # `/` 메뉴 숨김 (백그라운드 지식)
allowed-tools: Read Grep Bash         # invoke 시 권한 부여
paths: ['glob']                       # 매칭 파일 작업 시에만 활성화
---
```

- **`description` 이 핵심** — Claude가 이 텍스트만 보고 자동 invoke 여부 결정.
- **`description` + `when_to_use` 합쳐 1,536자 cap** (공식). 초과 시 잘림 → key use case 먼저 박아라.
- 다른 필드는 선택.

### 3.2 분량 — SKILL.md < 500줄 (공식 권장)

- skill 본체는 invoke 후 **세션 끝까지 컨텍스트에 남음** (auto-compaction에서도 부분 유지: 최근 invoke 기준 5,000 tokens).
- 500줄 넘으면 supporting file (`references/*.md`) 로 분리.

### 3.3 Progressive disclosure 패턴 (공식)

```
my-skill/
├── SKILL.md          # 진입점 — 짧고 navigation 중심
├── references/       # 상세 가이드 — Claude가 필요 시 lazy read
│   ├── step-1.md
│   └── step-2.md
└── scripts/          # 실행 스크립트 — Bash로 호출
```

SKILL.md는 "어떤 references를 언제 읽어야 하는지" navigation 역할. 상세 절차는 `references/`에 분리해서 lazy read.

### 3.4 invoke 패턴 결정 표

| 케이스 | 설정 |
|---|---|
| Claude 자동 + 사용자 수동 둘 다 | (default — 둘 다 가능) |
| 부수효과 있는 워크플로 (deploy·send-message 등) — 사용자만 invoke | `disable-model-invocation: true` |
| 백그라운드 지식 (legacy system 설명 등) — Claude만 자동 사용 | `user-invocable: false` |

### 3.5 동적 컨텍스트 주입 (공식)

skill 본문에 `` !`<command>` `` 또는 fenced ` ```! ` 블록 → 호출 시점에 shell 실행 결과를 본문에 inline. 예:

```yaml
---
description: 현재 변경사항 요약
---
## 변경
!`git diff HEAD`
```

→ Claude는 명령이 아닌 **결과**를 받음. 라이브 데이터 grounding에 유용.

### 3.6 변경 시 점검 ✅

- [ ] `description`에 key use case 먼저 박았나? (Claude 자동 invoke 판단 핵심)
- [ ] `description` + `when_to_use` 합쳐 < 1,536자?
- [ ] SKILL.md < 500줄? 초과 시 references/로 분리?
- [ ] 부수효과 있는 workflow면 `disable-model-invocation: true`?
- [ ] references/는 SKILL.md에서 link로 navigate 가능?
- [ ] CLAUDE.md·rules에 박는 게 더 맞는 내용 아닌가? (매 세션·매 파일 필요면 그쪽)

## 4. 공통 — context engineering 원칙

세 위치 모두 공통:

| 원칙 | 의미 |
|---|---|
| **High-signal tokens** | 빼도 모르는 줄은 즉시 삭제. 토큰당 의사결정 영향력 최대화. |
| **Lazy > Eager** | 매 세션 vs 매칭 read vs invoke — 가능한 한 늦은 단계로 미룸. |
| **Specificity** | "코드 깨끗히" X / "API handler는 `src/api/` 아래" O |
| **Single SoT** | 같은 룰이 두 파일에 있으면 충돌 위험 — 한 곳에서만. |
| **No redundancy with LLM 상식** | LLM이 아는 표준 패턴은 박지 마. |

## 5. 변경 트리거 — 이 룰을 다시 보는 시점

- CLAUDE.md / rules / skills **새 파일 추가** 시 → 어디 넣을지 결정
- 기존 파일 **분량이 부풀** 때 → 분리·축약 판단
- "Claude가 자꾸 룰 위배" 신호 → CLAUDE.md 비대 검토
- 룰·skill이 **동작 안 함** → description·paths 점검
- 사이클 retrospective에서 **새 룰 codify 결정** → 어디에 박을지

## 6. needs_review 게이트와의 관계

이 룰들의 작성·수정 자체는 **needs_review 아님** — 코딩 표준이라 자유롭게 갱신. 단 다음은 게이트 발동:

- CLAUDE.md `needs_review` 항목 추가/제거 (정책 변경)
- skill에 외부 명령·시크릿 호출 추가
- 룰·skill이 hooks 동작에 영향 (`.claude/hooks/**` 또는 `.claude/settings.json` 변경)

## 7. 참고 자료

- [Claude Code: Memory & CLAUDE.md](https://code.claude.com/docs/en/memory) — 공식
- [Claude Code: Skills](https://code.claude.com/docs/en/skills) — 공식
- [Claude Code: Best Practices](https://code.claude.com/docs/en/best-practices) — 공식
- [Agent Skills 표준](https://agentskills.io) — 오픈 표준
- `.claude/skills/zero-to-prototype/SKILL.md` §0.3 — Anthropic context engineering 원칙 우리 흡수 버전
