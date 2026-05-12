# Phase 7: Analytics & Performance

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

phase 0~6 빌드 완성

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

Vercel Web Analytics 통합 + Lighthouse 측정 + CWV 임계값 확인. PRD §성능 LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1 통과.

## 작업 내용

### 7.1 Vercel Web Analytics

`astro.config.mjs`의 `adapter` 옵션에 이미 `webAnalytics: { enabled: true }` 박혀있음 (Phase 0). 활성 검증.

빌드 후 `dist/` 안 HTML들에 Vercel Analytics script가 자동 inject됐는지 확인:

```bash
grep -r "va.vercel-scripts.com\|/_vercel/insights" dist/ | head -3
```

### 7.2 Astro `<Image />` 적용 — 해당 없음 (대부분)

현재 디자인 SoT는 SVG 마스코트 + CSS gradient placeholder cover (실제 raster cover 이미지 없음). `astro:assets`의 `<Image />`는 raster 위주. SVG는 그대로 `<img>` 사용 정합.

실제 cover 이미지가 콘텐츠에 추가되는 시점(추후 사이클)부터 `<Image />`로 옮기는 phase 별도 생성.

### 7.3 Lighthouse 측정

```bash
npm run build
npm run preview &
sleep 5

# Lighthouse CLI (이미 설치돼 있으면)
npx lighthouse http://localhost:4321/ --quiet --chrome-flags="--headless" --output=json --output-path=/tmp/lh-home.json
npx lighthouse http://localhost:4321/progress/ --quiet --chrome-flags="--headless" --output-path=/tmp/lh-progress.json
npx lighthouse http://localhost:4321/notes/01-intent --quiet --chrome-flags="--headless" --output-path=/tmp/lh-note.json
```

3 페이지 CWV (LCP·INP·CLS) 측정 결과 저장. 임계값 초과 시 원인 분석:

| 메트릭 | PRD 임계값 | 일반 원인 | 개선책 |
|---|---|---|---|
| LCP > 2.5s | font 로딩 지연·큰 이미지 | preload 명시·subset 조정·Image 컴포넌트 |
| INP > 200ms | JS 실행 |  notes-progress.js scroll listener throttle |
| CLS > 0.1 | font swap·image without size | font-display: optional·image width/height 명시 |

### 7.4 결과 기록

`planning/cycles/v1-prototype/build/phase7-output.json`에 측정 결과 + 통과/실패 기록 (run-phases.py가 자동 처리; 사람이 손댈 일 X).


## Acceptance Criteria

```bash
npm run build
grep -q "_vercel/insights\|vercel-scripts" dist/index.html       # analytics script injected
npm run preview &
sleep 5
# Lighthouse 3개 페이지
npx lighthouse http://localhost:4321/ --output=json --output-path=/tmp/lh-home.json --chrome-flags="--headless"
node -e "const r=require('/tmp/lh-home.json'); const lcp=r.audits['largest-contentful-paint'].numericValue; const cls=r.audits['cumulative-layout-shift'].numericValue; console.log('LCP:', lcp, 'CLS:', cls); if (lcp > 2500 || cls > 0.1) process.exit(1);"
```

수동 확인 (PRD §성능 임계값 75th percentile 가정 — prototype 단계는 측정·기록만 §5.1):
- LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1
- 임계값 초과 시 retrospective(Phase 13단계)에서 기록.

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 7 status를 `"completed"`로 변경.

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
- Vercel Web Analytics 외부 호출 신규 추가 (사용자 페이지 뷰·referrer 데이터를 Vercel 서버로 전송). cookie-less라 PRD §보안 "사용자 데이터 수집 0" 정합이지만, IP·user-agent는 Vercel side에서 일시 처리.
- review_summary: "Vercel Web Analytics 활성 — PV·referrer·외부 link click 수집. cookie-less, IP는 Vercel internal."
- review_files: `astro.config.mjs` (webAnalytics enabled), `dist/index.html` (script injection 검증)

## 주의사항

- 측정은 production-like 환경에서 (preview 모드). dev server는 HMR·source map 등으로 CWV 왜곡.
- INP는 사용자 인터랙션 후 측정되는 메트릭 — Lighthouse 자동 측정엔 INP가 limited. PSI(PageSpeed Insights)나 실사용 RUM 데이터가 더 정확. prototype 단계엔 LCP/CLS만 robust 측정.
- Lighthouse 점수가 임계값 미달이면 retrospective(13단계)에 기록 후 mvp 사이클에서 본격 최적화. prototype은 측정 기록만.
