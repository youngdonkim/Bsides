# Phase 1: Tokens & Base Layout

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

phase 0: `astro.config.mjs`, `package.json`, `tsconfig.json`, `src/pages/index.astro` (placeholder)

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

디자인 토큰 · BaseLayout · Header · Footer · Astro Font integration. 모든 페이지가 공통 chrome으로 렌더되는 상태.

## 작업 내용

### 1.1 디자인 토큰 · CSS

`site/styles/brand.css` → `src/styles/brand.css`로 paste. 단 다음 변경:
- 첫 줄 Google Fonts `@import url("...googleapis.com/...")` 라인 **제거** (Astro Font integration으로 대체).
- jsDelivr Pretendard 두 줄(`https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/...`)은 그대로 유지.

`site/styles/components.css` → `src/styles/components.css` 그대로 paste.

### 1.2 Astro Font integration

`astro.config.mjs`에 `fonts` 필드 추가:

```js
fonts: [
  {
    name: 'Nanum Pen Script',
    cssVariable: '--b-font-hand-nps',
    provider: fontProviders.google(),
    weights: [400],
    subsets: ['korean', 'latin'],
  },
  {
    name: 'Gaegu',
    cssVariable: '--b-font-hand-gaegu',
    provider: fontProviders.google(),
    weights: [400, 700],
    subsets: ['korean', 'latin'],
  },
],
```

brand.css의 `--b-font-hand: "Nanum Pen Script", "Gaegu", cursive;`는 그대로. 위 Astro Font cssVariable은 폰트 자체를 self-host로 가져오는 용도. 직접 참조는 brand.css의 `--b-font-hand` 통해서.

`src/layouts/BaseLayout.astro`에서 `<Font cssVariable="--b-font-hand-nps" preload />`·`<Font cssVariable="--b-font-hand-gaegu" preload />` 추가.

### 1.3 OperatorMeta const

`src/data/operator.ts`:

```ts
export const OPERATOR = {
  name: '현지',
  kakaoOpen: 'https://open.kakao.com/o/bsides',
  kakaoHandle: '@bsides',
  email: 'hi@bsides.kr',
  domain: 'bsides.kr',
  brandTagline: '혼자가 가능해진 시대, 출시까지 같이 가는 프로젝트 팀 빌딩 및 재능 품앗이 서비스.',
} as const;
```

### 1.4 BaseLayout.astro

`src/layouts/BaseLayout.astro` — site/index.html head 구조 그대로 + Font·Slot. props:

```astro
---
interface Props {
  title: string;
  description: string;
  ogTitle?: string;
  ogDescription?: string;
  currentPage?: 'home' | 'progress' | 'notes';
}
const { title, description, ogTitle = title, ogDescription = description, currentPage } = Astro.props;
import { Font } from 'astro:assets';
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';
import '../styles/brand.css';
import '../styles/components.css';
---
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content={description} />
    <meta property="og:title" content={ogTitle} />
    <meta property="og:description" content={ogDescription} />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="/assets/og.svg" />
    <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
    <Font cssVariable="--b-font-hand-nps" preload />
    <Font cssVariable="--b-font-hand-gaegu" preload />
    <title>{title}</title>
  </head>
  <body data-page={currentPage} style="font-family: var(--b-font-sans);">
    <div id="root">
      <Header currentPage={currentPage} />
      <slot />
      <Footer />
    </div>
  </body>
</html>
```

### 1.5 Header.astro

`site/index.html`의 새 헤더 마크업 그대로. props로 `currentPage` 받아 nav active state inline 처리 (현재 site/는 JS로 처리하지만 Astro에선 build 시점 결정 가능):

```astro
---
import { OPERATOR } from '../data/operator';
interface Props { currentPage?: 'home' | 'progress' | 'notes'; }
const { currentPage } = Astro.props;
const navItems = [
  { key: 'progress', href: '/progress', label: '진행상황' },
  { key: 'notes', href: '/notes', label: 'Notes' },
];
---
<header style="...sticky 헤더 스타일...">
  <!-- 로고 + nav (currentPage 매칭 link에 활성 스타일) + CTA -->
</header>
```

### 1.6 Footer.astro

`site/index.html`의 footer 마크업 그대로. `OPERATOR` const 참조해서 카톡·이메일·tagline 박음.

### 1.7 placeholder index.astro 갱신

`src/pages/index.astro`를 BaseLayout 사용하는 형태로:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout
  title="Bsides — LLM이 만든 그럴듯한 초고 위에, 감성 한 스푼."
  description="..."
  currentPage="home"
>
  <main>홈 콘텐츠는 Phase 2에서.</main>
</BaseLayout>
```

### 1.8 assets/ public/로 이동

`site/assets/spooni/*.svg` (10개), `site/assets/og.svg`, `site/assets/favicon.svg`을 `public/assets/`로 복사.


## Acceptance Criteria

```bash
npm run build
npm run typecheck
# dev server 확인
npm run dev &
sleep 5
curl -s http://localhost:4321/ | grep "Bsides"
curl -s http://localhost:4321/assets/favicon.svg | head -1   # SVG 응답
```

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 1 status를 `"completed"`로 변경.

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

이 phase 특이사항: 폰트·CSS·assets 추가만. needs_review 트리거 없음.

## 주의사항

- brand.css의 Google Fonts `@import` 라인만 삭제하고 jsDelivr 두 줄은 유지.
- BaseLayout의 `<style>` 안에 critical CSS 추가하지 말 것 (brand.css·components.css가 :root variables·.b-container 등 cover).
- Header sticky 마크업은 site/index.html과 시각 정합 유지. inline style 복붙 OK.
