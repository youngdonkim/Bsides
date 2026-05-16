---
name: 12-deploy
description: 배포 단계 가이드. 호스팅 결정·시크릿·도메인·모니터링·롤백 플랜을 정하고 배포 자동화(GitHub Actions deploy job)를 셋업·실행. SKILL.md §3의 12번 단계.
---

배포는 **빌드 결과를 실제 환경에 반영**하는 단계다. 도메인·사이클별 호스팅 옵션을 짚고, 시크릿·도메인 연결·모니터링·롤백 플랜까지 한 번에 정리. 첫 사이클은 빠르게(URL 받으면 끝), 이후 사이클은 운영 안전망 추가.

## 1. 단계 목표

- **호스팅 결정** + 배포 명령·자동화 셋업.
- **시크릿** GitHub Secrets에 등록 (사용자가 직접).
- **도메인** 연결 (옵션, prototype은 무료 서브도메인 OK).
- **모니터링** 셋업 (Sentry 등, mvp 이상 권장).
- **롤백 플랜** (production 필수).

## 2. 진행 절차

### 2.1 사이클 분기

- **prototype**: 호스팅 1곳 정해서 빠르게. URL 받으면 끝.
- **mvp**: + 모니터링·도메인·자동 배포 트리거.
- **production**: + 롤백·점진적 배포·데이터 백업·보안 점검.

### 2.2 호스팅 결정 — 플랫폼 분기

`intent.md` `platform` + `platforms` + Architecture 외부 의존성 base. AI가 후보 제시:

#### web (정적 또는 SSR)
- **Vercel** — Next.js·React·Vue 권장. CI 통합 좋음. 빠른 prototype에 디폴트.
- **Netlify** — 정적 + serverless functions.
- **Cloudflare Pages** — edge·빠름·무료 트래픽 넉넉.
- **Firebase Hosting** — Google. Auth·DB와 통합 시 강력.
- **GitHub Pages** — 정적만. 토이 프로젝트.
- **AWS Amplify**.

#### api-server (백엔드)
- **Railway** — 간단·빠름. DB+API+정적 한 묶음. prototype에 디폴트.
- **Render** — 비슷한 결.
- **Fly.io** — 글로벌 배포·edge.
- **GCP Cloud Run** — 컨테이너·serverless·자동 스케일. mvp~production에 강력.
- **AWS** — ECS·Lambda·App Runner. 복잡하지만 풀 스택.
- **Heroku** — 간단하지만 prototype에선 충분.
- **자체 호스팅** — DigitalOcean·Linode·Hetzner.

#### mobile
- **iOS**: TestFlight (베타) → App Store (production)
- **Android**: Google Play Internal → Closed → Open → Production
- **Firebase App Distribution**: 양쪽 베타 통합.

#### library
- **npm** (JS/TS) / **PyPI** (Python) / **Cargo** (Rust) / **pub.dev** (Dart) / **Maven Central** (Java/Kotlin) / **Go modules** (git tag).

#### desktop
- 각 OS 패키지 (DMG·MSI·AppImage) — GitHub Releases에 자동 업로드.
- 또는 Mac App Store·Microsoft Store (mvp 이후).

#### cross-platform
- **Firebase 통합** = web + mobile 둘 다 cover (Auth·Hosting·App Distribution).
- **Railway/Render** = 풀스택(api-server + DB + 정적 frontend).
- 메인 플랫폼 + 추가 platforms 모두 cover하는 묶음 우선.

#### 추천 흐름

```
호스팅 후보:
- {플랫폼 표준 1~2개 추천} ← prototype 디폴트
- {풀스택 통합 옵션} ← 백엔드·프론트 한 곳에 묶고 싶을 때
- {엔터프라이즈 옵션} ← 나중 사이클에서 검토

이번 사이클은? 모르겠으면 [추천] 디폴트로.
```

### 2.3 시크릿 셋업

8-automation-setup.md에서 만든 `.env.example` 키들을 GitHub Secrets에도 추가해야 CI/배포에서 동작.

```
GitHub Secrets에 추가 필요:
- OPENAI_API_KEY
- DATABASE_URL
- ...

추가 방법:
1. GitHub repo → Settings → Secrets and variables → Actions
2. New repository secret
3. Name + Value 입력 → Add secret

추가 끝나면 알려줘 — 안 했으면 배포 시 빌드 실패함.
```

AI는 키 못 다룸. 사용자가 직접 추가 후 confirm.

### 2.4 도메인 연결 (옵션)

- **prototype**: 무료 서브도메인 (`<프로젝트>.vercel.app`, `<프로젝트>.up.railway.app` 등). 도메인 비용 X.
- **mvp 이상**: 커스텀 도메인 권장.
  - 도메인 등록 (네임칩·Cloudflare Registrar·Namecheap 등) — 사용자가 직접
  - DNS 설정 (호스팅 플랫폼 가이드 따라 CNAME/A 레코드 추가)
  - HTTPS 인증서 자동 (Vercel·Netlify·Cloudflare는 자동 발급)

### 2.5 모니터링·관측성

- **prototype**: 호스팅 자체 로그만 (Vercel logs, Railway logs).
- **mvp**: + **Sentry** (에러 트래킹) — 무료 플랜 충분. 설정 30분.
- **production**: + uptime 모니터링 (UptimeRobot·Better Uptime) + 메트릭 (DataDog·Grafana Cloud) + 알람.

### 2.6 배포 자동화 — GitHub Actions

8-automation-setup.md의 `.github/workflows/ci.yml`에 deploy job 추가 또는 별도 `.github/workflows/deploy.yml`.

