# Phase 4: Progress Track

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

phase 3: content.config.ts, lib/content.ts, sample 콘텐츠 각 1개

이전 phase 코드를 꼼꼼히 읽고 설계 의도를 이해한 뒤 작업하라.

## Goal

진행상황 목록 + 상세 + 빈 상태 + 사이 회차 멘토 variant. 메인에 MentorCard·ProgressCard grid 통합. S2·S3·S4 시나리오 통과.

## 작업 내용

### 4.1 ProgressCard.astro

`src/components/ProgressCard.astro`:

```astro
---
import type { CollectionEntry } from 'astro:content';
interface Props {
  post: CollectionEntry<'progress'>;
}
const { post } = Astro.props;
const gradients = {
  olive: 'linear-gradient(135deg, rgb(205, 208, 166) 0%, rgb(185, 192, 148) 100%)',
  sand: 'linear-gradient(135deg, rgb(232, 220, 184) 0%, rgb(216, 200, 149) 100%)',
  pink: 'linear-gradient(135deg, rgb(239, 201, 184) 0%, rgb(227, 176, 154) 100%)',
};
const grad = gradients[post.data.cover?.gradient ?? 'olive'];
const dateStr = post.data.date.toISOString().slice(0, 10);
---
<a href={`/progress/${post.id}`} style="display: block; color: inherit; text-decoration: none;">
  <div style="...site/progress.html 카드 inline 스타일 그대로...">
    <div style={`aspect-ratio: 16 / 10; background: ${grad}; ...`}>
      <div style="...회차 #N 손글씨 라벨...">#{post.data.round}</div>
    </div>
    <div style="padding: 22px 22px 24px; ...">
      <div class="t-caption">{post.data.round}회차 · {dateStr} · 멤버 {post.data.member}</div>
      <div class="t-title-3" style="...">{post.data.title}</div>
      <div class="t-body" style="...">{post.data.lead}</div>
    </div>
  </div>
</a>
```

### 4.2 ProgressEmpty.astro

site/progress-empty.html의 빈 상태 박스 (confused.svg + "곧 첫 회차 시작" + apply link).

### 4.3 ProgressDetail.astro

`src/components/ProgressDetail.astro`:

```astro
---
import type { CollectionEntry } from 'astro:content';
import { render } from 'astro:content';
import { OPERATOR } from '../data/operator';
interface Props {
  post: CollectionEntry<'progress'>;
  prev: CollectionEntry<'progress'> | null;
  next: CollectionEntry<'progress'> | null;
}
const { post, prev, next } = Astro.props;
const { Content } = await render(post);
---
{/* site/progress-round-3-mimirog-launch.html 마크업 그대로 + Content 슬롯 */}
<main data-screen-label={`03 Detail · ${post.id}`}>
  ...메타 (회차·날짜·멤버)...
  <h1 class="t-display">{post.data.title}</h1>
  ...hero image with sticky note...
  <div class="b-container" style="max-width: 720px; ...mascot ribbon">
    <img src="/assets/spooni/guide.svg" alt="..." />
    <span style="..."> 회차 노트</span>
  </div>
  <article class="b-container" style="max-width: 720px;">
    <div class="t-body" style="...">
      <Content />
    </div>
    {/* workshop callout */}
    <div style="...">
      <a href="/#apply">카톡으로 신청하기 →</a>
    </div>
    {/* prev/next */}
    <nav class="b-detail-nav">
      {prev ? <a href={`/progress/${prev.id}`}>...</a> : <div>없음</div>}
      {next ? <a href={`/progress/${next.id}`}>...</a> : <div>없음</div>}
    </nav>
  </article>
</main>
```

### 4.4 MentorCard.astro

`src/components/home/MentorCard.astro` — `CurrentMember` 받아 active/between 분기:

```astro
---
import type { CurrentMember } from '../../data/current-member';
interface Props { member: CurrentMember; }
const { member } = Astro.props;
const isActive = member.cycle_state === 'active';
---
{isActive ? (
  {/* site/index.html의 "이번 사이클 멤버" 카드 마크업 그대로 */}
  <section style="...">
    <div class="...sup-label">Now running</div>
    <h2>이번 사이클 멤버</h2>
    ...live pill·도토리룸·메타 4종·이번 회차 보기 link...
  </section>
) : (
  {/* site/index-between-cycles.html의 "다음 회차 준비 중" 마크업 */}
  <section style="...">
    <div class="...sup-label">Between cycles</div>
    <h2>다음 회차 준비 중</h2>
    ...waiting.svg + 다음 회차 주인공 모집...
  </section>
)}
```

