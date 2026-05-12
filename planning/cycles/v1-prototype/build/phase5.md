# Phase 5: Notes Track

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

phase 3: content collections·types · phase 4: ProgressCard·MentorCard 패턴 참조용

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

Notes 목차 (3 그룹) + 13 단계 페이지 + localStorage 진도 + 13 Markdown 콘텐츠 추출. S1 학습 코스 흐름 통과.

## 작업 내용

### 5.1 NoteRow.astro

`src/components/notes/NoteRow.astro`:

```astro
---
import type { CollectionEntry } from 'astro:content';
interface Props { note: CollectionEntry<'notes'>; }
const { note } = Astro.props;
const d = note.data;
const slug = note.id;  // 예: '01-intent'
---
<a href={`/notes/${slug}`} data-note-step={d.num} style="display: grid; grid-template-columns: 56px 1fr auto; ...">
  <span style="font-family: var(--b-font-hand); font-size: 32px; color: var(--b-olive);">{d.num}</span>
  <div>
    <div style="display: flex; gap: 10px; margin-bottom: 4px;">
      <span class="t-caption" style="color: var(--b-olive); text-transform: uppercase;">{d.en}</span>
      <span class="t-title-3">{d.ko}</span>
    </div>
    <div class="t-body" style="...">{d.lead}</div>
  </div>
  <span data-read-badge style="display: none; ...">✓ 읽음</span>
</a>
```

### 5.2 NoteGroup.astro

```astro
---
import type { NoteGroupKey } from '../../data/note-groups';
import { NOTE_GROUPS } from '../../data/note-groups';
interface Props { groupKey: NoteGroupKey; }
const { groupKey } = Astro.props;
const g = NOTE_GROUPS[groupKey];
---
<section style="padding: 32px 0px;">
  <div class="b-container">
    <div style="margin-bottom: 18px;">
      <div style="...sup-label...">{g.en}</div>
      <h2 class="t-title-2">{g.ko}</h2>
      <div class="t-body" style="...">{g.lead}</div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 12px;">
      <slot />
    </div>
  </div>
</section>
```

### 5.3 NoteDetail.astro

`src/components/notes/NoteDetail.astro`:

```astro
---
import type { CollectionEntry } from 'astro:content';
import { render } from 'astro:content';
import { NOTE_GROUPS } from '../../data/note-groups';

interface Props {
  note: CollectionEntry<'notes'>;
  prev: CollectionEntry<'notes'> | null;
  next: CollectionEntry<'notes'> | null;
}

const { note, prev, next } = Astro.props;
const d = note.data;
const group = NOTE_GROUPS[d.group];
const { Content } = await render(note);
---
<main data-screen-label={`Notes · ${d.num} ${d.en}`} data-current-step={d.num}>
  {/* 메타 */}
  <div class="b-container" style="...">
    <a href="/notes" class="t-caption">← Notes 목차</a>
    <div style="display: flex; gap: 10px; ...">
      <span style="...olive pill">{d.num} / 13</span>
      <span class="t-caption">{group.en}</span>
      <span>·</span>
      <span class="t-caption">{group.ko} 그룹</span>
    </div>
    <h1 class="t-display">
      <span style="...">{d.en}</span>
      {d.h1_lead}
    </h1>
    <p class="t-body">{d.lead}</p>
  </div>

  {/* mascot ribbon */}
  <div class="b-container" style="display: flex; gap: 14px;">
    <img src="/assets/spooni/guide.svg" alt="..." />
    <span style="font-family: var(--b-font-hand);">학습 노트 · {d.read_time}</span>
  </div>

  {/* 본문 */}
  <article class="b-container" style="max-width: 720px;">
    <div class="t-body" style="display: grid; gap: 20px;">
      <p style="...italic">{d.italic}</p>
      <Content />
    </div>

    {/* workshop callout */}
    <div style="margin-top: 56px; ...">
      <div class="t-title-3">이걸 워크샵에선 어떻게 다루나?</div>
      <div class="t-caption">{d.workshop_text}</div>
      <a href="/#apply">객원 멤버로 합류 →</a>
    </div>

    {/* prev / next */}
    <nav class="b-detail-nav">
      {prev ? (
        <div><a href={`/notes/${prev.id}`}>
          <div class="t-caption">← {prev.data.num} {prev.data.en}</div>
          <div class="t-body-strong">{prev.data.ko}</div>
        </a></div>
      ) : (
        <div><a href="/notes">
          <div class="t-caption">← Notes 목차</div>
          <div class="t-body-strong">13단계 처음으로</div>
        </a></div>
      )}
      {next ? (
        <div style="text-align: right;"><a href={`/notes/${next.id}`}>
          <div class="t-caption">다음 단계 →</div>
          <div class="t-body-strong">{next.data.num} {next.data.en} · {next.data.ko}</div>
        </a></div>
      ) : (
        <div style="text-align: right;"><a href="/notes">
          <div class="t-caption">사이클 끝 ↺</div>
          <div class="t-body-strong">Notes 목차로 돌아가기</div>
        </a></div>
      )}
    </nav>
  </article>
</main>
```

### 5.4 progress JS

`site/scripts/notes-progress.js` → `src/scripts/notes-progress.js`로 그대로 paste.

`BaseLayout.astro`에서 `<script src="/scripts/notes-progress.js" defer></script>` 추가 (또는 Astro `<script is:inline>`로 paste — Astro는 module로 처리 가능). v1엔 단순히 `public/scripts/notes-progress.js`에 두고 src 참조도 OK.

### 5.5 notes 페이지

