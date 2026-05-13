---
name: design-system
description: Bsides 디자인 시스템 룰 — CSS 토큰 SoT, 반복 패턴 클래스 추출, 인라인 정책, Astro Font 매칭.
paths:
  - 'src/**/*.astro'
  - 'src/styles/*.css'
  - 'src/content/**/*.md'
  - 'src/pages/**/*.astro'
---

# Bsides Design System

디자인 SoT는 `site/` (plain HTML+CSS+JS). 시각 정합 기준이고, 컴포넌트 추출 후에도 비교 reference로 유지.

## 토큰 (브랜드)

- **SoT**: `src/styles/brand.css` 의 CSS variables `--b-*`. 모든 컴포넌트가 여기서 색·여백·radius·shadow 참조.
- **금지**: 컴포넌트·페이지에서 hex 색·`rgba(...)`·`Npx` radius·`box-shadow:` raw 값 박기. 토큰에 없으면 `brand.css`에 의미 토큰 먼저 추가 후 사용.
  - 예외: `border-radius: 0px`·`50%` (각 명시적 0/원형 의도) 는 OK.

### 의미 토큰 목록 (참고)

- color: `--b-paper*`·`--b-ink*`·`--b-olive*`·`--b-note-*`·`--b-live*`·`--b-line*`·`--b-card*`
- font: `--b-font-sans`·`--b-font-hand` (체인) / Astro 자동 생성 `--b-font-hand-nps`·`--b-font-hand-gaegu`
- radius: `--b-r-{8,12,14,16,20,24,32}`·`--b-r-note`·`--b-r-pill`
- shadow: `--b-shadow-{1,2,note,cta,cta-lg,pulse}`
- overlay: `--b-paper-glass`·`--b-ink-hand-faint`·`--b-cover-inner-shade`

## 클래스 추출 정책

- **반복 2회 이상이면 추출**. 동일 인라인 클러스터가 두 곳 이상이면 `src/styles/components.css` 로 클래스 추출. modifier(`--size`·`--color`)는 BEM 비슷한 더블 대시.
- **layout-only 인라인은 유지**. `position`·`top`·`left`·`width`·`transform: rotate(...)`·`aspect-ratio` 등은 instance마다 다르니 인라인에 남겨.
- 현재 추출된 클래스 (확장 시 충돌 점검):
  - structure: `.b-container`·`.b-hero-grid`·`.b-hero-cluster`·`.b-mentor-grid`·`.b-mentor-image`·`.b-cta-row`·`.b-relay-callout`·`.b-detail-nav`·`.b-header-glass`
  - typography: `.t-display`·`.t-title-{1,2,3}`·`.t-body`·`.t-body-strong`·`.t-label`·`.t-caption`·`.t-hand`·`.t-hand-caption`
  - components: `.b-sticky-note`(+size/color)·`.b-btn-primary`(+size)·`.b-btn-secondary`·`.b-btn-pill`·`.b-cover-shade`·`.b-cover-caption`·`.b-badge-round`·`.b-live-dot`·`.b-note-card`(+title/body)
  - util: `.b-hand-underline`·`.vh`

## Astro Font 매칭 (gotcha)

- Astro Font integration이 `@font-face` family를 hashed name(예: `"Nanum Pen Script-04cc69bb47ee2158"`)으로 self-host함.
- 따라서 CSS·인라인에서 **`'Gaegu'`·`'Nanum Pen Script'` 같은 hardcoded family name 직접 참조 금지** — match 실패해 `cursive` fallback 적용.
- 항상 Astro가 노출한 `var(--b-font-hand-nps)`·`var(--b-font-hand-gaegu)` 변수 chain 사용:
  ```css
  font-family: var(--b-font-hand-gaegu), var(--b-font-hand-nps), cursive;
  ```
- 등록은 `astro.config.mjs`의 `fonts:` 배열. 새 폰트 추가하면 `BaseLayout.astro`에 `<Font cssVariable="..." preload />` 도 같이 추가.

## 한국어 폰트 sub-setting

- `subsets: ['korean', 'latin']` 필수. 기본 latin만 두면 한글에 무거운 fallback 트리거.
- 실제 사용 weight만 `weights:` 명시. 모든 weight 받으면 payload 폭증.