### 4.5 progress 페이지

`src/pages/progress/index.astro`:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import ProgressCard from '../../components/ProgressCard.astro';
import ProgressEmpty from '../../components/ProgressEmpty.astro';
import { getSortedProgress } from '../../lib/content';
const posts = await getSortedProgress();
const isEmpty = posts.length === 0;
---
<BaseLayout title="..." description="..." currentPage="progress">
  <main data-screen-label={isEmpty ? '02 Progress list · empty' : '02 Progress list'}>
    {/* 헤더 영역 ("← Bsides" + h2 진행상황 + lead) */}
    {isEmpty ? <ProgressEmpty /> : (
      <div style="display: grid; ...">
        {posts.map((post) => <ProgressCard post={post} />)}
      </div>
    )}
  </main>
</BaseLayout>
```

`src/pages/progress/[slug].astro`:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import ProgressDetail from '../../components/ProgressDetail.astro';
import { getCollection } from 'astro:content';
import { getProgressSiblings } from '../../lib/content';

export async function getStaticPaths() {
  const posts = await getCollection('progress', ({ data }) => data.published);
  return posts.map((post) => ({ params: { slug: post.id }, props: { post } }));
}

const { post } = Astro.props;
const { prev, next } = await getProgressSiblings(post.id);
---
<BaseLayout
  title={`${post.data.round}회차 · ${post.data.title} — Bsides`}
  description={post.data.lead}
  currentPage="progress"
>
  <ProgressDetail post={post} prev={prev} next={next} />
</BaseLayout>
```

### 4.6 메인 통합

`src/pages/index.astro`에 MentorCard + 최근 진행상황 grid 추가:

```astro
---
import MentorCard from '../components/home/MentorCard.astro';
import ProgressCard from '../components/ProgressCard.astro';
import { CURRENT_MEMBER } from '../data/current-member';
import { getSortedProgress } from '../lib/content';
const recent = (await getSortedProgress()).slice(0, 3);
---
...
<Hero />
<PersonaStrip />
<HowItWorks />
<MentorCard member={CURRENT_MEMBER} />
<section><!-- Latest / 최근 진행상황 -->
  ...
  <div style="display: grid; ...">
    {recent.map((post) => <ProgressCard post={post} />)}
  </div>
</section>
<ApplySection />
```

### 4.7 잘못된 slug 처리

Astro `output: 'static'`에선 `getStaticPaths`가 build 시점에 모든 slug 결정. 잘못된 slug는 자동으로 404로 (Phase 6 `404.astro`가 cover). 별도 not-found 페이지 불필요 — site/progress-not-found.html은 design SoT 단계 산출물이고 production에선 404로 통합.


## Acceptance Criteria

```bash
npm run build
npm run typecheck
npm run dev &
sleep 5
curl -s http://localhost:4321/progress/ | grep "미미로그"
curl -s http://localhost:4321/progress/round-3-mimirog-launch | grep "출시 직후"
curl -s -o /dev/null -w "%{http_code}" http://localhost:4321/progress/non-existent  # 404
```

수동 확인:
- 메인의 "이번 사이클 멤버" + "최근 진행상황" grid가 site/index.html과 시각 정합
- `CURRENT_MEMBER.cycle_state`를 `'between'`으로 임시 변경 → 메인 변형 (after 검증 원복)
- 진행상황 목록 / 상세 / S2·S3·S4 시나리오 통과

## AC 검증 방법

위 AC 커맨드를 실행하라. 모두 통과하면 `planning/cycles/v1-prototype/build/index.json`의 phase 4 status를 `"completed"`로 변경.

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

이 phase 특이사항: 정적 데이터 렌더링만. 외부 호출·시크릿 없음. needs_review 트리거 없음.

## 주의사항

- ProgressCard·MentorCard·ProgressDetail의 inline style은 site/ 마크업 그대로 paste. CSS class refactor 금지.
- `getStaticPaths` 함수는 build 시점에만 실행. dev server에선 첫 요청 시 평가.
- `<Content />`는 Markdown body를 렌더 — 안에서 h3·p·img·strong 등 기본 태그가 inline style 없이 들어옴. brand voice 정합 styled 출력은 `components.css`의 `.t-body` 클래스가 article 래퍼에 적용되도록 유지.
