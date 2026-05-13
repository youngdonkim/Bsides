# Bsides

> 혼자가 가능해진 시대, 출시까지 같이 가는 작은 메이커 동아리.
> 운영 · 현지 / hi@bsides.kr / [카톡 @bsides](https://open.kakao.com/o/bsides) / [bsides.kr](https://bsides.kr)

비즈니스 컨텍스트·아키텍처·디자인 결정은 `planning/cycles/<current>/` 하위 문서에 있어. 필요할 때 다음을 읽어:

- @planning/cycles/v1-prototype/intent.md — 제품 의도·타겟·성공 기준
- @planning/cycles/v1-prototype/architecture.md — 스택·시스템 결정·디렉토리
- @planning/cycles/v1-prototype/brand-guide.md — 컬러·voice·금지

토픽별 path-scoped 룰은 `.claude/rules/` 에 분리되어 있어 (해당 파일 작업 시 자동 로드):
- `design-system.md` — CSS 토큰, 클래스 추출, 인라인 정책, Astro Font 매칭
- `content-collections.md` — Markdown collections, Zod schema, frontmatter
- `deploy.md` — Vercel·GitHub·PR 머지·CI 워크플로
- `perf-astro.md` — Astro 5 perf baseline (Image·Font·Critical CSS)

## 코딩 컨벤션

- **TypeScript strict**. Node 22+ (Astro 5 engine).
- **컴포넌트**: 한 화면 = 한 `.astro` 페이지 (`src/pages/`) + 작은 컴포넌트 (`src/components/`).
- **콘텐츠 = Markdown collection** + Zod schema 검증 (`src/content.config.ts`).
- **API 엔드포인트 0개. 사용자 데이터 수집 0** — 카톡 외부 link만. localStorage(Notes 진도) 외 server-side 데이터 없음.

## brand voice

> "LLM이 만든 그럴듯한 초고 위에, 감성 한 스푼."

- 마케팅 클리셰 회피 — "혁신적인", "10x", "AI-powered" 등 (자세히는 brand-guide §10 금지 8가지).
- 친근·반말 OK, 멘토 톤보다 동료 톤.

## needs_review 게이트

다음 변경 시 사용자 승인 필수 — 자동 진행 X:

- 인증·권한·암호화 코드 신규/변경
- 외부 API 키·시크릿 신규 사용
- DB 스키마 변경 (Bsides에선 content collection Zod schema 변경 포함)
- 외부 API 호출 신규 추가 (특히 비용·사용자 데이터 외부 전송)
- 비결정성 의존 (타임존·시스템 시간·무작위 시드)
- sudo·root·OS 권한·파일시스템 외부 접근
- 외부 인프라 변경 (도메인·DNS·Vercel·GitHub secrets)
- **배포(`vercel --prod`·`vercel deploy`)** — 사용자 명시 지시 시에만. PreToolUse hook이 차단함. 자세히는 `.claude/rules/deploy.md`.
