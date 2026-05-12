---
platform: web
cycle: v1-prototype
created_at: 2026-05-12
updated_at: 2026-05-12
---

# 기술 스택

| 카테고리 | 결정 | 대안 | 이유 |
|---|---|---|---|
| 언어 | **TypeScript** | JavaScript | content schema Zod 타입 안전 + 미래 멤버 협업 시 명확성 |
| 프레임워크 | **Astro 5.x** | Next.js 14, 11ty | 콘텐츠 1급 시민 (`src/content/` collections) · zero-JS default · 현재 site/ HTML paste-and-go |
| DB | **없음** (Markdown collections) | SQLite, Postgres | PRD §보안 "사용자 데이터 수집 0" 확정. 콘텐츠 source = git |
| 인프라 | **Vercel** + `@astrojs/vercel` adapter | Cloudflare Pages, Netlify | Astro 통합 매끄러움 · preview URL 자동 · Web Analytics 무료 zero-config |
| 외부 서비스 | **Vercel Web Analytics** (F10) · **Astro Font** integration (Google Fonts provider) · **jsDelivr CDN** (Pretendard) | Plausible, self-host fonts | zero-config · 무료 · privacy friendly (no cookies) |

# 시스템 구조

미니멀 — 정적 사이트라 레이어 분리 과한 추상화는 불필요.

```
사용자 (외부 잠재 객원)
   │ HTTPS request
   ▼
Vercel Edge (CDN)
   │ 정적 .html 응답
   ▼
브라우저 — Astro 빌드 출력 (HTML + 최소 JS + CSS + assets)
   │
   ├─ 위 fold 즉시 렌더 (critical CSS inline)
   ├─ scripts/notes-progress.js (defer) — localStorage 진도 + nav active
   ├─ Vercel Analytics SDK — 페이지 뷰 수집
   └─ 카톡 외부 link 클릭 → 카톡 도메인으로 이탈
```

## 레이어

- **presentation** — `src/pages/`·`src/layouts/`·`src/components/`
- **content (data layer 대체)** — `src/content/notes/`·`src/content/progress/`·`src/data/`
- **styles** — `src/styles/brand.css`·`components.css`
- **client scripts** — `src/scripts/notes-progress.js` (단일 파일, 100 lines 미만)

## 모듈 경계

`features/` 분리 대신 **컴포넌트 단위 + collection 단위**. 정적 사이트 크기 (~7 화면) 라 features 추상화는 over-engineering.

## 핵심 데이터 흐름

### F1·F3·F4 통합 흐름 — 진행상황 콘텐츠 추가

```
1. 운영자: 워크샵 후 raw 메모/녹음
2. 운영자: LLM 가공 → Markdown 본문 + AI 이미지 path
3. 운영자: src/content/progress/round-N-slug.md 추가, git push
4. Vercel: webhook 받음 → npm run build → astro 빌드
5. Vercel: 정적 HTML dist/ 배포 (CDN propagate ~30s)
6. 외부 방문자: /progress/round-N-slug 새 URL 접근 가능
   + 메인 "최근 진행상황" grid 자동 update
   + sitemap.xml 자동 갱신
```

### F5 — 객원 신청 흐름

```
사용자 → #apply anchor scroll → 카톡 link click
       → 외부 카톡 도메인 이동 (사이트 이탈)
       → 카톡 메시지 전송 (운영자 카톡으로 수신)
```

신청 데이터 = 카톡 내부에만 존재. 사이트는 redirect만.

# API 명세 — 외부 0개

PRD §보안 확정. HTTP API endpoint 0.

## 내부 (컴포넌트 인터페이스)

`design/migration-plan.md §2` 컴포넌트 매핑 표 참조 — 14개 컴포넌트의 props 시그니처. 핵심:

- `BaseLayout(props: { title, description, ogTitle?, ogDescription? })`
- `MentorCard(props: { member: CurrentMember | null })` — null이면 사이 회차 variant
- `ProgressCard(props: { post: CollectionEntry<'progress'> })`
- `NoteRow(props: { note: CollectionEntry<'notes'> })`
- `NoteDetail(props: { note, prev?, next? })`

## 외부 fetch

- 빌드 시점: Google Fonts (Astro Font integration) · jsDelivr Pretendard
- 런타임: Vercel Analytics SDK 1개 (수집 endpoint는 Vercel 내부)
- 외부 사용자 데이터 fetch: **없음**

# 디렉토리 구조

