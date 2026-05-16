---
name: 8-automation-setup
description: Automation Setup 단계 가이드. 빌드 시작 전 프로젝트 환경(빌드 도구·CLAUDE.md·시크릿·테스트 인프라·CI/CD)을 자동 점검하고 셋업. CI/CD는 GitHub Actions 디폴트. SKILL.md §3의 8번 단계.
---

Automation Setup은 9번 Phase 빌드 시작 전 **프로젝트 자체의 작업 환경을 갖추는 단계**다. zero-to-proto 스킬과는 별개로, 이 프로젝트가 빌드되려면 필요한 도구·설정·CI를 점검·셋업한다.

**핵심 진행 방식**: AI가 단독으로 자동 점검 → 결과 보고 + 사용자 결정 항목 한 번에 제시 → AI가 셋업 실행. 사용자는 결정만.

## 1. 단계 목표

5가지 항목 점검·셋업.

- **빌드 도구**: Architecture 스택의 도구가 PATH에 있나 확인.
- **CLAUDE.md + `.claude/`**: 프로젝트별 코딩 컨벤션·도메인 지식·추가 스킬/hooks.
- **환경변수·시크릿**: Architecture 외부 의존성에 필요한 키가 셋업됐나.
- **테스트 인프라**: 단위 테스트 도구 설치·기본 설정.
- **CI/CD**: GitHub Actions 워크플로 초안 (이 스킬 디폴트).

## 2. 진행 절차

### 2.1 사이클 분기

- 첫 사이클이고 `automation-setup.md` 비어있음: 자동 점검 → 결과 보고 → 셋업 실행.
- 두 번째 이상 사이클: v1 셋업 그대로 + Architecture 변경분만 업데이트 (예: 새 의존성 추가됐으니 환경변수·시크릿 추가).

### 2.2 자동 점검 (AI 단독)

다음을 차례로 검증. 사용자 인터뷰 없이 AI 단독.

#### 2.2.1 빌드 도구 (Architecture 스택 의존)

플랫폼·스택별 점검 명령:

- **web/library/api-server (Node 계열)**: `node --version`, `npm --version` (또는 `pnpm`/`bun`/`yarn`).
- **mobile (Flutter)**: `flutter --version`, `dart --version`.
- **mobile (RN)**: `node --version`, RN CLI.
- **mobile (네이티브 iOS)**: `xcodebuild -version` (mac만).
- **mobile (네이티브 Android)**: `gradle --version` 또는 `./gradlew --version`.
- **cli/library (Go)**: `go version`.
- **cli/library (Rust)**: `cargo --version`, `rustc --version`.
- **api-server/library (Python)**: `python3 --version`, `uv --version` 또는 `poetry --version`.

각 결과를 `automation-setup.md`에 기록.

#### 2.2.2 CLAUDE.md + `.claude/`

- 프로젝트 루트 `CLAUDE.md` 존재? 내용에 (a) 프로젝트 도메인·intent 요약, (b) 코딩 컨벤션, (c) 핵심 의사결정 참조, (d) 사이클 정보가 있나?
- `.claude/skills/`에 프로젝트 특화 스킬 필요한지 점검 (보통 첫 사이클은 X — Architecture·Design이 다 결정돼서 추가 스킬 불필요).
- `.claude/hooks/`에 자동 검증 hook 필요한지 (예: 커밋 전 lint 자동 실행).

#### 2.2.3 환경변수·시크릿

`prd.md` 외부 의존성과 `architecture.md` 외부 서비스를 읽고:

- 각 의존성에 필요한 환경변수 키 추정 (예: `OPENAI_API_KEY`, `DATABASE_URL`, `STRIPE_SECRET_KEY`).
- 로컬 `.env` 파일 존재? 키들이 있나?
- `.env.example` 존재? (있어야 협업·CI에서 키 이름 알 수 있음.)
- `.gitignore`에 `.env` 포함됐나?

#### 2.2.4 테스트 인프라

플랫폼·스택별 점검:

- **web/library/api-server (Node)**: `package.json`의 `scripts.test`·`devDependencies`에 jest/vitest/playwright 등.
- **mobile (Flutter)**: `flutter test` 동작.
- **cli/library (Go)**: `go test ./...` 동작.
- **cli/library (Rust)**: `cargo test` 동작.
- **api-server/library (Python)**: pytest 또는 unittest 셋업.

