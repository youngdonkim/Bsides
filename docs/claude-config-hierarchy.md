# CLAUDE.md hierarchy — 사람용 레퍼런스

> Claude Code의 CLAUDE.md 로드 순서·위치별 범위·`@path` import·`CLAUDE.local.md` 사용법.
> LLM 룰은 `.claude/rules/claude-harness-tuning.md` §2 참조. 여긴 *사람이 셋업·디버깅* 할 때 보는 디테일.

## 위치별 범위

CLAUDE.md는 여러 위치에 둘 수 있고, **모두 concatenate되어 컨텍스트에 합쳐짐** (덮어쓰기 X). 같은 룰을 두 위치에 다르게 박으면 Claude가 충돌을 임의 선택.

| 위치 | 범위 | 로드 시점 | git 공유 |
|---|---|---|---|
| `~/.claude/CLAUDE.md` | **사용자 전역** — 내 모든 프로젝트 | 매 세션 풀 로드 (가장 먼저) | ❌ 내 머신만 |
| 프로젝트 루트 `./CLAUDE.md` (또는 `./.claude/CLAUDE.md`) | **프로젝트** — 팀 공유 | 매 세션 풀 로드 | ✅ git commit |
| 프로젝트 루트 `./CLAUDE.local.md` | **프로젝트, 개인용** | 매 세션 풀 로드 (`CLAUDE.md` 뒤에 append) | ❌ `.gitignore` 필수 |
| 하위 폴더 `<subdir>/CLAUDE.md` | **모노레포·서브프로젝트** | CWD 위쪽이면 launch 시, CWD 아래면 그 폴더 파일 read 시 on-demand | ✅ git commit |

## 로드 순서 (CWD가 `foo/bar/`일 때)

```
1. ~/.claude/CLAUDE.md        ← 사용자 전역, 가장 먼저
2. /CLAUDE.md                  ← root (있다면)
3. foo/CLAUDE.md
4. foo/bar/CLAUDE.md           ← CWD에 가장 가까움, 가장 나중
5. 각 단계에서 같은 폴더의 CLAUDE.local.md (해당 CLAUDE.md 뒤에 append)
```

→ 가장 가까운 위치가 **마지막에** 읽힘. 모순될 경우 Claude가 임의 선택 — 그래서 nested CLAUDE.md는 **상위와 모순되지 않게** 작성.

## `CLAUDE.local.md` 상세

- 항상 **프로젝트 루트** (`./CLAUDE.local.md`). subdirectory에 두면 동작하지만 권장 X.
- `.gitignore`에 `CLAUDE.local.md` 추가 필수 — 안 그러면 실수로 commit됨.
- **worktree별 분리**: 같은 repo의 여러 worktree에서 작업해도 `CLAUDE.local.md`는 worktree마다 별개. 공유 안 됨.
- worktree 간 공유 원하면 `~/.claude/<file>.md`에 두고 `CLAUDE.md`에서 `@~/.claude/<file>.md` import (이건 git에 들어가니 import 라인만 공유, 실제 파일은 내 home에).

## 영역별 다른 룰

nested CLAUDE.md 대신 **path-scoped rules**가 더 명확:

```yaml
# .claude/rules/frontend.md
---
paths: ['src/components/**/*']
---
# src/components/ 아래 파일 작업 시에만 자동 로드 — 영역 한정 분명함
```

nested CLAUDE.md는 "추가"되는 거지 "덮어쓰는" 게 아니라서 의도가 모호해짐.

## `@path` import 패턴

- `@path/to/file.md` 로 외부 파일 include. **단, import도 launch 시 풀 로드** → 컨텍스트 절약 X. **조직화 목적만**.
- 진짜 컨텍스트 절약은 `.claude/rules/` (path-scoped lazy load).
- worktree 간 개인 설정 공유 시 유용 (`@~/.claude/...`).

## 참고

- [Claude Code: Memory & CLAUDE.md](https://code.claude.com/docs/en/memory) — 공식