```
Bsides/
├── src/
│   ├── pages/
│   │   ├── index.astro                  # 메인 (between-cycles variant 포함)
│   │   ├── 404.astro                    # 사이트 전체 404
│   │   ├── progress/
│   │   │   ├── index.astro              # 목록 (빈 상태 conditional)
│   │   │   └── [slug].astro             # 상세
│   │   └── notes/
│   │       ├── index.astro              # 목차 + 3 그룹
│   │       └── [slug].astro             # 단계 페이지
│   ├── layouts/
│   │   └── BaseLayout.astro             # head + Header + Footer wrapper
│   ├── components/
│   │   ├── Header.astro · Footer.astro
│   │   ├── home/
│   │   │   ├── Hero.astro · HowItWorks.astro · MentorCard.astro · ApplySection.astro
│   │   ├── ProgressCard.astro · ProgressEmpty.astro · ProgressDetail.astro
│   │   ├── notes/
│   │   │   ├── NoteRow.astro · NoteGroup.astro · NoteDetail.astro
│   │   ├── WorkshopCallout.astro · StickyNote.astro · NotFoundBlock.astro
│   ├── content/
│   │   ├── notes/
│   │   │   ├── 01-intent.md ... 13-retro.md
│   │   └── progress/
│   │       └── round-3-mimirog-launch.md (+ 추후 회차)
│   ├── content.config.ts                # Zod schema
│   ├── data/
│   │   ├── operator.ts                  # OperatorMeta const
│   │   ├── current-member.ts            # CurrentMember (또는 content/_state/...)
│   │   └── note-groups.ts               # 그룹 매핑 const
│   ├── styles/
│   │   ├── brand.css                    # 디자인 토큰 SoT
│   │   └── components.css
│   └── scripts/
│       └── notes-progress.js            # localStorage 진도
├── public/
│   ├── assets/
│   │   ├── spooni/*.svg                 # 마스코트 10개
│   │   ├── og.svg
│   │   └── favicon.svg
│   ├── design-system.html               # DS 레퍼런스 (운영 내부용)
│   └── robots.txt
├── astro.config.mjs                     # adapter, fonts, integrations
├── tsconfig.json
├── package.json
└── planning/                            # 사이클 산출물 (현재 위치)
```

깊이 3-depth까지만. 빌드 단계에서 추가 정밀화.

# 횡단 룰·표준 입력 — §2.9

**`.claude/rules/` 적용 상태**:

| 룰 | 적용 여부 | 어디서 |
|---|---|---|
| `kakao-auth-share.md` | **N/A** | 인증·OAuth 미사용 (PRD §보안 사용자 데이터 0) |
| `sensitive-data-exposure.md` | **부분 적용** | 운영자 카톡 URL·이메일은 brand identity. 시크릿은 Vercel 환경변수만 (분석 토큰 등) |
| `page-auth-pattern.md` | **N/A** | 인증 가드 페이지 없음 |
| `file-upload-security.md` | **N/A** | 업로드 없음 |
| `ui-ux-baseline.md` | **이미 적용** | 5-design.md에서 입력됨 — `site/` 가 그 결과 |
| `perf-astro.md` (§2.10에서 자동 생성) | **적용** | Astro adapter·Image·Font·Vercel 통합. 빌드 phase에서 자동 활용 |

cycle 진행 중 위 룰에 위배되는 결정 필요 시 ADR 작성 (`planning/docs/adr/`).

# 누락 점검 — §2.11

## PRD Must 동작 위한 결정 cover 여부

| F# | 기능 | 필요한 결정 | 결정됨 |
|---|---|---|---|
| F1 | 메인 페이지 | SSG framework·라우팅·콘텐츠 source | ✅ |
| F3 | 진행상황 상세 | dynamic routing·collection schema | ✅ |
| F4 | 운영 워크플로 (git push 자동 배포) | CI/CD·webhook | ✅ Vercel 기본 |
| F5 | 카톡 신청 link | OperatorMeta const + 외부 link | ✅ |
| F7 | 반응형 | CSS break point | ✅ components.css `@media (max-width: 900px)` 기존 |
| F8 | 헤더·푸터 | Layout 컴포넌트 | ✅ |

## Cross-cutting 결정

| 항목 | 결정 |
|---|---|
| **로깅** | Vercel build log + 런타임 console (정적 사이트라 서버 로그 없음) |
| **에러 핸들링** | 빌드 시점: schema 검증 실패 → 빌드 중단. 런타임: 정적이라 에러 거의 없음. 잘못된 path → 404 페이지 |
| **환경 변수** | Vercel 대시보드. `.env.local` (gitignore). public 노출 변수만 `PUBLIC_` 접두사 |
| **CI/CD** | Vercel webhook → git push → 자동 빌드·배포. main = prod, 기타 branch = preview URL |
| **관측성** | Vercel Web Analytics (PV·referer·외부 link click) + Vercel build log |
| **시크릿** | Vercel 환경변수만. 코드에 박지 않기. 현재 시크릿 0 (analytics 토큰조차 build-time 아님) |
| **모니터링·alerting** | Vercel deploy 실패 시 운영자 이메일 알림 (Vercel 기본) |

# 마이그레이션

- **분석**: [design/migration-analysis.md](design/migration-analysis.md)
- **계획**: [design/migration-plan.md](design/migration-plan.md)

핵심 — Claude Design 출력을 site/에서 이미 plain HTML로 정리한 덕분에 Astro paste-and-go 수준 (공수 작음). Phase 0~3 분할.

# 데이터 모델

별도 산출물: [data-model.md](data-model.md)

4 엔티티 — `ProgressPost`·`NotePost`·`CurrentMember`·`OperatorMeta`. 모두 git 안 Markdown 또는 TS const. DB 없음.

# 사이클 업데이트 모드 — N/A (첫 사이클)

v2 사이클에서 §5 패턴으로 업데이트.