#### 2.2.5 CI/CD (GitHub Actions 디폴트)

- 프로젝트가 git 저장소인가? GitHub remote 설정됐나?
- `.github/workflows/` 폴더 존재? 워크플로 파일 있나?
- 사용자에게 GitHub Secrets 셋업 안내 필요한지 판별 (시크릿 있는 경우만).

### 2.3 결과 보고 + 사용자 결정 항목

한 번에 정리해서 제시. 톤 SKILL.md §1.3대로.

```
환경 점검 끝났어. 결과:

✓ Node v20.10.0 / npm 10.2.4 (OK)
✓ git 저장소 (origin: github.com/user/dotoriroom)
✗ CLAUDE.md 비어있음 — 보강 필요
✗ OPENAI_API_KEY 환경변수 missing
✗ .env.example 없음
✗ .github/workflows/ 없음

결정해야 할 거:
1. CLAUDE.md 보강 (intent·컨벤션·핵심 결정 박기) → 자동 생성할까?
2. OPENAI_API_KEY:
   - 로컬: .env에 직접 입력 (네가 키 줘야 함)
   - CI: GitHub Secrets (네가 GitHub 가서 추가)
   - 안내 받을래?
3. CI/CD GitHub Actions 워크플로 어디까지?
   - 최소 (prototype): lint + typecheck + test
   - +: e2e 테스트, 빌드 산출물 업로드
   - +: 배포 (호스팅 결정 후)
```

사용자 답에 따라 §2.4 셋업 실행.

### 2.4 셋업 실행 (AI가 수행)

사용자 결정에 따라 다음 파일 생성·수정.

#### 2.4.1 CLAUDE.md (보강 또는 생성)

- intent.md 핵심 요약 (플랫폼·문제·타겟·성공 기준)
- Architecture 핵심 결정 (스택·구조·디렉토리)
- 코딩 컨벤션 (스택 표준 + 프로젝트 특수 규칙)
- 사이클 정보 (현재 v1-prototype 진행 중)
- 다음 줄 박기: "기획 컨텍스트는 `planning/cycles/v{N}-{label}/` 참조."

#### 2.4.2 시크릿·환경변수

- `.env` 생성 (사용자가 키 직접 입력하도록 placeholder 박음).
- `.env.example` 생성 (키 이름만 박힘, 커밋됨).
- `.gitignore`에 `.env`·`.env.local` 추가.
- GitHub Secrets는 사용자가 직접 GitHub UI에서 추가 (AI는 키 못 다룸). 안내만 제공.

#### 2.4.3 테스트 인프라

- 스택별 표준 테스트 도구 설치 명령 안내 (예: `npm install -D vitest`).
- 기본 설정 파일 생성 (예: `vitest.config.ts`).
- `package.json`에 `scripts.test` 추가.

#### 2.4.4 GitHub Actions 워크플로

