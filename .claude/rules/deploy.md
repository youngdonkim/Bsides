---
name: deploy
description: Bsides 배포·CI·브랜치 워크플로 — Vercel 무료 티어, GitHub-Vercel 자동 배포, PR 머지 게이트.
paths:
  - '.github/workflows/**'
  - 'astro.config.mjs'
  - 'astro.config.ts'
  - 'vercel.json'
  - 'vercel.ts'
  - 'package.json'
---

# Deploy & branch workflow

## 자동 배포 금지

- **코드 수정 후 자동 deploy 금지**. 모든 배포는 사용자 명시 지시(예: "배포해", "deploy해") 후에만 진행.
- main 머지 시 Vercel GitHub integration이 자동 production deploy 트리거 — 즉 PR 머지 자체가 사용자의 명시적 배포 의사로 간주. 따라서 별도 `vercel --prod` CLI 호출은 대개 불필요.
- enforcement: `.claude/hooks/no-auto-deploy.sh` 가 `vercel --prod`·`vercel deploy`·`git push ... main` 명령을 PreToolUse(Bash) 단계에서 차단 (exit 2).
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
  - `chore/<topic>` · 잡일·문서·CI
  - `refactor/<topic>` · 리팩터
  - `content/<topic>` · 콘텐츠/카피 변경
- PR title: conventional commits 패턴 (`feat:`·`fix:`·`chore:`·`refactor:`·`content:`).
- CI 통과 후 머지. 머지 방식은 **merge commit** (history 보존).
- 머지 후 `--delete-branch` 로 원격 브랜치 정리. local도 `git branch -d`.

## CI

- `.github/workflows/ci.yml` — `pull_request → main` 과 `push → main` 두 트리거.
- Job 두 개:
  - **typecheck** (`npm run typecheck` = `astro check`)
  - **build** (`npm run build` = `astro build`)
- Node.js: **22** (Astro 5 engine requirement `>=22.12.0`). Vercel default는 24.x이지만 CI는 22로 정합.
- 두 job 모두 통과해야 PR mergeable.

## 환경 변수·시크릿

- v1엔 시크릿 **0개**. Vercel 대시보드·GitHub Secrets에 추가하지 않음.
- 새 시크릿·외부 API 호출이 생기면 `needs_review` 트리거.

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
