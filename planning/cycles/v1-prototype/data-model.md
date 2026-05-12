---
platform: web
cycle: v1-prototype
created_at: 2026-05-12
updated_at: 2026-05-12
storage: Markdown content collections (Astro). No DB.
---

# 엔티티

DB 없음. 모든 데이터 = git에 박힌 Markdown 파일 (`src/content/`). Astro `defineCollection` + Zod schema로 frontmatter 검증.

## 1. ProgressPost — 진행상황 회차

**위치**: `src/content/progress/{slug}.md`
**slug**: 파일명에서 자동 추출 (예: `round-3-mimirog-launch`)

### Frontmatter schema

| 필드 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `round` | int | required, ≥ 1 | 회차 번호 (`3`) |
| `date` | date (`YYYY-MM-DD`) | required | 회차 진행 날짜 (`2026-05-04`) |
| `member` | string | required | 멤버 이름 (`김도현`) |
| `title` | string | required, ≤ 80자 | 본문 제목 (`미미로그 출시 후기와 다음 사이클`) |
| `lead` | string | required, ≤ 150자 | 카드·메타용 1~2줄 요약 |
| `mentor` | string | optional | 외부 객원 멘토 있을 때만 |
| `cover` | object \| null | optional | `{ image?: string, gradient?: 'olive' \| 'sand' \| 'pink' }` — image path 없으면 brand 정합 gradient placeholder |
| `published` | boolean | default `true` | draft 처리용 |

### Body

Markdown. h3·p·인라인 이미지·sticky note (커스텀 component) 가능.

### 파생 데이터 (빌드 시점 계산)

- `slug` — 파일명
- `prev` / `next` — date 기준 sort 후 인덱스 (자동)
- `og:image` — `cover.image` 있으면 그 path, 없으면 사이트 공통 `assets/og.svg`

### 인덱스

- 기본 sort: `date` desc (최신순)
- 메인 미리보기: 최신 3개

---

## 2. NotePost — Notes 학습 단계

**위치**: `src/content/notes/{NN-slug}.md` (예: `01-intent.md`)

### Frontmatter schema

| 필드 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `num` | string | required, `/^\d{2}$/` | 단계 번호 zero-padded (`01`) |
| `en` | string | required | 영문 제목 (`Intent`) |
| `ko` | string | required | 한국어 제목 (`의도`) |
| `group` | enum | required | `'discover-plan' \| 'design-architect' \| 'build-ship'` |
| `read_time` | string | required | `'약 8분 읽기'` |
| `h1_lead` | string | required | 페이지 h1 보조 (`의도 — 무엇을, 누구를 위해, 왜.`) |
| `lead` | string | required, ≤ 180자 | 메타 description + 카드 1~2줄 |
| `italic` | string | required | 본문 첫 italic 인용 한 줄 |
| `workshop_text` | string | required | 본문 끝 funnel callout 내용 |
| `published` | boolean | default `true` | |

### Body

Markdown 본문. 운영자가 자유롭게 h3·p·sticky note·이미지 구성. brand voice 정합 5~15분 분량.

### 파생 데이터

- `slug` — 파일명에서 추출
- `prev` / `next` — `num` ASC sort 후 인덱스
- `group_en` / `group_ko` — `group` enum 매핑 (config 또는 const)

### 그룹 매핑 (const, 별도 파일)

```ts
// src/data/note-groups.ts
export const NOTE_GROUPS = {
  'discover-plan':    { en: 'Discover & Plan',    ko: '의도·기획',       range: ['01', '04'] },
  'design-architect': { en: 'Design & Architect', ko: '디자인·아키텍처', range: ['05', '08'] },
  'build-ship':       { en: 'Build & Ship',       ko: '빌드·배포',       range: ['09', '13'] },
} as const;
```

### 인덱스

- 기본 sort: `num` ASC
- 그룹별: `group` 동일한 것 묶음, 안에서 `num` ASC

---

## 3. CurrentMember — 이번 사이클 멤버

**위치**: `src/content/_state/current-member.md` (collection 1-entry 또는 single file content)
대안: `src/data/current-member.ts` (사이클당 빈도 낮으니 그냥 TS 모듈도 OK)

### Schema

| 필드 | 타입 | 제약 | 설명 |
|---|---|---|---|
| `project_title` | string | required | (`도토리룸 — 원룸 계약, 빠진 특약 같이 잡아요`) |
| `member_name` | string | required | (`김도현`) |
| `member_kind` | string | required | (`본인 프로젝트`) |
| `curriculum` | string | required | (`아이템·기획·개발·디자인·출시·홍보 6단계`) |
| `progress_label` | string | required | (`3회차 (6회차 사이클)`) |
| `next_workshop_at` | datetime | optional | ISO 8601 (`2026-05-18T20:00+09:00`) |
| `next_workshop_format` | string | optional | (`온라인 화상`) |
| `live_pill_label` | string | required | (`다음 워크샵 D-7`, 빌드 시 계산도 가능) |
| `current_round_slug` | string | required | progress collection slug |
| `cycle_state` | enum | required | `'active' \| 'between'` — between이면 사이 회차 variant 렌더링 |

### `cycle_state`가 `'between'`이면

대부분의 필드는 `null` 또는 placeholder로. 컴포넌트가 자동으로 waiting variant 렌더 (현재 site/index-between-cycles.html의 마크업).

---

## 4. OperatorMeta — 운영자·연락처

**위치**: `src/data/operator.ts` (변경 매우 드물어 상수)

### Schema

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

footer·apply section·meta 등 모든 곳이 이 const 참조.

---

# 관계

- `CurrentMember.current_round_slug` → `ProgressPost.slug` (1:1, optional)
- `NotePost` ↔ `ProgressPost`: 직접 관계 없음. 다른 축의 콘텐츠.

# 인덱스 (Astro content collection 빌드 시점 계산)

- Progress: `date` DESC
- Notes: `num` ASC

# 파생·집계 — 모두 즉시 계산 (캐시 X)

빌드 시점 1회 계산. 정적 사이트라 캐시 불필요.

# 사용자별 진도 데이터 — server 0

- localStorage key: `bsides:notes:read:{num}` — 단순 `'1'` 저장
- localStorage key: `bsides:notes:read:list` (옵션, 차후 batch 조회용)
- 서버 동기화 X. 디바이스마다 독립. 의도된 trade-off (PRD §보안 "사용자 데이터 수집 0").
