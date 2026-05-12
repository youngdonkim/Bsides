# Phase 2: Home Static Shell

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

phase 1: `src/layouts/BaseLayout.astro`, `src/components/Header.astro`, `src/components/Footer.astro`, `src/data/operator.ts`, `src/styles/*.css`, `public/assets/*`

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

메인 페이지의 콘텐츠 비의존 섹션만 — Hero · HowItWorks · ApplySection. ProgressCard·MentorCard는 Phase 4에서 통합.

## 작업 내용

### 2.1 Hero.astro

`src/components/home/Hero.astro` — `site/index.html`의 Hero 섹션 (sup-label + h1 with Gaegu 700 강조 + 보조 + CTA 2개 + sticky cluster 3장) 그대로 paste. props 없음 (메인 1개 전용).

핵심 보존:
- `class="b-hand-underline"`에 inline `font-family: 'Gaegu', 'Nanum Pen Script', cursive; font-weight: 700; font-size: 1.4em;` 유지
- `.b-hero-cluster` 3장의 회전·위치·sticky note 마크업

### 2.2 HowItWorks.astro

`src/components/home/HowItWorks.astro` — site/index.html "운영방식 4단계 카드" + "객원 → 정식 멤버" callout 통째로. 4 카드는 데이터 driven 가능하지만 sample 1개라 inline OK.

### 2.3 ApplySection.astro

`src/components/home/ApplySection.astro` — site/index.html `#apply` 섹션 그대로. welcome.svg 마스코트·3 단계 안내·카톡 link.

```astro
---
import { OPERATOR } from '../../data/operator';
---
<section id="apply" style="...">
  ...
  <a href={OPERATOR.kakaoOpen} target="_blank" rel="noopener noreferrer">카톡으로 신청하기 →</a>
  ...카톡 어렵다면 <a href={`mailto:${OPERATOR.email}`}>{OPERATOR.email}</a>...
</section>
```

### 2.4 PersonaStrip.astro (작은 컴포넌트)

site/index.html "이런 분에게" strip — 직장인·디자이너/개발자/마케터/기획자 카피.

### 2.5 메인 페이지 통합

`src/pages/index.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Hero from '../components/home/Hero.astro';
import PersonaStrip from '../components/home/PersonaStrip.astro';
import HowItWorks from '../components/home/HowItWorks.astro';
import ApplySection from '../components/home/ApplySection.astro';
---
<BaseLayout title="..." description="..." currentPage="home">
  <main data-screen-label="01 Home">
    <Hero />
    <PersonaStrip />
    <HowItWorks />
    {/* MentorCard·ProgressCard grid는 Phase 4 */}
    <ApplySection />
  </main>
</BaseLayout>
```


## Acceptance Criteria

```bash
npm run build
npm run typecheck
npm run dev &
sleep 5
curl -s http://localhost:4321/ | grep "감성 한 스푼"
curl -s http://localhost:4321/ | grep "운영방식 — 한 사이클"
curl -s http://localhost:4321/#apply -o /dev/null
```

수동 확인 (브라우저):
- `site/index.html`과 시각 정합 (Hero·sticky cluster·운영방식 4 카드·객원→정식 4단계·#apply 섹션)
- 헤더 nav `currentPage="home"`이므로 진행상황·Notes link 모두 비활성
- 모바일 320px 폭에서 sticky cluster `display: none` 정상 동작

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 2 status를 `"completed"`로 변경.

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

이 phase 특이사항: 정적 콘텐츠만. needs_review 트리거 없음.

## 주의사항

- "이번 사이클 멤버" 섹션과 "최근 진행상황" grid는 **이 phase에서 추가 X** — Phase 4에서 데이터 driven으로 통합.
- 모든 inline style은 site/index.html 그대로. CSS class 추출·refactor 금지 (v1 paste-and-go 원칙).
- ApplySection 카톡 link은 `OPERATOR.kakaoOpen` 참조하되 hardcoded URL 잔존 점검.