`.github/workflows/ci.yml` 생성. 기본 구조:

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4    # 스택에 맞게 변경
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run typecheck

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
```

- **PR 단위 CI**: PR 생성·업데이트 시 lint·typecheck·test 모두 통과해야 머지 가능.
- **Phase 빌드 commit은 작업 브랜치에 누적** — 매 commit CI 안 돔. 작업 브랜치 → main PR 시점에 한 번 검증.
- **시크릿 사용 시**: `secrets.OPENAI_API_KEY` 같이 참조. GitHub Secrets에 사용자가 추가해야 동작 — 안내 포함.
- **사이클별 확장**: v2-mvp에 e2e job, v3-production에 보안 스캔·배포 job 추가.

**1인 개발 흐름** (workflow가 PR/push 두 트리거 다 지원하니 사용자 선택):
- **옵션 A — 빠름 모드**: 작업 브랜치 → main 직접 머지 (`git merge`). main push 시 CI 돔. 단점: CI 실패 시 main 깨짐 (`git revert`로 복구).
- **옵션 B — 안전 모드 (추천)**: 작업 브랜치 → `gh pr create` → CI 통과 확인 → self-merge. PR 만드는 단계 추가되지만 main 안전.

사용자가 모르겠다 답하면 B 디폴트로.

## 3. 완료 체크리스트

- [ ] **빌드 도구** 모두 PATH에 있음 또는 사용자에게 설치 안내됨.
- [ ] **CLAUDE.md** 보강·생성됨 (intent·컨벤션·핵심 결정 4섹션).
- [ ] **`.env` + `.env.example`** 생성됨, `.gitignore` 처리됨.
- [ ] **GitHub Secrets** 안내 제공됨 (필요 시).
- [ ] **테스트 인프라** 설정됨, `npm test` (또는 동등) 동작.
- [ ] **`.github/workflows/ci.yml`** 생성됨, 최소 lint·typecheck·test job.
- [ ] **`automation-setup.md`** 점검 결과·결정·변경된 파일 목록 기록됨.

## 4. 산출물 스펙

### 4.1 사이클 안 메타 — `automation-setup.md`

위치: `planning/cycles/v{N}-{label}/automation-setup.md`.

```markdown
---
cycle: v1-prototype
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# 점검 결과
- 빌드 도구: Node v20.10.0 (OK)
- CLAUDE.md: 빈 상태 → 보강 완료
- 환경변수: OPENAI_API_KEY missing → .env에 추가
- 테스트: vitest 설치 (신규)
- CI/CD: GitHub Actions ci.yml 생성

# 사용자 결정
- CLAUDE.md 자동 생성: OK
- 시크릿 — 로컬 .env + GitHub Secrets 조합
- CI 범위 — 최소 (lint·typecheck·test)

# 변경된 파일
- /CLAUDE.md (생성)
- /.env, /.env.example (생성)
- /.gitignore (수정)
- /vitest.config.ts (생성)
- /.github/workflows/ci.yml (생성)
- /package.json (devDependencies·scripts 수정)

# 사용자에게 남은 액션
- [ ] GitHub Secrets에 OPENAI_API_KEY 추가
- [ ] .env에 실제 OPENAI_API_KEY 값 입력
```

### 4.2 프로젝트 루트 파일들

`automation-setup.md`에 변경 내역 다 기록. 실제 파일은 프로젝트 루트에:

- `/CLAUDE.md`
- `/.env`, `/.env.example`
- `/.gitignore`
- `/.github/workflows/ci.yml`
- 스택별 테스트 설정 (`vitest.config.ts` 등)

## 5. 사이클 업데이트 모드 (v2 이상)

```
v1 셋업 그대로 받음. v2 변경분만:

- Architecture에서 새 의존성 [목록] 추가됨 → 환경변수·시크릿 추가 필요.
- v2 새 기능 [목록] 따라 테스트 도구 추가? (e2e: playwright 등)
- CI 워크플로 확장? (v2 = e2e job 추가, v3 = 배포 job 추가가 디폴트)
```

**원칙**: v1 인프라 파일(`CLAUDE.md`, `ci.yml`, `.env.example`) 직접 수정 — 단, 변경 사유 `automation-setup.md`에 기록. 프로젝트 루트에 `*.v1-backup` 같은 보존 X (git history가 그 역할).

## 6. 좋은 예 vs 나쁜 예

핵심 차이는 **구체값·자동 검증** vs **추상·일반론**.

- **점검 결과** — 좋은: "Node v20.10.0 OK, OPENAI_API_KEY missing". / 나쁜: "환경 OK".
- **CI 워크플로** — 좋은: lint·typecheck·test job 분리 + GitHub Secrets 참조. / 나쁜: 한 step에 다 묶음.
- **CLAUDE.md** — 좋은: intent 핵심·스택·컨벤션·사이클 정보 4섹션. / 나쁜: "프로젝트 설명".

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. 자동 점검 → 결과 한 번에 제시 → 사용자 결정만 받음.
- **코칭**: SKILL.md §1.4대로. 사용자가 시크릿 관리 방식 모르면 플랫폼 표준 후보 제시(로컬 `.env` + GitHub Secrets 조합이 디폴트). CI 범위 모르면 사이클별 표준 제시 (prototype: 최소 / mvp: + e2e / production: + 배포·보안). GitHub Secrets 추가는 AI가 못 함 — 사용자에게 명확한 단계 안내(GitHub repo → Settings → Secrets and variables → Actions → New).
