# Bsides

> 혼자가 가능해진 시대, 출시까지 같이 가는 작은 메이커 동아리.
> 운영 · 현지 / hi@bsides.kr / [카톡 @bsides](https://open.kakao.com/o/bsides) / [bsides.kr](https://bsides.kr)

## 1. Intent 요약

- **플랫폼**: web (반응형, 320~1920px)
- **문제**: LLM으로 혼자 출시까지 가능해진 솔로 메이커가, 검증·디자인·자동화·홍보 같은 다른 분야가 부족한 상황에서, 서로의 전문성을 교환할 동료 커뮤니티가 없어 "그럴듯한 초고" 수준을 넘는 출시 품질로 끌어올리지 못한다.
- **타겟**: 사이드 프로젝트 지망 직장인 · 출시 의지 있는 디자이너·개발자·마케터·기획자.
- **성공 기준 (v1-prototype, 3개월)**: 워크샵 6회 · 출시 1건 · 멤버쉽 2명.
- **핵심 가설**: H1 릴레이 자생 · H2 organic 유입 충분성 · H3 사이클 → 출시.

## 2. Architecture 핵심 결정

- **언어**: TypeScript (strict)
- **프레임워크**: Astro 5.x + `@astrojs/vercel` adapter
- **DB**: 없음 (Markdown content collections — `src/content/notes/`·`src/content/progress/`)
- **인프라**: Vercel (호스팅 + CDN + CI/CD + Web Analytics)
- **외부 서비스**: Vercel Web Analytics · Astro Font integration (Google Fonts) · jsDelivr Pretendard

자세히는 `planning/cycles/v1-prototype/architecture.md`.

## 3. 코딩 컨벤션

- **CSS variables (`--b-*`)** 가 디자인 토큰 SoT. `src/styles/brand.css`. hex·shadow·radii 박지 말고 토큰 참조.
- **반복 패턴 클래스 추출** — sticky note, primary CTA, image cover shade 등 2회 이상 동일하게 반복되는 인라인 클러스터는 `src/styles/components.css`로 추출. layout-only 인라인(position·top·width·transform·rotate 등)은 인라인 유지.
- **컴포넌트**: 한 화면 = 한 `.astro` 페이지 + 작은 컴포넌트 다수 (`src/components/`).
- **콘텐츠 = Markdown collection** + Zod schema 검증 (`src/content.config.ts`).
- **API 엔드포인트 0개**. 사용자 데이터 수집 0. 카톡 외부 link만.
- **사용자 데이터 0** — PRD §보안 영구. localStorage (Notes 진도) 외 server-side 데이터 없음.

## 4. 사이클 정보

- **현재 진행**: v1-prototype (2026-05-10~)
- **기획 컨텍스트**: `planning/cycles/v1-prototype/` 참조 (intent · brand-guide · sketch · prd · design · architecture · data-model · build/).
- **Design SoT**: `site/` (plain HTML+CSS+JS, 빌드 단계의 시각 정합 기준).
- **빌드 계획**: `planning/cycles/v1-prototype/build/` 9 phase.

## 5. 자동화 룰

- `.claude/rules/perf-astro.md` — Astro 5 perf baseline (Image·Font·Critical CSS·Vercel adapter).
- 빌드 단계는 `python3 .claude/skills/zero-to-prototype/scripts/run-phases.py v1-prototype` 자동 실행.
- needs_review 게이트: 보안·시크릿·DB 스키마·외부 호출·비결정성·권한 상승 시 사용자 승인 필수.

## 6. brand voice 한 줄

> "LLM이 만든 그럴듯한 초고 위에, 감성 한 스푼."

마케팅 클리셰("혁신적인", "10x", "AI-powered") 회피. 친근·반말 OK, 멘토 톤보다 동료 톤. brand-guide.md §10 금지 사항 8가지.
