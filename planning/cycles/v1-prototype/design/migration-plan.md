---
cycle: v1-prototype
created_at: 2026-05-12
updated_at: 2026-05-12
target: Astro 5.x + @astrojs/vercel
---

# 1. 디자인 토큰 추출

**원천**: `site/styles/brand.css` (CSS variables — surface·ink·olive·sticky·line·typography·radii·shadow).

**대상**: `src/styles/brand.css` 그대로 paste. CSS variables가 코드 어디서든 `var(--b-olive)` 등으로 그대로 동작.

**변경 항목 1개**: Google Fonts `@import url("...")` 라인 제거. Astro Font integration으로 대체 (`astro.config.mjs` `fonts:` 필드). Pretendard·Pretendard JP는 jsDelivr CDN 그대로 (Astro Font는 jsDelivr 미지원이라 self-host or CDN 그대로).

# 2. 컴포넌트 매핑 표

HTML 섹션을 `.astro` 컴포넌트로 분해.

| 현재 site/ 마크업 | Astro 컴포넌트 | 위치 |
|---|---|---|
| Header (sticky nav + Bsides 로고 + Notes/진행상황 link + CTA) | `<Header />` | `src/components/Header.astro` |
| Footer (운영자 정보·카톡·이메일) | `<Footer />` | `src/components/Footer.astro` |
| 페이지 전체 head + body + Header + Footer 보일러플레이트 | `<BaseLayout title desc og>` | `src/layouts/BaseLayout.astro` |
| Hero (sup-label + h1 + 보조 + CTA + sticky cluster) — 메인 전용 | `<Hero />` | `src/components/home/Hero.astro` |
| 운영방식 4단계 카드 grid + 객원→정식 4단계 callout | `<HowItWorks />` | `src/components/home/HowItWorks.astro` |
| 이번 사이클 멤버 카드 (live pill·메타 4종·이미지) | `<MentorCard member={...} />` | `src/components/home/MentorCard.astro` |
| 사이 회차 멘토 카드 variant (waiting 마스코트) | 위 컴포넌트의 `member={null}` 분기 | 동일 컴포넌트 안 |
| 최근 진행상황 card grid (메인) + 진행상황 목록 페이지 grid | `<ProgressCard post={...} />` + grid wrapper | `src/components/ProgressCard.astro` |
| 진행상황 0개 빈 상태 | `<ProgressEmpty />` | `src/components/ProgressEmpty.astro` |
| 신청 anchor 섹션 (#apply) | `<ApplySection />` | `src/components/ApplySection.astro` |
| 진행상황 상세 (hero image + sticky note + article + workshop callout + prev/next nav) | `<ProgressDetail post={...} />` | `src/components/ProgressDetail.astro` |
| Notes 목차 row (단계 번호 + 영문/한국어 제목 + lead + 읽음 배지) | `<NoteRow note={...} />` | `src/components/notes/NoteRow.astro` |
| Notes 그룹 section (sup-label + lead + rows) | `<NoteGroup ...>` (slot으로 rows 받음) | `src/components/notes/NoteGroup.astro` |
| Notes 단계 페이지 (meta + h1 + mascot ribbon + article + workshop callout + prev/next) | `<NoteDetail note={...} />` | `src/components/notes/NoteDetail.astro` |
| 404 mascot + 한 줄 + 메인 link | `<NotFoundBlock mascot copy />` | `src/components/NotFoundBlock.astro` |
| Workshop funnel callout (Notes 단계·Progress 상세 공통) | `<WorkshopCallout text />` | `src/components/WorkshopCallout.astro` |
| Sticky note (3색 회전 + 손글씨 카피) | `<StickyNote color rotate>{children}</StickyNote>` | `src/components/StickyNote.astro` |

**컴포넌트 인터페이스 (TypeScript)**:
- `Header.astro` — props 없음. `Astro.url.pathname`으로 active nav 판정 (현재 site/는 body data-page로 처리 — Astro에선 더 자연스러움).
- `BaseLayout.astro` — props: `title`, `description`, `ogTitle`, `ogDescription`, `currentNote?` (Notes 진도 트래킹용).
- `MentorCard.astro` — props: `member: CurrentMember | null`. null이면 사이 회차 variant.
- `ProgressCard.astro` — props: `post: CollectionEntry<'progress'>`.
- `NoteRow.astro` — props: `note: CollectionEntry<'notes'>`.
- `NoteDetail.astro` — props: `note`, `prev?`, `next?` (목차 sorted index 기반).

# 3. 화면 단위 우선순위 — phase 분할 후보 (Build plan 입력)

Build plan (7단계)에서 확정. 여기선 큰 그림만.

**Phase 0 — 셋업·토큰**:
- Astro 프로젝트 init (`npm create astro@latest`)
- `@astrojs/vercel` adapter 설치
- `src/styles/brand.css` paste
- `astro.config.mjs`에 fonts·integrations 설정
- `BaseLayout.astro` + `Header.astro` + `Footer.astro` (보일러플레이트)
- 첫 빌드 → Vercel preview deploy 성공 검증

**Phase 1 — 메인 + 진행상황 트랙**:
- `src/content.config.ts`에 `progress` collection 정의
- 메인 페이지 모든 섹션 (Hero·HowItWorks·MentorCard·ProgressCard grid·ApplySection)
- 진행상황 목록 + 상세 (collection 기반)
- 빈 상태·사이 회차 conditional
- 첫 사용자 시나리오 통과 검증 (S1·S2·S3)

**Phase 2 — Notes 트랙**:
- `notes` collection 정의
- 13개 Markdown 콘텐츠 추출 (Python 1회성 스크립트로 site/notes-*.html → `src/content/notes/*.md`)
- Notes 목차 (3 그룹 + 13 row)
- Notes 단계 페이지 (prev/next 자동)
- localStorage 진도 JS port

**Phase 3 — 부속 화면 + 최적화**:
- 404 페이지
- design-system.html은 `public/`에 그대로 paste
- Astro `<Image />` 적용 (cover 이미지)
- Font integration 검증 (subset 적용·CWV 측정)
- `@vercel/analytics` 통합
- sitemap·robots.txt 자동 생성

# 4. 백엔드 연동 분리 — 해당 없음

PRD §보안 "사용자 데이터 수집 0" 확정. API 엔드포인트 0개. 외부 데이터 fetch도 빌드 시점 only (Markdown 콘텐츠는 git 안 자체 source).

mock → 실제 API 교체 단계 **없음**. v1 prototype에서 v2 이후로도 이 결정 유지될 가능성 높음 (intent 비목표 영구).

# 5. 마이그레이션 후 검증 체크리스트

- [ ] Vercel preview deploy 성공 (Phase 0 끝)
- [ ] PRD §성능 임계값 통과 — LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1 (Lighthouse 측정)
- [ ] 모든 internal link 작동 (현재 site/와 동일)
- [ ] sketch.md 5 시나리오 (S1~S5) 통과
- [ ] Notes 진도 localStorage 동작 (목차 read 배지)
- [ ] 헤더 active nav 동작 (현재 경로 기반)
- [ ] OG image·favicon meta 모든 페이지
- [ ] 모바일 320px ~ 1920px 반응형
- [ ] Vercel Web Analytics 데이터 수집 확인
