---
name: deploy
description: Bsides 배포·CI·브랜치 워크플로 — Vercel 무료 티어, GitHub-Vercel 자동 배포, PR 머지 게이트, Claude Code 훅 2종.
paths:
  - '.github/workflows/**'
  - 'astro.config.mjs'
  - 'astro.config.ts'
  - 'vercel.json'
  - 'vercel.ts'
  - 'package.json'
  - '.claude/hooks/**'
  - '.claude/settings.json'
---

# Deploy & branch workflow

## 자동 배포 금지

- **코드 수정 후 자동 deploy 금지**. 모든 배포는 사용자 명시 지시(예: "배포해", "deploy해") 후에만 진행.
- main 머지 시 Vercel GitHub integration이 자동 production deploy 트리거 — 즉 PR 머지 자체가 사용자의 명시적 배포 의사로 간주. 따라서 별도 `vercel --prod` CLI 호출은 대개 불필요.
- enforcement: `.claude/hooks/no-auto-deploy.sh` 가 PreToolUse(Bash) 단계에서 차단 (exit 2). 자세히는 §훅 1.
- 통과시키려면 운영자가 직접 터미널에서 실행하거나, 사용자가 명시 요청 후 hook을 임시 우회.

## 인프라

- Vercel 무료 (Hobby) 티어, 기본 도메인 사용. 커스텀 도메인 없음.
- production URL: **https://bsides-one.vercel.app** (사용자 명시 alias)
  - Vercel 자동 생성 URL(`bsides-youngdonkims-projects.vercel.app`)은 Hobby plan deployment protection 기본 ON으로 401 응답.
  - 따라서 외부에 공유하는 주소는 항상 `bsides-one.vercel.app`.
- Vercel ↔ GitHub 연결됨 (`youngdonkim/Bsides`). main push → 자동 production deploy. PR push → preview URL 자동 생성 + PR 코멘트.

## 브랜치·PR 워크플로

- **main에 직접 push 금지**. 모든 변경은 PR을 거침.
- branch 네이밍:
  - `feat/<topic>` · 새 기능
  - `fix/<topic>` · 버그 수정
  - `chore/<topic>` · 잡일·CI 설정·deps
  - `refactor/<topic>` · 리팩터
  - `content/<topic>` · 콘텐츠/카피 변경 (`src/content/**`)
  - `docs/<topic>` · `docs/` 폴더 아래 **사용자·팀이 읽는 문서** 추가·수정 (README·가이드·튜토리얼)
  - `harness-md/<topic>` · `.claude/**`·`CLAUDE.md` 추가·수정·삭제 (Claude harness 컨텍스트 — skills·rules·hooks·settings·CLAUDE.md 본체). LLM이 읽는 파일이라 `docs/`와 별개 category.
- PR title: conventional commits 패턴 (`feat:`·`fix:`·`chore:`·`refactor:`·`content:`·`docs:`·`harness-md:`).
- **docs vs harness-md 판단**: 변경 대상이 **사람이 읽는 deliverable** (사용자 가이드 등)이면 `docs:`. **Claude/LLM이 읽고 작업하는 컨텍스트** (skills·rules·CLAUDE.md)면 `harness-md:`. 둘 다 markdown이지만 독자가 다름.
- **PR 직전 wip 커밋 흡수**: `auto-wip-commit.sh` 가 누적해놓은 `wip:` 커밋들은 push 전 의미 단위 commit으로 흡수. `git reset --soft origin/main` + 재커밋 패턴.
- CI 통과 후 머지. 머지 방식은 **Squash and merge** — PR의 모든 commit을 단일 commit으로 합쳐 main에 추가.
  - **이유**: main history 선형·간결 (PR 단위 1 commit). 우리는 PR 직전 wip 흡수 정책으로 이미 의미 단위 commit으로 정리하므로, squash가 자연스러운 다음 단계.
  - **트레이드오프**: feature branch의 개별 commit 보존 X (PR description에 남김). 필요 시 PR description에 commit 메시지·근거 상세 기록.
  - GitHub repo Settings → Pull Requests → "Squash and merge" 활성, 다른 옵션 비활성 권장.