`src/pages/notes/index.astro`:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import NoteGroup from '../../components/notes/NoteGroup.astro';
import NoteRow from '../../components/notes/NoteRow.astro';
import { getSortedNotes } from '../../lib/content';
import { NOTE_GROUPS } from '../../data/note-groups';

const notes = await getSortedNotes();
const byGroup = {
  'discover-plan': notes.filter((n) => n.data.group === 'discover-plan'),
  'design-architect': notes.filter((n) => n.data.group === 'design-architect'),
  'build-ship': notes.filter((n) => n.data.group === 'build-ship'),
};
---
<BaseLayout
  title="Notes — Bsides"
  description="Bsides에서 같이 가는 한 사이클의 13단계 노트."
  currentPage="notes"
>
  <main data-screen-label="Notes · 목차">
    {/* Hero */}
    <section style="padding-top: 56px; padding-bottom: 24px;">
      <div class="b-container" style="max-width: 760px;">
        <div style="...sup-label">Notes · 학습 노트</div>
        <h1 class="t-display">
          프로토타입까지,<br />
          <span style="font-family: 'Gaegu', ...; color: var(--b-olive);">13단계 노트.</span>
        </h1>
        <p class="t-body">Bsides에서 같이 가는 한 사이클의 13단계. ...</p>
      </div>
    </section>

    {/* 3 groups */}
    {(Object.keys(NOTE_GROUPS) as Array<keyof typeof NOTE_GROUPS>).map((key) => (
      <NoteGroup groupKey={key}>
        {byGroup[key].map((note) => <NoteRow note={note} />)}
      </NoteGroup>
    ))}

    {/* Funnel back-loop */}
    <section style="padding: 48px 0px 80px;">
      <div class="b-container">
        <div style="background: var(--b-paper-warm); ...">
          <div>
            <div class="t-title-3">노트만으로는 부족하다면?</div>
            <div class="t-body">워크샵에선 운영자와 멤버가 같이 손잡고 한 사이클을 통과해요.</div>
          </div>
          <a href="/#apply">객원 멤버 신청 →</a>
        </div>
      </div>
    </section>
  </main>
</BaseLayout>
```

`src/pages/notes/[slug].astro`:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import NoteDetail from '../../components/notes/NoteDetail.astro';
import { getCollection } from 'astro:content';
import { getNoteSiblings } from '../../lib/content';

export async function getStaticPaths() {
  const notes = await getCollection('notes', ({ data }) => data.published);
  return notes.map((note) => ({ params: { slug: note.id }, props: { note } }));
}

const { note } = Astro.props;
const { prev, next } = await getNoteSiblings(note.data.num);
---
<BaseLayout
  title={`${note.data.num} ${note.data.en} · ${note.data.ko} — Bsides Notes`}
  description={note.data.lead}
  currentPage="notes"
>
  <NoteDetail note={note} prev={prev} next={next} />
</BaseLayout>
```

### 5.6 13 Markdown 콘텐츠 추출

`scripts/extract-notes.py` (1회성, build 안 들어가는 운영 도구) — `site/notes-{NN}-{slug}.html` 13개를 읽어 `src/content/notes/{NN}-{slug}.md`로 변환.

추출 로직:
1. `<body>` 안 `<main>`의 article 부분만 잡기
2. `<h3>` → `### h3`
3. `<p>` → 빈줄로 분리된 paragraph
4. `<strong>` → `**strong**`
5. sticky note div → Markdown 직접 마크업 보존 또는 custom astro component

본문 길이 짧으니 직접 손으로 1개씩 변환해도 OK. AI agent가 phase 실행 시 자동 변환 시도.

frontmatter는 site/notes-NN-slug.html에서 추출한 값들 (이미 phase 3 sample과 동일 schema).

### 5.7 메인 페이지 영향

메인에 Notes 카드/링크 추가는 별도. 이 phase는 `/notes` 트랙만. 메인 변경 없음.


## Acceptance Criteria

```bash
npm run build
npm run typecheck
npm run dev &
sleep 5
# 목차
curl -s http://localhost:4321/notes/ | grep "13단계 노트"
curl -s http://localhost:4321/notes/ | grep "Discover & Plan"
# 단계 페이지 (sample 1개 이상 + 후속 추출 후 13개 모두)
curl -s http://localhost:4321/notes/01-intent | grep "INTENT"
```

수동 확인:
- 13단계 모두 빌드 (build 출력 `dist/notes/01-intent/index.html` ~ `13-retro/index.html`)
- localStorage 진도 동작: 단계 페이지 80% 스크롤 → `bsides:notes:read:01` 저장 → 목차에서 "✓ 읽음" 배지
- 헤더 nav `currentPage="notes"`로 active state 적용
- prev/next nav 정상 (01 prev = 목차, 13 next = 사이클 끝 ↺)
- workshop callout 모든 단계 페이지 끝에

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 5 status를 `"completed"`로 변경.

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

이 phase 특이사항: 정적 콘텐츠 + localStorage (서버 0). needs_review 트리거 없음.

## 주의사항

- 13 Markdown 추출 시 sticky note의 시각적 마크업을 어떻게 옮길지 결정 — 옵션 A: HTML 직접 inline (Astro Markdown은 HTML 허용), 옵션 B: custom remark plugin. v1엔 옵션 A 단순함.
- NoteDetail의 `<Content />` 안에 h3·p가 inline style 없이 렌더 — components.css의 `.t-title-2`·`.t-body` 클래스가 article 외부 래퍼에 적용됨. h3에 별도 클래스 매핑은 v1에서 안 하고 기본 스타일 + brand 폰트 fallback으로 충분 시각 정합.
- localStorage key 형식 `bsides:notes:read:{NN}` 변경 금지 — site/scripts/notes-progress.js와 호환.
