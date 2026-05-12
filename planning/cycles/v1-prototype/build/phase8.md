# Phase 8: Deploy & Domain

## 사전 준비

먼저 아래 산출물을 반드시 읽고 프로젝트의 전체 설계 의도를 완전히 이해하라:

- `planning/cycles/v1-prototype/intent.md` — 무엇·왜·누구·platform
- `planning/cycles/v1-prototype/prd.md` — Must/Should/Could/Won't 명세 + 비기능 요구사항
- `planning/cycles/v1-prototype/architecture.md` — 기술 스택·시스템 구조·디렉토리·API 명세·횡단 룰 적용
- `planning/cycles/v1-prototype/data-model.md` — ProgressPost·NotePost·CurrentMember·OperatorMeta 4 엔티티
- `planning/cycles/v1-prototype/design/migration-analysis.md` — site/ 자산 인벤토리 + Astro 매핑
- `planning/cycles/v1-prototype/design/migration-plan.md` — 컴포넌트 매핑 표 + phase 분할
- `planning/cycles/v1-prototype/brand-guide.md` — 컬러·voice·시그널·금지 사항
- `planning/cycles/v1-prototype/sketch.md` — 시나리오 S1~S5 + 화면별 엣지 케이스
- `site/` — design SoT (현재 plain HTML+CSS+JS, 시각 정합 기준)
- `.claude/rules/perf-astro.md` — Astro 5 perf baseline (Image·Font·Critical CSS·Vercel adapter)

이전 phase 산출물:

phase 0~7 모두 통과, dist/ 빌드 산출물 정상

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

Vercel 프로젝트 connect + bsides.kr 도메인 DNS + preview/prod 환경 분리 + 첫 production deploy.

## 작업 내용

### 8.1 Vercel 프로젝트 연결

```bash
# Vercel CLI 설치 (전역, 1회)
npm install -g vercel

# 프로젝트 연결 — 운영자가 본인 Vercel 계정에 로그인 필요
cd /Users/youngdonkim/dev/Bsides
vercel link
```

대화형 질문에 답:
- Set up and link: Y
- Scope: 운영자 본인 계정
- Link to existing project: N
- Project name: bsides
- Directory: ./

`.vercel/project.json` 생성됨 — `.gitignore`에 이미 박혀있는지 확인.

### 8.2 환경 변수

v1엔 시크릿 0개. Vercel 대시보드 환경 변수 설정 불필요.

(Vercel Web Analytics는 별도 토큰 없이 자동 트래킹.)

### 8.3 도메인 DNS

운영자 작업 (Vercel 대시보드 또는 CLI):

1. Vercel 프로젝트 → Settings → Domains → `bsides.kr` 추가
2. 도메인 등록처 (Namecheap/Cloudflare/AWS Route53 등)에서 Nameserver를 Vercel로 변경, **또는** 등록처 그대로 두고 A/CNAME record를 Vercel 안내값으로 변경
3. Vercel이 자동 HTTPS (Let's Encrypt) 발급
4. www 서브도메인은 apex로 redirect (Vercel 기본)

### 8.4 첫 production deploy

```bash
vercel --prod
```

또는 GitHub 연결되어 있으면 `main` branch push → 자동 배포.

### 8.5 preview deploy 검증

PR 또는 non-main branch push 시 preview URL 자동 생성 검증:

```bash
git checkout -b test/preview-check
git commit --allow-empty -m "preview test"
git push -u origin test/preview-check
# Vercel webhook → preview URL 생성 → 운영자 콘솔/메일로 알림
```

검증 후 branch 삭제.

### 8.6 최종 검증

- `https://bsides.kr/` 응답 정상
- 모든 라우트 (`/progress`, `/progress/round-3-mimirog-launch`, `/notes`, `/notes/{NN}-{slug}` 13개, `/404`) 정상
- OG preview — `https://www.opengraph.xyz/url/https%3A%2F%2Fbsides.kr` 식으로 OG meta 검증
- favicon 브라우저 탭에 정상 표시
- Vercel Web Analytics 대시보드에 PV 데이터 들어오는지 확인 (배포 후 ~10분)


## Acceptance Criteria

```bash
# CLI에서
vercel ls                                 # 프로젝트 등록 확인
vercel inspect <production-url>           # 최신 deploy 정보
curl -s -o /dev/null -w "%{http_code}\n" https://bsides.kr/         # 200
curl -s -o /dev/null -w "%{http_code}\n" https://bsides.kr/notes/01-intent   # 200
curl -sI https://bsides.kr/ | grep -i "strict-transport-security"     # HTTPS HSTS
```

수동 확인 (운영자):
- 도메인 https://bsides.kr 응답
- 모든 시나리오 (S1·S2·S3·S4·S5) production에서 통과
- Vercel Analytics 대시보드 PV 수집 확인

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 8 status를 `"completed"`로 변경.

수정 3회 이상 실패하면 status `"error"`, `error_message` 필드에 에러 내용.

작업 중 사용자 개입 필요(API key·외부 서비스 인증·수동 설정)면 즉시 중단, status `"blocked"`, `blocked_reason`에 사유 + 사용자가 따라할 단계.

## needs_review 트리거 자체 점검

작업 완료 후 다음 중 하나라도 해당하면 status를 `"needs_review"`로 변경하고 `review_summary`·`review_files`에 핵심 변경 요약 기록:

- 인증·권한·암호화 코드 신규/변경
- 외부 API 키·시크릿 신규 사용
- DB 스키마 변경(컬럼 추가/제거/타입 변경, 마이그레이션 파일)
- 외부 API 호출 신규 추가 (특히 비용·사용자 데이터 외부 전송)
- 비결정성(타임존·시스템 시간·무작위 시드) 의존
- sudo·root·OS 권한·파일시스템 외부 접근

이 phase 특이사항: **⚠️ needs_review 트리거**:
- 외부 인프라 첫 연결 (Vercel 계정·도메인·DNS). 비가역적은 아니지만 운영 전환 시점.
- 도메인 DNS 변경 — 등록처에서 운영자 직접 수행. AI가 자동 못함.
- review_summary: "Vercel project connected + bsides.kr DNS 전환 + 첫 production deploy."
- review_files: `.vercel/project.json` (gitignored), Vercel 대시보드 설정

## 주의사항

- **운영자 수동 단계**: Vercel 계정 로그인, 도메인 DNS 전환은 AI 자동 X. 사용자 진행.
- `.vercel/`은 `.gitignore`에 박혀야 함 (Phase 0에서 확인).
- 첫 deploy 전에 환경 변수가 정말 0개인지 확인 (NODE_ENV 등 Vercel 자동). 시크릿 commit 점검.
- 도메인 DNS propagation은 최대 48시간. 첫 deploy는 Vercel 기본 `bsides.vercel.app` URL로 검증 후 도메인 연결.
- production deploy 후 Vercel 대시보드에서 빌드 로그 확인. 환경 차이로 dev/preview에서 안 보이던 에러 (예: case-sensitive 파일명 mismatch) 잡힐 수 있음.