- 머지 후 GitHub UI가 자동 remote 브랜치 삭제 (또는 `gh pr merge --squash --delete-branch`).
- **local 브랜치 삭제는 force 필요**: squash는 feature tip을 main의 ancestor로 만들지 않음 → `git branch -d` 거부됨. `git branch -D <name>` 로 강제 삭제. PR 머지 확인 후 안전.

## CI

- `.github/workflows/ci.yml` — `pull_request → main` 과 `push → main` 두 트리거.
- Job 두 개:
  - **typecheck** (`npm run typecheck` = `astro check`)
  - **build** (`npm run build` = `astro build`)
- Node.js: **22** (Astro 5 engine requirement `>=22.12.0`). Vercel default는 24.x이지만 CI는 22로 정합.
- 두 job 모두 통과해야 PR mergeable.

## 환경 변수·시크릿

- **환경 변수**: 코드 실행 시 외부에서 주입되는 값 (`.env`·Vercel 대시보드·GitHub Secrets).
- **시크릿**: 환경 변수 중 노출 금지인 것 — API 키·OAuth 비밀번호·서명 토큰 등.
- **v1 현황**: 시크릿 **0개**. Vercel 대시보드·GitHub Secrets 빈 상태. 코드 어디서도 `process.env.*` 호출 없음.
- **신규 시크릿·외부 API 호출 정책**: CLAUDE.md `needs_review` 게이트의 "외부 API 키·시크릿 신규 사용" 항목 적용 → 사용자 명시 승인 후 진행.
  - **자동 enforcement 아님** — Claude가 매 세션 CLAUDE.md 정책을 읽고 준수해야 함. 기술적 차단 훅 없음.
  - 향후 시크릿 도입 시 안전망 도구 검토: `gitleaks`·`secretlint` (pre-commit), CI 단계 패턴 스캔.

## 커스텀 도메인 (미래)

