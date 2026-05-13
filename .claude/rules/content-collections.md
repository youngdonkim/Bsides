---
name: content-collections
description: Bsides 콘텐츠 운영 룰 — Markdown collections, Zod schema 검증, frontmatter 규약.
paths:
  - 'src/content/**/*'
  - 'src/content.config.ts'
  - 'src/lib/content.ts'
  - 'src/data/note-groups.ts'
  - 'src/data/current-member.ts'
  - 'src/data/operator.ts'
---

# Content collections

Bsides는 DB 0 — 모든 운영 콘텐츠가 Markdown collection. `src/content/`.

## 두 컬렉션

- `src/content/notes/` — 학습 노트 13단계. `01-intent.md` ~ `13-retro.md`. 파일명 = slug (`NN-kebab`).
- `src/content/progress/` — 회차별 진행상황. `round-N-slug.md`.

## Schema 검증

- SoT: `src/content.config.ts`. Zod 스키마로 frontmatter 필드 검증. 빌드 시점에 검증 실패 → 빌드 fail.
- 새 필드 추가 시 schema·기존 모든 entry·렌더링 컴포넌트 세 곳 동시 갱신 필요.
- frontmatter 변경은 `needs_review` 트리거 (DB 스키마 변경에 준함).

## frontmatter 규약

### notes
- `num`: 1~13 (integer)
- `en`/`ko`: 영문·한글 제목
- `group`: `discover-plan`·`design-architect`·`build-ship` 중 하나
- `lead`·`italic`·`h1_lead`·`workshop_text`: 본문 partials
- `read_time`: "N분" 형식

### progress
- `round`: 회차 번호
- `date`: ISO date
- `member`: 멤버 이름
- `member_kind`: 멤버 카테고리
- `title`·`lead`: 카드·상세 헤더
- `cover.gradient`: `olive`·`sand`·`pink` 중 하나 (cover 색)

## 본문 안 HTML 인라인

- markdown 안에 raw HTML 인라인 허용 (Astro markdown processor 기본).
- 반복 패턴(예: "한 스푼 메모" sticky note)은 components.css 클래스 사용 (`.b-note-card`·`.b-note-card-title`·`.b-note-card-body`).
- 같은 패턴 한 번 더 등장하면 클래스 추출 검토 — design-system 룰 참조.

## 데이터 모듈

- `src/data/` 의 `current-member.ts`·`operator.ts`·`note-groups.ts` 는 TypeScript module. frontmatter로 빼기 어려운 cross-cutting 데이터 (현재 사이클 멤버·운영자 카톡 link·노트 그룹 분류).
- 변경 시 type 정의 같이 갱신.
