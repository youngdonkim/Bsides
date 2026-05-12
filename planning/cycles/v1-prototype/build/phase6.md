# Phase 6: Edge & Meta

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

phase 0~5

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

404 페이지 + design-system.html paste + @astrojs/sitemap + robots.txt. SEO·외부 공유 자산 활성.

## 작업 내용

### 6.1 404.astro

`src/pages/404.astro` — site/404.html 마크업 그대로 + BaseLayout:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout
  title="페이지를 찾을 수 없어요 — Bsides"
  description="요청하신 페이지를 찾을 수 없어요."
  currentPage={undefined}
>
  <main class="b-container" style="padding: 80px 24px; text-align: center; max-width: 640px;">
    <img src="/assets/spooni/rest.svg" alt="..." width="160" height="140" loading="lazy" style="...rotate(-4deg)" />
    <h1 class="t-title-1">길을 잃었어요</h1>
    <p class="t-body">스푼이가 자고 있는 사이 페이지가 사라졌나봐요.</p>
    <p class="t-caption">URL이 바뀌었거나, 아직 만들어지지 않은 페이지일 수 있어요.</p>
    <a href="/" style="...olive button">메인으로 돌아가기 →</a>
  </main>
</BaseLayout>
```

Vercel 호스팅에서 정적 404로 자동 서빙. `astro build`가 `dist/404.html` 출력.

### 6.2 design-system.html

`site/design-system.html` → `public/design-system.html`로 그대로 paste. 빌드 출력에 포함되어 `bsides.kr/design-system.html`로 접근 가능. **운영 내부용**: robots.txt에서 `Disallow` (다음 6.4).

### 6.3 @astrojs/sitemap

`astro.config.mjs`에 추가:

```js
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://bsides.kr',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('design-system'),  // 내부 페이지 제외
    }),
  ],
  // ...
});
```

빌드 후 `dist/sitemap-index.xml` + `sitemap-0.xml` 자동 생성.

### 6.4 robots.txt

`public/robots.txt`:

```
User-agent: *
Allow: /
Disallow: /design-system.html

Sitemap: https://bsides.kr/sitemap-index.xml
```

### 6.5 OG image · favicon link 검증

`BaseLayout.astro`에 이미 `<meta property="og:image" content="/assets/og.svg" />` + `<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />` 박혀있음 (Phase 1). 검증만.

### 6.6 between-cycles variant 동작 확인

`src/data/current-member.ts`의 `CURRENT_MEMBER.cycle_state` 값 따라 메인의 MentorCard 분기. Phase 4에서 이미 구현됐고 이 phase에서 시각적 변형 한 번 더 점검.

별도 `index-between-cycles.html` 페이지는 만들지 않음 — 동일 페이지에서 데이터 driven 분기 (site/ design SoT의 별도 파일은 운영자 review 편의 목적이었고 production에선 하나로 통합).


## Acceptance Criteria

```bash
npm run build
ls dist/404.html dist/sitemap-index.xml dist/sitemap-0.xml dist/robots.txt dist/design-system.html
curl -s http://localhost:4321/non-existent-path -o /dev/null -w "%{http_code}"   # 404 (preview 또는 prod에선 정상, dev에선 404 페이지 응답)
curl -s http://localhost:4321/robots.txt | grep "Disallow: /design-system"
```

수동 확인:
- 모든 페이지 head에 `<meta property="og:image">`·`<link rel="icon">` 박힘
- 임의 URL 접근 시 404 페이지가 rest.svg 마스코트와 함께 표시
- sitemap-0.xml에 `/`·`/progress`·`/progress/round-3-mimirog-launch`·`/notes`·`/notes/01-intent` ~ `/notes/13-retro` 포함됨

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 6 status를 `"completed"`로 변경.

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

이 phase 특이사항: sitemap 자동 생성·robots.txt 추가. 외부 호출·시크릿 없음. needs_review 트리거 없음.

## 주의사항

- `astro.config.mjs`의 `site` 필드는 sitemap의 absolute URL 생성 base — `https://bsides.kr`로 정확히. trailing slash 없이.
- `public/design-system.html`은 site/design-system.html과 같은 마크업이지만 brand.css/components.css 경로가 정합해야 — site/는 `styles/brand.css` 상대 경로, Astro public/은 `/styles/brand.css` absolute. 충돌 시 design-system.html은 자체 inline CSS로 두는 게 안전.
- robots.txt는 `public/`에 두면 그대로 root 서빙. `astro build` 출력에 자동 포함.
