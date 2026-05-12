---
cycle: v1-prototype
created_at: 2026-05-12
updated_at: 2026-05-12
source: site/ (plain HTML + CSS + JS, design SoT)
target: Astro 5.x + @astrojs/vercel + Vercel hosting
---

# 출발점 — 현재 site/

Claude Design 핸드오프 결과를 정리한 **plain HTML + CSS + 최소 JS**. React+Babel CDN 아님. 마이그 공수가 references §2.4 기준 표(JSX → SFC 변환)보다 명백히 작음.

## 자산 인벤토리

| 파일 | 용도 | 마이그 형태 |
|---|---|---|
| `site/index.html` | 메인 (운영방식·이번 사이클 멤버·최근 진행상황·신청) | `src/pages/index.astro` |
| `site/index-between-cycles.html` | 메인 사이 회차 variant | `src/pages/index.astro` 내부 conditional (콘텐츠로 분기) |
| `site/progress.html` | 진행상황 목록 (카드 3개 상태) | `src/pages/progress/index.astro` |
| `site/progress-empty.html` | 진행상황 0개 빈 상태 | `progress/index.astro` 내부 conditional |
| `site/progress-round-3-mimirog-launch.html` | 진행상황 상세 sample | `src/pages/progress/[slug].astro` (collection) |
| `site/progress-not-found.html` | 잘못된 slug | `getStaticPaths` 자동 처리. 별도 `progress/404.astro` 또는 본 페이지 fallback |
| `site/notes.html` | Notes 목차 | `src/pages/notes/index.astro` |
| `site/notes-{01-13}-{slug}.html` | Notes 13단계 | `src/pages/notes/[slug].astro` (collection) |
| `site/404.html` | 사이트 전체 404 | `src/pages/404.astro` |
| `site/design-system.html` | DS 레퍼런스 (운영 내부용) | `public/design-system.html` (정적 paste, build 출력 포함 X) |
| `site/styles/brand.css` | 디자인 토큰 SoT (CSS variables) | `src/styles/brand.css` 그대로 paste |
| `site/styles/components.css` | 타이포·레이아웃 클래스 | `src/styles/components.css` 그대로 paste |
| `site/styles/design-system.css` | DS 페이지 전용 | DS 페이지와 함께 `public/styles/`로 |
| `site/scripts/notes-progress.js` | localStorage 진도 + nav active | `src/scripts/notes-progress.js`. Layout에서 `<script src="...">` |
| `site/assets/spooni/*.svg` | 마스코트 10개 | `public/assets/spooni/` |
| `site/assets/og.svg` | OG 이미지 | `public/assets/og.svg` |
| `site/assets/favicon.svg` | favicon | `public/assets/favicon.svg` |

# 도착점 — Astro 5 + Vercel

## 스택 적용 패턴

- **Output 모드**: `output: 'static'` — 모든 페이지 빌드 시점에 정적 HTML로. SSR/ISR 안 씀.
- **Adapter**: `@astrojs/vercel` — Vercel Web Analytics·Image Optimization 사용 위해 필요 (정적 사이트지만 adapter는 부가 서비스 통합 목적).
- **Content collections** (`src/content.config.ts`):
  - `notes` collection: `src/content/notes/*.md`, Zod schema로 frontmatter 검증
  - `progress` collection: `src/content/progress/*.md`, 동일 패턴
- **Layout 컴포넌트**: 공통 head·header·footer는 `src/layouts/BaseLayout.astro` 1개. 모든 페이지가 import.
- **재사용 컴포넌트**: ProgressCard·NoteRow·MentorCard·ApplySection·SectionHeader·StickyNote 등 `src/components/`.
- **Image**: `astro:assets` `<Image />` — Vercel adapter의 `imageService: true`로 자동 최적화 (cover 이미지·마스코트 SVG는 그대로 `<img>`도 OK).
- **Fonts**: Astro 5 `astro:assets` Font integration — `astro.config.mjs`의 `fonts:` 필드에 Pretendard·Nanum Pen Script·Gaegu 정의. subset `latin`·`korean` 명시, preload. 현재 brand.css의 `@import url("...googleapis...")` 패턴은 폐기.

## 공수 평가 — 작음

- HTML → `.astro` SFC: 거의 paste-and-go. inline style·CSS variables 그대로 동작.
- JSX 변환 비용 0 (소스가 이미 plain HTML).
- 컴포넌트 분리는 mechanical refactor.
- 콘텐츠 추출은 Notes 13개 + Progress 1개 sample → Python 스크립트 (이번 사이클의 design SoT 만들 때 썼던 패턴)로 frontmatter 추출 자동화 가능.

# 차이점·결정 사항

| 항목 | 현재 site/ | Astro 목표 | 결정 |
|---|---|---|---|
| 라우팅 | `.html` flat 파일 (`progress-round-3-mimirog-launch.html`) | `progress/[slug].astro` dynamic | clean URL `/progress/round-3-...`로 (현재 `.html` 확장자 노출 X) |
| 콘텐츠 source | HTML 안 inline | Markdown frontmatter + body | Notes·Progress 모두 Markdown 추출 |
| 헤더·푸터 반복 | 모든 페이지에 inline 복붙 | `BaseLayout.astro`에서 1번 정의 | 마이그 시 자동 dedupe |
| 빈 상태·variant 화면 | 별도 `.html` 파일 | conditional rendering | 데이터 driven (collection 비면 빈 상태 자동) |
| Notes prev/next | Python에서 미리 계산해 박음 | `getCollection`으로 sort 후 인덱스 계산 | 빌드 시 자동 |
| 진도 JS | site/scripts/notes-progress.js | 그대로 import + `<ClientRouter />`는 비도입 (단순 navigate 충분) | 변동 X |
| Font 로딩 | Google Fonts `@import` (브라우저 fetch) | Astro Font integration (build 시 self-host) | CWV 개선·LCP 단축 |
| Analytics | 없음 (F10 미구현) | `@vercel/analytics` 통합 | zero-config |

# 위험·고려사항

- **CSS specificity** — 현재 HTML inline style이 많음. Astro로 옮긴 후에도 그대로 동작하지만, 점진적으로 컴포넌트 클래스로 추출 권장. v1 prototype 단계엔 paste-and-go 우선.
- **마스코트 SVG 사이즈** — 가장 큰 SVG가 152KB (start.svg). Astro Vercel adapter Image Optimization은 raster 위주. SVG는 그대로 서빙 + brotli 압축에 맡김. v1엔 충분.
- **Notes 13개 페이지 자동 생성** — Python으로 만든 정적 콘텐츠를 Markdown으로 옮기는 1회성 추출 스크립트 필요. build phase 단계에서 별도 phase로.
- **사이 회차 (between-cycles) variant** — 현재 별도 HTML 파일. Astro에선 `현재 멘토 콘텐츠 비었으면` conditional로 같은 페이지에서 분기. content collection이 비면 자동.

# 다음 단계

`migration-plan.md`에서 4 항목 명세:
1. 디자인 토큰 추출 (CSS variables 그대로 → `src/styles/brand.css`)
2. 컴포넌트 매핑 표 (HTML 섹션 → `.astro` 컴포넌트)
3. 화면 단위 우선순위 (phase 분할)
4. 백엔드 연동 분리 (해당 없음 — 정적)