- `bsides.kr` 미구매 상태. 사면:
  1. Vercel 대시보드 → Settings → Domains → `bsides.kr` 추가
  2. 등록처 DNS: `A @ → 76.76.21.21`, `CNAME www → cname.vercel-dns.com`
  3. propagation 후 자동 HTTPS (Let's Encrypt).
- 도메인 추가는 외부 인프라 변경 — `needs_review` 트리거.

## 자주 발생하는 함정

- **`bsides.vercel.app` 잡으려고 시도하지 말기** — 이미 외부 사용자(브라질 개발자 Rafael Pereira)가 점유 중.
- Vercel에 사용자가 안 산 도메인 alias 등록되면 production URL이 그쪽으로 잡혀 사이트가 죽는 것처럼 보임. `vercel domains rm <domain>` 으로 정리.
- 첫 deploy 시 Vercel CLI가 `.vercel/project.json`을 자동 생성. `.gitignore` 에 `.vercel/`·`.vercel` 둘 다 박혀있는지 확인.

---

# Claude Code 훅 2종

`.claude/settings.json` 에 등록됨. 두 훅은 목적이 다르며 **공존**.

## 훅 1 — `no-auto-deploy.sh` (PreToolUse: Bash)

**목적**: PR 워크플로 우회 차단. Claude가 코드 수정 후 자동으로 production에 직행하는 경로 봉쇄.

### 차단 패턴

| 차단 대상 | 예시 |
|---|---|
| Vercel production deploy | `vercel --prod`, `vercel deploy`, `vercel --target production` |
| main 명시 push | `git push origin main`, `git push main:main` |
| main 체크아웃 상태의 모든 push | `git push` (현재 브랜치가 main일 때 — gap 봉쇄) |

### 통과 패턴

- feature branch에서의 `git push -u origin feat-xxx` 등 모든 push (✅ PR 워크플로 정상 동작)
- `git status`, `git log`, `git commit` 등 비-push git 명령
- `vercel logs`, `vercel env list` 등 비-deploy vercel 명령

### 동작 원리

1. PreToolUse(Bash)로 명령어 가로채기
2. shell separator (`&&`, `||`, `;`, `|`, `&`) 로 sub-command 분리
3. 각 sub-command의 첫 토큰이 `vercel`/`git`인 경우만 검사 (commit message 등 quote 텍스트 우연 매칭 회피)
4. 차단 패턴 매칭 시 exit 2 + stderr로 사유 출력 → Claude가 명령 실행 못 함

### 우회

운영자가 직접 터미널에서 실행. Claude를 통해 진행하려면 일시적으로 hook 비활성화.

## 훅 2 — `auto-wip-commit.sh` (Stop)

**목적**: Claude 응답 1턴 종료 시점에 변경된 파일을 자동 WIP 커밋. 작업 손실 방지.

**중요**: 커밋만 함. **push 안 함** — push는 항상 사용자 명시 지시 후에만.

### 작동 흐름

```
Claude 응답 종료
   ↓
Stop hook 발동 → auto-wip-commit.sh 실행
   ↓
[skip 조건 검사 5종]
   ↓
모두 통과 시 → git add -A → 변경 통계·파일 list 추출 → git commit
```

### Skip 조건 (안전 우선)

| # | 조건 | 이유 |
|---|---|---|
| 1 | 현재 브랜치 = `main` 또는 detached HEAD | main 오염 방지. WIP 커밋은 feature branch에만 |
| 2 | merge/rebase/cherry-pick 진행 중 (`.git/MERGE_HEAD` 등) | conflict marker가 wip 커밋에 섞이는 사고 방지 |
| 3 | 이미 staged 파일 존재 | 사용자 수동 부분 stage 등의 의도 보호 |
| 4 | working tree 변경 없음 | 빈 커밋 방지 |
| 5 | 시크릿 패턴 파일이 staging 대상 (`.env*`, `*.key`, `*.pem`, `secret`, `credentials.json`, `id_rsa`, `id_ed25519`) | `.gitignore` 불완전 시 마지막 안전망 |

Skip 시 exit 0 (Claude 정상 종료 허용) + stderr로 이유 로그.

### 커밋 메시지 포맷

```
wip: <last user msg 첫 60자> — <파일1>, <파일2>, <파일3> 외 N개 (변경통계)
```

예시:

```
wip: 헤더 컴포넌트에 sticky note accent 추가해줘 — Header.astro, brand.css, index.astro 외 1개 (4 files changed, 87 insertions(+), 12 deletions(-))
```

힌트가 추출 안 되면 (transcript 없음 등):

```
wip: Header.astro, brand.css, index.astro 외 1개 (4 files changed, 87 insertions(+), 12 deletions(-))
```

### 메시지의 user msg 힌트는 어떻게 뽑나?

Stop hook stdin으로 들어오는 `transcript_path` (JSONL)에서:
1. `type == "user"` 이면서 `content` 가 string인 마지막 entry 추출 (tool_result 제외)
2. `<system-reminder>...</system-reminder>` 블록 제거
3. 줄바꿈 → 공백, 연속 공백 정규화, 60자 컷

### 실패 모드

- `git commit` 실패 (pre-commit hook 등) → 로그만 남기고 exit 0. Claude는 정상 종료.
- transcript 읽기 실패 → 힌트 없는 메시지로 fallback.
- jq 없음 → 힌트 없는 메시지로 fallback.

### 의도적으로 안 하는 것

- ❌ push (이건 사람 결정)
- ❌ main 브랜치 커밋
- ❌ 시크릿 휩쓸이
- ❌ merge conflict 와중 커밋
- ❌ 사용자 staged 작업 휩쓸이

## 두 훅의 관계

| 단계 | 훅 | 역할 |
|---|---|---|
| 도구 호출 전 | `no-auto-deploy.sh` (PreToolUse:Bash) | 위험한 배포·main push 차단 |
| 응답 종료 시 | `auto-wip-commit.sh` (Stop) | 작업 자동 백업 (feature branch에 한해) |

전형적 흐름:
```
feature branch에서 작업
   ↓
Claude가 파일 편집 (Edit/Write tool)
   ↓
Claude 응답 종료
   ↓
auto-wip-commit.sh 발동 → wip 커밋 1개 생성
   ↓
... 여러 턴 반복 ...
   ↓
사용자: "이제 PR 올려" → Claude가 git push -u (no-auto-deploy 통과, feature branch이므로)
   ↓
사용자가 GitHub UI에서 PR 머지 → Vercel 자동 배포
```

## 변경 시 주의

훅 동작 변경은 사용자 명시 승인 필요 (CLAUDE.md `needs_review` 게이트). 이유:

- 자동 배포 차단을 풀면 사고 위험 증가
- 자동 커밋 동작을 바꾸면 git history 형태가 바뀜
- 시크릿 패턴 가드를 빼면 `.env` 노출 위험
