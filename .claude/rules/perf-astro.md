---
name: perf-astro
description: Astro 5.x + Vercel adapter perf baseline. Astro 공식 docs 권장 + Web Vitals 산업 표준. v1-prototype Architecture (§2.10) 자동 생성.
paths:
  - 'src/**/*.astro'
  - 'src/**/*.ts'
  - 'src/**/*.tsx'
  - 'src/**/*.mjs'
  - 'astro.config.mjs'
  - 'astro.config.ts'
---

# Astro perf — high-signal 항목만

## Image
- `astro:assets`의 `<Image />` 사용. 직접 `<img>` 회피. Vercel adapter `imageService: true` 시 자동 최적화.
- `imagesConfig.sizes`로 viewport별 widths 명시 (기본 `[320, 640, 1280]` 정합).
- SVG 마스코트는 `<img>` 그대로 OK — Image 컴포넌트 raster 위주.

## Font
- Astro 5 `fonts:` integration 사용. `@import url("...googleapis.com/...")` 패턴 회피 (LCP 페널티).
- `subsets: ["latin", "korean"]` 명시 — 한국어 폰트 필수. default `latin`만 두면 한글 무거운 fallback 트리거.
- 실제 사용 weights만 `weights:` 명시. 모든 weight 받으면 payload 폭증.
- 위 fold 폰트는 `preload` 명시.

## Critical CSS
- 위 fold (Hero·Header) inline style·CSS variables는 그대로 inline 유지 → Astro가 자동 critical CSS extract.
- 대규모 `<style is:global>`은 page-specific으로 분리.

## Routing
- `output: 'static'` — SSG 1차 가정. SSR 도입은 명시적 결정 후 (서버 비용 + 위협 모델 변경 트리거).
- View Transitions (`<ClientRouter />`)은 미니멀 콘텐츠 사이트엔 안 박는 게 default — JS 추가 비용. 시각 인터랙션 강조 필요해질 때만.

## Content collections
- `defineCollection` + Zod schema 필수. frontmatter 검증 빌드 시점에 빠르게 실패해야.
- collection 변경 시 `astro sync` 자동 실행 (dev). prod 빌드는 자동.

## Vercel adapter
- `@astrojs/vercel` 정적 사이트도 adapter 사용 — Web Analytics·Image Optimization 통합.
- `webAnalytics: { enabled: true }` 명시 (Vercel 대시보드 활성과 별개).

## Web Vitals (산업 표준, 75th percentile)
- LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1
- prototype 사이클: 측정·기록만 (`SKILL.md §5.1`)
- prod 사이클: 강제 차단

## 회피
- ❌ Google Fonts `@import url(...)` — Astro Font integration으로 전환
- ❌ 외부 script `<script src="..." />` 무비판 추가 — JS 시작비용 ↑. analytics는 Vercel built-in 우선
- ❌ 큰 lottie/3D — 정적 콘텐츠 사이트엔 불필요
- ❌ Tailwind 도입 결정 (현재 inline style + CSS variables 모델로 충분. Tailwind 추가는 후속 cycle에서 명시적 결정 후)