**사이클별 배포 트리거**:
- **prototype**: 수동 배포 OK (사용자가 호스팅 CLI 직접 호출). 또는 main push 시 자동.
- **mvp**: PR main merge → 자동 staging 배포.
- **production**: tag push (`v1.0.0` 등) → 자동 production 배포.

호스팅별 deploy job 예시:

- **Vercel**: `vercel-action` 또는 Vercel Git integration (별도 workflow 불필요).
- **Railway**: `railway up` CLI를 GitHub Actions에서 호출.
- **Firebase**: `w9jds/firebase-action` 또는 `firebase-tools`.
- **GCP Cloud Run**: `google-github-actions/deploy-cloudrun`.
- **npm publish**: tag push → `npm publish` job.
- **App Store/Play Store**: Fastlane (mobile 표준).

### 2.7 롤백 플랜

- **prototype**: git revert + 재배포만. 따로 안 만듦.
- **mvp**: 호스팅 자체 rollback (Vercel·Railway는 이전 deployment로 즉시 되돌림 UI 제공).
- **production**: 명시적 롤백 절차 — `deploy-checklist.md`에 박음. 데이터 마이그레이션 있으면 down migration도 준비.

### 2.8 사용자 결정 흐름

AI가 위 5가지(호스팅·시크릿·도메인·모니터링·롤백)를 한 번에 정리해 보고:

```
배포 셋업할 거 정리했어:

1. 호스팅: [추천] {호스팅 1} — 어디로 갈래?
2. 시크릿: GitHub Secrets에 [N개] 추가 필요 — 직접 추가해줘
3. 도메인: prototype은 무료 서브도메인 디폴트 — 커스텀 원해?
4. 모니터링: prototype은 호스팅 로그만 — Sentry 추가할래?
5. 롤백: prototype은 git revert만 — OK?

차례로 답해줘. 모르면 [추천] 디폴트로.
```

각 결정 받은 후 AI가 자동화 셋업 (workflow 파일 생성·호스팅 CLI 명령 실행).

## 3. 완료 체크리스트

- [ ] **호스팅 결정** + 첫 배포 성공 (URL 받음).
- [ ] **시크릿** GitHub Secrets 추가 완료 (사용자 직접).
- [ ] **도메인** 결정·연결됨 (또는 prototype은 skip).
- [ ] **모니터링** prototype은 호스팅 로그 확인 / mvp~ Sentry 동작.
- [ ] **롤백 플랜** 사이클 라벨에 맞게 정리됨.
- [ ] **`.github/workflows/deploy.yml`** (또는 ci.yml에 deploy job) 동작 확인.
- [ ] **`deploy-checklist.md`** 결정·명령어·URL·남은 액션 기록됨.

## 4. 산출물 스펙

### 4.1 사이클 안 메타 — `deploy-checklist.md`

위치: `planning/cycles/v{N}-{label}/deploy-checklist.md`.

```markdown
---
cycle: v1-prototype
created_at: YYYY-MM-DD
deployed_url: https://dotoriroom.vercel.app
---

# 호스팅
- 플랫폼: Vercel
- 트리거: main push 시 자동
- workflow: .github/workflows/deploy.yml

# 시크릿 (GitHub Secrets)
- ✓ OPENAI_API_KEY
- ✓ DATABASE_URL

# 도메인
- 무료 서브도메인: dotoriroom.vercel.app
- 커스텀: 추후 mvp에서 (도메인 미정)

# 모니터링
- prototype: Vercel logs만
- mvp 추가 예정: Sentry

# 롤백
- prototype: git revert + push
- mvp 추가 예정: Vercel rollback UI

# 사용자에게 남은 액션
- [ ] 첫 배포 후 https URL 직접 열어 동작 확인
- [ ] 도메인 등록 (mvp 사이클에서)
```

### 4.2 프로젝트 루트 파일

- `.github/workflows/deploy.yml` — 호스팅별 deploy job
- 호스팅 설정 파일 (`vercel.json`·`railway.json`·`firebase.json` 등) — 호스팅에 따라
- `Dockerfile` — 컨테이너 호스팅 시

## 5. 사이클 업데이트 모드 (v2 이상)

- **호스팅 유지** 또는 변경 사유 명시 (예: prototype Vercel → mvp는 스케일·DB 통합 위해 Railway).
- **시크릿** 새 의존성 추가됐으면 GitHub Secrets에도 추가 (사용자 직접).
- **도메인 mvp에서 커스텀 연결** (prototype 무료 → mvp 자체 도메인).
- **모니터링 mvp 추가** (Sentry 등) / **production 추가** (uptime·메트릭).
- **롤백 production 정착** (down migration·점진적 배포·자동 롤백 트리거).

## 6. 좋은 예 vs 나쁜 예

- **호스팅 결정** — 좋은: "Vercel — Next.js와 통합 쉬움, 무료 트래픽 충분, 5분이면 첫 배포". / 나쁜: "어딘가에 배포함".
- **시크릿** — 좋은: GitHub Secrets에 키 명시 + 추가 가이드. / 나쁜: ".env에만 두고 GitHub 안 박음 → CI 빌드 실패".
- **롤백** — 좋은: "Vercel 대시보드에서 이전 deployment 클릭, 30초 안 복구". / 나쁜: "문제 생기면 고친다".

## 7. 사용자 응대 톤 + 인터뷰 코칭

- **톤**: SKILL.md §1.3대로 반말·친근·짧게. 5가지 결정 한 번에 정리해 받음.
- **코칭**: SKILL.md §1.4대로. 사용자가 호스팅 모르면 §2.2 플랫폼 표준 후보 + 추천. 시크릿 추가 방법은 단계별 명시 (UI 경로). 도메인은 prototype에선 skip 권유. 모니터링 첫 사이클엔 가볍게. 롤백은 사이클 라벨에 맞게(prototype/mvp/production) 자동 분기.
