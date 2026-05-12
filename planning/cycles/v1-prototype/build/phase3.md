# Phase 3: Content Collections & Types

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

phase 0~2: 프로젝트 셋업, layout, 메인 정적 섹션

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

notes·progress content collections 정의 + Zod schema + CurrentMember/NoteGroups const + sample 콘텐츠 각 1개. `astro sync`로 타입 생성 검증.

## 작업 내용

### 3.1 src/content.config.ts

```ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    num: z.string().regex(/^\d{2}$/),
    en: z.string(),
    ko: z.string(),
    group: z.enum(['discover-plan', 'design-architect', 'build-ship']),
    read_time: z.string(),
    h1_lead: z.string(),
    lead: z.string().max(180),
    italic: z.string(),
    workshop_text: z.string(),
    published: z.boolean().default(true),
  }),
});

const progress = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/progress' }),
  schema: z.object({
    round: z.number().int().positive(),
    date: z.coerce.date(),
    member: z.string(),
    title: z.string().max(80),
    lead: z.string().max(150),
    mentor: z.string().optional(),
    cover: z
      .object({
        image: z.string().optional(),
        gradient: z.enum(['olive', 'sand', 'pink']).optional(),
      })
      .nullable()
      .optional(),
    published: z.boolean().default(true),
  }),
});

export const collections = { notes, progress };
```

### 3.2 src/data/note-groups.ts

```ts
export const NOTE_GROUPS = {
  'discover-plan': {
    en: 'Discover & Plan',
    ko: '의도·기획',
    lead: '무엇을, 누구를 위해, 왜 만드는지부터 깎아내는 단계.',
    range: ['01', '04'] as const,
  },
  'design-architect': {
    en: 'Design & Architect',
    ko: '디자인·아키텍처',
    lead: '진짜 만들 모양을 시각·기술 결정으로 박는 단계.',
    range: ['05', '08'] as const,
  },
  'build-ship': {
    en: 'Build & Ship',
    ko: '빌드·배포',
    lead: '실제로 코드를 짜고 동작하는 상태로 만드는 단계.',
    range: ['09', '13'] as const,
  },
} as const;

export type NoteGroupKey = keyof typeof NOTE_GROUPS;
```

### 3.3 src/data/current-member.ts

```ts
export type CycleState = 'active' | 'between';

export interface CurrentMember {
  cycle_state: CycleState;
  project_title: string | null;
  member_name: string | null;
  member_kind: string | null;
  curriculum: string | null;
  progress_label: string | null;
  next_workshop_at: string | null;  // ISO 8601
  next_workshop_format: string | null;
  live_pill_label: string | null;
  current_round_slug: string | null;
}

export const CURRENT_MEMBER: CurrentMember = {
  cycle_state: 'active',
  project_title: '도토리룸 — 원룸 계약, 빠진 특약 같이 잡아요',
  member_name: '김도현',
  member_kind: '본인 프로젝트',
  curriculum: '아이템·기획·개발·디자인·출시·홍보 6단계',
  progress_label: '3회차 (6회차 사이클)',
  next_workshop_at: '2026-05-18T20:00:00+09:00',
  next_workshop_format: '온라인 화상',
  live_pill_label: '다음 워크샵 D-7',
  current_round_slug: 'round-3-mimirog-launch',
};
```

### 3.4 sample 콘텐츠 — Notes 01-intent.md

`src/content/notes/01-intent.md` — site/notes-01-intent.html에서 본문 추출 + frontmatter:

```md
---
num: "01"
en: Intent
ko: 의도
group: discover-plan
read_time: 약 8분 읽기
h1_lead: 의도 — 무엇을, 누구를 위해, 왜.
lead: 한 사이클의 첫 단계. 출처 스토리·문제·타겟·성공 기준·가설을 손에 잡힐 정도로 구체화해.
italic: '"좋은 의도 없이 시작한 프로젝트는, 좋은 코드로도 못 살린다." — 운영 노트'
workshop_text: Intent 단계는 워크샵 첫 회차에서 운영자가 직접 인터뷰로 깎아드려요. 본인의 출처 스토리를 직접 말로 풀면서 다섯 항목이 자연스레 잡혀요.
---

Intent 단계는 한 사이클의 첫 단추예요. ...
```

본문은 site/notes-01-intent.html의 article 안 내용을 Markdown으로 변환. h3·p·sticky note(custom component 또는 일반 callout) 보존.

### 3.5 sample 콘텐츠 — Progress round-3

`src/content/progress/round-3-mimirog-launch.md`:

```md
---
round: 3
date: 2026-05-04
member: 김도현
title: 미미로그 출시 후기와 다음 사이클
lead: 출시 직후 일주일, 사용자 피드백 22개를 어떻게 추리고 다음 회차 주제로 묶었는지.
cover:
  gradient: olive
---

이번 회차는 출시 직후 첫 주를 어떻게 보냈는지...
```

### 3.6 헬퍼 — getSortedNotes / getSortedProgress

`src/lib/content.ts`:

```ts
import { getCollection, type CollectionEntry } from 'astro:content';

export async function getSortedNotes(): Promise<CollectionEntry<'notes'>[]> {
  const all = await getCollection('notes', ({ data }) => data.published);
  return all.sort((a, b) => a.data.num.localeCompare(b.data.num));
}

export async function getSortedProgress(): Promise<CollectionEntry<'progress'>[]> {
  const all = await getCollection('progress', ({ data }) => data.published);
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export async function getNoteSiblings(currentNum: string) {
  const sorted = await getSortedNotes();
  const idx = sorted.findIndex((n) => n.data.num === currentNum);
  return {
    prev: idx > 0 ? sorted[idx - 1] : null,
    next: idx < sorted.length - 1 ? sorted[idx + 1] : null,
  };
}

export async function getProgressSiblings(currentSlug: string) {
  const sorted = await getSortedProgress();
  const idx = sorted.findIndex((p) => p.id === currentSlug);
  return {
    prev: idx < sorted.length - 1 ? sorted[idx + 1] : null,  // 과거가 prev
    next: idx > 0 ? sorted[idx - 1] : null,  // 더 최신이 next
  };
}
```

### 3.7 astro sync 검증

`npm run astro sync` → `.astro/content.d.ts` 생성. 타입 안전 확인.


## Acceptance Criteria

```bash
npm run astro sync     # 타입 생성
npm run build          # 빌드 성공 (collection 검증 통과)
npm run typecheck      # CollectionEntry 타입 정합
```

추가: 빌드 후 `.astro/content.d.ts` 존재 확인 + frontmatter 1개 일부러 깨뜨려서 (`num: "x"` 같은) 빌드 실패하는지 검증, 후 원복.

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 3 status를 `"completed"`로 변경.

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

이 phase 특이사항: 스키마 정의·sample 콘텐츠만. needs_review 트리거 없음.

## 주의사항

- Zod schema 변경 시 `npm run astro sync` 재실행 필수.
- sample 콘텐츠는 진짜 frontmatter 값 — 추후 추가될 모든 콘텐츠가 같은 schema 통과해야 함.
- `lib/content.ts`의 sort는 `localeCompare` 사용 — num이 zero-padded 문자열이므로 안전.
